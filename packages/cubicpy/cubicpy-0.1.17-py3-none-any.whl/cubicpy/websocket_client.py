import asyncio
import websockets
import json
import logging
import argparse
import random

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WebSocketClient:
    def __init__(self, host="localhost", port=8765):
        self.uri = f"ws://{host}:{port}"
        self.ws = None
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.logger.debug(f"WebSocketClient initialized with URI: {self.uri}")

    async def connect(self, room_name):
        """WebSocketサーバーに接続"""
        try:
            self.logger.debug(f"Attempting to connect to {self.uri}")
            self.ws = await websockets.connect(self.uri)
            self.logger.debug("Connected to server, sending room name: {room_name}")
            await self.ws.send(room_name)
            response = await self.ws.recv()
            self.logger.debug(f"Received response: {response}")
            if response == "Connected":
                self.connected = True
                self.logger.info("Successfully connected to server")
                return True
            else:
                self.logger.error(f"Unexpected response: {response}")
                return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    async def create_cube(self, position, size):
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
            return False

    async def receive_messages(self):
        """メッセージを受信"""
        while self.connected:
            try:
                message = await self.ws.recv()
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

def generate_connection_code():
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