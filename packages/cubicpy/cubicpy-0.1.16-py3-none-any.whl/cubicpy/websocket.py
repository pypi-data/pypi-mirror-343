import asyncio
import websockets
import json
import logging
import random
from panda3d.core import Point3, TransformState, Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WebSocketClient:
    def __init__(self, physics_engine):
        self.physics_engine = physics_engine
        self.connection_code = None
        self.ws = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.reconnect_delay = 5  # 再接続までの遅延（秒）
        self._stop = False
        self.logger.debug("WebSocketClient initialized")
        
    async def connect(self, room_name):
        """WebSocketサーバーに接続"""
        uri = f"ws://localhost:8765"
        self.logger.debug(f"Attempting to connect to {uri}")
        while not self._stop:
            try:
                self.ws = await websockets.connect(uri, ping_interval=None, close_timeout=1)
                self.logger.debug(f"Connected to server, sending room name: {room_name}")
                await self.ws.send(room_name)
                response = await self.ws.recv()
                self.logger.debug(f"Received response: {response}")
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
                    self.logger.debug(f"Waiting {self.reconnect_delay} seconds before reconnecting...")
                    await asyncio.sleep(self.reconnect_delay)
                    self.logger.info("Attempting to reconnect...")
        return False
            
    async def receive_messages(self):
        """メッセージを受信して処理"""
        self.logger.debug("Starting message receive loop")
        while not self._stop:
            if not self.connected or self.ws is None:
                self.logger.debug("Not connected, waiting...")
                await asyncio.sleep(1)
                continue
                
            try:
                self.logger.debug("Waiting for messages...")
                async for message in self.ws:
                    if self._stop:
                        break
                    try:
                        self.logger.debug(f"Received raw message: {message}")
                        data = json.loads(message)
                        self.logger.info(f"Received message: {data}")
                        await self.process_message(data)  # 非同期処理に変更
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
            
    async def process_message(self, data):
        """受信したメッセージを処理"""
        try:
            if data.get("type") == "create_cube":
                position = data.get("position", [0, 0, 0])
                size = data.get("size", [1, 1, 1])
                self.logger.info(f"Creating cube at {position} with size {size}")
                await self.create_cube(position, size)
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            
    async def create_cube(self, position, size):
        """キューブを生成"""
        try:
            self.logger.debug("Creating cube shape")
            # 剛体を作成
            body = BulletRigidBodyNode('cube')
            shape = BulletBoxShape((size[0]/2, size[1]/2, size[2]/2))
            body.addShape(shape)
            body.setMass(1.0)
            
            # 位置を設定
            self.logger.debug(f"Setting cube position to {position}")
            body.setTransform(TransformState.makePos(Point3(*position)))
            
            # 物理エンジンに追加
            self.logger.debug("Attaching rigid body to physics engine")
            self.physics_engine.bullet_world.attachRigidBody(body)
            
            self.logger.info(f"Created cube at {position} with size {size}")
        except Exception as e:
            self.logger.error(f"Error creating cube: {e}")
            
    async def close(self):
        """接続を閉じる"""
        self.logger.debug("Closing connection")
        self._stop = True
        if self.ws:
            await self.ws.close()
            self.connected = False
            self.ws = None
            self.logger.debug("Connection closed")
            
    def generate_connection_code(self):
        """4桁の接続コードを生成"""
        self.connection_code = str(random.randint(1000, 9999))
        self.logger.debug(f"Generated connection code: {self.connection_code}")
        return self.connection_code

class WebSocketServer:
    def __init__(self, physics_engine, host="localhost", port=8765):
        self.physics_engine = physics_engine
        self.host = host
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.rooms = {}  # ルーム名とWebSocket接続のマッピング
        self.logger.debug(f"WebSocketServer initialized on {host}:{port}")

    async def handle_client(self, websocket, path):
        """クライアントの接続を処理"""
        room_name = None
        try:
            self.logger.debug(f"New client connected from {websocket.remote_address}")
            
            # ルーム名を受信
            room_name = await websocket.recv()
            self.logger.debug(f"Received room name: {room_name}")

            # ルームに接続を追加
            if room_name not in self.rooms:
                self.rooms[room_name] = set()
                self.logger.debug(f"Created new room: {room_name}")
            self.rooms[room_name].add(websocket)
            self.logger.info(f"Client connected to room: {room_name}")

            # 接続確認を送信
            await websocket.send("Connected")
            self.logger.debug("Sent connection confirmation")

            # メッセージの受信ループ
            async for message in websocket:
                try:
                    self.logger.debug(f"Received raw message: {message}")
                    data = json.loads(message)
                    self.logger.info(f"Received message: {data}")

                    if data["type"] == "create_cube":
                        position = data["position"]
                        size = data["size"]
                        self.logger.info(f"Creating cube at {position} with size {size}")
                        await self.create_cube(position, size)
                        # キューブ作成の確認を送信
                        await websocket.send(json.dumps({
                            "type": "cube_created",
                            "position": position,
                            "size": size
                        }))
                        self.logger.debug("Sent cube creation confirmation")
                except json.JSONDecodeError as e:
                    self.logger.error(f"Invalid JSON message: {message}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid JSON format"
                    }))
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": str(e)
                    }))

        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Client disconnected from room {room_name}")
        except Exception as e:
            self.logger.error(f"Unexpected error in handle_client: {e}")
        finally:
            # ルームから接続を削除
            if room_name in self.rooms:
                self.rooms[room_name].remove(websocket)
                if not self.rooms[room_name]:
                    del self.rooms[room_name]
                    self.logger.debug(f"Room {room_name} deleted")

    async def create_cube(self, position, size):
        """キューブを作成"""
        try:
            self.logger.debug("Creating cube shape")
            # キューブの形状を作成
            shape = BulletBoxShape(Vec3(size[0]/2, size[1]/2, size[2]/2))
            
            # 剛体ノードを作成
            node = BulletRigidBodyNode('cube')
            node.addShape(shape)
            node.setMass(1.0)
            
            # 位置を設定
            self.logger.debug(f"Setting cube position to {position}")
            node.setTransform(TransformState.makePos(Point3(*position)))
            
            # 物理エンジンに追加
            self.logger.debug("Attaching rigid body to physics engine")
            self.physics_engine.bullet_world.attachRigidBody(node)
            
            self.logger.info("Cube created successfully")
        except Exception as e:
            self.logger.error(f"Error creating cube: {e}")
            raise

    async def start(self):
        """WebSocketサーバーを開始"""
        try:
            self.logger.info(f"Starting WebSocket server on {self.host}:{self.port}")
            server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port
            )
            self.logger.info(f"WebSocket server started successfully")
            await server.wait_closed()
        except Exception as e:
            self.logger.error(f"Error starting WebSocket server: {e}")
            raise

def start_websocket_server(physics_engine, host="localhost", port=8765):
    """WebSocketサーバーを開始する関数"""
    server = WebSocketServer(physics_engine, host, port)
    asyncio.run(server.start()) 