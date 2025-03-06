import os

from app import create_app

app = create_app()
app.run(
    host=os.environ.get("BIND_HOST", '0.0.0.0'),
    port=os.environ.get("BIND_PORT", 80),
)
