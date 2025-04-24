    # server.py
from mcp.server import create_app, command, expose

@command
def hello(name: str) -> str:
    """Says hello to the given name."""
    return f"Hello, {name}!"

app = create_app()