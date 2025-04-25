"""This module provides general helpers for traces with no dependencies on the agent evaluation harness."""

import json
import time
import uuid
from typing import Any, Dict, List, Optional

import mlflow.entities as mlflow_entities
import mlflow.tracing.constant as mlflow_tracing_constant
from mlflow.tracing.utils import (
    build_otel_context,
    decode_id,
)
from opentelemetry.sdk.trace import ReadableSpan as OTelReadableSpan
from opentelemetry.sdk.trace import Status, StatusCode

_TRACE_REQUEST_METADATA_LEN_LIMIT = 250


def span_is_type(
    span: mlflow_entities.Span,
    span_type: str | List[str],
) -> bool:
    """Check if the span is of a certain span type or one of the span types in the collection"""
    if span.attributes is None:
        return False
    if not isinstance(span_type, List):
        span_type = [span_type]
    return (
        span.attributes.get(mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE)
        in span_type
    )


def get_leaf_spans(trace: mlflow_entities.Trace) -> List[mlflow_entities.Span]:
    """Get all leaf spans in the trace."""
    if trace.data is None:
        return []
    spans = trace.data.spans or []
    leaf_spans_by_id = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_id:
            leaf_spans_by_id.pop(span.parent_id, None)
    return list(leaf_spans_by_id.values())


def get_root_span(trace: mlflow_entities.Trace) -> Optional[mlflow_entities.Span]:
    """Get the root span in the trace."""
    if trace.data is None:
        return None
    spans = trace.data.spans or []
    # Root span is the span that has no parent
    return next((span for span in spans if span.parent_id is None), None)


# ================== Trace Creation/Modification ==================
def _generate_trace_id() -> str:
    """
    Generate a new trace ID. This is a 16-byte hex string.
    """
    return uuid.uuid4().hex


def _generate_span_id() -> str:
    """
    Generate a new span ID. This is a 8-byte hex string.
    """
    return uuid.uuid4().hex[:16]  # OTel span spec says it's only 8 bytes (16 hex chars)


def create_minimal_trace(
    request: Dict[str, Any],
    response: Any,
    retrieval_context: Optional[List[Dict[str, str]]] = None,
) -> mlflow_entities.Trace:
    """
    Create a minimal trace object with a single span, based on given request/response.
    This trace is not associated with any run or experiment.

    :param request: The request object. This is expected to be a JSON-serializable object
    :param response: The response object. This is expected to be a JSON-serializable object, but we cannot guarantee this
    :return: A new trace object.
    """
    serialized_request = (
        json.dumps(request, default=lambda o: o.__dict__)
        if not isinstance(request, str)
        else request
    )
    # Do a best-effort conversion to dump the raw model output, otherwise just dump the string
    try:
        serialized_response = (
            json.dumps(response, default=lambda o: o.__dict__)
            if not isinstance(response, str)
            else response
        )
    except:
        serialized_response = str(response)

    request_metadata = {
        mlflow_tracing_constant.TraceMetadataKey.INPUTS: serialized_request[
            :_TRACE_REQUEST_METADATA_LEN_LIMIT
        ],
        mlflow_tracing_constant.TraceMetadataKey.OUTPUTS: serialized_response[
            :_TRACE_REQUEST_METADATA_LEN_LIMIT
        ],
    }

    # We force-serialize the request/response to fit into OpenTelemetry attributes, which require
    # JSON-serialized values.
    attribute_request = json.dumps(request, default=lambda o: o.__dict__)
    # Do a best-effort conversion to dump the raw model output, otherwise just dump the string
    try:
        attribute_response = json.dumps(response, default=lambda o: o.__dict__)
    except:
        attribute_response = json.dumps(str(response))

    trace_id = _generate_trace_id()
    info = mlflow_entities.TraceInfo(
        request_id=trace_id,
        experiment_id=None,
        status=mlflow_entities.trace_status.TraceStatus.OK,
        timestamp_ms=time.time_ns() // 1_000_000,
        execution_time_ms=0,
        request_metadata=request_metadata,
    )
    root_span = mlflow_entities.Span(
        otel_span=OTelReadableSpan(
            name="root_span",
            context=build_otel_context(
                trace_id=decode_id(trace_id), span_id=decode_id(_generate_span_id())
            ),
            status=Status(StatusCode.OK),
            parent=None,
            attributes={
                mlflow_tracing_constant.SpanAttributeKey.REQUEST_ID: json.dumps(
                    trace_id
                ),
                mlflow_tracing_constant.SpanAttributeKey.INPUTS: attribute_request,
                mlflow_tracing_constant.SpanAttributeKey.OUTPUTS: attribute_response,
            },
        ),
    )

    spans = [root_span]
    # Create a retrieval span if retrieval_context is provided
    if retrieval_context is not None:
        retrieval_span = mlflow_entities.Span(
            otel_span=OTelReadableSpan(
                name="retrieval_span",
                context=build_otel_context(
                    trace_id=decode_id(trace_id), span_id=decode_id(_generate_span_id())
                ),
                status=Status(StatusCode.OK),
                parent=root_span._span.context,
                attributes={
                    mlflow_tracing_constant.SpanAttributeKey.REQUEST_ID: json.dumps(
                        trace_id
                    ),
                    mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE: json.dumps(
                        mlflow_entities.SpanType.RETRIEVER
                    ),
                    mlflow_tracing_constant.SpanAttributeKey.OUTPUTS: json.dumps(
                        retrieval_context
                    ),
                },
            ),
        )
        spans.append(retrieval_span)

    data = mlflow_entities.TraceData(
        request=serialized_request, response=serialized_response, spans=spans
    )
    trace = mlflow_entities.Trace(info=info, data=data)
    return trace


def create_minimal_error_trace(
    request: Dict[str, Any], response: Any
) -> mlflow_entities.Trace:
    """
    Create a minimal trace object with a single span, based on given request/response and error message.

    :param request: The request object. This is expected to be a JSON-serializable object
    :param response: The response object. This is expected to be a JSON-serializable object, but we cannot guarantee this
    :return: A new trace object.
    """
    trace = create_minimal_trace(request, response)
    trace.info.status = mlflow_entities.trace_status.TraceStatus.ERROR
    return trace


def inject_experiment_run_id_to_trace(
    trace: mlflow_entities.Trace, experiment_id: str, run_id: str
) -> mlflow_entities.Trace:
    """
    Inject the experiment and run ID into the trace metadata.

    :param trace: The trace object
    :param experiment_id: The experiment ID to inject
    :param run_id: The run ID to inject
    :return: The updated trace object
    """
    if trace.info.request_metadata is None:
        trace.info.request_metadata = {}
    trace.info.request_metadata[mlflow_tracing_constant.TraceMetadataKey.SOURCE_RUN] = (
        run_id
    )
    trace.info.experiment_id = experiment_id
    return trace


def update_trace_id(
    trace: mlflow_entities.Trace, new_trace_id: str
) -> mlflow_entities.Trace:
    """
    Helper method to update the trace ID of a trace object. This method updates both the TraceInfo
    as well as the trace ID of all spans in the trace.

    :param trace: The trace object
    :param new_trace_id: The new trace ID
    :return: The updated trace object
    """
    trace.info.request_id = new_trace_id
    trace.data.spans = [
        mlflow_entities.LiveSpan.from_immutable_span(
            span, span.parent_id, new_trace_id, new_trace_id
        ).to_immutable_span()
        for span in trace.data.spans
    ]
    return trace


def clone_trace_to_reupload(trace: mlflow_entities.Trace) -> mlflow_entities.Trace:
    """
    Prepare a trace for cloning by resetting traceId and clearing various fields.
    This has the downstream effect of causing the trace to be recreated with a new trace_id.

    :param trace: The trace to prepare
    :return: The prepared trace
    """
    prepared_trace = mlflow_entities.Trace.from_dict(trace.to_dict())

    # Since the semantics of this operation are to _clone_ the trace, and assessments are tied to
    # a specific trace, we clear assessments as well.
    prepared_trace.info.assessments = []

    # Tags and metadata also contain references to the source run, trace data artifact location, etc.
    # We clear these as well to ensure that the trace is not tied to the original source of the trace.
    for key in [k for k in prepared_trace.info.tags.keys() if k.startswith("mlflow.")]:
        prepared_trace.info.tags.pop(key)
    for key in [
        k
        for k in prepared_trace.info.request_metadata.keys()
        if k.startswith("mlflow.")
        and k
        not in [
            mlflow_tracing_constant.TraceMetadataKey.INPUTS,
            mlflow_tracing_constant.TraceMetadataKey.OUTPUTS,
        ]
    ]:
        prepared_trace.info.request_metadata.pop(key)

    return update_trace_id(prepared_trace, uuid.uuid4().hex)
