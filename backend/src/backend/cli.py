import asyncio
from datetime import date
from pathlib import Path
import typer
from multiprocessing import freeze_support
from alembic.command import upgrade
from alembic.config import Config
from backend.config import config
import uvicorn

from backend.core.db import get_session
from backend.repositories.doctors import SQLDoctorRepository
from backend.schemas.auth import Gender
from backend.schemas.users import DoctorCreate
from backend.services.doctors import get_doctor_service

app = typer.Typer()


@app.command()
def migrate():
    alembic_cfg = Config(config.ALEMBIC_CFG)
    alembic_cfg.set_main_option("script_location", str(config.MIGRATIONS_DIR))
    upgrade(alembic_cfg, "head")


@app.command()
def runserver(host: str = "127.0.0.1", port: int = 8000):
    asgi_path = config.BASE_DIR.joinpath("core").joinpath("asgi.py")
    module_path = asgi_path.relative_to(Path.cwd()).as_posix().replace('/', ".").replace('.py', ':app').split('.',1)[1]
    print(f"Start ASGI module: {module_path}")
    uvicorn.run(module_path, host=host, port=port, reload=config.DEBUG, workers=1)



async def create_doctor_async(payload: DoctorCreate):
    async for session in get_session():
        doctor_service = await get_doctor_service(SQLDoctorRepository(session))
        try:
            await doctor_service.create(payload, False)
        except Exception as e:
            print(f"[RED]Error: {str(e)}[/RED]")

@app.command()
def create_doctor(
    first_name: str = typer.Option(prompt_required=True, prompt=True),
    last_name: str = typer.Option(prompt_required=True, prompt=True),
    middle_name: str = typer.Option(prompt_required=True, prompt=True),
    email: str = typer.Option(prompt_required=True, prompt=True),
    phone_number: str = typer.Option(prompt_required=True, prompt=True),
    birth_data: str = typer.Option(prompt_required=True, prompt=True, default="1991-07-24"),
    gender: str = typer.Option(prompt_required=True, prompt=True, default="male"),
    password: str = typer.Option(prompt_required=True, prompt=True),
    specialization: str = typer.Option(prompt_required=True, prompt=True),
    department_id: int | None = typer.Option(prompt_required=False, prompt=True, default=None),
    role_id: int = typer.Option(prompt_required=True, prompt=True, default=1),
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
    freeze_support()
    app()
