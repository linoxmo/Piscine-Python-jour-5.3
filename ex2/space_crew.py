from enum import Enum
from pydantic import Field, BaseModel, model_validator, ValidationError
from datetime import datetime


class MyError(Exception):
    pass


class Rank(Enum):
    Cadet = "cadet"
    Officer = "officer"
    Lieutenant = "lieutenant"
    Captain = "captain"
    Commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age:  int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=10*365)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_information(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise MyError("Mission ID muss start with the letter M")

        if not any(
            member.rank in (Rank.Commander, Rank.Captain)
            for member in self.crew
        ):
            raise MyError("There is no Captain or Commander ")

        if (self.duration_days > 365):
            if sum(member.years_experience > 5
                   for member in self.crew) / len(self.crew) < 0.5:
                raise MyError(
                    "For long mission, half "
                    "of the crew must have 5 years experiences")

        if not (member.is_active for member in self.crew):
            raise MyError("Not all member are actives")
        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=" * 41)

    try:
        crew = [
            CrewMember(
                member_id="CM1",
                name="Sarah Connor",
                rank=Rank.Commander,
                age=45,
                specialization="Mission Command",
                years_experience=20,
            ),
            CrewMember(
                member_id="CM2",
                name="John Smith",
                rank=Rank.Lieutenant,
                age=38,
                specialization="Navigation",
                years_experience=10,
            ),
            CrewMember(
                member_id="CM3",
                name="Alice Johnson",
                rank=Rank.Officer,
                age=35,
                specialization="Engineering",
                years_experience=8,
            ),
        ]

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2028, 5, 15),
            duration_days=900,
            crew=crew,
            budget_millions=2500.0,
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")

        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) \
                - {member.specialization}"
            )

    except (ValidationError, MyError) as e:
        print(e)

    print("=" * 41)

    try:
        crew_1 = [
            CrewMember(
                member_id="CM4",
                name="Bob Wilson",
                rank=Rank.Officer,
                age=30,
                specialization="Engineering",
                years_experience=3,
            ),
            CrewMember(
                member_id="CM5",
                name="Emma Brown",
                rank=Rank.Lieutenant,
                age=29,
                specialization="Science",
                years_experience=2,
            ),
        ]

        mission = SpaceMission(
            mission_id="M2025_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime(2029, 1, 1),
            duration_days=100,
            crew=crew_1,
            budget_millions=100.0,
        )

    except (ValidationError, MyError) as e:
        print("Expected validation error:")
        print(e)
