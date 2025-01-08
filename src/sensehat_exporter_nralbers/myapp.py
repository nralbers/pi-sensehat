from fastapi import FastAPI
from prometheus_client import REGISTRY, make_asgi_app

from sensehat_exporter_nralbers.exporter import CustomCollector

# Create app

app = FastAPI(debug=False)
REGISTRY.register(CustomCollector())

# Add prometheus asgi middleware to route /metrics requests

metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)
