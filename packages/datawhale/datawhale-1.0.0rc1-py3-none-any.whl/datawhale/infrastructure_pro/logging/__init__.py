#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
提供日志记录功能
"""

from .logger import get_user_logger, get_system_logger

__all__ = ["get_user_logger", "get_system_logger"]
