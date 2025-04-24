import socket
import threading
import json
from typing import Dict, List, Optional, Callable
from .base import BaseAI

class ChatRoomAI(BaseAI):
    """聊天室AI功能"""
    
    def __init__(self, config: Optional[Dict] = None):
        super().__init__(config)
        self.host = "0.0.0.0"  # 默认监听所有网络接口
        self.port = 5001  # 默认端口
        self.clients: List[socket.socket] = []
        self.server_socket: Optional[socket.socket] = None
        self.is_running = False
        self.message_callback: Optional[Callable] = None
        
    def start_server(self, port: int = 5001) -> Dict[str, str]:
        """启动聊天室服务器
        
        Args:
            port: 服务器端口号
            
        Returns:
            Dict[str, str]: 包含服务器信息的字典
        """
        try:
            self.port = port
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_running = True
            
            # 启动接受连接的线程
            accept_thread = threading.Thread(target=self._accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            return {
                "status": "success",
                "message": f"聊天室服务器已启动，监听端口: {self.port}",
                "host": self.host,
                "port": str(self.port)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"启动服务器失败: {str(e)}"
            }
    
    def join_chatroom(self, host: str, port: int) -> Dict[str, str]:
        """加入聊天室
        
        Args:
            host: 服务器主机地址
            port: 服务器端口号
            
        Returns:
            Dict[str, str]: 包含连接信息的字典
        """
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            self.clients.append(client_socket)
            
            # 启动接收消息的线程
            receive_thread = threading.Thread(target=self._receive_messages, args=(client_socket,))
            receive_thread.daemon = True
            receive_thread.start()
            
            return {
                "status": "success",
                "message": f"成功连接到聊天室 {host}:{port}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"连接失败: {str(e)}"
            }
    
    def send_message(self, message: str) -> Dict[str, str]:
        """发送消息到聊天室
        
        Args:
            message: 要发送的消息内容
            
        Returns:
            Dict[str, str]: 包含发送状态的字典
        """
        try:
            if not self.clients:
                return {
                    "status": "error",
                    "message": "未连接到任何聊天室"
                }
            
            message_data = {
                "type": "message",
                "content": message
            }
            
            for client in self.clients:
                client.send(json.dumps(message_data).encode())
            
            return {
                "status": "success",
                "message": "消息发送成功"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"发送消息失败: {str(e)}"
            }
    
    def set_message_callback(self, callback: Callable[[str], None]) -> None:
        """设置消息接收回调函数
        
        Args:
            callback: 接收消息时的回调函数
        """
        self.message_callback = callback
    
    def stop(self) -> Dict[str, str]:
        """停止聊天室
        
        Returns:
            Dict[str, str]: 包含停止状态的字典
        """
        try:
            self.is_running = False
            if self.server_socket:
                self.server_socket.close()
            for client in self.clients:
                client.close()
            self.clients.clear()
            
            return {
                "status": "success",
                "message": "聊天室已停止"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"停止聊天室失败: {str(e)}"
            }
    
    def _accept_connections(self) -> None:
        """接受新的客户端连接"""
        while self.is_running:
            try:
                client_socket, address = self.server_socket.accept()
                self.clients.append(client_socket)
                
                # 启动接收消息的线程
                receive_thread = threading.Thread(target=self._receive_messages, args=(client_socket,))
                receive_thread.daemon = True
                receive_thread.start()
                
                if self.message_callback:
                    self.message_callback(f"新用户加入: {address}")
            except:
                break
    
    def _receive_messages(self, client_socket: socket.socket) -> None:
        """接收消息
        
        Args:
            client_socket: 客户端socket
        """
        while self.is_running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = json.loads(data.decode())
                if message["type"] == "message" and self.message_callback:
                    self.message_callback(message["content"])
            except:
                break
        
        # 客户端断开连接
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        client_socket.close() 