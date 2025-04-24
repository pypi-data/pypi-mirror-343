# Copyright (c) 2024 Anthropic, PBC
# Copyright (c) 2025 Featureform, Inc.
#
# Licensed under the MIT License. See LICENSE file in the
# project root for full license information.

import argparse
import logging
import sys
from functools import partial
from urllib.parse import urlparse

import anyio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

import mcpengine.types as types
from mcpengine.client.session import ClientSession
from mcpengine.client.sse import sse_client
from mcpengine.client.stdio import StdioServerParameters, stdio_client
from mcpengine.client.transports.http import http_client
from mcpengine.shared.session import RequestResponder
from mcpengine.types import JSONRPCMessage

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("client")


async def message_handler(
    message: RequestResponder[types.ServerRequest, types.ClientResult]
    | types.ServerNotification
    | Exception,
) -> None:
    if isinstance(message, Exception):
        logger.error("Error: %s", message)
        return

    logger.info("Received message from server: %s", message)


async def run_session(
    read_stream: MemoryObjectReceiveStream[JSONRPCMessage | Exception],
    write_stream: MemoryObjectSendStream[JSONRPCMessage],
):
    async with ClientSession(
        read_stream, write_stream, message_handler=message_handler
    ) as session:
        logger.info("Initializing session")
        await session.initialize()
        logger.info("Initialized")


async def main(
    command_or_url: str, args: list[str], env: list[tuple[str, str]], http_mode: str
):
    env_dict = dict(env)

    if urlparse(command_or_url).scheme in ("http", "https"):
        if http_mode == "http":
            async with http_client(command_or_url) as streams:
                await run_session(*streams)
        elif http_mode == "sse":
            async with sse_client(command_or_url) as streams:
                await run_session(*streams)
        else:
            raise ValueError("http_mode must be one of 'http' or 'sse'")
    else:
        # Use stdio client for commands
        server_parameters = StdioServerParameters(
            command=command_or_url, args=args, env=env_dict
        )
        async with stdio_client(server_parameters) as streams:
            await run_session(*streams)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("command_or_url", help="Command or URL to connect to")
    parser.add_argument("args", nargs="*", help="Additional arguments")
    parser.add_argument(
        "-e",
        "--env",
        nargs=2,
        action="append",
        metavar=("KEY", "VALUE"),
        help="Environment variables to set. Can be used multiple times.",
        default=[],
    )
    parser.add_argument(
        "-m",
        "--http-mode",
        choices=["http", "sse"],
        default="sse",
        help="The style of HTTP communication to use.",
    )

    args = parser.parse_args()
    anyio.run(
        partial(main, args.command_or_url, args.args, args.env, args.http_mode),
        backend="trio",
    )


if __name__ == "__main__":
    cli()
