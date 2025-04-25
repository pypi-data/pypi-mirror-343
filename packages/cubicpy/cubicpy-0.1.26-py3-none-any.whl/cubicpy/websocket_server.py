import asyncio
import websockets
import json
import logging
import threading
from panda3d.core import Vec3
import argparse
import random
import numpy as np
from scipy.spatial.transform import Rotation as R

def convert_hpr_from_A_to_B(h, p, r):
    # オイラー角 (Z-X-Y順) → 回転行列（座標系A）
    # NOTE: rotate_hpr expects angles in degrees
    rot_a = R.from_euler('zxy', [h, p, r], degrees=True)
    R_a = rot_a.as_matrix()

    # 座標変換行列（座標系A → B）
    M = np.array([
        [1, 0,  0],
        [0, 0,  1],
        [0, -1, 0]
    ])
    
    # 相似変換で座標系Bにおける回転行列を得る
    R_b = M @ R_a @ M.T
    
    # 座標系Bでの回転行列 → オイラー角（ZXY順）
    rot_b = R.from_matrix(R_b)
    h_b, p_b, r_b = rot_b.as_euler('zxy', degrees=True)
    
    return h_b, p_b, r_b

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class WebSocketServer:
    def __init__(self, app, host="websocket.voxelamming.com", room=None):
        self.app = app
        # ローカルホストの場合はws://を使用
        protocol = "wss://" if host != "localhost" else f"ws://{host}:8765"
        self.relay_uri = f"{protocol}{host}"
        self.room = room or str(random.randint(1000, 9999))
        self.logger = logging.getLogger(__name__)
        self.websocket = None
        self.logger.debug(f"WebSocketServer initialized for {self.relay_uri}")

    async def connect(self):
        """リレーサーバーに接続"""
        try:
            # SSL検証を無効化（ローカルテスト用）
            ssl_context = None if "localhost" in self.relay_uri else True
            self.websocket = await websockets.connect(
                self.relay_uri,
                ssl=ssl_context,
                open_timeout=30,  # タイムアウト時間を30秒に延長
                close_timeout=10,
                ping_interval=20,
                ping_timeout=20
            )
            self.logger.info(f"Connected to relay server at {self.relay_uri}")
            
            # ルーム名を送信
            await self.websocket.send(self.room)
            self.logger.debug(f"Sent room name: {self.room}")
            print(f"\nルーム番号を生成しました: {self.room}")
            print(f"このルーム番号をクライアントに伝えてください")
            self.app.set_top_left_text(f"Room: {self.room}")

            # メッセージの受信ループ
            while True:
                try:
                    message = await self.websocket.recv()
                    self.logger.debug(f"Received message: {message}")
                    data = json.loads(message)
                    self.logger.info(f"Received data: {data}")

                    # メッセージを処理
                    print(data)
                    if data["boxes"]:
                        size = data["size"]
                        shape = data["shape"]
                        object_type = shape if shape == "sphere" else "cube"

                        if shape == "plane":
                            scale = (size, size, size * 0.001)
                        else:
                            scale = (size, size, size)
                        
                        if data["nodeTransform"]:
                            x, y, z, h, p, r = data["nodeTransform"]
                            self.app.transform_manager.push_matrix()
                            self.app.transform_manager.translate(*(Vec3(x, -z, y) * size))  # 座標変換
                            h_b, p_b, r_b = convert_hpr_from_A_to_B(h, p, r)  # 座標変換
                            self.app.transform_manager.rotate_hpr(h_b, p_b, r_b)  # 座標変換

                        for box in data["boxes"]:
                            print(box)
                            x, y, z, r, g, b, alpha, texture = box
                            # キューブを配置
                            object_data = {
                                'position': Vec3(x, -z, y) * size,  # 座標変換
                                'scale': scale,
                                'color': Vec3(r, g, b),
                                'color_alpha': alpha
                            }
                            self.app.api.add(object_type, **object_data)
                        
                        if data["nodeTransform"]:
                            self.app.transform_manager.pop_matrix()

                        # ワールドを再生成
                        self.app.reset_all()
                        
                        response = 'オブジェクトの配置が完了しました'
                        await self.websocket.send(response)
                        self.logger.info(f"Processed cube placement: {response}")
                        print(response)

                except json.JSONDecodeError as e:
                    self.logger.error(f"Invalid JSON message: {message}")
                except websockets.exceptions.ConnectionClosed:
                    self.logger.info("Connection closed by client")
                    break
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")
                    break

        except websockets.exceptions.ConnectionClosed:
            self.logger.info("Disconnected from relay server")
            print("リレーサーバーから切断されました")
        except websockets.exceptions.InvalidStatusCode as e:
            self.logger.error(f"Invalid status code: {e.status_code}")
            print(f"サーバー接続エラー: ステータスコード {e.status_code}")
        except websockets.exceptions.InvalidHandshake:
            self.logger.error("Invalid handshake")
            print("サーバーとのハンドシェイクに失敗しました")
        except TimeoutError:
            self.logger.error("Connection timeout")
            print("サーバーへの接続がタイムアウトしました。以下の点を確認してください：")
            print("1. サーバーが起動しているか")
            print("2. ホスト名とポート番号が正しいか")
            print("3. ファイアウォールの設定")
        except Exception as e:
            self.logger.error(f"Error in connect: {e}")
            print(f"予期せぬエラーが発生しました: {e}")
            raise

    async def close(self):
        """接続を閉じる"""
        if self.websocket:
            await self.websocket.close()
            self.logger.info("Connection closed")

    def start(self):
        """サーバーを開始"""
        self.logger.info(f"Starting WebSocket server for room {self.room}")
        asyncio.run(self.connect())

    def run_in_thread(self):
        """別スレッドでサーバーを実行"""
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()
        return thread
            
async def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="WebSocket server test")
    parser.add_argument("--host", default="websocket.voxelamming.com", 
                       help="Relay server host (without https:// or http://)")
    args = parser.parse_args()

    # 物理エンジンはテスト用にNoneを渡す
    server = WebSocketServer(None, args.host)
    
    try:
        print('サーバーを起動します')
        await server.connect()
    except KeyboardInterrupt:
        print("\n終了します...")
    finally:
        await server.close()

if __name__ == "__main__":
    asyncio.run(main()) 