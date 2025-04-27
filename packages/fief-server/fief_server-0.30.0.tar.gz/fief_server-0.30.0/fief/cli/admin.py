import asyncio
import functools
import os

import typer
import uvicorn
from dramatiq import cli as dramatiq_cli

from fief import __version__
from fief.db.main import create_main_engine
from fief.db.migration import migrate_schema
from fief.services.initializer import (
    AdminAPIKeyAlreadyExists,
    DefaultTenantDoesNotExist,
    Initializer,
    UserDoesNotExist,
)
from fief.services.user_manager import InvalidPasswordError, UserAlreadyExistsError
from fief.services.user_roles import UserRoleAlreadyExists
from fief.settings import settings


def asyncio_command(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


engine = create_main_engine()
initializer = Initializer(engine, settings)


def add_commands(app: typer.Typer) -> typer.Typer:
    @app.command("create-admin")
    @asyncio_command
    async def create_admin(
        user_email: str = typer.Option(..., help="The admin user email"),
        user_password: str = typer.Option(
            ...,
            prompt=True,
            confirmation_prompt=True,
            hide_input=True,
            help="The admin user password",
        ),
    ):
        """Create a an admin user."""

        try:
            await initializer.create_admin(user_email, user_password)
            typer.echo("Admin created")
        except DefaultTenantDoesNotExist as e:
            typer.secho(
                "Default tenant does not exist. Please run 'fief migrate'", fg="red"
            )
            raise typer.Exit(code=1) from e
        except UserAlreadyExistsError as e:
            typer.secho("User already exists", fg="red")
            raise typer.Exit(code=1) from e
        except InvalidPasswordError as e:
            typer.secho(
                f"Invalid password: {', '.join(map(str, e.messages))}",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1) from e

    @app.command("create-admin-api-key")
    @asyncio_command
    async def create_main_admin_api_key(
        token: str = typer.Argument(..., help="The admin API key token"),
    ):
        """Create a main Fief admin API key."""
        try:
            await initializer.create_admin_api_key(token)
            typer.echo("Admin API key created")
        except AdminAPIKeyAlreadyExists as e:
            typer.secho("Admin API key already exists", fg="red")
            raise typer.Exit(code=1) from e

    @app.command("grant-admin-role")
    @asyncio_command
    async def grant_admin_role(
        user_email: str = typer.Argument(..., help="The admin user email"),
    ):
        """Grant the admin role to an existing user."""

        try:
            await initializer.grant_admin_role(user_email)
            typer.echo("Admin role granted")
        except DefaultTenantDoesNotExist as e:
            typer.secho(
                "Default tenant does not exist. Please run 'fief migrate'", fg="red"
            )
            raise typer.Exit(code=1) from e
        except UserDoesNotExist as e:
            typer.secho("User does not exist", fg="red")
            raise typer.Exit(code=1) from e
        except UserRoleAlreadyExists as e:
            typer.secho("User already has the admin role", fg="red")
            raise typer.Exit(code=1) from e

    @app.command()
    def info():
        """Show current Fief version and settings."""
        typer.secho(f"Fief version: {__version__}", bold=True)
        typer.secho("Settings", bold=True)
        for key, value in settings.model_dump().items():
            typer.echo(f"{key}: {value}")

    @app.command("migrate")
    @asyncio_command
    async def migrate():
        """
        Apply database migrations to the database and initialize required objects.
        """
        await migrate_schema(engine)
        await initializer.init_all()

    @app.command(
        "run-server",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    )
    def run_server(
        ctx: typer.Context,
        host: str = "0.0.0.0",
        migrate: bool = typer.Option(
            True,
            help="Run the migrations and initialize required objects before starting.",
        ),
        create_main_user: bool = typer.Option(
            True, help="Create the main Fief user before starting if needed."
        ),
        create_main_admin_api_key: bool = typer.Option(
            True, help="Create the main Fief admin API key before starting if needed."
        ),
        app: str = typer.Option(
            os.environ.get("FIEF_ASGI_APP_PATH", "fief.app:app"),
            help="The ASGI app to run.",
        ),
    ):
        """Run the Fief server."""

        async def _pre_run_server():
            if migrate:
                await migrate_schema(engine)
                await initializer.init_all()

            if create_main_user:
                user_email = settings.fief_main_user_email
                user_password = (
                    settings.fief_main_user_password.get_secret_value()
                    if settings.fief_main_user_password
                    else None
                )
                if user_email is None:
                    typer.secho(
                        "Admin email not provided in settings. Skipping its creation.",
                        fg=typer.colors.YELLOW,
                    )
                else:
                    try:
                        await initializer.create_admin(user_email, user_password)
                        typer.echo("Admin created")
                    except DefaultTenantDoesNotExist as e:
                        typer.secho(
                            "Default tenant does not exist. Please run 'fief migrate'",
                            fg="red",
                        )
                        raise typer.Exit(code=1) from e
                    except InvalidPasswordError as e:
                        typer.secho(
                            f"Invalid password: {', '.join(map(str, e.messages))}",
                            fg=typer.colors.RED,
                        )
                        raise typer.Exit(code=1) from e
                    except UserAlreadyExistsError:
                        typer.echo("Admin already exists")

            if create_main_admin_api_key:
                token = settings.fief_main_admin_api_key
                if token is None:
                    typer.secho(
                        "Admin API key not provided in settings. Skipping its creation.",
                        fg=typer.colors.YELLOW,
                    )
                else:
                    try:
                        await initializer.create_admin_api_key(token.get_secret_value())
                        typer.echo("Admin API key created")
                    except AdminAPIKeyAlreadyExists:
                        typer.secho("This admin API key already exists")

        asyncio.run(_pre_run_server())

        args = [*ctx.args, app]
        uvicorn_context = uvicorn.main.make_context(None, args, parent=ctx)
        uvicorn_context.forward(uvicorn.main, app=app, host=host, port=settings.port)

    @app.command(
        "run-worker",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
        add_help_option=False,
    )
    def run_worker(
        ctx: typer.Context,
        worker: str = typer.Option(
            os.environ.get("FIEF_WORKER_PATH", "fief.worker"), help="The worker to run."
        ),
        scheduler: str = typer.Option(
            os.environ.get("FIEF_SCHEDULER_PATH", "fief.scheduler:schedule"),
            help="The scheduler to run.",
        ),
    ):
        """
        Run the Fief worker.

        Just forwards the options to the Dramatiq CLI.
        """
        parser = dramatiq_cli.make_argument_parser()
        args = parser.parse_args(ctx.args + [worker, f"-f{scheduler}"])
        dramatiq_cli.main(args)

    return app
