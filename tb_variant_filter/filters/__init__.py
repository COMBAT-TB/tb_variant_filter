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


def get_filters() -> List[Filter]:
    return [RegionFilter]


from .region_filter import RegionFilter  # noqa: E402


__all__ = ["Filter", "RegionFilter"]
