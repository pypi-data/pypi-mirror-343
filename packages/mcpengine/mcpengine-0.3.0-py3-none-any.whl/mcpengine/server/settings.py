# Copyright (c) 2024 Anthropic, PBC
# Copyright (c) 2025 Featureform, Inc.
#
# Licensed under the MIT License. See LICENSE file in the
# project root for full license information.

from __future__ import annotations as _annotations

from collections.abc import Callable
from contextlib import (
    AbstractAsyncContextManager,
)
from typing import Any, Generic, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from mcpengine.server.auth.providers.config import IdpConfig
from mcpengine.server.lowlevel.server import LifespanResultT


class Settings(BaseSettings, Generic[LifespanResultT]):
    """MCPEngine server settings.

    All settings can be configured via environment variables with the prefix MCPENGINE_.
    For example, MCPENGINE_DEBUG=true will set debug=True.
    """

    model_config = SettingsConfigDict(
        env_prefix="MCPENGINE_",
        env_file=".env",
        extra="ignore",
    )

    # Server settings
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # HTTP settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Used for the SSE handling in 2024-11-05 version.
    sse_path: str = "/sse"
    message_path: str = "/messages/"

    # Used for the single HTTP endpoint path in 2025-03-26 version.
    mcp_path: str = "/mcp"

    # resource settings
    warn_on_duplicate_resources: bool = True

    # tool settings
    warn_on_duplicate_tools: bool = True

    # prompt settings
    warn_on_duplicate_prompts: bool = True

    dependencies: list[str] = Field(
        default_factory=list,
        description="List of dependencies to install in the server environment",
    )

    lifespan: Callable[[Any], AbstractAsyncContextManager[LifespanResultT]] | None = (
        Field(None, description="Lifespan context manager")
    )

    # auth settings
    idp_config: IdpConfig | None = Field(
        None, description="Configuration for an OAuth2 or OIDC provider"
    )
