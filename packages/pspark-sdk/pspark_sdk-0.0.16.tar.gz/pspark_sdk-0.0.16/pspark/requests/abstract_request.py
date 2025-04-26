from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Union


def remove_none_recursive(obj: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
    if isinstance(obj, dict):
        return {k: remove_none_recursive(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_recursive(v) for v in obj if v is not None]
    else:
        return obj


@dataclass
class AbstractRequest(ABC):  # noqa: B024
    def as_dict(self) -> dict:
        result = asdict(self)

        for name in self._get_excluded_properties():
            result.pop(name, None)

        return remove_none_recursive(result)

    def _get_excluded_properties(self) -> list:
        return []
