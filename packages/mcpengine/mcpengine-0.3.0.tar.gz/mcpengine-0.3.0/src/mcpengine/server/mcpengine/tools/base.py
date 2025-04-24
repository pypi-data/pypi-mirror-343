# Copyright (c) 2024 Anthropic, PBC
# Copyright (c) 2025 Featureform, Inc.
#
# Licensed under the MIT License. See LICENSE file in the
# project root for full license information.

from __future__ import annotations as _annotations

import inspect
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from mcpengine.server.auth.errors import AuthenticationError, AuthorizationError
from mcpengine.server.mcpengine.exceptions import ToolError
from mcpengine.server.mcpengine.utilities.func_metadata import (
    FuncMetadata,
    func_metadata,
)

if TYPE_CHECKING:
    from mcpengine.server.mcpengine.server import Context
    from mcpengine.server.session import ServerSessionT
    from mcpengine.shared.context import LifespanContextT


class Tool(BaseModel):
    """Internal tool registration info."""

    fn: Callable[..., Any] = Field(exclude=True)
    name: str = Field(description="Name of the tool")
    description: str = Field(description="Description of what the tool does")
    scopes: list[str] | None = Field(
        None, description="List of scopes required for this tool"
    )
    parameters: dict[str, Any] = Field(description="JSON schema for tool parameters")
    fn_metadata: FuncMetadata = Field(
        description="Metadata about the function including a pydantic model for tool"
        " arguments"
    )
    is_async: bool = Field(description="Whether the tool is async")
    context_kwarg: str | None = Field(
        None, description="Name of the kwarg that should receive context"
    )

    @classmethod
    def from_function(
        cls,
        fn: Callable[..., Any],
        name: str | None = None,
        description: str | None = None,
        scopes: list[str] | None = None,
        context_kwarg: str | None = None,
    ) -> Tool:
        """Create a Tool from a function."""
        from mcpengine.server.mcpengine import Context

        func_name = name or fn.__name__

        if func_name == "<lambda>":
            raise ValueError("You must provide a name for lambda functions")

        func_doc = description or fn.__doc__ or ""
        is_async = inspect.iscoroutinefunction(fn)

        if context_kwarg is None:
            sig = inspect.signature(fn)
            for param_name, param in sig.parameters.items():
                if param.annotation is Context:
                    context_kwarg = param_name
                    break

        func_arg_metadata = func_metadata(
            fn,
            skip_names=[context_kwarg] if context_kwarg is not None else [],
        )
        parameters = func_arg_metadata.arg_model.model_json_schema()

        return cls(
            fn=fn,
            name=func_name,
            description=func_doc,
            scopes=scopes,
            parameters=parameters,
            fn_metadata=func_arg_metadata,
            is_async=is_async,
            context_kwarg=context_kwarg,
        )

    async def run(
        self,
        arguments: dict[str, Any],
        context: Context[ServerSessionT, LifespanContextT] | None = None,
    ) -> Any:
        """Run the tool with arguments."""
        try:
            return await self.fn_metadata.call_fn_with_arg_validation(
                self.fn,
                self.is_async,
                arguments,
                {self.context_kwarg: context}
                if self.context_kwarg is not None
                else None,
            )
        except (AuthenticationError, AuthorizationError) as err:
            raise err
        except Exception as e:
            raise ToolError(f"Error executing tool {self.name}: {e}") from e
