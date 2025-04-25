from inspect import signature
from numbers import Number
import uuid
import requests
import datetime
import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
import threading
from typing import Optional
from agentid.group_chat import GroupChat  # 修改为从agentid包导入
from agentid import logger
from agentid.auth_client import AuthClient
from agentid.client import IClient

class MessageClient(IClient):
    def __init__(self, agent_id: str, server_url: str):
        """心跳客户端类        
        Args:
            agent_id: 代理ID
            server_url: 服务器URL
        """
        self.agent_id = agent_id
        self.server_url = server_url
        self.auth_client = AuthClient(agent_id, server_url)  # 使用AuthClient
        self.ws_thread: Optional[threading.Thread] = None
        self.msg_seq = 0
        self.session_id = ""
        self.identifying_code = ""
        self.is_running = False
        self.ws = None
        self.ws_url = ""
        self.last_invite_req = None
        self.last_msg = None
        self.last_receiver = None
        self.last_session_id = None
        self.last_ref_msg_id = None

        # 等待WebSocket连接建立或出错
        self.ws_connected = threading.Event()
        self.session_created = threading.Event()
        self.on_message_recive = None
        self.ws_error = None

    def set_on_message_recive(self, on_message_recive):
        self.on_message_recive = on_message_recive

    def create_group_chat(self, name, subject):
        if self.auth_client.signature is None:
            self.auth_client.sign_in()

        groupchat = GroupChat(self.agent_id, self.server_url, self.auth_client.signature)
        groupchat.create_chat_group(name, subject)
        return groupchat

    def create_group_chat_with_session(self, session_id):
        if self.auth_client.signature is None:
            self.auth_client.sign_in()
        groupchat = GroupChat(self.agent_id, self.server_url, self.auth_client.signature, session_id)
        groupchat.set_session_id(session_id)
        return groupchat

    def sign_in(self)-> bool:
        return self.auth_client.sign_in() is not None

    def sign_out(self):
        self.auth_client.sign_out()