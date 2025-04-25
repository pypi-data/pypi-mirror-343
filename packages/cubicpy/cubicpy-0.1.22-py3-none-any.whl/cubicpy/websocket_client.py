import asyncio
import websockets
import json
import logging
import argparse
import random
import time
from typing import Optional, Dict, List, Tuple

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WebSocketClient:
    def __init__(self, host="localhost", port=8765):
        self.uri = f"ws://{host}:{port}"
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.max_retries = 5
        self.retry_interval = 10  # 10 seconds
        self.heartbeat_interval = 10  # 10 seconds
        self.timeout_interval = 20  # 20 seconds
        self.last_heartbeat = 0
        self.last_received = 0
        self.room_name = None
        self.logger.debug(f"WebSocketClient initialized with URI: {self.uri}")

    async def connect(self, room_name: str, retries: int = 0) -> bool:
        """WebSocketサーバーに接続"""
        if retries >= self.max_retries:
            self.logger.error(f"Failed to connect after {self.max_retries} attempts")
            return False

        if retries > 0:
            self.logger.info(f"Retrying connection in {self.retry_interval} seconds...")
            await asyncio.sleep(self.retry_interval)

        try:
            self.logger.debug(f"Attempting to connect to {self.uri}")
            self.ws = await websockets.connect(self.uri)
            self.room_name = room_name
            self.logger.debug(f"Connected to server, sending room name: {room_name}")
            await self.ws.send(room_name)
            response = await self.ws.recv()
            self.logger.debug(f"Received response: {response}")
            
            if response == "Connected":
                self.connected = True
                self.last_heartbeat = time.time()
                self.last_received = time.time()
                self.logger.info("Successfully connected to server")
                asyncio.create_task(self.heartbeat_check())
                return True
            else:
                self.logger.error(f"Unexpected response: {response}")
                return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return await self.connect(room_name, retries + 1)

    async def heartbeat_check(self):
        """ハートビートチェック"""
        while self.connected:
            try:
                current_time = time.time()
                
                # タイムアウトチェック
                if current_time - self.last_received > self.timeout_interval:
                    self.logger.warning("Connection timeout detected")
                    self.connected = False
                    break
                
                # ハートビート送信
                if current_time - self.last_heartbeat >= self.heartbeat_interval:
                    await self.send_heartbeat()
                    self.last_heartbeat = current_time
                
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.error(f"Error in heartbeat check: {e}")
                self.connected = False
                break

    async def send_heartbeat(self):
        """ハートビートを送信"""
        if self.connected and self.ws:
            try:
                await self.ws.send("ping")
                self.logger.debug("Sent heartbeat")
            except Exception as e:
                self.logger.error(f"Error sending heartbeat: {e}")
                self.connected = False

    async def create_cube(self, position: Tuple[float, float, float], size: Tuple[float, float, float]) -> bool:
        """キューブを作成するメッセージを送信"""
        if not self.connected:
            self.logger.error("Not connected to server")
            return False

        try:
            message = {
                "type": "create_cube",
                "position": position,
                "size": size
            }
            self.logger.debug(f"Creating cube message: {message}")
            await self.ws.send(json.dumps(message))
            self.logger.debug("Message sent successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            self.connected = False
            return False

    async def receive_messages(self):
        """メッセージを受信"""
        while self.connected:
            try:
                message = await self.ws.recv()
                self.last_received = time.time()
                
                # ハートビートメッセージはスキップ
                if message == "pong":
                    continue
                    
                self.logger.debug(f"Received message: {message}")
                data = json.loads(message)
                
                if data["type"] == "cube_created":
                    self.logger.info("Cube created successfully on server")
                elif data["type"] == "error":
                    self.logger.error(f"Server error: {data['message']}")
            except websockets.exceptions.ConnectionClosed:
                self.logger.info("Connection closed by server")
                self.connected = False
            except Exception as e:
                self.logger.error(f"Error receiving message: {e}")
                self.connected = False

    async def close(self):
        """接続を閉じる"""
        if self.ws:
            await self.ws.close()
            self.connected = False
            self.logger.debug("Connection closed")

def generate_connection_code() -> str:
    """4桁の接続コードを生成"""
    return str(random.randint(1000, 9999))

async def main():
    parser = argparse.ArgumentParser(description="WebSocket client for CubicPy")
    parser.add_argument("--host", default="localhost", help="WebSocket server host")
    parser.add_argument("--port", type=int, default=8765, help="WebSocket server port")
    parser.add_argument("--code", help="Connection code")
    args = parser.parse_args()

    connection_code = args.code if args.code else generate_connection_code()
    print(f"Connection code: {connection_code}")

    client = WebSocketClient(args.host, args.port)
    if await client.connect(connection_code):
        # 原点にキューブを配置
        print("Creating cube at origin...")
        if await client.create_cube(position=(0, 0, 0), size=(1, 1, 1)):
            print("Cube created successfully")
        await client.receive_messages()
    await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 