from enum import Enum


class AgentState(str, Enum):
    """Agent执行状态"""
    # 空闲状态，表示代理尚未开始执行任务
    IDLE = "IDLE"
    # 运行中状态，表示代理正在执行任务
    RUNNING = "RUNNING"
    # 完成状态，表示代理已成功完成任务
    FINISHED = "FINISHED"
    # 错误状态，表示代理在执行过程中遇到了错误
    ERROR = "ERROR"