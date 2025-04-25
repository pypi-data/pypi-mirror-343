import asyncio
import websockets
import json
import logging
import random
from panda3d.core import Point3, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape

class WebSocketClient:
    def __init__(self, physics_engine):
        self.physics_engine = physics_engine
        self.connection_code = None
        self.ws = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.reconnect_delay = 5  # 再接続までの遅延（秒）
        self._stop = False
        
    async def connect(self, room_name):
        """WebSocketサーバーに接続"""
        uri = f"ws://localhost:8765"
        while not self._stop:
            try:
                self.ws = await websockets.connect(uri, ping_interval=None, close_timeout=1)
                await self.ws.send(room_name)
                response = await self.ws.recv()
                if response == "Invalid room name":
                    self.logger.error("Invalid room name")
                    return False
                self.logger.info(f"Connected to room: {room_name}")
                self.connected = True
                return True
            except Exception as e:
                self.logger.error(f"Connection error: {e}")
                self.connected = False
                self.ws = None
                if not self._stop:
                    await asyncio.sleep(self.reconnect_delay)
                    self.logger.info("Attempting to reconnect...")
        return False
            
    async def receive_messages(self):
        """メッセージを受信して処理"""
        while not self._stop:
            if not self.connected or self.ws is None:
                await asyncio.sleep(1)
                continue
                
            try:
                async for message in self.ws:
                    if self._stop:
                        break
                    try:
                        data = json.loads(message)
                        self.process_message(data)
                    except json.JSONDecodeError:
                        self.logger.error(f"Invalid JSON: {message}")
            except websockets.exceptions.ConnectionClosed:
                if not self._stop:
                    self.logger.info("Connection closed, attempting to reconnect...")
                    self.connected = False
                    self.ws = None
                    await asyncio.sleep(self.reconnect_delay)
            except Exception as e:
                if not self._stop:
                    self.logger.error(f"Error in receive_messages: {e}")
                    self.connected = False
                    self.ws = None
                    await asyncio.sleep(self.reconnect_delay)
            
    def process_message(self, data):
        """受信したメッセージを処理"""
        try:
            if data.get("type") == "create_cube":
                position = data.get("position", [0, 0, 0])
                size = data.get("size", [1, 1, 1])
                self.create_cube(position, size)
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            
    def create_cube(self, position, size):
        """キューブを生成"""
        try:
            # 剛体を作成
            body = BulletRigidBodyNode('cube')
            shape = BulletBoxShape((size[0]/2, size[1]/2, size[2]/2))
            body.addShape(shape)
            body.setMass(1.0)
            
            # 位置を設定
            body.setTransform(TransformState.makePos(Point3(*position)))
            
            # 物理エンジンに追加
            self.physics_engine.bullet_world.attachRigidBody(body)
            
            self.logger.info(f"Created cube at {position} with size {size}")
        except Exception as e:
            self.logger.error(f"Error creating cube: {e}")
            
    async def close(self):
        """接続を閉じる"""
        self._stop = True
        if self.ws:
            await self.ws.close()
            self.connected = False
            self.ws = None
            
    def generate_connection_code(self):
        """4桁の接続コードを生成"""
        self.connection_code = str(random.randint(1000, 9999))
        return self.connection_code 