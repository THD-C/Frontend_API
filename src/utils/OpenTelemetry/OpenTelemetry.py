from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import src.utils.OpenTelemetry.config as Config


# OpenTelemetry
trace_resource = Resource.create(
    attributes={
        SERVICE_NAME: Config.SERVICE_NAME,
    }
)
trace.set_tracer_provider(TracerProvider(resource=trace_resource))

# OTLP Exporter
# if Config.USE_TEMPO:
otlp_exporter: OTLPSpanExporter = OTLPSpanExporter(
    endpoint=f"http://{Config.TEMPO_HOSTNAME}:{Config.TEMPO_PORT}", insecure="true"
)
span_processor: BatchSpanProcessor = BatchSpanProcessor(otlp_exporter)
tracer_provider: TracerProvider = trace.get_tracer_provider()
tracer_provider.add_span_processor(span_processor)


def get_trace_id() -> str:
    current_span = trace.get_current_span()
    trace_id = current_span.get_span_context().trace_id
    if trace_id == 0:
        str_trace_id = None
    else:
        str_trace_id = "{trace:032x}".format(trace=trace_id)

    return str_trace_id


def get_span_id() -> str:
    current_span = trace.get_current_span()
    span_id = current_span.get_span_context().span_id

    if span_id == 0:
        str_span_id = None
    else:
        str_span_id = "{span:016x}".format(span=span_id)

    return str_span_id


def get_response_headers() -> dict[str, str]:
    return {"trace_id": get_trace_id()}


def get_current_span():
    current_span = trace.get_current_span()
    current_span.set_status(status=trace.StatusCode(2))

    return current_span


def set_current_span_status(errors: bool | set[bool] = None):
    current_span = trace.get_current_span()

    if errors is None:
        current_span.set_status(status=trace.StatusCode(1))
        return None

    if isinstance(errors, bool):
        if errors is not True:
            current_span.set_status(status=trace.StatusCode(1))

    elif isinstance(errors, set):
        if True not in errors:
            current_span.set_status(status=trace.StatusCode(1))
