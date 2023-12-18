# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.curdir), "internal", "proto_gens"))

import argparse
import asyncio
import traceback
from typing import Any, Dict

import grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger as loguru_logger

from internal.logger.loguru_logger import init_global_logger
from internal.proto_gens import (
    {{ServiceNameInUnderScoreCase}}_pb2,
    {{ServiceNameInUnderScoreCase}}_pb2_grpc
)
from internal.service.impl import {{ServiceNameInCamelCase}}
from internal.utils.global_vars import get_config, set_config

# Coroutine to be invoked when the event loop is shutting down.
_cleanup_coroutine = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--conf",
        type=str,
        default="./etc/{{ServiceName}}-dev.json",
        help="the service config file",
    )
    args = parser.parse_args()
    set_config(args.conf)


async def serve(conf: Dict[str, Any]):
    global _cleanup_coroutine

    server = grpc.aio.server(
        options=(
            ("grpc.keepalive_time_ms", 10000),
            ("grpc.keepalive_timeout_ms", 3000),
            ("grpc.keepalive_permit_without_calls", True),
            ("grpc.http2.max_pings_without_data", 0),
            ("grpc.http2.min_time_between_pings_ms", 10000),
            ("grpc.http2.min_ping_interval_without_data_ms", 5000),
        )
    )
    servicer = {{ServiceNameInCamelCase}}(conf)
    {{ServiceNameInUnderScoreCase}}_pb2_grpc.add_{{ServiceNameInCamelCase}}Servicer_to_server(servicer, server)
    SERVICE_NAMES = (
        {{ServiceNameInUnderScoreCase}}_pb2.DESCRIPTOR.services_by_name["{{ServiceNameInCamelCase}}"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:{}".format(conf["service_port"]))
    await server.start()
    loguru_logger.info("Server started, listening on [::]:{}".format(conf["service_port"]))
    loguru_logger.info("Started {{ServiceNameInCamelCase}} Server 🤘.")

    async def server_graceful_shutdown():
        loguru_logger.warning("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(grace=5)
        await servicer.close()
        loguru_logger.info("Stopped {{ServiceNameInCamelCase}} Server 🤘.")
    _cleanup_coroutine = server_graceful_shutdown

    await server.wait_for_termination()


if __name__ == "__main__":
    parse_args()
    conf = get_config()
    init_global_logger(level=conf["log_level"])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(serve(conf=conf))
    except Exception:
        traceback.print_exc()
    finally:
        tasks = []
        if _cleanup_coroutine is not None:
            tasks.append(asyncio.ensure_future(_cleanup_coroutine()))
        loop.run_until_complete(asyncio.gather(*tasks))
        # NOTE: Wait 250 ms for the underlying connections to close.
        # https://docs.aiohttp.org/en/stable/client_advanced.html#Graceful_Shutdown
        loop.run_until_complete(asyncio.sleep(0.250))
        loop.close()
