import asyncio
import websockets
import json
import logging
from panda3d.core import Point3, Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from direct.showbase.ShowBase import ShowBase

class WebSocketClient:
    def __init__(self, physics_engine):
        self.physics_engine = physics_engine
        self.connection_code = None
        self.ws = None
        self.logger = logging.getLogger(__name__)
        
    async def connect(self, room_name):
        """WebSocketサーバーに接続"""
        uri = f"ws://localhost:8765"
        try:
            self.ws = await websockets.connect(uri)
            await self.ws.send(room_name)
            response = await self.ws.recv()
            if response == "Invalid room name":
                self.logger.error("Invalid room name")
                return False
            self.logger.info(f"Connected to room: {room_name}")
            return True
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
            
    async def receive_messages(self):
        """メッセージを受信して処理"""
        try:
            async for message in self.ws:
                try:
                    data = json.loads(message)
                    self.process_message(data)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON: {message}")
        except websockets.exceptions.ConnectionClosed:
            self.logger.info("Connection closed")
            
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
        if self.ws:
            await self.ws.close()
            
    def generate_connection_code(self):
        """4桁の接続コードを生成"""
        import random
        self.connection_code = str(random.randint(1000, 9999))
        return self.connection_code 