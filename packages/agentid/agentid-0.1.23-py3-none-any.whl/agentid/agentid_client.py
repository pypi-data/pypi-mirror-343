from datetime import date
import queue
import socket
import json
import string
import time
from typing import Union, final
import signal
import threading
import typing

class ServerConnectionError(Exception):
    """Custom exception for server connection errors."""
    pass

from agentid import logger
from agentid.db.db_mananger import DBManager
from agentid.agentid import AgentId
from agentid.ca_client import CAClient
from agentid.env import Environ
from agentid.message import AssistantMessageBlock


class AgentIdClient:
    """
    agentid客户端
    用于创建aid，加载aid,获取aid授权列表,管理aid
    示例用法:
    """
    def __init__(self, ca_server, timeout=10):
        """
        初始化客户端
        :param ca_server: 证书服务器地址(必须包含http://或https://)
        :param timeout: 连接超时时间(秒)
        """
        # 确保ca_server以http://或https://开头
        self.ca_server = ca_server or Environ.CA_SERVER.get()  # 移除末尾的斜杠
        if not ca_server.startswith(('http://', 'https://')):
            raise ValueError("无效的CA服务器地址")

        self.ca_server = ca_server.rstrip('/')  # 移除末尾的斜杠

        self.timeout = timeout
        self.ca_client = CAClient(ca_server, timeout)
        self.db_manager = DBManager()
        self.agentid: AgentId = None
        self._shutdown_flag = threading.Event()  # 初始化信号量

    @final
    def get_agentid_list(self):
        list = self.db_manager.get_agentid_list()
        return list

    @final
    def get_agentid(self, id):
        agents = [_id for _id in self.db_manager.get_agentid_list() if _id == id]
        return agents[0] if agents else None
        
    @final
    def update_aid_info(self, aid, avaUrl, name, description):
        self.db_manager.update_aid_info(aid, avaUrl, name, description)
        return True

    @final
    def load_aid(self, agent_id: string)->bool:
        try: 
            logger.debug(f"尝试加载agent_id: {agent_id}")  # 调试用
            result = self.db_manager.load_aid(agent_id)
            if not result or len(result) < 2:  # 检查返回结果是否有效
                logger.erorr(f"未找到agent_id: {agent_id} 或数据不完整")
                return False

            logger.debug(f"加载agent_id: {agent_id} 成功: {result}")  # 调试用
            ep_aid, ep_url = result[0], result[1]  # 安全获取前两个值
            avaUrl = result[2] if len(result) > 2 else ""
            name = result[3] if len(result) > 3 else ""
            description = result[4] if len(result) > 4 else ""
            if ep_aid and ep_url:
                self.agentid =  AgentId(agent_id, ep_aid, ep_url)
                return True

            ep_url = self.ca_client.resign_csr(agent_id)
            logger.debug(f"重新签名CSR成功: {ep_url}")  # 调试用
            if ep_url:
                self.db_manager.update_aid(agent_id, "ep_aid", ep_url)
                agentid = AgentId(agent_id, "ep_aid", ep_url)
                agentid.set_avaUrl(avaUrl)
                agentid.set_name(name)
                agentid.set_description(description)
                self.agentid = agentid
                return True

        except Exception as e:
            logger.exception(f"加载和验证密钥对时出错: {e}")  # 调试用
            return False

    @final
    def create_aid(self, aid: str):
        """连接到服务器"""
        # 生成 Ed25519 私钥
        logger.debug(f"向服务端申请创建aid: {aid}")  # 调试用
        result = self.ca_client.send_csr_to_server(aid)
        if result == True:
            self.db_manager.create_aid(aid)
            return
        raise RuntimeError('创建aid失败')

    def connect(self):
        """通过connect2entrypoint可以连接到任何接入服务器,将验证你的身份"""
        self.agentid.connect2entrypoint()
        return

    def add_message_listener(
        self, listener: typing.Callable[[dict], typing.Awaitable[None]]
    ):
        self.agentid.add_message_listener(listener)

    def online(self):
        self.agentid.online()
    def offline(self):
        self.agentid.offline()

    def send_message(self, to_aid_list: list, sessionId: str, message: 
                        Union[AssistantMessageBlock, list[AssistantMessageBlock], dict]):
        return self.agentid.send_message(to_aid_list, sessionId, message)

    def register_signal_handler(self):
        """
        注册信号处理函数
        """
        signal.signal(signal.SIGTERM, self.signal_handle)
        signal.signal(signal.SIGINT, self.signal_handle)

    def serve_forever(self):
        """
        """
        logger.info(f"agentid client[{self.agentid.id}] serve forever")
        while not self._shutdown_flag.is_set():
            time.sleep(1)

    def signal_handle(self, signum, frame):
        """
        信号处理函数
        :param signum: 信号编号
        :param frame: 当前栈帧
        """
        logger.info(f"recvied signal: {signum}, program exiting...")
        logger.info(f"agentid client[{self.agentid.id}] exited")
        self._shutdown_flag.set()  # 设置关闭标志
