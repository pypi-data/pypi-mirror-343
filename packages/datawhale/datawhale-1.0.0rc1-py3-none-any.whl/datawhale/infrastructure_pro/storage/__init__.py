#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DataWhale 新版文件存储服务模块

提供基于元数据配置的文件存储功能，支持灵活的文件结构和数据管理。

主要组件:
- StorageService: 主存储服务类
- Dataset: 数据集对象

用户接口:
- save: 保存数据到存储系统
- query: 从存储系统查询数据
- delete: 从存储系统删除数据
- exists: 检查数据是否存在
- dw_create_dataset: 创建DataWhale本地数据集
- dw_save: 保存数据到DataWhale本地数据集
- dw_query: 从DataWhale本地数据集查询数据
- dw_delete: 从DataWhale本地数据集删除数据
- dw_exists: 检查DataWhale本地数据集数据是否存在
- infer_dtypes: 从DataFrame推断数据类型
"""

from .storage_service import StorageService
from .dataset import Dataset
from .interface import (
    create_dataset, save, query, delete, exists,
    dw_create_dataset, dw_save, dw_query, dw_delete, dw_exists,
    infer_dtypes
)

__all__ = [
    # 核心类
    "StorageService",
    # "MetaInfoManager", # 暂时注释掉不存在的类
    # "LayerManager",
    # "UpdateStrategyFactory",
    "Dataset",
    # "CSVReader",
    # 用户接口 - 基础接口
    "create_dataset",
    "save",
    "query",
    "delete",
    "exists",
    # 用户接口 - DataWhale本地存储接口
    "dw_create_dataset",
    "dw_save",
    "dw_query",
    "dw_delete", 
    "dw_exists",
    # 工具函数
    "infer_dtypes",
]
