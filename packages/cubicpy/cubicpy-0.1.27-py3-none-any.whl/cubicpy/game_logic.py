import threading
import time


class GameLogic:
    """ゲームのロジックを管理するクラス"""

    def __init__(self, app):
        """ゲームロジックの初期化"""
        self.app = app
        self.running = False
        self.thread = None
        self.score = 0
        self.last_update_time = 0
        self.target_type = 'cube'  # デフォルトのターゲットタイプ
        self.tolerance = 0.1  # 動いたとみなす閾値
        self.angle_tolerance = 45
        self.motion_state = 'moved'  # 'moved' or 'fallen'  # 動いたか倒れたかを選ぶ

    def start(self):
        """ゲームロジックのスレッドを開始"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """ゲームロジックのスレッドを停止"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None

    def get_motion_count(self):
        """倒れたピンの数を取得"""
        try:
            count = 0
            max_score = 0
            for obj in self.app.world_manager.body_objects:
                if obj['type'] == self.target_type:
                    # スコアの最大値を更新
                    max_score += 1

                    # オブジェクトが動いたかチェック
                    if self.motion_state == 'moved':
                        # 初期位置と現在位置を比較
                        initial_pos = obj['object'].node_pos
                        current_pos = obj['object'].model_node.getPos()

                        # 位置の差を計算
                        dx = abs(current_pos.x - initial_pos.x)
                        dy = abs(current_pos.y - initial_pos.y)

                        # 閾値以上に動いたら倒れたと判断
                        if dx > self.tolerance or dy > self.tolerance:
                            count += 1
                    elif self.motion_state == 'fallen':
                        # 初期位置と現在位置を比較
                        initial_hpr = obj['object'].node_hpr
                        current_hpr = obj['object'].model_node.getHpr()
                        # 各軸の傾き

                        # 向きの差を計算 (x=heading, y=pitch, z=roll)
                        dh = abs(current_hpr.x - initial_hpr.x) % 360
                        dp = abs(current_hpr.y - initial_hpr.y) % 360
                        dr = abs(current_hpr.z - initial_hpr.z) % 360

                        # 180度を超える場合は小さい方の角度を使用
                        if dh > 180: dh = 360 - dh
                        if dp > 180: dp = 360 - dp
                        if dr > 180: dr = 360 - dr

                        # いずれかの角度が閾値を超えたら倒れたと判断
                        if dp > self.angle_tolerance or dr > self.angle_tolerance:
                            count += 1

            return count, max_score
        except Exception as e:
            print(f"エラー: {e}")
            return 0

    def update_score_display(self):
        """スコア表示を更新"""
        current_score, max_score = self.get_motion_count()

        # スコアの最大値が0のときはチェック対象がないので何もしない
        if max_score == 0:
            return

        # スコアが最大値を超えた場合は最大値に設定
        if current_score == max_score:
            self.app.set_bottom_left_text(f"Game Clear")
        # スコアが変わった場合のみ更新
        elif current_score != self.score:
            self.score = current_score
            self.app.set_bottom_left_text(f"Score: {self.score}")

    def _run(self):
        """内部スレッドの実行関数"""
        while self.running:
            try:
                # 現在の時刻を取得（スコア更新の間隔調整用）
                current_time = time.time()

                # 一定間隔でスコア更新（負荷軽減のため）
                if current_time - self.last_update_time > 0.2:  # 0.2秒間隔
                    self.update_score_display()
                    self.last_update_time = current_time

                time.sleep(0.05)  # 短い待機時間でCPU負荷を抑える

            except Exception as e:
                print(f"ゲームロジック実行中にエラー: {e}")
                time.sleep(1)  # エラー時は長めに待機