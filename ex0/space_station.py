from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class Station(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length = 50)
    crew_size: int = Field(ge=1, le= 20)
    power_level: float = Field(ge= 0.0,le = 100.0)
    oxygen_level: float = Field(ge= 0.0, le= 100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(
        default=None,
        max_length=200
    )

def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        V_station = Station(station_id="000", 
                            name="International Space Station", 
                            crew_size=6, 
                            power_level= 85.5 , 
                            oxygen_level= 92.3, 
                            last_maintenance=datetime.now())
        print("Valid station created:")
        print("Station Name:", V_station.name)
        print("Crew", V_station.crew_size)
        print("Power", V_station.power_level)
        print("Oxygen", V_station.oxygen_level)
    except ValidationError as e:
        print(e)
    print("========================================")
    try:
        V_station = Station(station_id="000", 
                            name="hey", 
                            crew_size=0, 
                            power_level= 85.5 , 
                            oxygen_level= 92.3, 
                            last_maintenance=datetime.now())
    except ValidationError as e:
        print(e)


if __name__ == '__main__':
    main()