"""Async Python client for Pulsegrow API."""

from .client import PulsegrowClient
from .exceptions import (
    PulsegrowAuthError,
    PulsegrowConnectionError,
    PulsegrowError,
    PulsegrowRateLimitError,
)
from .models import (
    DataPoint,
    Device,
    DeviceData,
    Hub,
    Invitation,
    LightReading,
    LightReadingsResponse,
    Sensor,
    SensorDetails,
    TimelineEvent,
    TriggeredThreshold,
    UserUsage,
)

try:
    from ._version import version as __version__
except ImportError:
    # Fallback for development installations without setuptools-scm
    __version__ = "0.0.0.dev0"

__all__ = [
    # Client
    "PulsegrowClient",
    # Exceptions
    "PulsegrowError",
    "PulsegrowAuthError",
    "PulsegrowConnectionError",
    "PulsegrowRateLimitError",
    # Models
    "DataPoint",
    "Device",
    "DeviceData",
    "Hub",
    "Invitation",
    "LightReading",
    "LightReadingsResponse",
    "Sensor",
    "SensorDetails",
    "TimelineEvent",
    "TriggeredThreshold",
    "UserUsage",
]
