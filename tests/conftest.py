"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def event_loop_policy():
    """Set event loop policy for tests."""
    import asyncio

    return asyncio.DefaultEventLoopPolicy()
