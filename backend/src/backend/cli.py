import asyncio
import typer
from datetime import date
from backend.schemas.auth import Gender
from backend.services.doctors import get_doctor_service
from backend.core import get_session
from backend.repositories.doctors import SQLDoctorRepository
from backend.schemas.doctors import DoctorCreate

app = typer.Typer()

async def create_doctor_async(payload: DoctorCreate):
    async for session in get_session():
        doctor_service = await get_doctor_service(SQLDoctorRepository(session))
        try:
            await doctor_service.create(payload, False)
        except Exception as e:
            print(f"[RED]Error: {str(e)}[/RED]")

@app.command()
def create_doctor(
    first_name: str = typer.prompt("Enter first name"),
    last_name: str = typer.prompt("Enter last name"),
    middle_name: str = typer.prompt("Enter middle name"),
    email: str = typer.prompt("Enter email (optional)"),
    phone_number: str = typer.prompt("Enter phone number"),
    birth_data: str = typer.prompt("Enter birth date (YYYY-MM-DD)"),
    gender: str = typer.prompt("Enter gender (male/female)"),
    password: str = typer.prompt("Enter password"),
    specialization: str = typer.prompt("Enter specialization"),
    department_id: int = typer.prompt("Enter department id", type=int),
    role_id: int = typer.prompt("Enter role id", type=int),
):
    """Create a new doctor"""
    birth_date = date.fromisoformat(birth_data)
    gender_enum = Gender.MALE if gender.lower() == "male" else Gender.FEMALE
    
    payload = DoctorCreate(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone_number=phone_number,
        birth_data=birth_date,
        email=email,
        gender=gender_enum,
        specialization=specialization,
        department_id=department_id,
        password=password,
        role_id=role_id
    )   

    asyncio.run(create_doctor_async(payload))

    typer.echo(f"Doctor {first_name} {last_name} created successfully!")

if __name__ == "__main__":
    app()
