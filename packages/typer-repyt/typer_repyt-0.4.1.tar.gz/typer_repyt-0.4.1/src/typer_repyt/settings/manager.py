import json
from pathlib import Path
from typing import Any, cast

from inflection import dasherize
from pydantic import BaseModel, ValidationError

from typer_repyt.exceptions import (
    ConfigInitError,
    ConfigResetError,
    ConfigSaveError,
    ConfigUnsetError,
    ConfigUpdateError,
)


def get_settings_path(app_name: str) -> Path:
    return Path.home() / ".local/share" / app_name / "settings.json"


class SettingsManager:
    def __init__(self, app_name: str, settings_model: type[BaseModel]):
        self.app_name: str = app_name
        self.settings_model: type[BaseModel] = settings_model
        self.settings_path: Path = get_settings_path(self.app_name)
        self.invalid_warnings: dict[str, str] = {}
        self.settings_instance: BaseModel
        with ConfigInitError.handle_errors("Failed to initialize settings"):
            settings_values: dict[str, Any] = {}
            if self.settings_path.exists():
                settings_values = json.loads(self.settings_path.read_text())
            try:
                self.settings_instance = self.settings_model(**settings_values)
            except ValidationError as err:
                self.settings_instance = self.settings_model.model_construct(**settings_values)
                self.set_warnings(err)

    def set_warnings(self, err: ValidationError):
        self.invalid_warnings = {}
        for data in err.errors():
            key: str = cast(str, data["loc"][0])
            message = data["msg"]
            self.invalid_warnings[key] = message

    def update(self, **settings_values: Any):
        with ConfigUpdateError.handle_errors("Failed to update settings"):
            combined_settings = {**self.settings_instance.model_dump(), **settings_values}
            try:
                self.settings_instance = self.settings_model(**combined_settings)
                self.invalid_warnings = {}
            except ValidationError as err:
                self.settings_instance = self.settings_model.model_construct(**combined_settings)
                self.set_warnings(err)

    def unset(self, *unset_keys: str):
        with ConfigUnsetError.handle_errors("Failed to remove keys"):
            settings_values = {k: v for (k, v) in self.settings_instance.model_dump().items() if k not in unset_keys}
            try:
                self.settings_instance = self.settings_model(**settings_values)
                self.invalid_warnings = {}
            except ValidationError as err:
                self.settings_instance = self.settings_model.model_construct(**settings_values)
                self.set_warnings(err)

    def reset(self):
        with ConfigResetError.handle_errors("Failed to reset settings"):
            try:
                self.settings_instance = self.settings_model()
                self.invalid_warnings = {}
            except ValidationError as err:
                self.settings_instance = self.settings_model.model_construct()
                self.set_warnings(err)

    def validate(self):
        self.settings_model(**self.settings_instance.model_dump())

    def pretty(self, with_style: bool = True) -> str:
        (bold_, _bold) = ("[bold]", "[/bold]") if with_style else ("", "")
        (red_, _red) = ("[red]", "[/red]") if with_style else ("", "")
        lines: list[str] = []
        parts: list[tuple[str, Any]] = []
        for field_name, field_value in self.settings_instance:
            if field_name == "invalid_warning":
                continue
            field_string = str(field_value)
            if field_name in self.invalid_warnings:
                field_string = f"{red_}{field_string}{_red}"
            parts.append((dasherize(field_name), field_string))

        max_field_len = max(len(field_name) for field_name, _ in parts)
        lines.extend(f"{bold_}{k:>{max_field_len}}{_bold} -> {v}" for k, v in parts)

        if self.invalid_warnings:
            lines.append("")
            lines.append(f"{red_}Configuration is invalid:{_red}")
            lines.extend(f"{bold_}{k:>{max_field_len}}{_bold} -> {v}" for k, v in self.invalid_warnings.items())

        return "\n".join(lines)

    def save(self):
        with ConfigSaveError.handle_errors(f"Failed to save settings to {self.settings_path}"):
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            self.settings_path.write_text(self.settings_instance.model_dump_json(indent=2))
