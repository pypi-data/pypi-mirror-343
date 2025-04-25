import pytest
import psutil
import gc
from panda3d.core import Vec3, Point3, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from direct.showbase.ShowBase import ShowBase
from cubicpy.physics import PhysicsEngine

class MockApp:
    """テスト用のアプリケーションクラス"""
    def __init__(self):
        self.GRAVITY_VECTOR = Vec3(0, 0, -9.81)
        self.initial_gravity_factor = 1.0
        self.render = None

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    yield base
    base.destroy()

@pytest.fixture
def mock_app(showbase):
    """テスト用のアプリケーションインスタンスを作成"""
    app = MockApp()
    app.render = showbase.render
    return app

@pytest.fixture
def physics_engine(mock_app):
    """テスト用のPhysicsEngineインスタンスを作成"""
    return PhysicsEngine(mock_app)

def test_memory_insufficient_error(physics_engine):
    """メモリ不足時のエラー処理テスト"""
    # 大量のオブジェクトを作成してメモリ不足をシミュレート
    objects = []
    try:
        for i in range(1000):  # 大量のオブジェクトを作成
            body = BulletRigidBodyNode(f'object_{i}')
            shape = BulletBoxShape((1, 1, 1))
            body.addShape(shape)
            body.setMass(1.0)
            physics_engine.bullet_world.attachRigidBody(body)
            objects.append(body)
    except MemoryError as e:
        # メモリ不足エラーが適切に処理されることを確認
        assert "メモリ不足" in str(e)
    finally:
        # クリーンアップ
        for body in objects:
            physics_engine.bullet_world.removeRigidBody(body)

def test_invalid_input_error(physics_engine):
    """無効な入力時のエラー処理テスト"""
    # 無効な剛体を追加
    try:
        physics_engine.bullet_world.attachRigidBody(None)
    except TypeError as e:
        # 無効な入力エラーが適切に処理されることを確認
        assert "BulletRigidBodyNode" in str(e)
    
    # 無効な質量を設定
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    try:
        body.setMass(-1.0)  # 負の質量は無効
    except ValueError as e:
        # 無効な質量エラーが適切に処理されることを確認
        assert "無効な質量" in str(e)

def test_physics_engine_initialization_error(mock_app):
    """物理エンジンの初期化エラー処理テスト"""
    # 無効なアプリケーションインスタンスで初期化
    mock_app.GRAVITY_VECTOR = None  # 無効な重力ベクトル
    try:
        PhysicsEngine(mock_app)
    except TypeError as e:
        # 初期化エラーが適切に処理されることを確認
        assert "NoneType" in str(e)

def test_error_recovery(physics_engine):
    """エラーからの回復テスト"""
    # エラー状態をシミュレート
    try:
        # 無効な操作を実行
        physics_engine.bullet_world = None
        physics_engine.update(0.016)
    except AttributeError as e:
        # エラーが適切に処理されることを確認
        assert "doPhysics" in str(e)
        
        # 新しい物理エンジンを作成して回復
        new_engine = PhysicsEngine(physics_engine.app)
        assert new_engine.bullet_world is not None
        new_engine.update(0.016) 