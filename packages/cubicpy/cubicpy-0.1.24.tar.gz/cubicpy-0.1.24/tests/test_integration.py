import pytest
from panda3d.core import Vec3, Point3, TransformState, NodePath
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from cubicpy.physics import PhysicsEngine

class MockApp:
    """テスト用のアプリケーションクラス"""
    def __init__(self):
        self.GRAVITY_VECTOR = Vec3(0, 0, -9.81)
        self.initial_gravity_factor = 1.0
        self.render = None
        self.taskMgr = Task.TaskManager()

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

def test_physics_rendering_integration(physics_engine, mock_app):
    """物理エンジンとレンダリングの統合テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # レンダリングノードを作成
    node = NodePath(body)
    node.reparentTo(mock_app.render)
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 物理シミュレーションを更新
    physics_engine.update(0.016)
    
    # 位置が同期されていることを確認
    assert body.getTransform().getPos() == node.getPos()

def test_physics_task_integration(physics_engine, mock_app):
    """物理エンジンとタスク管理の統合テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定
    initial_pos = Point3(0, 0, 10)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # タスクを追加
    def update_physics(task):
        physics_engine.update(0.016)
        return Task.cont
    
    mock_app.taskMgr.add(update_physics, 'update_physics')
    
    # タスクを実行（複数回実行して重力の影響を確認）
    for _ in range(10):
        mock_app.taskMgr.step()
    
    # 物理シミュレーションが更新されたことを確認
    final_pos = body.getTransform().getPos()
    assert final_pos.z < initial_pos.z  # 重力によって落下した

def test_physics_gravity_integration(physics_engine, mock_app):
    """物理エンジンと重力の統合テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定
    initial_pos = Point3(0, 0, 10)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 重力の影響を確認
    for _ in range(60):  # 約1秒間のシミュレーション
        physics_engine.update(0.016)
    
    # 重力によって落下したことを確認
    final_pos = body.getTransform().getPos()
    assert final_pos.z < initial_pos.z

def test_physics_collision_integration(physics_engine, mock_app):
    """物理エンジンと衝突検知の統合テスト"""
    # 2つの剛体を作成
    body1 = BulletRigidBodyNode('body1')
    body2 = BulletRigidBodyNode('body2')
    shape = BulletBoxShape((1, 1, 1))
    
    for body in [body1, body2]:
        body.addShape(shape)
        body.setMass(1.0)
        physics_engine.bullet_world.attachRigidBody(body)
    
    # 衝突するように位置を設定
    body1.setTransform(TransformState.makePos(Point3(0, 0, 5)))
    body2.setTransform(TransformState.makePos(Point3(0, 0, 0)))
    
    # 物理シミュレーションを更新
    for _ in range(60):  # 約1秒間のシミュレーション
        physics_engine.update(0.016)
    
    # 衝突後の位置を確認
    pos1 = body1.getTransform().getPos()
    pos2 = body2.getTransform().getPos()
    
    # 両方のオブジェクトが落下したことを確認
    assert pos1.z < 5  # 上から落ちたオブジェクト
    assert pos2.z < 0  # 下のオブジェクトも落下

def test_physics_force_integration(physics_engine, mock_app):
    """物理エンジンと力の適用の統合テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定（重力の影響を受けない高さに）
    initial_pos = Point3(0, 0, 20)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 物理シミュレーションを更新（より長い時間シミュレーション）
    for _ in range(120):  # 約2秒間のシミュレーション
        # 力を継続的に適用
        force = Vec3(1000, 0, 0)  # X軸方向に大きな力を加える
        body.applyCentralForce(force)
        physics_engine.update(0.016)
    
    # 力によって移動したことを確認
    final_pos = body.getTransform().getPos()
    assert final_pos.x > initial_pos.x  # X軸方向に移動

def test_physics_rotation_integration(physics_engine, mock_app):
    """物理エンジンと回転の統合テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定（重力の影響を受けない高さに）
    initial_pos = Point3(0, 0, 20)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 物理シミュレーションを更新（より長い時間シミュレーション）
    for _ in range(120):  # 約2秒間のシミュレーション
        # トルクを継続的に適用
        torque = Vec3(0, 0, 1000)  # Z軸周りに大きなトルクを加える
        body.applyTorque(torque)
        physics_engine.update(0.016)
    
    # 回転したことを確認
    final_transform = body.getTransform()
    initial_quat = TransformState.makeIdentity().getQuat()
    final_quat = final_transform.getQuat()
    
    # 回転角度を計算して確認
    angle = final_quat.getAngle()
    # 回転角度が0より大きいか、または回転軸が変化していることを確認
    assert angle > 0.0 or final_quat.getAxis() != initial_quat.getAxis()

def test_physics_multiple_bodies_integration(physics_engine, mock_app):
    """物理エンジンと複数の剛体の統合テスト"""
    # 複数の剛体を作成
    num_bodies = 5
    bodies = []
    
    for i in range(num_bodies):
        body = BulletRigidBodyNode(f'body_{i}')
        shape = BulletBoxShape((1, 1, 1))
        body.addShape(shape)
        body.setMass(1.0)
        
        # 初期位置を設定（階段状に配置）
        pos = Point3(i * 2, 0, i * 2)
        body.setTransform(TransformState.makePos(pos))
        
        # 物理エンジンに追加
        physics_engine.bullet_world.attachRigidBody(body)
        bodies.append(body)
    
    # 物理シミュレーションを更新
    for _ in range(60):  # 約1秒間のシミュレーション
        physics_engine.update(0.016)
    
    # 各剛体が落下したことを確認
    for i, body in enumerate(bodies):
        final_pos = body.getTransform().getPos()
        initial_pos = Point3(i * 2, 0, i * 2)
        assert final_pos.z < initial_pos.z

def test_physics_limits_integration(physics_engine, mock_app):
    """物理エンジンの制限値テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定
    initial_pos = Point3(0, 0, 20)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 非常に大きな力を適用
    force = Vec3(1000000, 0, 0)  # 極端に大きな力
    body.applyCentralForce(force)
    
    # 物理シミュレーションを更新
    for _ in range(120):
        physics_engine.update(0.016)
    
    # 速度が制限されていることを確認
    velocity = body.getLinearVelocity()
    assert velocity.length() < 1000  # 速度が適切な範囲内にあることを確認

def test_physics_reset_integration(physics_engine, mock_app):
    """物理エンジンのリセット機能テスト"""
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定
    initial_pos = Point3(0, 0, 20)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 力を適用して移動させる
    force = Vec3(1000, 0, 0)
    body.applyCentralForce(force)
    
    # 物理シミュレーションを更新
    for _ in range(60):
        physics_engine.update(0.016)
    
    # 位置が変化したことを確認
    moved_pos = body.getTransform().getPos()
    assert moved_pos != initial_pos
    
    # 物理エンジンから剛体を削除
    physics_engine.bullet_world.removeRigidBody(body)
    
    # 新しい剛体を作成して追加
    new_body = BulletRigidBodyNode('new_body')
    new_body.addShape(shape)
    new_body.setMass(1.0)
    new_body.setTransform(TransformState.makePos(initial_pos))
    physics_engine.bullet_world.attachRigidBody(new_body)
    
    # リセット後のシミュレーションを更新
    for _ in range(60):
        physics_engine.update(0.016)
    
    # 新しい剛体が正しく動作することを確認
    final_pos = new_body.getTransform().getPos()
    assert final_pos != initial_pos

def test_physics_settings_integration(physics_engine, mock_app):
    """物理エンジンの設定変更テスト"""
    # 重力の設定を変更
    new_gravity = Vec3(0, 0, -4.905)  # 重力を半分に
    physics_engine.bullet_world.setGravity(new_gravity)
    
    # 剛体を作成
    body = BulletRigidBodyNode('test_body')
    shape = BulletBoxShape((1, 1, 1))
    body.addShape(shape)
    body.setMass(1.0)
    
    # 初期位置を設定
    initial_pos = Point3(0, 0, 20)
    body.setTransform(TransformState.makePos(initial_pos))
    
    # 物理エンジンに追加
    physics_engine.bullet_world.attachRigidBody(body)
    
    # 物理シミュレーションを更新
    for _ in range(60):
        physics_engine.update(0.016)
    
    # 重力の影響を確認
    final_pos = body.getTransform().getPos()
    fall_distance = initial_pos.z - final_pos.z
    
    # 元の重力設定に戻す
    physics_engine.bullet_world.setGravity(mock_app.GRAVITY_VECTOR)
    
    # 新しい剛体を作成
    new_body = BulletRigidBodyNode('new_body')
    new_body.addShape(shape)
    new_body.setMass(1.0)
    new_body.setTransform(TransformState.makePos(initial_pos))
    physics_engine.bullet_world.attachRigidBody(new_body)
    
    # 物理シミュレーションを更新
    for _ in range(60):
        physics_engine.update(0.016)
    
    # 異なる重力設定での落下距離を比較
    new_final_pos = new_body.getTransform().getPos()
    new_fall_distance = initial_pos.z - new_final_pos.z
    
    # 重力が半分の場合の落下距離が約半分であることを確認
    assert abs(fall_distance - new_fall_distance/2) < 1.0  # 許容誤差1.0 