import asyncio

import typer
from sqlalchemy import select

from {{ cookiecutter.project_slug }}.auth.models import User
from {{ cookiecutter.project_slug }}.auth.security import hash_password
from {{ cookiecutter.project_slug }}.db import async_session

app = typer.Typer(help="{{ cookiecutter.project_name }} CLI")


@app.command()
def createsuperuser(
  email: str = typer.Option(..., prompt=True),
  password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True),
  full_name: str = typer.Option("", prompt=True),
) -> None:
  """Create a superuser account."""

  async def _create():
    async with async_session() as session:
      result = await session.execute(select(User).where(User.email == email))
      if result.scalar_one_or_none() is not None:
        typer.echo(f"Error: User with email {email} already exists.", err=True)
        raise typer.Exit(code=1)
      user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        is_active=True,
        is_superuser=True,
      )
      session.add(user)
      await session.commit()
      typer.echo(f"Superuser {email} created successfully.")

  asyncio.run(_create())


@app.command()
def seed() -> None:
  """Seed the database with sample data."""
  typer.echo("Seeding database... (not yet implemented)")


if __name__ == "__main__":
  app()
