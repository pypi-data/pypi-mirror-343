#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CSV文件读取器

提供CSV文件的读取、查询和保存功能。
"""

import os
import pandas as pd
import numpy as np
import logging
from io import StringIO
from typing import Dict, List, Optional, Union, Any

# 配置日志
logger = logging.getLogger(__name__)

class CSVOperator:
    """
    CSV文件读取器
    
    提供对CSV文件的读取、查询和保存功能。
    
    Attributes:
        dtypes: 列数据类型字典，指定CSV文件中各列的数据类型
    """
    
    def __init__(self, dtypes: Dict[str, str]):
        """
        初始化CSV读取器
        
        Args:
            dtypes: 列数据类型字典，键为列名，值为数据类型（如'string', 'float64', 'int64'等）
        """
        self.dtypes = dtypes
    
    def query(self, file_path: str, fields: Optional[List[str]] = None) -> pd.DataFrame:
        """
        查询CSV文件数据
        
        Args:
            file_path: CSV文件的绝对路径
            fields: 需要选择的字段列表，默认为None表示选择所有字段
            
        Returns:
            包含查询结果的DataFrame
            
        Raises:
            FileNotFoundError: 文件不存在时抛出
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 如果未指定字段，则使用所有字段
        if fields is None:
            fields = list(self.dtypes.keys())
        else:
            # 确保所有指定的字段都在dtypes中
            for field in fields:
                if field not in self.dtypes:
                    raise ValueError(f"字段 '{field}' 不在dtypes定义中")
        
        # 只读取需要的列以提高效率
        usecols = fields
        dtype_dict = {field: self.dtypes[field] for field in fields}
        
        df = pd.read_csv(file_path, usecols=usecols, dtype=dtype_dict)
        return df
    
    def read_last_line(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        读取CSV文件的最后一行
        
        使用块读取策略高效获取文件最后一行，适用于大文件
        
        Args:
            file_path: CSV文件的绝对路径
            
        Returns:
            包含最后一行数据的DataFrame，如果文件为空或不存在返回None
            
        Raises:
            FileNotFoundError: 文件不存在时抛出
            Exception: 读取过程中发生错误时抛出
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        try:
            # 首先尝试读取文件头部获取列名
            with open(file_path, 'r', encoding='utf-8') as f:
                # 读取第一行（表头）
                header = f.readline().strip()
                if not header:  # 文件为空
                    return None
                    
                # 定位到文件末尾
                f.seek(0, 2)
                file_size = f.tell()
                
                if file_size <= len(header) + 1:  # 只有表头
                    return None
                    
                # 读取最后一行
                block_size = 4096
                last_line = ""
                while file_size > 0:
                    read_size = min(block_size, file_size)
                    f.seek(file_size - read_size)
                    block = f.read(read_size)
                    
                    lines = block.split("\n")
                    if len(lines) > 1:
                        last_line = lines[-2] if lines[-1] == "" else lines[-1]
                        break
                    last_line = lines[0]
                    
                    file_size -= read_size
                    
                last_line = last_line.strip() if last_line else None
                if not last_line:
                    return None
                    
                # 创建DataFrame并转换数据类型
                columns = header.split(",")
                data = last_line.split(",")
                
                # 确保data和columns长度一致
                if len(data) != len(columns):
                    # 尝试处理CSV中可能包含的引号内逗号的情况
                    data = pd.read_csv(pd.StringIO(last_line), header=None).iloc[0].tolist()
                    
                df = pd.DataFrame([data], columns=columns)
                
                # 应用数据类型转换
                for col in df.columns:
                    if col in self.dtypes:
                        # 根据self.dtypes中定义的类型进行转换
                        dtype = self.dtypes[col]
                        if dtype == 'float64' or dtype == 'float':
                            df[col] = pd.to_numeric(df[col], errors='coerce').astype('float64')
                        elif dtype == 'int64' or dtype == 'int':
                            df[col] = pd.to_numeric(df[col], errors='coerce').astype('int64')
                        elif dtype == 'string' or dtype == 'str':
                            df[col] = df[col].astype('string')
                
                logger.info(f"成功读取文件最后一行：{file_path}")
                return df
                
        except Exception as e:
            error_msg = f"读取文件最后一行失败：{str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def save(self, file_path: str, data: pd.DataFrame, mode: str = 'overwrite') -> None:
        """
        保存数据到CSV文件
        
        Args:
            file_path: CSV文件的绝对路径
            data: 要保存的DataFrame数据
            mode: 保存模式，'overwrite'表示覆盖，'append'表示追加，默认为'overwrite'
            
        Raises:
            ValueError: mode参数不正确时抛出
        """
        if mode not in ['overwrite', 'append']:
            raise ValueError("mode参数必须为'overwrite'或'append'")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 检查数据列是否与dtypes一致
        for column in data.columns:
            if column not in self.dtypes:
                raise ValueError(f"数据列 '{column}' 不在dtypes定义中")
        
        # 根据mode决定写入方式
        if mode == 'overwrite':
            data.to_csv(file_path, index=False)
        else:  # mode == 'append'
            # 如果文件不存在，则创建新文件
            if not os.path.exists(file_path):
                data.to_csv(file_path, index=False)
            else:
                # 读取现有文件的第一行（表头）
                with open(file_path, 'r', encoding='utf-8') as f:
                    header = f.readline().strip()
                    if not header:  # 文件为空
                        data.to_csv(file_path, index=False)
                        return
                    
                    # 检查列名是否匹配
                    existing_columns = header.split(',')
                    if existing_columns != list(data.columns):
                        raise ValueError(f"新数据的列与现有文件不匹配。现有列：{existing_columns}，新数据列：{list(data.columns)}")
                
                # 追加到现有文件
                data.to_csv(file_path, mode='a', header=False, index=False)