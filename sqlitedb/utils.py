"""Utility class."""

from enum import Enum


class UserStatus(Enum):
    """User Status."""

    ACTIVE = "active"
    SUSPENDED = "suspended"
    TEMP_BANNED = "temporarily banned"


class ErrorCodes(Enum):
    """List of error codes."""

    exceptions = -1


class UserType(Enum):
    """User type."""

    USER = "user"
    CHANNEL = "channel"
    GROUP = "group"
