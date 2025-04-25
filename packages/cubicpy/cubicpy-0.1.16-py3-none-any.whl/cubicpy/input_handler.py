import sys


class InputHandler:
    """キー入力処理クラス"""

    def __init__(self, app):
        self.app = app
        self.custom_handler = None

        # キー入力の登録
        self.setup_keys()

    def setup_keys(self):
        """キー入力の設定"""
        self.app.accept('escape', sys.exit)
        # デバッグ表示の切り替え
        self.app.accept('z', self.app.toggle_debug)
        # 重力の変更
        self.app.accept('f', self.app.change_gravity, [0.1])
        self.app.accept('g', self.app.change_gravity, [10])
        # ワールドのリセット
        self.app.accept('r', self.handle_key_with_custom, ['r'])
        # 地面の傾き
        self.app.accept("w", self.handle_key_with_custom, ['w', -1, 0])  # X軸 (前傾)
        self.app.accept("s", self.handle_key_with_custom, ['s', 1, 0])  # X軸 (後傾)
        self.app.accept("a", self.handle_key_with_custom, ['a', 0, -1])  # Y軸 (左傾)
        self.app.accept("d", self.handle_key_with_custom, ['d', 0, 1])  # Y軸 (右傾)
        # オブジェクトの削除
        self.app.accept('x', self.handle_key_with_custom, ['x'])
        # オブジェクトの発射
        self.app.accept('space', self.handle_key_with_custom, ['space'])

        # その他の一般的なキー（アルファベット）
        for key in "abcdefghijklmnopqrstuvwxyz":
            if key not in "wasdrzfgx":  # 既に登録済みのキーは除外
                self.app.accept(key, self.handle_key_with_custom, [key])

    def set_custom_handler(self, handler):
        """カスタムキーハンドラを設定"""
        self.custom_handler = handler

    def handle_key_with_custom(self, key, *args):
        """
        標準の処理とカスタムハンドラの両方を実行

        Args:
            key (str): 押されたキー
            *args: 追加の引数（地面の傾きなど）
        """
        # 標準のキー処理を実行
        if key == 'r':
            self.app.reset_all()
        elif key == 'w' and len(args) >= 2:
            self.app.tilt_ground(args[0], args[1])
        elif key == 's' and len(args) >= 2:
            self.app.tilt_ground(args[0], args[1])
        elif key == 'a' and len(args) >= 2:
            self.app.tilt_ground(args[0], args[1])
        elif key == 'd' and len(args) >= 2:
            self.app.tilt_ground(args[0], args[1])
        elif key == 'x':
            self.app.remove_selected()
        elif key == 'space':
            self.app.launch_objects()

        # カスタムハンドラがあれば実行
        if self.custom_handler:
            self.custom_handler(key)