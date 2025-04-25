import pytest
import time
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

def get_memory_usage():
    """現在のメモリ使用量を取得（MB単位）"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

def force_garbage_collection():
    """ガベージコレクションを強制的に実行"""
    gc.collect()
    gc.collect()  # 2回実行して確実に

def test_physics_performance(physics_engine):
    """物理エンジンのパフォーマンステスト
    
    このテストは以下の点を確認します：
    1. 物理シミュレーションのパフォーマンス（FPS）
    2. オブジェクト生成時のメモリ使用量
    3. シミュレーション中のメモリ使用量の増加が許容範囲内か
    
    注意: Panda3DのBullet物理エンジンはシミュレーション中に一時的に
    大量のメモリを消費することがあります。これはライブラリの特性上
    正常な動作です。
    """
    # テストパラメータ
    num_objects = 25
    test_duration = 1.0
    min_fps = 30
    target_fps = 60
    dt = 1.0 / target_fps
    max_memory_increase = 500  # 許容する最大メモリ増加量（MB）
    
    # 初期メモリ使用量を記録
    force_garbage_collection()
    initial_memory = get_memory_usage()
    print(f"初期メモリ使用量: {initial_memory:.2f}MB")
    
    # 物理オブジェクトの生成
    objects = []
    
    try:
        # オブジェクト生成時のメモリ使用量を記録
        start_memory = get_memory_usage()
        
        # 形状を再利用
        shared_shape = BulletBoxShape((1, 1, 1))
        
        for i in range(num_objects):
            # 物理オブジェクトを作成
            body = BulletRigidBodyNode(f'object_{i}')
            body.addShape(shared_shape)
            body.setMass(1.0)
            
            # 物理エンジンに追加
            physics_engine.bullet_world.attachRigidBody(body)
            objects.append(body)
        
        # オブジェクト生成後のメモリ使用量を記録
        end_memory = get_memory_usage()
        memory_increase = end_memory - start_memory
        print(f"オブジェクト生成後のメモリ増加量: {memory_increase:.2f}MB")
        
        # メモリ増加量が許容範囲内か確認
        assert memory_increase < max_memory_increase, \
            f"メモリ増加量が許容範囲を超えています: {memory_increase:.2f}MB > {max_memory_increase}MB"
        
        # 物理シミュレーションの実行
        start_time = time.time()
        elapsed_time = 0
        frame_count = 0
        
        while elapsed_time < test_duration:
            # 物理シミュレーションを更新
            physics_engine.update(dt)
            
            # フレームカウントを更新
            frame_count += 1
            elapsed_time = time.time() - start_time
        
        # FPSを計算
        fps = frame_count / elapsed_time
        print(f"平均FPS: {fps:.2f}")
        
        # FPSが目標値を満たしているか確認
        assert fps >= min_fps, f"FPSが目標値を下回っています: {fps:.2f} < {min_fps}"
        
    finally:
        # クリーンアップ
        for body in objects:
            physics_engine.bullet_world.removeRigidBody(body)
        
        # 最終メモリ使用量を記録
        force_garbage_collection()
        final_memory = get_memory_usage()
        memory_leak = final_memory - initial_memory
        print(f"メモリリーク: {memory_leak:.2f}MB")
        
        # メモリリークが許容範囲内か確認
        assert memory_leak < max_memory_increase, \
            f"メモリリークが許容範囲を超えています: {memory_leak:.2f}MB > {max_memory_increase}MB" 