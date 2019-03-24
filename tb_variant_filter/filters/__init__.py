# these filter modules are very closely tied to the command line interface (tb_variant_filter.cli)
from abc import abstractmethod
import argparse
from typing import List

from vcfpy import record


class Filter(object):
    @abstractmethod
    def __init__(self, args: argparse.Namespace):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def customize_parser(cls, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def __call__(self, record: record):
        pass


class UnionFilter(Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def __repr__(self) -> str:
        name = f"{self.__class__.__name__} on "
        name += ", ".join(repr(variant_filter) for variant_filter in self.filters)
        return name

    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        pass

    def __call__(self, record: record) -> bool:
        return any([filter(record) for filter in self.filters])


from .region_filter import RegionFilter  # noqa: E402
from .close_to_indel_filter import CloseToIndelFilter  # noqa: E402
from .alt_percentage_filter import AltPercentageDepthFilter  # noqa: E402


def get_filters() -> List[Filter]:
    return [RegionFilter, CloseToIndelFilter, AltPercentageDepthFilter]


__all__ = [variant_filter.__name__ for variant_filter in get_filters()] + [
    "UnionFilter",
    "get_filters",
]
