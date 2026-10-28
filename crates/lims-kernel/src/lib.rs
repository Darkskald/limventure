//! Shared kernel used by every bounded context.
//!
//! architecturekit writes no audit metadata itself (no actor, no reason), so every
//! event embeds an [`Audit`] value. See ADR-0003 and ADR-0004.
//! upstream: AK-001, ESDB-004

use std::fmt;

use architecturekit::Schema;
use serde::{Deserialize, Serialize};

/// Identifier segment usable inside an `EventSourcingDB` subject.
fn validate_segment(kind: &'static str, value: &str) -> Result<(), KernelError> {
    let valid = !value.is_empty()
        && value
            .chars()
            .all(|c| c.is_ascii_alphanumeric() || c == '-' || c == '_');
    if valid {
        Ok(())
    } else {
        Err(KernelError::InvalidIdentifier {
            kind,
            value: value.to_owned(),
        })
    }
}

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum KernelError {
    #[error("invalid {kind} '{value}': use [A-Za-z0-9_-]+")]
    InvalidIdentifier { kind: &'static str, value: String },
}

/// Tenant identifier. Part of every subject (ADR-0004).
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
pub struct TenantId(String);

impl TenantId {
    /// # Errors
    /// Returns [`KernelError::InvalidIdentifier`] if the value cannot be used in a subject.
    pub fn new(value: impl Into<String>) -> Result<Self, KernelError> {
        let value = value.into();
        validate_segment("tenant id", &value)?;
        Ok(Self(value))
    }

    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl TryFrom<String> for TenantId {
    type Error = KernelError;
    fn try_from(value: String) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl From<TenantId> for String {
    fn from(value: TenantId) -> Self {
        value.0
    }
}

impl fmt::Display for TenantId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

/// Who caused an event: a person or an external/internal system.
///
/// `id` is an opaque identifier (e.g. `person:<uuid>`), never a name or e-mail — personal
/// data lives in the erasable person registry (ADR-0010).
///
/// A struct rather than an enum because architecturekit cannot derive JSON schemas for enums.
/// upstream: AK-002
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Schema)]
#[serde(rename_all = "camelCase")]
pub struct Actor {
    /// `user` or `system`.
    pub kind: String,
    pub id: String,
}

impl Actor {
    #[must_use]
    pub fn user(id: impl Into<String>) -> Self {
        Self {
            kind: "user".into(),
            id: id.into(),
        }
    }

    #[must_use]
    pub fn system(id: impl Into<String>) -> Self {
        Self {
            kind: "system".into(),
            id: id.into(),
        }
    }
}

/// Audit envelope embedded in every event's data.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Schema)]
#[serde(rename_all = "camelCase")]
pub struct Audit {
    pub actor: Actor,
    /// Mandatory for corrections when the tenant's regulatory profile demands it.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub reason: Option<String>,
    /// Correlates all events caused by one user intent or inbound integration message.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub correlation_id: Option<String>,
}

impl Audit {
    #[must_use]
    pub fn by(actor: Actor) -> Self {
        Self {
            actor,
            reason: None,
            correlation_id: None,
        }
    }
}

/// Builds tenant-scoped subjects `/tenants/<tenant>/<context>/<aggregate>/<id>`.
/// The only sanctioned way to construct a subject (ADR-0004).
/// Fallible instead of `SubjectScheme::build`, which panics on invalid values — upstream: AK-012
///
/// # Errors
/// Returns [`KernelError::InvalidIdentifier`] if `id` contains characters not allowed in a subject.
pub fn subject(
    tenant: &TenantId,
    context: &str,
    aggregate: &str,
    id: &str,
) -> Result<String, KernelError> {
    validate_segment("aggregate id", id)?;
    Ok(format!("/tenants/{tenant}/{context}/{aggregate}/{id}"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builds_tenant_scoped_subject() {
        let tenant = TenantId::new("acme").unwrap();
        assert_eq!(
            subject(&tenant, "sampling", "sample", "S-0001").unwrap(),
            "/tenants/acme/sampling/sample/S-0001"
        );
    }

    #[test]
    fn rejects_path_injection() {
        assert!(TenantId::new("acme/other").is_err());
        let tenant = TenantId::new("acme").unwrap();
        assert!(subject(&tenant, "sampling", "sample", "../x").is_err());
    }
}
