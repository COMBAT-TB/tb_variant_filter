from abc import abstractmethod
import argparse
from typing import List

from vcfpy import record


class Filter(object):
    @abstractmethod
    def customize_parser(cls, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def __call__(self, record: record):
        pass


class IntersectFilter(Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        pass

    def __call__(self, record: record) -> bool:
        for filter in self.filters:
            if filter(record):
                return True
        return False


def get_filters() -> List[Filter]:
    return [RegionFilter]


from .region_filter import RegionFilter  # noqa: E402


__all__ = [variant_filter.__name__ for variant_filter in get_filters()] + ["IntersectFilter", "get_filters"]
