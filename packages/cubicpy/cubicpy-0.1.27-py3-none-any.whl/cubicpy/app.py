from pkg_resources import resource_filename
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from . import (
    DEFAULT_GRAVITY_FACTOR,
    CameraControl, Axis, InputHandler,
    ModelManager, PhysicsEngine, WorldManager,
    ApiMethod, Draw2DText, TransformManager, GameLogic
)


class CubicPyApp(ShowBase):
    """CubicPy アプリケーションのメインクラス"""
    GRAVITY_VECTOR = Vec3(0, 0, -9.81) * (10 ** -1)  # 重力ベクトル（10の1に補正）
    DEFAULT_WINDOW_SIZE = (900, 600)
    RESTITUTION = 0.5  # 反発係数
    FRICTION = 0.5  # 摩擦係数

    def __init__(self, code_file=None, gravity_factor=DEFAULT_GRAVITY_FACTOR, window_size=DEFAULT_WINDOW_SIZE,
                 camera_lens='perspective', restitution=RESTITUTION, friction=FRICTION):
        ShowBase.__init__(self)
        self.code_file = code_file
        self.initial_gravity_factor = gravity_factor
        self.window_size = window_size
        self.camera_lens = camera_lens
        self.custom_key_handler = None
        self.restitution = restitution
        self.friction = friction

        # ウィンドウ設定
        self.setup_window("CubicPy World", self.window_size)

        # カメラと座標軸
        CameraControl(self)
        Axis(self)

        # 各サブシステムの初期化
        self.model_manager = ModelManager(self)
        self.physics = PhysicsEngine(self)

        # ワールド管理システムの初期化
        self.world_manager = WorldManager(self)

        # 座標変換マネージャーの初期化
        self.transform_manager = TransformManager(self)

        # APIメソッドの初期化（オブジェクト配置用）
        self.api = ApiMethod(self)

        # APIに座標変換マネージャーへの参照を設定
        self.api.transform_manager = self.transform_manager

        # 入力ハンドラの設定
        self.input_handler = InputHandler(self)

        # ゲームロジックの初期化
        self.game_logic = GameLogic(self)

        # 物理シミュレーションタスクの開始
        self.taskMgr.add(self.update_physics, 'update_physics')

        # テキスト表示
        # フォントパスを取得
        font_path = resource_filename('cubicpy', 'font/PixelMplus10-Regular.ttf')

        # フォントローダーを使用してファイルからフォントを読み込む
        self.font = self.loader.loadFont(font_path)

        # アプリ情報をテキスト表示
        self.top_left_text = Draw2DText(self.font, self.a2dTopLeft, '')
        self.bottom_left_text = Draw2DText(self.font, self.a2dBottomLeft, '', pos=(0.05, 0.1))
        self.space_button_text = Draw2DText(self.font, self.a2dTopRight, 'Space', pos=(-0.3, -1.0), fg=(1, 0, 0, 1),
                                            frame=(1, 0, 0, 1))
        self.space_button_text.hide()
        self.x_button_text = Draw2DText(self.font, self.a2dTopRight, 'x', pos=(-0.4, -1.0), fg=(1, 0, 0, 1),
                                        frame=(1, 0, 0, 1))
        self.x_button_text.hide()

        # コードファイルが指定されていれば、ワールド構築
        if code_file:
            self.world_manager.build_world()

    def setup_window(self, title, size):
        """ウィンドウ設定"""
        props = WindowProperties()
        props.setTitle(title)
        props.setSize(*size)
        self.win.requestProperties(props)

    def update_physics(self, task):
        """物理シミュレーションの更新"""
        dt = globalClock.getDt()
        self.physics.update(dt)
        return task.cont

    # カスタムキーハンドラの設定メソッド
    def set_key_handler(self, handler):
        """カスタムキーハンドラを設定"""
        self.custom_key_handler = handler

        # InputHandlerクラスのカスタムハンドラ設定メソッドを使用
        if hasattr(self.input_handler, 'set_custom_handler'):
            self.input_handler.set_custom_handler(handler)
        else:
            # フォールバック: InputHandlerが対応していない場合
            print("Warning: InputHandler does not support custom handlers. Some functionality may be limited.")

            # 基本的なキーをバインド
            for key in "abcdefghijklmnopqrstuvwxyz":
                self.accept(key, lambda k=key: handler(k))

            # 特殊キー
            self.accept("space", lambda: handler("space"))

    # ApiMethodクラスのメソッドを統合
    def add_cube(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, hpr=(0, 0, 0),
                 base_point=0, remove=False, velocity=(0, 0, 0)):
        """箱を追加"""
        return self.api.add_cube(position, scale, color, mass, color_alpha, hpr, base_point, remove, velocity)

    def add_sphere(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1,
                   hpr=(0, 0, 0),
                   base_point=0, remove=False, velocity=(0, 0, 0)):
        """球を追加"""
        return self.api.add_sphere(position, scale, color, mass, color_alpha, hpr, base_point, remove, velocity)

    def add_cylinder(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1,
                     hpr=(0, 0, 0),
                     base_point=0, remove=False, velocity=(0, 0, 0)):
        """円柱を追加"""
        return self.api.add_cylinder(position, scale, color, mass, color_alpha, hpr, base_point, remove, velocity)

    def add_ground(self, color=(0, 1, 0), color_alpha=0.3):
        """地面を追加"""
        return self.api.add_ground(color, color_alpha)

    def add(self, obj_type, **kwargs):
        """汎用オブジェクト追加"""
        return self.api.add(obj_type, **kwargs)

    def from_body_data(self, body_data):
        """オブジェクトデータからボディを構築"""
        self.api.from_body_data(body_data)

    # 座標変換関連メソッド
    def push_matrix(self):
        """現在の変換状態をスタックに保存"""
        return self.api.push_matrix()

    def pop_matrix(self):
        """スタックから変換状態を復元"""
        return self.api.pop_matrix()

    def translate(self, x, y, z):
        """指定した位置に移動"""
        return self.api.translate(x, y, z)

    def rotate_hpr(self, h, p, r):
        """HPR（Heading-Pitch-Roll）で回転"""
        return self.api.rotate_hpr(h, p, r)

    def reset_matrix(self):
        """変換をリセット"""
        return self.api.reset_matrix()

    # WorldManagerクラスのメソッドを統合
    def reset(self):
        """オブジェクトをリセット"""
        # ワールドを再構築
        self.world_manager.rebuild_from_api_data()

    def tilt_ground(self, dx, dy):
        self.world_manager.tilt_ground(dx, dy)

    # PhysicsEngineクラスのメソッドを統合
    def toggle_debug(self):
        self.physics.toggle_debug()

    def change_gravity(self, value):
        # 物理エンジンの重力を変更
        self.physics.change_gravity(value)
        # そしてワールドを再構築  # この行は削除すると、地面を傾けても崩壊しない
        self.world_manager.rebuild()

    # Draw2DTextクラスのメソッドを統合
    def set_top_left_text(self, display_text):
        self.top_left_text.setText(display_text)

    def set_bottom_left_text(self, display_text):
        self.bottom_left_text.setText(display_text)

    # ワールドのリセット
    def reset_all(self):
        """すべてをリセット"""
        self.physics.reset_gravity()
        self.world_manager.reset_rotation()
        self.world_manager.rebuild()

    # メソッドをオーバーライド
    def run(self, key_handler=None):
        """
        世界を構築して実行

        Args:
            key_handler (function, optional): キー入力時に呼び出されるコールバック関数
        """
        if key_handler:
            self.set_key_handler(key_handler)

        if self.code_file is None:
            # APIからのオブジェクトデータでワールドを構築
            self.world_manager.build_from_api_data()

        # アプリを実行
        super().run()

    # 選択したオブジェクトを削除
    def remove_selected(self):
        self.world_manager.remove_selected()

    # 選択したオブジェクトを発射
    def launch_objects(self):
        """初速度ベクトルが設定されたオブジェクトを発射"""
        self.world_manager.launch_objects()

    @property
    def world_node(self):
        """ワールドノードへの参照を提供"""
        return self.world_manager.get_world_node()