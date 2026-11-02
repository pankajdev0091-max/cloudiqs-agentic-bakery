"""
Strands SDK compatibility shim.

Provides fallback stubs for ``Agent`` and ``@tool`` when the Strands Agents
SDK is not installed, allowing the rest of the codebase to import freely
without guarding every single import statement.
"""

try:
    from strands import Agent, tool  # noqa: F401
    from strands.multiagent import GraphBuilder, Swarm  # noqa: F401

    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False

    class Agent:
        """Stub that mirrors the Strands Agent constructor signature."""

        def __init__(self, *, system_prompt: str = "", tools: list = None,
                     name: str = "", **kwargs):
            self.system_prompt = system_prompt
            self.tools = tools or []
            self.name = name

        def __call__(self, message: str, **kwargs):
            return f"[Agent stub] Received: {message}"

    def tool(fn=None, *, name=None, description=None, inputSchema=None,
             context=None, **kwargs):
        """Stub decorator that preserves the function as-is."""
        if fn is None:
            return lambda f: f
        return fn

    class GraphBuilder:
        """Stub for strands.multiagent.GraphBuilder."""
        def add_node(self, *a, **kw): return self
        def add_edge(self, *a, **kw): return self
        def set_entry_point(self, *a, **kw): return self
        def build(self): return None

    class Swarm:
        """Stub for strands.multiagent.Swarm."""
        def __init__(self, **kw): pass
