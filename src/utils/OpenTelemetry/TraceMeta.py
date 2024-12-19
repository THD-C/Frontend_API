from opentelemetry import trace
from opentelemetry.trace import Tracer
from opentelemetry.trace.status import Status, StatusCode
from functools import wraps


def trace_method(tracer: Tracer, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__) as span:
            try:
                result = func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)

    return wrapper


def record_trace_exception(e: Exception):
    span = trace.get_current_span()
    span.record_exception(e)
    span.set_status(status=Status(StatusCode.ERROR, str(e)))


class TraceMeta(type):
    def __new__(cls, name, bases, dct):
        tracer = trace.get_tracer(name)
        for attr, value in dct.items():
            if callable(value):
                dct[attr] = trace_method(tracer, value)
        return super().__new__(cls, name, bases, dct)
