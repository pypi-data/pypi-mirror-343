from numbers import Number
import queue
import uuid
import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
import websocket
import threading
import time
import ssl
import json
from typing import Optional
from agentid.log import logger
from agentid.message_client import MessageClient
from agentid.message_serialize import InviteMessageReq


class Group:

    def __init__(self, agent_id: str, message_client: MessageClient):
        """心跳客户端类        
        Args:
            agent_id: 代理ID
            server_url: 服务器URL
        """
        self.agent_id = agent_id
        self.identifying_code = ""
        self.on_message_receive = None
        self.message_client: MessageClient = message_client
        self.queue = queue.Queue()
        self.invite_message = None
        
    def initialize(self, name: str, subject: str, *, group_type: str = "public", session_id=None)->str:
        logger.info(f"sign in success: {self.agent_id}")
        self.message_client.set_message_handler(self)
        if not self.message_client.start_websocket_client():
            logger.error("Failed to start WebSocket client.")
            return
        
        if not session_id:
            self._create(name, subject, group_type)
            # 等待创建群组的响应
            self.session_id = self.queue.get(timeout=5)
            self.queue.task_done()
        else:
            self.session_id = session_id
            logger.info(f"join group: {self.session_id}")
        return self.session_id

    def can_invite_member(self):
        return not not self.identifying_code

    def set_session_id(self, session_id: str):
        self.session_id = session_id

    def set_on_message_receive(self, on_message_recive):
        self.on_message_receive = on_message_recive

    def __on_create_chat_group_ack(self, js):
        if "session_id" in js and "status_code" in js and "message" in js and "identifying_code" in js:
            self.session_id = js["session_id"]
            self.identifying_code = js["identifying_code"]
            self.queue.put(self.session_id)

            if js["status_code"] == 200 or js["status_code"] == "200":
                logger.info(f"create_chat_group_ack: {js}")
            else:
                logger.error(f"create_chat_group_ack failed: {js}")
        else:
            logger.error("收到的消息中不包括session_id字段，不符合预期格式")

    def _create(self, group_name: str, subject: str, group_type: str = "public"):
        logger.info(f"create_chat_group: {group_name}, {subject}, {group_type}")
        try:
            logger.debug(f"check WebSocket connection status")  # 调试日志
            data = {
                    "cmd" : "create_chat_group_req",
                    "data" : {
                        "request_id": f"{uuid.uuid4().hex}",
                        "type": f"{group_type}",
                        "group_name": f"{group_name}",
                        "subject": f"{subject}",
                        "timestamp": f"{int(time.time() * 1000)}"
                    },
                }
            msg = json.dumps(data)
            self.message_client.send_msg(msg)
            logger.debug(f"send message: {msg}")  # 调试日志
        except Exception as e:
            logger.exception(f'send create chat group message exception: {e}')  # 记录异常

    def close_chat_group(self, session_id: str):
        pass

    # accept invite request
    def accept_invite(self, invite_req: InviteMessageReq):
        try:
            data = {
                    "cmd" : "join_chat_group_req",
                    "data" : {
                        "session_id": invite_req.SessionId,
                        "request_id": f"{int(time.time() * 1000)}",
                        "inviter_agent_id": invite_req.InviterAgentId,
                        "invite_code": invite_req.InviteCode,
                        "last_msg_id": "0"
                    },
                }
            msg = json.dumps(data)
            self.message_client.send_msg(msg)
            logger.debug(f"send join chat group message: {msg}")  # 调试日志
        except Exception as e:
            logger.exception(f'send join chat group message exception: {e}')  # 记录异常

    def reject_invite(self, invite_req: InviteMessageReq):
        pass

    def leave_group(self, session_id: str):
        pass

    def invite_member(self, acceptor_aid: str):
        try:
            data = {
                    "cmd" : "invite_agent_req",
                    "data" : {
                        "session_id": self.session_id,
                        "request_id": f"{uuid.uuid4().hex}",
                        "inviter_id": self.agent_id,
                        "acceptor_id": acceptor_aid,
                        "invite_code": self.identifying_code,
                    },
                }
            msg = json.dumps(data)
            ret = self.message_client.send_msg(msg)
            logger.debug(f"send invite message: {msg} , ret:{ret}")  # 调试日志  
            return ret
        except Exception as e:
            logger.exception(f'send invite message exception: {e}')  # 记录异常
            return False

    def eject_member(self,  eject_aid: str):
        try:
            data = {
                    "cmd" : "eject_agent_req",
                    "data" : {
                        "session_id": f"{self.session_id}",
                        "request_id": f"{int(time.time() * 1000)}",
                        "eject_agent_id": self.agent_id,
                        "identifying_code": self.identifying_code,
                    },
                }
            msg = json.dumps(data)
            self.message_client.send_msg(msg)
            logger.debug(f"send eject message: {msg}")  # 调试日志
            return True
        except Exception as e:
            logger.exception(f'send eject message exception: {e}')
            return False

    def get_member_list(self):
        try:
            # SessionId       string `json:"session_id"`
            # RequestId       string `json:"request_id"`
            data = {
                    "cmd" : "get_member_list",
                    "data" : {
                        "session_id": f"{self.session_id}",
                        "request_id": f"{int(time.time() * 1000)}",
                    },
                }
            msg = json.dumps(data)
            self.message_client.send_msg(msg)
            logger.debug(f"send get member list message: {msg}")  # 调试日志
            return True
        except Exception as e:
            logger.exception(f'send get member list message exception: {e}')
            return False

    def send_msg(self, msg: str, receiver: str, ref_msg_id : str = ""):
        data = {
                    "cmd" : "chat_group_message",
                    "data" : {
                        "session_id": self.session_id,
                        "ref_msg_id": ref_msg_id,
                        "sender": f"{self.agent_id}",
                        "receiver": receiver,
                        "message": msg,
                        "timestamp": f"{int(time.time() * 1000)}"
                    },
                }
        msg = json.dumps(data)
        logger.debug(f"send message: {msg}")
        self.message_client.send_msg(msg)

    def on_message(self, ws, message):
        """接收到服务器消息时的处理函数"""
        # print(f"message_client收到消息: {message}")
        # 如果需要解析 JSON 数据，可以使用 json.loads(message)
        logger.debug(f"received a message: {message}")
        js = json.loads(message)
        if "cmd" not in js or "data" not in js:
            logger.error("收到的消息中不包括cmd字段，不符合预期格式")
            return
        cmd = js["cmd"]

        if cmd == "create_chat_group_ack":
            self.__on_create_chat_group_ack(js["data"])

        elif cmd == "chat_group_message":
            if self.on_message_receive is not None:
                self.on_message_receive(js["data"])
                # TODO after receive message, send ack
            else:
                logger.error("on_message_recive is None")

    def on_open(self, ws):
        """WebSocket连接建立时的处理函数"""
        logger.info("WebSocket connection opened.")
        # 成员断线加入
        if self.invite_message is not None:
            self.accept_invite(self.invite_message)

        # owner重新加入
        if self.identifying_code:
            self.owner_rejoin()

    def owner_rejoin(self):
        try:
            data = {
                "cmd": "join_chat_group_req",
                "data": {
                    "session_id": self.session_id,
                    "request_id": f"{int(time.time() * 1000)}",
                    "inviter_agent_id": "",
                    "invite_code": self.identifying_code,
                    "last_msg_id": "0",
                },
            }
            msg = json.dumps(data)
            self.message_client.send_msg(msg)
            logger.debug(f"send owner rejoin message: {msg}")  # 调试日志
        except Exception as e:
            logger.exception(f'send owner rejoin message exception: {e}')

class GroupManager:

    def __init__(self, agent_id: str, server_url: str):
        self.lock = threading.Lock()
        self.groups = {}
        self.agent_id = agent_id
        self.server_url = server_url
    
    def get(self, session_id: str):
        with self.lock:
            group: Group = self.groups.get(session_id)
            return group

    def create_group(self, name: str, subject: str, group_type: str = "public"):
        with self.lock:
            if name in self.groups:
                logger.error(f"Group {name} already exists.")
                return None

            message_client = MessageClient(self.agent_id, self.server_url)
            message_client.initialize()
            
            group = Group(self.agent_id, message_client)
            session = group.initialize(name, subject, group_type=group_type)
            if not session:
                logger.error(f"Failed to create group {name}.")
                return None
            self.groups[session] = group
            logger.info(f"Group {name} created: {session}.")
            return group

    def join_group(self, req: InviteMessageReq):
        print("join group")
        with self.lock:
            message_client = MessageClient(self.agent_id, self.server_url)
            message_client.initialize()
            
            group: Group = Group(self.agent_id, message_client)
            if not group.initialize("", "", session_id=req.SessionId):
                logger.error(f"Failed to join group {req.SessionId}.")
                return None
            group.accept_invite(req)
            group.invite_message = req
            self.groups[req.SessionId] = group
            return group

    def leave_group(self, session_id: str):
        pass

    def invite_member(self, session_id: str, acceptor_aid: str):
        with self.lock:
            if session_id not in self.groups:
                logger.error(f"Group {session_id} does not exist.")
                return False
            group: Group = self.groups[session_id]
            return group.invite_member(acceptor_aid)

    def send_msg(self, session_id: str, msg: str, receiver: str, ref_msg_id: str = ""):
        with self.lock:
            if session_id not in self.groups:
                logger.error(f"Group {session_id} does not exist.")
                return False
            group: Group = self.groups[session_id]
            group.send_msg(msg, receiver, ref_msg_id)
            return True
