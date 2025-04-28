#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""任务框架模块，包含任务执行、批量任务管理与执行等功能"""

# 从任务系统导入核心组件
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

# 导入接口函数
from .interface import (
    execute_task,
    execute_batch_tasks,
    resume_batch_tasks,
    retry_failed_tasks,
    get_failed_tasks,
    get_unfinished_tasks,
)

__all__ = [
    # 核心组件
    "Task",
    "TaskStatus",
    "with_retry",
    "Result",
    "BatchStatus",
    "BatchTask",
    "BatchTaskExecutor",
    "BatchTaskFailureManager",
    "BatchTaskUnfinishedManager",
    # 接口函数
    "execute_task",
    "execute_batch_tasks",
    "resume_batch_tasks",
    "retry_failed_tasks",
    "get_failed_tasks",
    "get_unfinished_tasks",
]
