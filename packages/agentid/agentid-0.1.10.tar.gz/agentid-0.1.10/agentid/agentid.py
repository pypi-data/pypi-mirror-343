import json
import asyncio

from dataclasses import dataclass
from typing import Literal, Optional, Union, Dict, List
import typing

from agentid import logger
from agentid.entrypoint_client import EntrypointClient
from agentid.heartbeat_client import HeartbeatClient
from agentid.message_client import MessageClient
from agentid.db.db_mananger import DBManager
from agentid.env import Environ
from agentid.message import AssistantMessageBlock
from agentid.group_chat import GroupChat


class AgentId:

    def __init__(self, agent_id: str, ep_aid:str, ep_url: str):
        self.id = agent_id
        self.ep_aid = ep_aid

        # TODO self.ep_url =f'ep.{".join(self.aid.split(".")[1:])}'
        self.ep_url = ep_url or Environ.ENTRY_SERVER.get()

        self.avaUrl = ""
        self.name = ""
        self.description = ""
        self.ep = EntrypointClient(agent_id, self.ep_url)
        # self.message_client = None  # 添加消息客户端属性
        self.message_clinent = {}
        self.groupchat_map={}
        self.message_client = MessageClient(self.id, self.ep.get_message_server())
        self.async_message_listener_func = None  # 添加消息监听器属性
        self.message_listener_func = None  # 添加消息监听器属性

        self.hbc = None
        self.s = None
        self.db_manager = DBManager(self.id)
        self.message_listener_funcs = []  # 添加消息监听器属性

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

    def add_message_listener(
        self, listener: typing.Callable[[dict], typing.Awaitable[None]]
    ):
        """消息监听器装饰器"""
        logger.debug("设置异步消息监听器")
        if not asyncio.iscoroutinefunction(listener):
            raise TypeError("监听器必须是异步函数(async def)")

        self.message_listener_funcs.append(listener)
        return listener

    def create_chat_group(self, name, subject, to_aid_list):
        """创建与多个agent的会话
        :param name: 群组名称
        :param subject: 群组主题
        :param to_aid_list: 目标agent ID列表
        :return: 会话ID或None
        """
        logger.debug(f"创建会话开始，参与者: {to_aid_list}")
        try:
            # 确保message_client已初始化
            if self.message_client is None:
                self.message_client = MessageClient(self.id, self.ep.get_message_server())
                self.message_client.sign_in()  # 确保登录状态                
            # 调用message_client创建群组并添加参与者
            groupchat = self.message_client.create_group_chat(name, subject)
            if groupchat is None:
                print("创建会话失败，可能是网络问题或其他错误")
                return None
            groupchat.set_on_message_recive(self.__agentid_message_listener)
            self.groupchat_map[groupchat.session_id] = groupchat
            print(f"创建会话成功，会话ID为：{groupchat.session_id}")
            self.db_manager.create_conversation(self.id,groupchat.session_id,groupchat.identifying_code,name, "public",to_aid_list)
            return groupchat.session_id
        except Exception as e:
            logger.exception(f"创建会话失败: {e}")
            return None

    def invite_member(self, session_id, to_aid):
        groupchat = self.groupchat_map.get(session_id)
        if self.message_client is None:
            self.message_client = MessageClient(self.id,self.ep.get_message_server())
            self.message_client.sign_in()  # 确保登录状态
            
        if groupchat is not None:
            groupchat.invite_member(to_aid)
            print(f"邀请 {to_aid} 加入会话 {session_id}")
            self.db_manager.invite_member(self.id,session_id,to_aid)
            
    def get_on_line_status(self,aids):
        return self.hbc.get_on_line_status(aids)
        
    def get_conversation_list(self,aid,main_aid,page,page_size):
        return self.db_manager.get_conversation_list(aid,main_aid,page,page_size)

    def send_message(self, to_aid_list: list, sessionId: str, message: Union[AssistantMessageBlock, list[AssistantMessageBlock], dict]):
        # 处理对象转换为字典
        if isinstance(message, (AssistantMessageBlock, dict)):
            message_data = message.__dict__ if hasattr(message, '__dict__') else message
        elif isinstance(message, list):
            message_data = [msg.__dict__ if hasattr(msg, '__dict__') else msg for msg in message]
        groupchat = self.groupchat_map.get(sessionId)
        print("send_message",to_aid_list)  # 打印收到的消息
        if self.message_client != None:
            if groupchat is None:
                print("groupchat is None")
                groupchat = GroupChat(self.id,self.ep.get_message_server,self.message_client.signature,sessionId)
                groupchat.set_on_message_recive(self.__agentid_message_listener)
                groupchat.start()
                return
            logger.debug(f"发送消息: {message_data}, to_aid_list: {to_aid_list}, sessionId: {sessionId}")
            groupchat.send_msg(json.dumps(message_data), ";".join(to_aid_list), "")
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
            return True
        else:
            logger.error(
                "消息发送失败: aid: {aid}, to_aid_list: {to_aid_list}, sessionId: {sessionId}, message: {message}"
            )
            return False

    def post_public_data(self,json_path):
        """
        发送数据到接入点服务器
        :param json_path: JSON文件路径
        :return: 响应内容或None
        """
        self.ep.post_public_data(json_path)

    def add_friend_agent(self,aid,name,description,avaUrl):
        self.db_manager.add_friend_agent(self.id,aid,name,description,avaUrl)

    def get_friend_agent_list(self):
        return self.db_manager.get_friend_agent_list(self.id)

    def connect2entrypoint(self):
        """连接到接入点服务器"""
        self.ep.sign_in()
        # 实现连接逻辑
        return self.ep

    def connect2entrypoint_other_url(self,server_url: str):
        """连接到接入点服务器"""
        self.ep = EntrypointClient(self.id,server_url)
        self.ep.sign_in()
        # 实现连接逻辑
        return self.ep

    def __heart_message_listener(self, invite_req):
        # 使用pprint打印格式化信息
        from pprint import pprint
        # pprint(
        #     vars(invite_req) if hasattr(invite_req, "__dict__") else invite_req,
        #     stream=logger.debug,
        # )
        # 使用对象属性访问而不是字典下标
        session_id = invite_req.SessionId if hasattr(invite_req, 'SessionId') else None
        groupchat = self.groupchat_map.get(session_id)
        if groupchat is None:
            groupchat = self.message_client.create_group_chat_with_session(session_id)
            self.groupchat_map[session_id] = groupchat
        groupchat.on_recv_invite(invite_req)
        groupchat.set_on_message_recive(self.__agentid_message_listener)

    def run_message_listeners(self, data):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            tasks = [self._safe_call(func, data) for func in self.message_listener_funcs]
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()

    async def _safe_call(self, func, data):
        try:
            await func(data)
        except Exception as e:
            logger.exception(f"message_listener_func: 异步消息处理异常: {e}")

    def __agentid_message_listener(self, data):
        logger.debug(f"消息服务器监听到新消息: {data}")
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
        groupchat = self.groupchat_map.get(session_id)
        if groupchat is not None:
            return groupchat.can_invite_member(session_id)
        else:
            chat = self.db_manager.get_conversation_by_id(self.id,session_id)
            if chat.identifying_code == "" or chat.identifying_code == None:
                return False
            else:
                return True

    def online(self):
        if self.ep == None:
            logger.error("before connect entrypoint, please call connect2entrypoint")
            return False
        if self.hbc != None:
            self.hbc.offline()
            self.hbc.sign_out()

        self.ep.get_entrypoint_config()
        logger.debug("connected entrypoint server: " + self.id)
        self.hbc = HeartbeatClient(self.id,self.ep.get_heartbeat_server())
        self.hbc.set_on_recv_invite(self.__heart_message_listener)
        if self.hbc.sign_in():
            self.hbc.online()

    def offline(self):
        """离线状态"""
        if self.hbc != None:
            self.hbc.offline()
            self.hbc.sign_out()

            
    def get_agent_list(self):
        """获取所有agentid列表"""
        return self.ep.get_agent_list()
    
    def get_all_public_data(self):
        """获取所有agentid列表"""
        return self.ep.get_all_public_data()

    def get_session_member_list(self,session_id):
        return self.db_manager.get_session_member_list(self.id,session_id)

    def __repr__(self):
        return f'AgentId(aid={self.id}, ep_aid={self.ep_aid}, ep_url={self.ep_url})'

