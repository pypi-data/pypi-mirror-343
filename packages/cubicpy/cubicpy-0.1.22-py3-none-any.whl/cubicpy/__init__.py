# CubicPy パッケージの初期化

__version__ = '0.1.22'

# デフォルト設定
DEFAULT_GRAVITY_FACTOR = 1.0

# 位置計算用関数
from .base_point import BasePoint, get_position_offset

# メインクラス（循環参照を回避するために遅延インポート）
from .camera import CameraControl
from .axis import Axis
from .geom_utils import *
from .safe_exec import SafeExec
from .input_handler import InputHandler
from .model_manager import ModelManager
from .physics import PhysicsEngine
from .transform import TransformManager
from .api_method import ApiMethod
from .draw_text import Draw2DText, Draw3DText

# オブジェクトクラス
from .cube import Cube
from .sphere import Sphere
from .cylinder import Cylinder
from .safe_exec import SafeExec

# ワールド管理
from .world_manager import WorldManager

# ゲームロジック
from .game_logic import GameLogic

# メインアプリケーション
from .app import CubicPyApp

# サンプル関連機能をエクスポート
from .examples import get_sample_path, list_samples


# 簡単にサンプルを実行するための補助関数
def run_sample(sample_name, gravity_factor=DEFAULT_GRAVITY_FACTOR):
    """指定したサンプルを実行する

    Args:
        sample_name: サンプル名（.pyなしのファイル名）
        gravity_factor: 重力係数
    """
    app = CubicPyApp(get_sample_path(sample_name), gravity_factor=gravity_factor)
    app.run()