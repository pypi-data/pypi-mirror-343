# coding:utf-8

from typing import Any
from typing import Dict
from typing import Iterator
from typing import List


class SingleObject:  # pylint:disable=too-few-public-methods
    def __init__(self, origin_data: Dict[str, Any]):
        self.__origin_data: Dict[str, Any] = origin_data

    def __getitem__(self, name: str) -> Any:
        return self.__origin_data[name]

    @property
    def origin(self) -> Dict[str, Any]:
        """origin data"""
        return self.__origin_data


class MultiObject:
    def __init__(self, origin_data: Dict[str, Any]):
        self.__origin_data: Dict[str, Any] = origin_data
        content: List[Dict[str, Any]] = origin_data["content"]
        assert (length := len(content)) == origin_data["total"], f"Unexpected content length: {length}"  # noqa:E501
        self.__objects: List[SingleObject] = [SingleObject(item) for item in content]  # noqa:E501

    def __len__(self) -> int:
        return len(self.__objects)

    def __iter__(self) -> Iterator[SingleObject]:
        return iter(self.__objects)

    def __getitem__(self, name: str) -> Any:
        return self.__origin_data[name]

    @property
    def origin(self) -> Dict[str, Any]:
        """origin data"""
        return self.__origin_data
