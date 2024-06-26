# -*- coding: utf-8 -*-
import asyncio
from typing import Any, Dict, Optional

import grpc.aio
from loguru import logger as loguru_logger

from internal.classes.singleton import Singleton
from internal.proto_gens import (
    {{ServiceNameInUnderScoreCase}}_pb2,
    {{ServiceNameInUnderScoreCase}}_pb2_grpc
)
from internal.utils.helper import timeit


class {{ServiceNameInCamelCase}}({{ServiceNameInUnderScoreCase}}_pb2_grpc.{{ServiceNameInCamelCase}}Servicer, metaclass=Singleton):

    def __init__(
        self,
        *,
        conf: Optional[Dict[str, Any]] = None
    ):
        pass

    async def close(self):
        await asyncio.sleep(0)

    @timeit
    async def Ping(
        self,
        request: {{ServiceNameInUnderScoreCase}}_pb2.PingRequest,
        context: grpc.aio.ServicerContext
    ):
        resp = {{ServiceNameInUnderScoreCase}}_pb2.PongResponse()

        metadata = dict(context.invocation_metadata())
        trace_id = metadata.get("x-request-id", "None")
        span_id = ""
        with loguru_logger.contextualize(trace_id=trace_id, span_id=span_id):
            loguru_logger.debug("Ping")
            return resp
