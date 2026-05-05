from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Counter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
import os

# Business Metric
REGISTRATIONS_TOTAL = Counter(
    "synq_registrations_total", 
    "Total number of user registrations"
)

def setup_monitoring(app: FastAPI):
    # Prometheus
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=[".*admin.*", "/metrics", "/health"],
        env_var_name="ENABLE_METRICS",
    )
    instrumentator.add(metrics.request_size())
    instrumentator.add(metrics.response_size())
    instrumentator.add(metrics.latency())
    instrumentator.add(metrics.requests())
    instrumentator.instrument(app).expose(app)

    # OpenTelemetry Tracing
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4317")
    
    resource = Resource.create({"service.name": "synq-backend"})
    provider = TracerProvider(resource=resource)
    
    # Use OTLP Exporter (gRPC by default for 4317)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)

def count_registration():
    REGISTRATIONS_TOTAL.inc()
