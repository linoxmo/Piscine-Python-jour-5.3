from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional


class ContactType(Enum):
    Radio = "radio"
    Visual = "visual"
    Physical = "physical"
    Telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength:  float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=60 * 24)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                "contact_id must start with 'AC' (Alien Contact)"
            )

        if (
            self.contact_type == ContactType.Physical
            and self.is_verified
        ):
            raise ValueError(
                "Physical contact reports must be verified"
            )

        if (
            self.contact_type == ContactType.Telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if (
            self.signal_strength > 7.0
            and not self.message_received
        ):
            raise ValueError(
                "Strong signals (> 7.0) must include a received message"
            )

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.now(),
        location="Area 51, Nevada",
        contact_type=ContactType.Radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True
    )

    print("Valid contact report:")
    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type.value}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: '{valid_contact.message_received}'")
    print("======================================")
    try:
        valid_contact_1 = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.Physical,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True
        )

        print("Valid contact report:")
        print(f"ID: {valid_contact_1.contact_id}")
        print(f"Type: {valid_contact_1.contact_type.value}")
        print(f"Location: {valid_contact_1.location}")
        print(f"Signal: {valid_contact_1.signal_strength}/10")
        print(f"Duration: {valid_contact_1.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact_1.witness_count}")
        print(f"Message: '{valid_contact_1.message_received}'")
        print("======================================")
    except ValidationError as e:
        print(e)
    print("======================================")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Nevada Desert",
            contact_type=ContactType.Telepathic,
            signal_strength=5.0,
            duration_minutes=20,
            witness_count=2,
            message_received=None,
            is_verified=False
        )

    except ValidationError as e:
        print("Expected validation error:", e)
        print("Telepathic contact requires at least 3 witnesses")


if __name__ == '__main__':
    main()
