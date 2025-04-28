#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DataWhale基础设施模块接口

提供任务图、任务阶段、存储服务和任务系统的统一接口
"""

# 从task_gragh模块导入
from datawhale.infrastructure_pro.task_gragh import (
    Node, Graph, NodeStatus, GraphStatus,
    node, create_graph
)

# 从task_stage模块导入
from datawhale.infrastructure_pro.task_stage import (
    Stage, StageStatus
)

# 从storage模块导入
from datawhale.infrastructure_pro.storage import (
    StorageService, Dataset,
    create_dataset, save, query, delete, exists,
    dw_create_dataset, dw_save, dw_query, dw_delete, dw_exists,
    infer_dtypes
)

# 从task_system模块导入
from datawhale.infrastructure_pro.task_system import (
    Task, TaskStatus, with_retry, Result,
    BatchStatus, BatchTask, BatchTaskExecutor,
    BatchTaskFailureManager, BatchTaskUnfinishedManager,
    execute_task, execute_batch_tasks, resume_batch_tasks,
    retry_failed_tasks, get_failed_tasks, get_unfinished_tasks
)

# 从logging模块导入
from datawhale.infrastructure_pro.logging import (
    get_user_logger, get_system_logger
)

__all__ = [
    # task_gragh模块
    "Node", "Graph", "NodeStatus", "GraphStatus", "node", "create_graph",
    
    # task_stage模块
    "Stage", "StageStatus",
    
    # storage模块
    "StorageService", "Dataset", "create_dataset", 
    "save", "query", "delete", "exists",
    "dw_create_dataset", "dw_save", "dw_query", "dw_delete", "dw_exists",
    "infer_dtypes",
    
    # task_system模块
    "Task", "TaskStatus", "with_retry", "Result",
    "BatchStatus", "BatchTask", "BatchTaskExecutor",
    "BatchTaskFailureManager", "BatchTaskUnfinishedManager",
    "execute_task", "execute_batch_tasks", "resume_batch_tasks",
    "retry_failed_tasks", "get_failed_tasks", "get_unfinished_tasks",

    # logging模块
    "get_user_logger", "get_system_logger"
]
