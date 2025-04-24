from importlib.metadata import version

def test_version_matches_package():
    assert version("mcp-context-pointer") == __import__("mcp_context_pointer").__version__ 