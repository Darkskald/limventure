//! Sampling bounded context — walking skeleton.
//!
//! Placeholder until the ESDM model in `model/` defines the real aggregate.

use architecturekit::{Command, Decider, DomainError, Event, Events, Precondition, State};
use lims_kernel::{Audit, KernelError, TenantId, subject};
use serde::{Deserialize, Serialize};

pub const CONTEXT: &str = "sampling";

#[derive(Debug, Serialize, Deserialize, Event)]
#[event(type = "io.limventure.sampling.sample-registered.v1")]
#[serde(rename_all = "camelCase")]
pub struct SampleRegistered {
    pub matrix: String,
    pub audit: Audit,
}

#[derive(Debug, Events)]
pub enum SampleEvent {
    Registered(SampleRegistered),
}

#[derive(Debug, Clone, Default)]
pub struct Sample {
    is_registered: bool,
}

impl State for Sample {
    type Event = SampleEvent;

    fn evolve(self, event: &SampleEvent) -> Self {
        match event {
            SampleEvent::Registered(_) => Sample {
                is_registered: true,
            },
        }
    }
}

#[derive(Debug, Clone)]
pub struct RegisterSample {
    subject: String,
    pub sample_id: String,
    pub matrix: String,
    pub audit: Audit,
}

impl RegisterSample {
    /// # Errors
    /// Returns [`KernelError`] if the sample id cannot be used in a subject.
    pub fn new(
        tenant: &TenantId,
        sample_id: &str,
        matrix: &str,
        audit: Audit,
    ) -> Result<Self, KernelError> {
        Ok(Self {
            subject: subject(tenant, CONTEXT, "sample", sample_id)?,
            sample_id: sample_id.to_owned(),
            matrix: matrix.to_owned(),
            audit,
        })
    }
}

impl Command for RegisterSample {
    fn subject(&self) -> String {
        self.subject.clone()
    }

    fn preconditions(&self) -> Vec<Precondition> {
        vec![Precondition::on_pristine_subject(self.subject.clone())]
    }
}

#[must_use]
pub fn register_sample() -> Decider<RegisterSample, Sample, DomainError> {
    Decider::new(|cmd: RegisterSample, sample: Sample| async move {
        if sample.is_registered {
            return Err(DomainError::new(format!(
                "sample {} already registered",
                cmd.sample_id
            )));
        }
        Ok(vec![SampleEvent::Registered(SampleRegistered {
            matrix: cmd.matrix,
            audit: cmd.audit,
        })])
    })
}

#[cfg(test)]
mod tests {
    use architecturekit::testing::given;
    use lims_kernel::Actor;

    use super::*;

    fn cmd() -> RegisterSample {
        let tenant = TenantId::new("acme").unwrap();
        RegisterSample::new(
            &tenant,
            "S-0001",
            "sunflower-oil",
            Audit::by(Actor::user("jane")),
        )
        .unwrap()
    }

    #[tokio::test]
    async fn refuses_duplicate_registration() {
        let existing = SampleEvent::Registered(SampleRegistered {
            matrix: "sunflower-oil".into(),
            audit: Audit::by(Actor::user("jane")),
        });
        given(&register_sample(), [existing])
            .when(cmd())
            .await
            .then_failed(DomainError::new("sample S-0001 already registered"));
    }
}
