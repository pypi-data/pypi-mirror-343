#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DataWhale 存储接口模块

为存储服务提供简洁易用的用户接口，支持Dataset多层数据集管理。

主要功能:
- 创建数据集
- 保存数据到数据集
- 从数据集查询数据
- 删除数据集或数据集中的文件
- 检查数据集中的数据是否存在

提供两种接口:
1. 基础接口: 直接操作Dataset对象(create_dataset, save, query, delete, exists)
2. DataWhale本地存储接口: 使用StorageService进行操作(dw_create_dataset, dw_save, dw_query, dw_delete, dw_exists)
"""

from typing import Dict, Optional, List, Any, Union
import pandas as pd
import os
from .dataset import Dataset
from .storage_service import StorageService

# 初始化全局存储服务实例
_storage_service = StorageService()


def create_dataset(
    name: str,
    format: str = "csv",
    structure_fields: List[str] = None,
    update_mode: str = "append",
    dtypes: Dict = None,
    data_folder: str = None,
    meta_folder: str = None,
) -> Optional[Dataset]:
    """
    创建多层数据集
    
    Args:
        name: 数据集名称
        format: 文件格式，默认为"csv"
        structure_fields: 用于生成动态层的字段列表，决定文件层级结构(层级数=字段数+1)
        update_mode: 更新模式，可选值："append"或"overwrite"，默认为"append"
        dtypes: 数据类型映射字典
        data_folder: 数据存储目录的绝对路径，必须提供
        meta_folder: 元数据存储目录的绝对路径，必须提供
        
    Returns:
        Optional[Dataset]: 创建的数据集对象，如果创建失败则返回None
        
    Examples:
        >>> dataset = create_dataset(
        ...     name="stocks_daily",
        ...     format="csv",
        ...     structure_fields=["code", "trade_date"],
        ...     update_mode="append",
        ...     dtypes={
        ...         "code": "object",
        ...         "trade_date": "object",
        ...         "open": "float64",
        ...         "close": "float64",
        ...         "volume": "float64"
        ...     },
        ...     data_folder="/path/to/data",
        ...     meta_folder="/path/to/meta"
        ... )
    """
    try:
        # 验证路径参数
        if data_folder is None or meta_folder is None:
            raise ValueError("必须提供data_folder和meta_folder的绝对路径")
            
        # 构建元信息字典
        meta_info = {
            "name": name,
            "format": format,
            "update_mode": update_mode,
            "dtypes": dtypes or {}
        }
        
        # 如果有结构字段，添加dataset部分
        if structure_fields:
            meta_info["dataset"] = {
                "structure_fields": structure_fields
            }
        
        # 创建数据集
        dataset = Dataset.create_dataset(
            folder=data_folder,
            meta_folder=meta_folder,
            meta_info=meta_info
        )
        
        return dataset
    except Exception as e:
        print(f"创建数据集失败: {str(e)}")
        return None


def save(
    data: pd.DataFrame, 
    dataset_name: str, 
    field_values: Dict[str, str] = None, 
    mode: str = None,
    data_folder: str = None,
    meta_folder: str = None,
    **kwargs
) -> bool:
    """
    保存数据到多层数据集
    
    Args:
        data: 要保存的DataFrame数据
        dataset_name: 数据集名称
        field_values: 字段值映射，用于指定动态层的值
        mode: 保存模式，可选值："overwrite"或"append"
              如果为None，则使用数据集默认的更新模式
        data_folder: 数据存储目录的绝对路径，必须提供
        meta_folder: 元数据存储目录的绝对路径，必须提供
        **kwargs: 额外参数
            
    Returns:
        bool: 保存是否成功
        
    Examples:
        >>> df = pd.DataFrame({
        ...     'code': ['000001'],
        ...     'trade_date': ['2023-01-01'],
        ...     'open': [10.1],
        ...     'close': [10.2],
        ...     'volume': [1000]
        ... })
        >>> save(df, "stocks_daily", field_values={'code': '000001', 'trade_date': '2023-01-01'},
        ...      data_folder="/path/to/data", meta_folder="/path/to/meta")
    """
    try:
        # 验证路径参数
        if data_folder is None or meta_folder is None:
            raise ValueError("必须提供data_folder和meta_folder的绝对路径")
        
        # 加载数据集
        dataset = Dataset.load_dataset(
            name=dataset_name,
            folder=data_folder,
            meta_folder=meta_folder
        )
        
        # 保存数据
        dataset.save(data, field_values, mode)
        return True
    except Exception as e:
        print(f"保存数据失败: {str(e)}")
        return False


def query(
    dataset_name: str, 
    field_values: Dict[str, Union[str, List[str]]] = None,
    sort_by: str = None,
    parallel: bool = True,
    data_folder: str = None,
    meta_folder: str = None,
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    从多层数据集查询数据
    
    Args:
        dataset_name: 数据集名称
        field_values: 字段值映射，用于指定要查询的数据路径
        sort_by: 排序字段
        parallel: 是否使用并行查询，默认为True
        data_folder: 数据存储目录的绝对路径，必须提供
        meta_folder: 元数据存储目录的绝对路径，必须提供
        **kwargs: 额外参数
            
    Returns:
        Optional[pd.DataFrame]: 查询结果，如果查询失败则返回None
        
    Examples:
        >>> df = query("stocks_daily", field_values={'code': '000001'},
        ...            data_folder="/path/to/data", meta_folder="/path/to/meta")
        >>> df = query("stocks_daily", field_values={'code': ['000001', '000002']},
        ...            data_folder="/path/to/data", meta_folder="/path/to/meta")
    """
    try:
        # 验证路径参数
        if data_folder is None or meta_folder is None:
            raise ValueError("必须提供data_folder和meta_folder的绝对路径")
        
        # 加载数据集
        dataset = Dataset.load_dataset(
            name=dataset_name,
            folder=data_folder,
            meta_folder=meta_folder
        )
        
        # 查询数据
        return dataset.query(field_values, sort_by, parallel)
    except Exception as e:
        print(f"查询数据失败: {str(e)}")
        return None


def delete(
    dataset_name: str, 
    field_values: Dict[str, str] = None,
    data_folder: str = None,
    meta_folder: str = None
) -> bool:
    """
    从多层数据集删除数据
    
    Args:
        dataset_name: 数据集名称
        field_values: 字段值映射，用于指定要删除的数据路径
                     如果为None，则删除整个数据集
        data_folder: 数据存储目录的绝对路径，必须提供
        meta_folder: 元数据存储目录的绝对路径，必须提供
            
    Returns:
        bool: 删除是否成功
        
    Examples:
        >>> delete("stocks_daily", field_values={'code': '000001', 'trade_date': '2023-01-01'},
        ...        data_folder="/path/to/data", meta_folder="/path/to/meta")
        >>> delete("stocks_daily", data_folder="/path/to/data", meta_folder="/path/to/meta")  # 删除整个数据集
    """
    try:
        # 验证路径参数
        if data_folder is None or meta_folder is None:
            raise ValueError("必须提供data_folder和meta_folder的绝对路径")
        
        # 加载数据集
        dataset = Dataset.load_dataset(
            name=dataset_name,
            folder=data_folder,
            meta_folder=meta_folder
        )
        
        # 删除数据
        return dataset.delete(field_values)
    except Exception as e:
        print(f"删除数据失败: {str(e)}")
        return False


def exists(
    dataset_name: str, 
    field_values: Dict[str, str] = None,
    data_folder: str = None,
    meta_folder: str = None
) -> bool:
    """
    检查多层数据集或其中的数据是否存在
    
    Args:
        dataset_name: 数据集名称
        field_values: 字段值映射，用于指定要检查的数据路径
                     如果为None，则只检查数据集是否存在
        data_folder: 数据存储目录的绝对路径，必须提供
        meta_folder: 元数据存储目录的绝对路径，必须提供
            
    Returns:
        bool: 数据集或指定数据是否存在
        
    Examples:
        >>> exists("stocks_daily", data_folder="/path/to/data", meta_folder="/path/to/meta")
        >>> exists("stocks_daily", field_values={'code': '000001', 'trade_date': '2023-01-01'},
        ...        data_folder="/path/to/data", meta_folder="/path/to/meta")
    """
    try:
        # 验证路径参数
        if data_folder is None or meta_folder is None:
            raise ValueError("必须提供data_folder和meta_folder的绝对路径")
            
        try:
            # 尝试加载数据集
            dataset = Dataset.load_dataset(
                name=dataset_name,
                folder=data_folder,
                meta_folder=meta_folder
            )
            
            # 如果只需检查数据集是否存在，直接返回True
            if field_values is None:
                return True
                
            # 检查指定数据是否存在
            return dataset.exists(field_values)
        except Exception:
            # 数据集加载失败，表示数据集不存在
            return False
    except Exception:
        return False


# ============ DataWhale本地存储接口 ============

def dw_create_dataset(
    name: str,
    dtypes: Dict,
    format: str = None,
    structure_fields: List[str] = None,
    update_mode: str = None,
) -> Dataset:
    """
    创建DataWhale本地数据集(使用配置的存储路径)
    
    Args:
        name: 数据集名称
        dtypes: 数据类型配置，必须提供
        format: 文件格式，默认使用配置中的default_format
        structure_fields: 文件结构字段列表，决定文件层级结构(层级数=字段数+1)
        update_mode: 更新模式，默认为append
        
    Returns:
        Dataset: 创建的数据集对象
        
    Examples:
        >>> dataset = dw_create_dataset(
        ...     name="stocks_daily",
        ...     dtypes={
        ...         "code": "object",
        ...         "trade_date": "object",
        ...         "open": "float64",
        ...         "close": "float64",
        ...         "volume": "float64"
        ...     },
        ...     structure_fields=["code", "trade_date"],
        ...     update_mode="append"
        ... )
    """
    return _storage_service.create_dataset(
        name=name,
        dtypes=dtypes,
        format=format,
        structure_fields=structure_fields,
        update_mode=update_mode
    )


def dw_save(
    data: pd.DataFrame, 
    data_name: str, 
    field_values: Dict[str, str] = None, 
    mode: str = None,
    **kwargs
) -> bool:
    """
    保存数据到DataWhale本地数据集
    
    Args:
        data: 要保存的DataFrame数据
        data_name: 数据集名称
        field_values: 字段值映射，用于指定动态层的值
        mode: 保存模式，可选值："overwrite"或"append"。如果为None，则使用数据集默认的更新模式
        **kwargs: 额外参数
            
    Returns:
        bool: 保存是否成功
        
    Examples:
        >>> df = pd.DataFrame({
        ...     'code': ['000001'],
        ...     'trade_date': ['2023-01-01'],
        ...     'open': [10.1],
        ...     'close': [10.2],
        ...     'volume': [1000]
        ... })
        >>> dw_save(df, "stocks_daily", field_values={'code': '000001', 'trade_date': '2023-01-01'})
    """
    return _storage_service.save(
        data=data,
        data_name=data_name,
        field_values=field_values,
        mode=mode,
        **kwargs
    )


def dw_query(
    data_name: str, 
    field_values: Dict[str, Union[str, List[str]]] = None,
    **kwargs
) -> Optional[pd.DataFrame]:
    """
    从DataWhale本地数据集查询数据
    
    Args:
        data_name: 数据集名称
        field_values: 字段值映射，用于指定要查询的数据路径
        **kwargs: 额外参数
            - sort_by: 排序字段
            - parallel: 是否使用并行查询，默认为True
            - max_workers: 最大工作线程数
            
    Returns:
        Optional[pd.DataFrame]: 查询结果，如果查询失败则返回None
        
    Examples:
        >>> df = dw_query("stocks_daily", field_values={'code': '000001'})
        >>> df = dw_query("stocks_daily", field_values={'code': ['000001', '000002']}, sort_by="trade_date")
    """
    return _storage_service.query(
        data_name=data_name,
        field_values=field_values,
        **kwargs
    )


def dw_delete(data_name: str, field_values: Dict[str, str] = None) -> bool:
    """
    从DataWhale本地数据集删除数据
    
    Args:
        data_name: 数据集名称
        field_values: 字段值映射，用于指定要删除的数据路径。如果为None，则删除整个数据集。
            
    Returns:
        bool: 删除是否成功
        
    Examples:
        >>> dw_delete("stocks_daily", field_values={'code': '000001', 'trade_date': '2023-01-01'})
        >>> dw_delete("stocks_daily")  # 删除整个数据集
    """
    return _storage_service.delete(
        data_name=data_name,
        field_values=field_values
    )


def dw_exists(data_name: str, field_values: Dict[str, str] = None) -> bool:
    """
    检查DataWhale本地数据集或其中的数据是否存在
    
    Args:
        data_name: 数据集名称
        field_values: 字段值映射，用于指定要检查的数据路径。如果为None，则只检查数据集是否存在。
            
    Returns:
        bool: 数据集或指定数据是否存在
        
    Examples:
        >>> dw_exists("stocks_daily")
        >>> dw_exists("stocks_daily", field_values={'code': '000001', 'trade_date': '2023-01-01'})
    """
    return _storage_service.exists(
        data_name=data_name,
        field_values=field_values
    )


def infer_dtypes(data: pd.DataFrame) -> Dict[str, str]:
    """
    根据数据自动推断字段类型
    
    分析DataFrame的每一列，根据实际数据自动推断适合的数据类型。
    支持的类型映射:
    - 整数类型 -> 'int64'
    - 浮点类型 -> 'float64'
    - 字符串/对象类型 -> 'string'
    - 布尔类型 -> 'bool'
    - 日期时间类型 -> 'datetime64'
    
    Args:
        data: 待分析的数据框
        
    Returns:
        Dict[str, str]: 字段名到类型字符串的映射字典
        
    Examples:
        >>> df = pd.DataFrame({
        ...     'code': ['000001', '000002'],
        ...     'price': [10.5, 20.8],
        ...     'volume': [10000, 20000]
        ... })
        >>> dtypes = infer_dtypes(df)
        >>> print(dtypes)
        {'code': 'string', 'price': 'float64', 'volume': 'int64'}
        
    Raises:
        TypeError: 当输入不是pandas DataFrame时
    """
    # 从MetaInfo类使用该方法
    from .metainfo.metainfo import MetaInfo
    return MetaInfo.infer_dtypes_from_data(data) 