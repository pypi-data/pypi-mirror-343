from typing import Any, Callable

from pydantic import BaseModel, ConfigDict, model_serializer

import logging
import os


def make_logger(name: str, level: str = "INFO"):
    logger = logging.getLogger(name)
    level_name = os.environ.get("AGENT_LOGGING_LEVEL", level).upper()
    numeric_level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(numeric_level)
    return logger


logger = make_logger(__name__)


class LazyCaller(BaseModel):
    func: Callable
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}
    _evaluated: bool = False
    _result: Any = None
    name: str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__(
            func=func,
            args=args,
            kwargs=kwargs,
            name=kwargs.get("name") or func.__name__,
        )
        logger.debug(f"CREATE NEW CALLER with {kwargs}")
        self._evaluated = False
        self._result = None

    def _resolve_nested(self, value: Any) -> Any:
        logger.debug("Resolving: %s", value)
        if hasattr(value, "execute") and callable(value.execute):
            logger.debug("Resolving lazy object: %s", value)
            resolved = self._resolve_nested(value.execute())
            logger.debug("Resolved lazy object to: %s", resolved)
            return resolved
        elif isinstance(value, dict):
            logger.debug("Resolving dict: %s", value)
            return {k: self._resolve_nested(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            logger.debug("Resolving collection: %s", value)
            if isinstance(value, list):
                return [self._resolve_nested(item) for item in value]
            elif isinstance(value, tuple):
                return tuple(self._resolve_nested(item) for item in value)
            elif isinstance(value, set):
                return {self._resolve_nested(item) for item in value}
        else:
            return value

    def execute(self) -> Any:
        if not self._evaluated:
            resolved_args = self._resolve_nested(self.args)
            resolved_kwargs = self._resolve_nested(self.kwargs)
            logger.debug("Resolved args: %s", resolved_args)
            logger.debug("Resolved kwargs: %s", resolved_kwargs)
            result = self.func(*resolved_args, **resolved_kwargs)

            # Recursively resolve nested lazy objects, if part of the result is lazy
            result = self._resolve_nested(result)

            self._result = result
            self._evaluated = True
        return self._result

    @model_serializer
    def serialize_model(self) -> dict:
        """Only serialize the name, not the problematic object"""
        return {"name": self.name}
