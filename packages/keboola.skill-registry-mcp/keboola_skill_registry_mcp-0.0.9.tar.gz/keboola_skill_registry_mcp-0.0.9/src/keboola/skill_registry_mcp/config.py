"""Configuration handling for the Keboola MCP server."""

import dataclasses
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    """Server configuration."""

    skill_registry_token: str
    skill_registry_url: str = 'http://localhost:8888/'

    def __repr__(self):
        params: list[str] = []
        for f in dataclasses.fields(self):
            value = getattr(self, f.name)
            if value:
                if "token" in f.name or "password" in f.name:
                    params.append(f"{f.name}='****'")
                else:
                    params.append(f"{f.name}='{value}'")
            else:
                params.append(f"{f.name}=None")
        return f'Config({", ".join(params)})'
