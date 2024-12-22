from fastapi import FastAPI

from prometheus_client import make_asgi_app
import sensor_app.exporter
# Create app

app = FastAPI(debug=False)



# Add prometheus asgi middleware to route /metrics requests

metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)