"""
Canonical time unit and calendar model.

This module defines the universal timeline representation used internally.
All dates are represented in a UTC-like universal timeline, with localized
display handled in Phase 6 (Visualization).

ARCHITECTURE:
- Internal representation: Universal timeline (UTC-like, continuous)
- Display: Localized calendars (Gregorian, local calendars, time zones) in Phase 6
- Time unit: 1 tick = 1 day (default, configurable)
- Calendar: Gregorian calendar for internal representation
- Time zones: UTC internally, localized in display layer

TIME REPRESENTATION:
- Internal: datetime objects in UTC
- Ticks: Integer count of days since epoch
- Era: String representation (YYYY or YYYY-MM-DD)
- Leap years: Handled by Python datetime
- Time zones: UTC internally, conversion in display layer only
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

# Epoch: January 1, 1 CE (Gregorian calendar)
# Using year 1 as epoch for historical simulations
EPOCH = datetime(1, 1, 1, tzinfo=timezone.utc)

# Default: 1 tick = 1 day
TICKS_PER_DAY = 1


def ticks_to_datetime(ticks: int, epoch: datetime = EPOCH) -> datetime:
    """Convert tick count to datetime.
    
    Args:
        ticks: Number of ticks since epoch
        epoch: Starting point (default: January 1, 1 CE)
        
    Returns:
        datetime in UTC
    """
    return epoch + timedelta(days=ticks * TICKS_PER_DAY)


def datetime_to_ticks(dt: datetime, epoch: datetime = EPOCH) -> int:
    """Convert datetime to tick count.
    
    Args:
        dt: datetime to convert
        epoch: Starting point (default: January 1, 1 CE)
        
    Returns:
        Number of ticks since epoch
    """
    delta = dt - epoch
    return int(delta.total_seconds() / (86400 * TICKS_PER_DAY))


def format_era(dt: datetime, precision: str = "year") -> str:
    """Format datetime as era string.
    
    Args:
        dt: datetime to format
        precision: "year" (YYYY) or "date" (YYYY-MM-DD)
        
    Returns:
        Era string representation
    """
    if precision == "year":
        return str(dt.year)
    elif precision == "date":
        return dt.strftime("%Y-%m-%d")
    else:
        raise ValueError(f"Unknown precision: {precision}")


def parse_era(era_str: str) -> datetime:
    """Parse era string to datetime.
    
    Args:
        era_str: Era string (YYYY or YYYY-MM-DD)
        
    Returns:
        datetime in UTC
    """
    if len(era_str) == 4:
        # Year only
        return datetime(int(era_str), 1, 1, tzinfo=timezone.utc)
    elif len(era_str) == 10:
        # Date format
        return datetime.fromisoformat(era_str).replace(tzinfo=timezone.utc)
    else:
        raise ValueError(f"Invalid era format: {era_str}")


def localize_datetime(dt: datetime, timezone_name: Optional[str] = None) -> datetime:
    """Convert UTC datetime to local timezone (for display only).
    
    This is used in Phase 6 (Visualization) for localized display.
    Internal representation remains UTC.
    
    Args:
        dt: UTC datetime
        timezone_name: Timezone name (e.g., "America/New_York")
        
    Returns:
        Localized datetime (still UTC internally, conversion happens in display)
    """
    # For now, return as-is. Phase 6 will handle timezone conversion
    # This is a placeholder for future timezone support
    return dt

