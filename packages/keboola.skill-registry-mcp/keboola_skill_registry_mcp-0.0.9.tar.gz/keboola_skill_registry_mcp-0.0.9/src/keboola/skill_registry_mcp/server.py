"""MCP server implementation for Keboola Skill Registry."""

import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional, AsyncIterator

from mcp.server.fastmcp import FastMCP

from .client import SkillRegistryClient
from .config import Config
from .mcp import KeboolaSkillRegistryMcpServer
from .sr_tools import SRToolManager

logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    sr_client: SkillRegistryClient


def context_factory(sr_client: SkillRegistryClient):
    @asynccontextmanager
    async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
        """Manage application lifecycle with type-safe context"""
        # Initialize on startup
        client = sr_client
        try:
            yield AppContext(sr_client=client)
        finally:
            pass

    return app_lifespan


def create_server(config: Optional[Config] = None) -> FastMCP:
    """Create and configure the MCP server.

    Args:
        config: Server configuration. If None, loads from environment.

    Returns:
        Configured FastMCP server instance
    """
    # Initialize FastMCP server with system instructions
    sr_client = SkillRegistryClient(config.skill_registry_url, config.skill_registry_token)
    sr_manager = SRToolManager.from_skill_registry(sr_client)

    mcp = KeboolaSkillRegistryMcpServer(
        "Agent Skill Set",
        dependencies=["httpx"],
        lifespan=context_factory(sr_client),
        sr_manager=sr_manager,
    )

    return mcp
