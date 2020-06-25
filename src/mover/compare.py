# -*- coding: utf-8 -*-

from constants import DELTA


def compare_with_delta(a, b):
    return abs(a - b) < DELTA

