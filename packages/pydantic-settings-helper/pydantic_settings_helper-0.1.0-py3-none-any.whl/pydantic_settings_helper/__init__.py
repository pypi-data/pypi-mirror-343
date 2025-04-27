from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class PydanticSettingsSetupError(RuntimeError):
    """Custom exception for Pydantic settings setup errors."""

    def __init__(self, message: str, original_exception: ValidationError | None = None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception


def load_settings[SettingsClass: type[BaseSettings]](
    settings_class: SettingsClass,
) -> SettingsClass:
    model_config = settings_class.model_config
    env_prefix = model_config.get("env_prefix")
    cli_prefix = model_config.get("cli_prefix")
    try:
        return settings_class()
    except ValidationError as exc:
        lines = ["\nConfiguration error — missing values:\n"]
        for err in exc.errors():
            error_location: tuple[int | str, ...] = err["loc"]
            full_error_location = ".".join(
                str(error_location_part) for error_location_part in error_location
            )
            env_var = f"{env_prefix}{full_error_location.replace('.', '_').upper()}"
            cli_flag = f"--{cli_prefix}{full_error_location.replace('.', '-')}"
            lines.append(
                f" • `{full_error_location}` → set via ${env_var!r} or `{cli_flag}`"
            )
        raise PydanticSettingsSetupError("\n".join(lines), exc)


def SettingsSubModel(
    *args,
    **kwargs,
):
    """A wrapper for Field to create a settings sub-model."""
    return Field(
        *args,
        default_factory=dict,
        validate_default=True,
        **kwargs,
    )
