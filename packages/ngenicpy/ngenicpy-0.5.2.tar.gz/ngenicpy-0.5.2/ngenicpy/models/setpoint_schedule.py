"""Setpoint Schedule model for Ngenic Tune API."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx

from ..const import API_PATH  # noqa: TID252
from .base import NgenicBase

_LOGGER = logging.getLogger(__name__)


class SetpointSchedule(NgenicBase):
    """Setpoint Schedule model for Ngenic Tune API."""

    def __init__(
        self,
        session: httpx.AsyncClient,
        json_data: dict[str, Any],
        tune_uuid: str,
        away_days: int = 60,
    ) -> None:
        """Initialize the model."""
        self._parent_tune_uuid = tune_uuid
        self._away_days = away_days

        super().__init__(session=session, json_data=json_data)

        now = datetime.now(UTC).replace(second=0, microsecond=0)

        self._active = (
            (now >= self.start_time() and now < self.end_time())
            if self.start_time() is not None and self.end_time() is not None
            else False
        )

    def start_time(self) -> datetime | None:
        """Get startTime attribute."""

        try:
            date_string = self["startTime"]
        except Exception:  # pylint: disable=broad-except
            date_string = None

        try:
            return datetime.fromisoformat(date_string).astimezone(UTC)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.debug("Failed to parse startTime: %s", date_string)
            return None

    def end_time(self) -> datetime | None:
        """Get endTime attribute."""

        try:
            date_string = self["endTime"]
        except Exception:  # pylint: disable=broad-except
            date_string = None

        try:
            return datetime.fromisoformat(date_string).astimezone(UTC)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.debug("Failed to parse endTime: %s", date_string)
            return None

    def name(self) -> str:
        """Get name attribute."""
        return self["name"]

    def active(self) -> bool:
        """Get active attribute."""
        return self._active

    def activate_away(self) -> None:
        """Set the away schedule as activated from now on."""
        self._active = True
        now = datetime.now(UTC).replace(second=0, microsecond=0)

        # set schedule startTime to datetime.now(UTC) in ISO 8601:2004
        self["startTime"] = now.isoformat()

        # set schedule endTime to datetime.now(UTC) + XX days in ISO 8601:2004
        self["endTime"] = (now + timedelta(days=self._away_days)).isoformat()

    def deactivate_away(self) -> None:
        """Set the away schedule as deactivated."""
        self._active = False
        self["startTime"] = None
        self["endTime"] = None

    def set_schedule(self, start_time: datetime, end_time: datetime) -> None:
        """Set custom schedule."""
        self._active = True
        self["startTime"] = start_time.astimezone(UTC).isoformat()
        self["endTime"] = end_time.astimezone(UTC).isoformat()

    def update(self) -> None:
        """Update this schedule with its current values."""

        url = API_PATH["setpoint_schedules"].format(tune_uuid=self._parent_tune_uuid)

        try:
            schedule_uuid = self.uuid()
        except Exception:  # pylint: disable=broad-except
            schedule_uuid = None

        if not self._active and schedule_uuid is None:
            _LOGGER.debug("Deactivated schedule with no UUID, skipping update")
        elif not self._active:
            self._delete(f"{url}/{schedule_uuid}")
        elif schedule_uuid is not None:
            self._put(f"{url}/{schedule_uuid}", data=self.json())
        else:
            self._post(url, data=self.json())

    async def async_update(self) -> None:
        """Update this schedule with its current values (async)."""

        url = API_PATH["setpoint_schedules"].format(tune_uuid=self._parent_tune_uuid)

        try:
            schedule_uuid = self.uuid()
        except Exception:  # pylint: disable=broad-except
            schedule_uuid = None

        if not self._active and schedule_uuid is None:
            _LOGGER.debug("Deactivated schedule with no UUID, skipping update")
        elif not self._active:
            await self._async_delete(f"{url}/{schedule_uuid}")
        elif schedule_uuid is not None:
            await self._async_put(f"{url}/{schedule_uuid}", data=self.json())
        else:
            await self._async_post(url, data=self.json())
