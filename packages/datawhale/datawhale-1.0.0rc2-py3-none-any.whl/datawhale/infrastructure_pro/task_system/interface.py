#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""任务框架接口模块，提供简便的任务执行和管理功能"""

from typing import Dict, List, Any, Callable, TypeVar, Optional
import time

from datawhale.infrastructure_pro.task_system.task_execution import (
    Task,
    TaskStatus,
    with_retry,
    Result,
)
from datawhale.infrastructure_pro.task_system.batch_task import (
    BatchStatus,
    BatchTask,
    BatchTaskExecutor,
    BatchTaskFailureManager,
    BatchTaskUnfinishedManager,
)
from datawhale.infrastructure_pro.logging import get_user_logger, get_system_logger

# 创建用户日志和系统日志记录器
user_logger = get_user_logger(__name__)
system_logger = get_system_logger(__name__)

T = TypeVar("T")


def execute_task(
    task_func: Callable[..., T],
    task_params: Dict[str, Any] = None,
    task_id: str = None,
    task_type: str = "default",
    max_retries: int = None,
    retry_interval: float = None,
    backoff_factor: float = None,
) -> Result[T]:
    """执行单个任务

    Args:
        task_func: 任务执行函数
        task_params: 任务参数
        task_id: 任务ID，默认自动生成
        task_type: 任务类型
        max_retries: 最大重试次数
        retry_interval: 重试间隔（秒）
        backoff_factor: 重试间隔的退避因子

    Returns:
        Result[T]: 任务执行结果
    """
    # 记录任务开始
    system_logger.info(f"开始执行单个任务：task_type={task_type}, task_id={task_id}")

    task = Task(
        task_type=task_type,
        params=task_params or {},
        task_func=task_func,
        task_id=task_id,
        max_retries=max_retries,
        retry_interval=retry_interval,
        backoff_factor=backoff_factor,
    )

    result = task.execute()

    # 记录任务结果
    if result.success:
        system_logger.info(f"任务执行成功：task_id={task.task_id}")
    else:
        system_logger.error(
            f"任务执行失败：task_id={task.task_id}, error={result.error}"
        )
        user_logger.error(f"任务执行失败：{result.error}")

    return result


def execute_batch_tasks(
    task_func: Callable[..., T],
    task_params_list: List[Dict[str, Any]],
    batch_id: str = None,
    task_type: str = "default",
    max_workers: int = None,
    task_timeout: float = None,
    task_interval: float = None,
    task_max_retries: int = None,
    task_retry_interval: float = None,
    backoff_factor: float = None,
    record_failed: bool = True,
    batch_mode: str = "new",
    failed_task_storage_dir: str = None,
    unfinished_task_storage_dir: str = None,
) -> BatchTask:
    """执行批量任务

    Args:
        task_func: 任务执行函数
        task_params_list: 任务参数列表
        batch_id: 批次ID，默认自动生成
        task_type: 任务类型
        max_workers: 最大工作线程数
        task_timeout: 单个任务超时时间（秒）
        task_interval: 任务提交间隔（秒）
        task_max_retries: 最大重试次数
        task_retry_interval: 重试间隔（秒）
        backoff_factor: 重试间隔的退避因子
        record_failed: 是否记录失败任务
        batch_mode: 批次模式，可选值为"new"、"resume"和"retry"
        failed_task_storage_dir: 失败任务管理器的存储目录，如果为None则使用默认目录
        unfinished_task_storage_dir: 未完成任务管理器的存储目录，如果为None则使用默认目录

    Returns:
        BatchTask: 批次任务对象
    """
    # 参数验证
    if batch_mode not in ["new", "resume", "retry"]:
        raise ValueError(f"不支持的批次模式: {batch_mode}，可选值为'new'、'resume'和'retry'")
    
    if batch_mode in ["resume", "retry"] and batch_id is None:
        raise ValueError(f"在{batch_mode}模式下必须提供batch_id")
    
    if batch_mode == "new" and not task_params_list and batch_id is None:
        raise ValueError("在创建新批次模式下，如果没有提供batch_id，则必须提供任务参数列表")
    
    # 记录批量任务开始
    task_count = len(task_params_list) if task_params_list else "未知"
    system_logger.info(
        f"准备执行批量任务：batch_mode={batch_mode}, task_type={task_type}, "
        f"任务数量={task_count}, batch_id={batch_id}"
    )
    user_logger.info(f"准备执行{task_count}个任务，模式：{batch_mode}")

    executor = BatchTaskExecutor(
        task_type=task_type,
        max_workers=max_workers,
        task_interval=task_interval,
        task_timeout=task_timeout,
        record_failed=record_failed,
        max_retries=task_max_retries,
        retry_interval=task_retry_interval,
        backoff_factor=backoff_factor,
        failed_task_storage_dir=failed_task_storage_dir,
        unfinished_task_storage_dir=unfinished_task_storage_dir,
    )

    return executor.execute_batch_tasks(
        task_func=task_func,
        task_params_list=task_params_list,
        batch_id=batch_id,
        task_timeout=task_timeout,
        task_interval=task_interval,
        max_workers=max_workers,
        task_max_retries=task_max_retries,
        task_retry_interval=task_retry_interval,
        backoff_factor=backoff_factor,
        batch_mode=batch_mode,
    )


def resume_batch_tasks(
    task_func: Callable[..., T],
    batch_id: str,
    task_type: str = "default",
    max_workers: int = None,
    task_timeout: float = None,
    task_interval: float = None,
    task_max_retries: int = None,
    task_retry_interval: float = None,
    backoff_factor: float = None,
    failed_task_storage_dir: str = None,
    unfinished_task_storage_dir: str = None,
) -> BatchTask:
    """恢复批量任务

    Args:
        task_func: 任务执行函数
        batch_id: 批次ID
        task_type: 任务类型
        max_workers: 最大工作线程数
        task_timeout: 单个任务超时时间（秒）
        task_interval: 任务提交间隔（秒）
        task_max_retries: 最大重试次数
        task_retry_interval: 重试间隔（秒）
        backoff_factor: 重试间隔的退避因子
        failed_task_storage_dir: 失败任务管理器的存储目录，如果为None则使用默认目录
        unfinished_task_storage_dir: 未完成任务管理器的存储目录，如果为None则使用默认目录

    Returns:
        BatchTask: 批次任务对象
    """
    # 记录恢复任务
    system_logger.info(f"恢复批量任务：batch_id={batch_id}, task_type={task_type}")
    user_logger.info(f"正在恢复批次任务：{batch_id}")

    return execute_batch_tasks(
        task_func=task_func,
        task_params_list=[],  # 恢复模式不需要提供参数列表
        batch_id=batch_id,
        task_type=task_type,
        max_workers=max_workers,
        task_timeout=task_timeout,
        task_interval=task_interval,
        task_max_retries=task_max_retries,
        task_retry_interval=task_retry_interval,
        backoff_factor=backoff_factor,
        batch_mode="resume",
        failed_task_storage_dir=failed_task_storage_dir,
        unfinished_task_storage_dir=unfinished_task_storage_dir,
    )


def retry_failed_tasks(
    task_func: Callable[..., T],
    batch_id: str,
    task_type: str = "default",
    max_workers: int = None,
    task_timeout: float = None,
    task_interval: float = None,
    task_max_retries: int = None,
    task_retry_interval: float = None,
    backoff_factor: float = None,
    failed_task_storage_dir: str = None,
    unfinished_task_storage_dir: str = None,
) -> BatchTask:
    """重试失败的批量任务

    Args:
        task_func: 任务执行函数
        batch_id: 批次ID
        task_type: 任务类型
        max_workers: 最大工作线程数
        task_timeout: 单个任务超时时间（秒）
        task_interval: 任务提交间隔（秒）
        task_max_retries: 最大重试次数
        task_retry_interval: 重试间隔（秒）
        backoff_factor: 重试间隔的退避因子
        failed_task_storage_dir: 失败任务管理器的存储目录，如果为None则使用默认目录
        unfinished_task_storage_dir: 未完成任务管理器的存储目录，如果为None则使用默认目录

    Returns:
        BatchTask: 批次任务对象
    """
    # 记录重试任务
    system_logger.info(f"重试失败任务：batch_id={batch_id}, task_type={task_type}")
    user_logger.info(f"正在重试失败任务：{batch_id}")

    return execute_batch_tasks(
        task_func=task_func,
        task_params_list=[],  # 重试模式不需要提供参数列表
        batch_id=batch_id,
        task_type=task_type,
        max_workers=max_workers,
        task_timeout=task_timeout,
        task_interval=task_interval,
        task_max_retries=task_max_retries,
        task_retry_interval=task_retry_interval,
        backoff_factor=backoff_factor,
        batch_mode="retry",
        failed_task_storage_dir=failed_task_storage_dir,
        unfinished_task_storage_dir=unfinished_task_storage_dir,
    )


def get_failed_tasks(
    batch_id: str, 
    task_type: str = "default",
    storage_dir: str = None,
) -> List[Dict[str, Any]]:
    """获取失败任务列表

    Args:
        batch_id: 批次ID
        task_type: 任务类型
        storage_dir: 失败任务管理器的存储目录，如果为None则使用默认目录

    Returns:
        List[Dict[str, Any]]: 失败任务列表
    """
    system_logger.info(f"获取失败任务列表：batch_id={batch_id}, task_type={task_type}")

    manager = BatchTaskFailureManager(task_type, storage_dir=storage_dir)
    manager.load_batch_tasks(batch_id)
    tasks = manager.get_failed_tasks(batch_id)

    system_logger.info(f"找到{len(tasks)}个失败任务：batch_id={batch_id}")
    return tasks


def get_unfinished_tasks(
    batch_id: str, 
    task_type: str = "default",
    storage_dir: str = None,
) -> List[Dict[str, Any]]:
    """获取未完成任务列表

    Args:
        batch_id: 批次ID
        task_type: 任务类型
        storage_dir: 未完成任务管理器的存储目录，如果为None则使用默认目录

    Returns:
        List[Dict[str, Any]]: 未完成任务列表
    """
    system_logger.info(
        f"获取未完成任务列表：batch_id={batch_id}, task_type={task_type}"
    )

    manager = BatchTaskUnfinishedManager(task_type, storage_dir=storage_dir)
    manager.load_batch_tasks(batch_id)
    tasks = manager.get_unfinished_tasks(batch_id)

    system_logger.info(f"找到{len(tasks)}个未完成任务：batch_id={batch_id}")
    return tasks


def execute_new_batch_tasks(
    task_func: Callable[..., T],
    task_params_list: List[Dict[str, Any]],
    batch_id: str = None,
    task_type: str = "default",
    max_workers: int = None,
    task_timeout: float = None,
    task_interval: float = None,
    task_max_retries: int = None,
    task_retry_interval: float = None,
    backoff_factor: float = None,
    record_failed: bool = True,
    failed_task_storage_dir: str = None,
    unfinished_task_storage_dir: str = None,
) -> BatchTask:
    """创建并执行新的批量任务
    
    此函数专门用于创建和执行新的批次任务，与execute_batch_tasks的区别是它不支持批次模式参数。

    Args:
        task_func: 任务执行函数
        task_params_list: 任务参数列表
        batch_id: 批次ID，默认自动生成
        task_type: 任务类型
        max_workers: 最大工作线程数
        task_timeout: 单个任务超时时间（秒）
        task_interval: 任务提交间隔（秒）
        task_max_retries: 最大重试次数
        task_retry_interval: 重试间隔（秒）
        backoff_factor: 重试间隔的退避因子
        record_failed: 是否记录失败任务
        failed_task_storage_dir: 失败任务管理器的存储目录，如果为None则使用默认目录
        unfinished_task_storage_dir: 未完成任务管理器的存储目录，如果为None则使用默认目录

    Returns:
        BatchTask: 批次任务对象
    """
    # 记录批量任务开始
    task_count = len(task_params_list) if task_params_list else 0
    system_logger.info(
        f"准备执行新批量任务：task_type={task_type}, "
        f"任务数量={task_count}, batch_id={batch_id}"
    )
    user_logger.info(f"准备执行{task_count}个新任务")

    # 参数验证
    if not task_params_list:
        raise ValueError("任务参数列表不能为空")

    executor = BatchTaskExecutor(
        task_type=task_type,
        max_workers=max_workers,
        task_interval=task_interval,
        task_timeout=task_timeout,
        record_failed=record_failed,
        max_retries=task_max_retries,
        retry_interval=task_retry_interval,
        backoff_factor=backoff_factor,
        failed_task_storage_dir=failed_task_storage_dir,
        unfinished_task_storage_dir=unfinished_task_storage_dir,
    )

    return executor.execute_batch_tasks(
        task_func=task_func,
        task_params_list=task_params_list,
        batch_id=batch_id,
        task_timeout=task_timeout,
        task_interval=task_interval,
        max_workers=max_workers,
        task_max_retries=task_max_retries,
        task_retry_interval=task_retry_interval,
        backoff_factor=backoff_factor,
        batch_mode="new",  # 固定为新建模式
    )
