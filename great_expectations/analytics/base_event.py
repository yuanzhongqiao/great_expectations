from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, List, Optional
from uuid import UUID

from great_expectations.analytics.config import get_config


@dataclass(frozen=True)
class Action:
    """Action is the "verb" representing what happened.

    Attributes:
        name: A description of what happened. For example (<object>.<verb>) "validation_result.saved" or "token.deleted"
    """

    name: str

    def __repr__(self):
        return self.name


@dataclass
class Event:
    """Details of an analytics event.

    Attributes:
        action: The "verb" describing what action this event represents.
    """

    action: Action

    @property
    def data_context_id(self) -> UUID:
        return get_config().data_context_id

    @property
    def organization_id(self) -> UUID:
        return get_config().organization_id

    @property
    def oss_id(self) -> UUID:
        return get_config().oss_id

    @property
    def user_id(self) -> UUID:
        return get_config().user_id

    _allowed_actions: ClassVar[Optional[List[Action]]] = None

    def __post_init__(self):
        allowed_actions = self.get_allowed_actions()
        if (
            allowed_actions is not None
            and self.action not in self.get_allowed_actions()
        ):
            raise ValueError(
                f"Action [{self.action}] must be one of {self.get_allowed_actions()}"
            )

    @classmethod
    def get_allowed_actions(cls):
        return cls._allowed_actions

    def properties(self) -> dict:
        props = {
            "data_context_id": self.data_context_id,
            "organization_id": self.organization_id,
            "oss_id": self.oss_id,
            "service": "python-client",
        }
        return {**props, **self._properties()}

    def _properties(self) -> dict:
        """Returns event specific properties.

        Events can be extended with additional properties. Subclasses should define
        a _properties method to return them all as a dict.

        Returns:
            A dict representation of the event specific properties
        """
        return {}
