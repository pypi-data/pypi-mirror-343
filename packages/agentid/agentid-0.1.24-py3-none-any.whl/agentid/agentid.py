import abc
from contextlib import AbstractAsyncContextManager, asynccontextmanager
import json
import asyncio

from dataclasses import dataclass
import time
from typing import Any, AsyncIterator, Callable, Literal, Optional, Union, Dict, List
import typing
import signal
import threading


from agentid.log import logger
from agentid.ca_client import CAClient
from agentid.entrypoint_client import EntrypointClient
from agentid.heartbeat_client import HeartbeatClient
from agentid.message_client import MessageClient
from agentid.db.db_mananger import DBManager
from agentid.env import Environ
from agentid.message import AssistantMessageBlock
from agentid.group_manager import GroupManager, Group
from agentid.config import Config


class _AgentId(abc.ABC):
    """
    AgentId类的抽象基类
    """
    def __init__(self):
        self.shutdown_flag = threading.Event()  # 初始化信号量
        self.exit_hook_func = None
    def register_signal_handler(self, exit_hook_func=None):
        """
        注册信号处理函数
        
        """
        signal.signal(signal.SIGTERM, self.signal_handle)
        signal.signal(signal.SIGINT, self.signal_handle)
        self.exit_hook_func = exit_hook_func
        
    def serve_forever(self):
        """ """
        logger.info(f"agentid client[{self.id}] serve forever")
        while not self.shutdown_flag.is_set():
            time.sleep(1)

    def signal_handle(self, signum, frame):
        """
        信号处理函数
        :param signum: 信号编号
        :param frame: 当前栈帧
        """
        logger.info(f"recvied signal: {signum}, program exiting...")
        logger.info(f"agentid client[{self.id}] exited")
        self.shutdown_flag.set()  # 设置关闭标志
        if self.exit_hook_func:
            self.exit_hook_func(signum, frame)

class AgentId(_AgentId):

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = ""
        self.avaUrl = ""
        self.description = ""
        self.ca_client = CAClient(Config.ca_server or Environ.CA_SERVER.get())
        self.ep_url = Config.entry_server or Environ.ENTRY_SERVER.get()
        self.message_handlers = []  # 添加消息监听器属性
        self.heartbeat_client = None
        self.db_manager = DBManager()

    def initialize(self):
        logger.debug("initialzing entrypoint server")
        self.entry_client = EntrypointClient(self.id, self.ep_url)
        self.entry_client.initialize()

        logger.debug("initialzing heartbeat server")
        self.heartbeat_client = HeartbeatClient(
            self.id, self.entry_client.get_heartbeat_server()
        )
        self.heartbeat_client.initialize()

        self.group_manager = GroupManager(
            self.id, self.entry_client.get_message_server()
        )
        self.db_manager.set_aid(self.id)

    def set_avaUrl(self,avaUrl):
        self.avaUrl = avaUrl
        return self

    def set_name(self,name):
        self.name = name
        return self

    def set_description(self,description):
        self.description = description
        return self

    def get_agentid_info(self):
        return {
            'aid':self.id,
            'name':self.name,
            'description':self.description,
            'avaUrl':self.avaUrl,
            'ep_aid':self.ep_aid,
            'ep_url':self.ep_url,
        }

    def get_message_list(self,session_id,page=1, page_size=10):
        return self.db_manager.get_message_list(self.id,session_id,page,page_size)

    def add_message_handler(
        self, handler: typing.Callable[[dict], typing.Awaitable[None]]
    ):
        """消息监听器装饰器"""
        logger.debug("add message handler")
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError("监听器必须是异步函数(async def)")

        self.message_handlers.append(handler)

    def create_chat_group(self, name, subject, *, type='public'):
        """创建与多个agent的会话
        :param name: 群组名称
        :param subject: 群组主题
        :param to_aid_list: 目标agent ID列表
        :return: 会话ID或None
        """
        logger.debug(f"create group: {name}, subject: {subject}, type: {type}")
        group = self.group_manager.create_group(name, subject, type)
        group.set_on_message_receive(self.__agentid_message_listener)
        return group.session_id

    def invite_member(self, session_id, to_aid):
        to_aid = self.build_id(to_aid)
        if self.group_manager.invite_member(session_id, to_aid):
            self.db_manager.invite_member(self.id, session_id, to_aid)
        else:
            logger.error(f"failed to invite: {to_aid} -> {session_id}")

    def get_online_status(self,aids):
        return self.heartbeat_client.get_online_status(aids)

    def get_conversation_list(self,aid,main_aid,page,page_size):
        return self.db_manager.get_conversation_list(aid,main_aid,page,page_size)

    def send_message(self, to_aid_list: list, sessionId: str, message: Union[AssistantMessageBlock, list[AssistantMessageBlock], dict]):
        # 处理对象转换为字典
        if isinstance(message, (AssistantMessageBlock, dict)):
            message_data = message.__dict__ if hasattr(message, '__dict__') else message
        elif isinstance(message, list):
            message_data = [msg.__dict__ if hasattr(msg, '__dict__') else msg for msg in message]

        self.group_manager.send_msg(sessionId ,json.dumps(message_data), ";".join(to_aid_list), "")
        self.db_manager.insert_message(
            "user",
            self.id,
            sessionId,
            self.id,
            "",
            ",".join(to_aid_list),
            json.dumps(message_data),
            "text",
            "sent",
        )

    def post_public_data(self,json_path):
        """
        发送数据到接入点服务器
        :param json_path: JSON文件路径
        :return: 响应内容或None
        """
        self.entry_client.post_public_data(json_path)

    def add_friend_agent(self,aid,name,description,avaUrl):
        self.db_manager.add_friend_agent(self.id,aid,name,description,avaUrl)

    def get_friend_agent_list(self):
        return self.db_manager.get_friend_agent_list(self.id)

    def __on_heartbeat_invite_message(self, invite_req):
        group: Group = self.group_manager.join_group(invite_req)
        group.set_on_message_receive(self.__agentid_message_listener)

    def run_message_listeners(self, data):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            tasks = [self._safe_call(func, data) for func in self.message_handlers]
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()

    async def _safe_call(self, func, data):
        try:
            await func(data)
        except Exception as e:
            logger.exception(f"message_listener_func: 异步消息处理异常: {e}")

    def __agentid_message_listener(self, data):
        logger.debug(f"received a message: {data}")
        session_id = data["session_id"]
        message_id = data["message_id"]

        sender = data["sender"]
        receiver = data["receiver"]
        message = json.loads(data["message"]) if isinstance(data["message"], str) else data["message"]
        if isinstance(message, list):
            # self.__insert_group_chat(self.aid,session_id,"",name)
            self.db_manager.insert_message("assistant",self.id,session_id,sender, message_id, receiver, data["message"], "text", "success")
        else:
            message_list = []  # 修改变量名避免与内置list冲突
            message_list.append(message)
            # self.__insert_group_chat(self.aid,session_id,"",name)
            self.db_manager.insert_message("assistant",self.id,session_id,sender, message_id, receiver, json.dumps(message_list), "text", "success")

        self.run_message_listeners(data)

    def __insert_group_chat(self,aid,session_id,identifying_code,name):
        conversation =  self.db_manager.get_conversation_by_id(aid,session_id)
        if conversation is None:
            # identifying_code,name, type,to_aid_list
            self.db_manager.create_conversation(aid,session_id,identifying_code,name,"public",[])
        return

    def can_invite_member(self,session_id):
        group = self.group_manager.get(session_id)
        if group:
            return group.can_invite_member(session_id)
        else:
            chat = self.db_manager.get_conversation_by_id(self.id,session_id)
            if chat.identifying_code == "" or chat.identifying_code == None:
                return False
            else:
                return True

    def online(self):
        self.heartbeat_client.online()
        self.heartbeat_client.set_on_recv_invite(self.__on_heartbeat_invite_message)
        logger.info(f'agentid {self.id} is ready!')

    def offline(self):
        """离线状态"""
        if self.heartbeat_client:
            self.heartbeat_client.offline()
            self.heartbeat_client.sign_out()
        if self.entry_client:
            self.entry_client.sign_out()

    def get_agent_list(self):
        """获取所有agentid列表"""
        return self.entry_client.get_agent_list()

    def get_all_public_data(self):
        """获取所有agentid列表"""
        return self.entry_client.get_all_public_data()

    def get_session_member_list(self,session_id):
        return self.db_manager.get_session_member_list(self.id,session_id)

    def build_id(self, id):
        ep = self.ep_url.split('.')
        end_str = f'{ep[-2]}.{ep[-1]}'
        if id.endswith(end_str):
            return id

        return f'{id}.{ep[-2]}.{ep[-1]}'

    def load_aid(self, agent_id: str) -> bool:
        self.id = self.build_id(agent_id)
        try:
            logger.debug(f"load agentid: {self.id}")  # 调试用
            result = self.db_manager.load_aid(self.id)
            if result[0] is None:  # 检查返回结果是否有效
                logger.error(f"未找到agent_id: {self.id} 或数据不完整: {result}")
                return

            ep_aid, ep_url = result[0], result[1]  # 安全获取前两个值
            avaUrl = result[2] if len(result) > 2 else ""
            name = result[3] if len(result) > 3 else ""
            description = result[4] if len(result) > 4 else ""

            if ep_aid and ep_url:
                return self

            ep_url = self.ca_client.resign_csr(self.id)
            logger.debug(f"resign: {ep_url}")  # 调试用
            if ep_url:
                self.db_manager.update_aid(self.id, "ep_aid", ep_url)
                self.set_avaUrl(avaUrl)
                self.set_name(name)
                self.set_description(description)
                return self

        except Exception as e:
            logger.exception(f"加载和验证密钥对时出错: {e}")  # 调试用
            return False

    def create_aid(self, agent_id: str):
        self.id = self.build_id(agent_id)
        """连接到服务器"""
        # 生成 Ed25519 私钥
        logger.debug(f"create agentid: {self.id}")  # 调试用
        result = self.ca_client.send_csr_to_server(self.id)
        if result == True:
            self.db_manager.create_aid(self.id)
            # self.load_aid(self.id)
            return self
        raise RuntimeError("create agentid")

    def get_agentid_list(self):
        list = self.db_manager.get_agentid_list()
        return list

    def get_agentid(self, id):
        id = self.build_id(id)
        agents = [_id for _id in self.db_manager.get_agentid_list() if _id == id]
        return agents[0] if agents else None

    def update_aid_info(self, aid, avaUrl, name, description):
        self.db_manager.update_aid_info(aid, avaUrl, name, description)
        return True

    def message_handler(self, name: str|None = None):
        def wrapper(fn):
            # 动态获取 client 属性名
            self.add_message_handler(fn)
            return fn
        return wrapper

    def __repr__(self):
        return f"AgentId(aid={self.id})"
