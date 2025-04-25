import asyncio
import websockets
import json
import logging
import argparse
import random
import time

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
        self.ping_interval = 5  # ping送信間隔（秒）
        self.last_ping_time = 0
        self.logger.debug(f"WebSocketClient initialized with URI: {self.uri}")

    async def connect(self, room_name):
        """WebSocketサーバーに接続"""
        try:
            self.logger.debug(f"Attempting to connect to {self.uri}")
            self.ws = await websockets.connect(self.uri)
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
            return False

    async def send_message(self, message):
        """メッセージを送信"""
        if not self.connected or not self.ws:
            self.logger.error("Not connected to server")
            return False
        try:
            self.logger.debug(f"Sending message: {message}")
            await self.ws.send(json.dumps(message))
            self.logger.debug("Message sent successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False

    async def create_cube(self, position=(0, 0, 0), size=(1, 1, 1)):
        """キューブを作成するメッセージを送信"""
        message = {
            "type": "create_cube",
            "position": position,
            "size": size
        }
        self.logger.debug(f"Creating cube message: {message}")
        return await self.send_message(message)

    async def send_ping(self):
        """pingを送信"""
        if not self.connected or not self.ws:
            return False
        try:
            current_time = time.time()
            if current_time - self.last_ping_time >= self.ping_interval:
                self.logger.debug("Sending ping")
                await self.ws.ping()
                self.last_ping_time = current_time
                return True
        except Exception as e:
            self.logger.error(f"Error sending ping: {e}")
            self.connected = False
        return False

    async def receive_messages(self):
        """メッセージを受信"""
        while self.connected and self.ws:
            try:
                # pingを送信
                await self.send_ping()
                
                # メッセージを受信
                message = await asyncio.wait_for(self.ws.recv(), timeout=1.0)
                self.logger.debug(f"Received message: {message}")
                
                # メッセージを処理
                try:
                    data = json.loads(message)
                    if data.get("type") == "error":
                        self.logger.error(f"Server error: {data.get('message')}")
                    elif data.get("type") == "cube_created":
                        self.logger.info("Cube created successfully on server")
                except json.JSONDecodeError:
                    self.logger.debug(f"Received non-JSON message: {message}")
                    
            except asyncio.TimeoutError:
                # タイムアウトは正常な動作
                continue
            except websockets.exceptions.ConnectionClosed:
                self.logger.error("Connection closed by server")
                self.connected = False
                break
            except Exception as e:
                self.logger.error(f"Error receiving message: {e}")
                self.connected = False
                break

    async def close(self):
        """接続を閉じる"""
        if self.ws:
            self.logger.debug("Closing connection")
            await self.ws.close()
            self.connected = False
            self.ws = None
            self.logger.debug("Connection closed")

def generate_connection_code():
    """4桁の接続コードを生成"""
    return str(random.randint(1000, 9999))

async def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='CubicPy WebSocket Client')
    parser.add_argument('--host', default='localhost', help='WebSocket server host')
    parser.add_argument('--port', type=int, default=8765, help='WebSocket server port')
    parser.add_argument('--code', help='Connection code (optional)')
    args = parser.parse_args()

    # 接続コードの生成または使用
    connection_code = args.code if args.code else generate_connection_code()
    print(f"Connection code: {connection_code}")

    # クライアントの作成と接続
    client = WebSocketClient(args.host, args.port)
    if not await client.connect(connection_code):
        print("Failed to connect to server")
        return

    try:
        # メッセージ受信タスクを開始
        receive_task = asyncio.create_task(client.receive_messages())

        # 原点にキューブを配置
        print("Creating cube at origin...")
        if await client.create_cube(position=(0, 0, 0), size=(1, 1, 1)):
            print("Cube created successfully")
        else:
            print("Failed to create cube")

        # ユーザー入力の待機
        print("\nPress Enter to create a random cube, or 'q' to quit")
        while client.connected:
            cmd = input()
            if cmd.lower() == 'q':
                break

            # ランダムな位置とサイズでキューブを作成
            position = (
                random.uniform(-5, 5),
                random.uniform(-5, 5),
                random.uniform(5, 10)
            )
            size = (
                random.uniform(0.5, 2),
                random.uniform(0.5, 2),
                random.uniform(0.5, 2)
            )
            
            print(f"Creating cube at {position} with size {size}")
            if await client.create_cube(position, size):
                print("Cube created successfully")
            else:
                print("Failed to create cube")

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await client.close()
        if 'receive_task' in locals():
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass

if __name__ == '__main__':
    asyncio.run(main()) 