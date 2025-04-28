#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""任务图模块，用于构建和执行有向无环图(DAG)任务
支持使用node装饰器创建节点，以及使用create_graph创建和执行任务图
"""

from datawhale.infrastructure_pro.task_gragh.node import node, Node, NodeStatus
from datawhale.infrastructure_pro.task_gragh.graph import Graph, GraphStatus
from datawhale.infrastructure_pro.task_gragh.interface import create_graph

__all__ = [
    # 核心类
    "Node", "Graph", "NodeStatus", "GraphStatus",
    # 核心功能
    "node", "create_graph"
] 