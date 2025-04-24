use crate::{lib_context::get_auth_registry, prelude::*};

use indexmap::IndexMap;
use serde::de::DeserializeOwned;
use sqlx::PgPool;
use std::{
    borrow::Cow,
    collections::{BTreeMap, BTreeSet, HashMap, HashSet},
    fmt::{Debug, Display},
    str::FromStr,
};

use super::{
    db_metadata, CombinedState, DesiredMode, ExistingMode, FlowSetupState, FlowSetupStatusCheck,
    ObjectSetupStatusCheck, ObjectStatus, ResourceIdentifier, ResourceSetupInfo,
    ResourceSetupStatusCheck, SetupChangeType, StateChange, TargetSetupState,
};
use super::{AllSetupState, AllSetupStatusCheck};
use crate::execution::db_tracking_setup;
use crate::{
    lib_context::FlowContext,
    ops::{executor_factory_registry, interface::ExecutorFactory},
};

enum MetadataRecordType {
    FlowVersion,
    FlowMetadata,
    TrackingTable,
    Target(String),
}

impl Display for MetadataRecordType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MetadataRecordType::FlowVersion => f.write_str(db_metadata::FLOW_VERSION_RESOURCE_TYPE),
            MetadataRecordType::FlowMetadata => write!(f, "FlowMetadata"),
            MetadataRecordType::TrackingTable => write!(f, "TrackingTable"),
            MetadataRecordType::Target(target_id) => write!(f, "Target:{}", target_id),
        }
    }
}

impl std::str::FromStr for MetadataRecordType {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        if s == db_metadata::FLOW_VERSION_RESOURCE_TYPE {
            Ok(Self::FlowVersion)
        } else if s == "FlowMetadata" {
            Ok(Self::FlowMetadata)
        } else if s == "TrackingTable" {
            Ok(Self::TrackingTable)
        } else if let Some(target_id) = s.strip_prefix("Target:") {
            Ok(Self::Target(target_id.to_string()))
        } else {
            anyhow::bail!("Invalid MetadataRecordType string: {}", s)
        }
    }
}

fn from_metadata_record<S: DeserializeOwned + Debug + Clone>(
    state: Option<serde_json::Value>,
    staging_changes: sqlx::types::Json<Vec<StateChange<serde_json::Value>>>,
) -> Result<CombinedState<S>> {
    let current: Option<S> = state.map(serde_json::from_value).transpose()?;
    let staging: Vec<StateChange<S>> = (staging_changes.0.into_iter())
        .map(|sc| -> Result<_> {
            Ok(match sc {
                StateChange::Upsert(v) => StateChange::Upsert(serde_json::from_value(v)?),
                StateChange::Delete => StateChange::Delete,
            })
        })
        .collect::<Result<_>>()?;
    Ok(CombinedState { current, staging })
}

pub async fn get_existing_setup_state(pool: &PgPool) -> Result<AllSetupState<ExistingMode>> {
    let setup_metadata_records = db_metadata::read_setup_metadata(pool).await?;

    let setup_metadata_records = if let Some(records) = setup_metadata_records {
        records
    } else {
        return Ok(AllSetupState::default());
    };

    // Group setup metadata records by flow name
    let setup_metadata_records = setup_metadata_records.into_iter().fold(
        BTreeMap::<String, Vec<_>>::new(),
        |mut acc, record| {
            acc.entry(record.flow_name.clone())
                .or_default()
                .push(record);
            acc
        },
    );

    let flows = setup_metadata_records
        .into_iter()
        .map(|(flow_name, metadata_records)| -> anyhow::Result<_> {
            let mut flow_ss = FlowSetupState::default();
            for metadata_record in metadata_records {
                let state = metadata_record.state;
                let staging_changes = metadata_record.staging_changes;
                match MetadataRecordType::from_str(&metadata_record.resource_type)? {
                    MetadataRecordType::FlowVersion => {
                        flow_ss.seen_flow_metadata_version =
                            db_metadata::parse_flow_version(&state);
                    }
                    MetadataRecordType::FlowMetadata => {
                        flow_ss.metadata = from_metadata_record(state, staging_changes)?;
                    }
                    MetadataRecordType::TrackingTable => {
                        flow_ss.tracking_table = from_metadata_record(state, staging_changes)?;
                    }
                    MetadataRecordType::Target(target_type) => {
                        flow_ss.targets.insert(
                            super::ResourceIdentifier {
                                key: metadata_record.key.clone(),
                                target_kind: target_type,
                            },
                            from_metadata_record(state, staging_changes)?,
                        );
                    }
                }
            }
            Ok((flow_name, flow_ss))
        })
        .collect::<Result<_>>()?;

    Ok(AllSetupState {
        has_metadata_table: true,
        flows,
    })
}

fn diff_state<E, D, T>(
    existing_state: Option<&E>,
    desired_state: Option<&D>,
    diff: impl Fn(Option<&E>, &D) -> Option<StateChange<T>>,
) -> Option<StateChange<T>>
where
    E: PartialEq<D>,
{
    match (existing_state, desired_state) {
        (None, None) => None,
        (Some(_), None) => Some(StateChange::Delete),
        (existing_state, Some(desired_state)) => {
            if existing_state.map(|e| e == desired_state).unwrap_or(false) {
                None
            } else {
                diff(existing_state, desired_state)
            }
        }
    }
}

fn to_object_status<A, B>(existing: Option<A>, desired: Option<B>) -> Result<ObjectStatus> {
    Ok(match (&existing, &desired) {
        (Some(_), None) => ObjectStatus::Deleted,
        (None, Some(_)) => ObjectStatus::New,
        (Some(_), Some(_)) => ObjectStatus::Existing,
        (None, None) => bail!("Unexpected object status"),
    })
}

#[derive(Debug, Default)]
struct GroupedResourceStates {
    desired: Option<TargetSetupState>,
    existing: CombinedState<TargetSetupState>,
}

fn group_resource_states<'a>(
    desired: impl Iterator<Item = (&'a ResourceIdentifier, &'a TargetSetupState)>,
    existing: impl Iterator<Item = (&'a ResourceIdentifier, &'a CombinedState<TargetSetupState>)>,
) -> Result<IndexMap<&'a ResourceIdentifier, GroupedResourceStates>> {
    let mut grouped: IndexMap<&'a ResourceIdentifier, GroupedResourceStates> = desired
        .into_iter()
        .map(|(key, state)| {
            (
                key,
                GroupedResourceStates {
                    desired: Some(state.clone()),
                    existing: CombinedState::default(),
                },
            )
        })
        .collect();
    for (key, state) in existing {
        let entry = grouped.entry(key);
        if state.current.is_some() {
            if let indexmap::map::Entry::Occupied(entry) = &entry {
                if entry.get().existing.current.is_some() {
                    bail!("Duplicate existing state for key: {}", entry.key());
                }
            }
        }
        let entry = entry.or_default();
        if let Some(current) = &state.current {
            entry.existing.current = Some(current.clone());
        }
        for s in state.staging.iter() {
            match s {
                StateChange::Upsert(v) => {
                    entry.existing.staging.push(StateChange::Upsert(v.clone()))
                }
                StateChange::Delete => entry.existing.staging.push(StateChange::Delete),
            }
        }
    }
    Ok(grouped)
}

pub fn check_flow_setup_status(
    desired_state: Option<&FlowSetupState<DesiredMode>>,
    existing_state: Option<&FlowSetupState<ExistingMode>>,
) -> Result<FlowSetupStatusCheck> {
    let metadata_change = diff_state(
        existing_state.map(|e| &e.metadata),
        desired_state.map(|d| &d.metadata),
        |_, desired_state| Some(StateChange::Upsert(desired_state.clone())),
    );

    let new_source_ids = desired_state
        .iter()
        .flat_map(|d| d.metadata.sources.values().map(|v| v.source_id))
        .collect::<HashSet<i32>>();
    let tracking_table_change = db_tracking_setup::TrackingTableSetupStatusCheck::new(
        desired_state.map(|d| &d.tracking_table),
        &existing_state
            .map(|e| Cow::Borrowed(&e.tracking_table))
            .unwrap_or_default(),
        (existing_state.iter())
            .flat_map(|state| state.metadata.possible_versions())
            .flat_map(|metadata| {
                metadata
                    .sources
                    .values()
                    .map(|v| v.source_id)
                    .filter(|id| !new_source_ids.contains(id))
            })
            .collect::<BTreeSet<i32>>()
            .into_iter()
            .collect(),
    );

    let mut target_resources = Vec::new();
    let mut unknown_resources = Vec::new();

    let grouped_target_resources = group_resource_states(
        desired_state.iter().flat_map(|d| d.targets.iter()),
        existing_state.iter().flat_map(|e| e.targets.iter()),
    )?;
    let registry = executor_factory_registry();
    for (resource_id, v) in grouped_target_resources.into_iter() {
        let factory = match registry.get(&resource_id.target_kind) {
            Some(factory) => factory,
            None => {
                unknown_resources.push(resource_id.clone());
                continue;
            }
        };
        let factory = match factory {
            ExecutorFactory::ExportTarget(factory) => factory,
            _ => bail!("Unexpected factory type for {}", resource_id.target_kind),
        };
        let state = v.desired.clone();
        let target_state = v
            .desired
            .and_then(|state| (!state.common.setup_by_user).then_some(state.state));
        let existing_without_setup_by_user = CombinedState {
            current: v
                .existing
                .current
                .and_then(|s| s.state_unless_setup_by_user()),
            staging: v
                .existing
                .staging
                .into_iter()
                .filter_map(|s| match s {
                    StateChange::Upsert(s) => {
                        s.state_unless_setup_by_user().map(StateChange::Upsert)
                    }
                    StateChange::Delete => Some(StateChange::Delete),
                })
                .collect(),
        };
        let never_setup_by_sys = target_state.is_none()
            && existing_without_setup_by_user.current.is_none()
            && existing_without_setup_by_user.staging.is_empty();
        let status_check = if never_setup_by_sys {
            None
        } else {
            Some(factory.check_setup_status(
                &resource_id.key,
                target_state,
                existing_without_setup_by_user,
                get_auth_registry(),
            )?)
        };
        target_resources.push(ResourceSetupInfo {
            key: resource_id.clone(),
            state,
            description: factory.describe_resource(&resource_id.key)?,
            status_check,
        });
    }
    Ok(FlowSetupStatusCheck {
        status: to_object_status(existing_state, desired_state)?,
        seen_flow_metadata_version: existing_state.and_then(|s| s.seen_flow_metadata_version),
        metadata_change,
        tracking_table: tracking_table_change.into_setup_info(),
        target_resources,
        unknown_resources,
    })
}

pub fn sync_setup(
    flows: &BTreeMap<String, Arc<FlowContext>>,
    all_setup_state: &AllSetupState<ExistingMode>,
) -> Result<AllSetupStatusCheck> {
    let mut flow_status_checks = BTreeMap::new();
    for (flow_name, flow_context) in flows {
        let existing_state = all_setup_state.flows.get(flow_name);
        flow_status_checks.insert(
            flow_name.clone(),
            check_flow_setup_status(Some(&flow_context.flow.desired_state), existing_state)?,
        );
    }
    Ok(AllSetupStatusCheck {
        metadata_table: db_metadata::MetadataTableSetup {
            metadata_table_missing: !all_setup_state.has_metadata_table,
        }
        .into_setup_info(),
        flows: flow_status_checks,
    })
}

pub fn drop_setup(
    flow_names: impl IntoIterator<Item = String>,
    all_setup_state: &AllSetupState<ExistingMode>,
) -> Result<AllSetupStatusCheck> {
    if !all_setup_state.has_metadata_table {
        api_bail!("CocoIndex metadata table is missing.");
    }
    let mut flow_status_checks = BTreeMap::new();
    for flow_name in flow_names.into_iter() {
        if let Some(existing_state) = all_setup_state.flows.get(&flow_name) {
            flow_status_checks.insert(
                flow_name,
                check_flow_setup_status(None, Some(existing_state))?,
            );
        }
    }
    Ok(AllSetupStatusCheck {
        metadata_table: db_metadata::MetadataTableSetup {
            metadata_table_missing: false,
        }
        .into_setup_info(),
        flows: flow_status_checks,
    })
}

async fn maybe_update_resource_setup<K, S, C: ResourceSetupStatusCheck>(
    write: &mut impl std::io::Write,
    resource: &ResourceSetupInfo<K, S, C>,
) -> Result<()> {
    if let Some(status_check) = &resource.status_check {
        if status_check.change_type() != SetupChangeType::NoChange {
            writeln!(write, "{}:", resource.description)?;
            for change in status_check.describe_changes() {
                writeln!(write, "  - {}", change)?;
            }
            write!(write, "Pushing...")?;
            status_check.apply_change().await?;
            writeln!(write, "DONE")?;
        }
    }
    Ok(())
}

pub async fn apply_changes(
    write: &mut impl std::io::Write,
    status_check: &AllSetupStatusCheck,
    pool: &PgPool,
) -> Result<()> {
    maybe_update_resource_setup(write, &status_check.metadata_table).await?;

    for (flow_name, flow_status) in &status_check.flows {
        if flow_status.is_up_to_date() {
            continue;
        }
        let verb = match flow_status.status {
            ObjectStatus::New => "Creating",
            ObjectStatus::Deleted => "Deleting",
            ObjectStatus::Existing => "Updating resources for ",
            _ => bail!("invalid flow status"),
        };
        write!(write, "\n{verb} flow {flow_name}:\n")?;

        let mut state_updates =
            HashMap::<db_metadata::ResourceTypeKey, Option<serde_json::Value>>::new();

        if let Some(metadata_change) = &flow_status.metadata_change {
            state_updates.insert(
                db_metadata::ResourceTypeKey::new(
                    MetadataRecordType::FlowMetadata.to_string(),
                    serde_json::Value::Null,
                ),
                metadata_change
                    .desired_state()
                    .map(serde_json::to_value)
                    .transpose()?,
            );
        }
        if flow_status
            .tracking_table
            .status_check
            .as_ref()
            .map(|c| c.change_type() != SetupChangeType::NoChange)
            .unwrap_or_default()
        {
            state_updates.insert(
                db_metadata::ResourceTypeKey::new(
                    MetadataRecordType::TrackingTable.to_string(),
                    serde_json::Value::Null,
                ),
                flow_status
                    .tracking_table
                    .state
                    .as_ref()
                    .map(serde_json::to_value)
                    .transpose()?,
            );
        }
        for target_resource in &flow_status.target_resources {
            state_updates.insert(
                db_metadata::ResourceTypeKey::new(
                    MetadataRecordType::Target(target_resource.key.target_kind.clone()).to_string(),
                    target_resource.key.key.clone(),
                ),
                target_resource
                    .state
                    .as_ref()
                    .map(serde_json::to_value)
                    .transpose()?,
            );
        }

        let new_version_id = db_metadata::stage_changes_for_flow(
            flow_name,
            flow_status.seen_flow_metadata_version,
            &state_updates,
            pool,
        )
        .await?;

        maybe_update_resource_setup(write, &flow_status.tracking_table).await?;

        for target_resource in &flow_status.target_resources {
            maybe_update_resource_setup(write, target_resource).await?;
        }

        let is_deletion = flow_status.status == ObjectStatus::Deleted;
        db_metadata::commit_changes_for_flow(
            flow_name,
            new_version_id,
            state_updates,
            is_deletion,
            pool,
        )
        .await?;

        writeln!(write, "Done for flow {}", flow_name)?;
    }
    Ok(())
}
