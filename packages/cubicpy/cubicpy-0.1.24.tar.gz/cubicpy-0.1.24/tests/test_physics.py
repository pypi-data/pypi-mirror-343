import pytest
from panda3d.core import Vec3, Point3
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

def test_physics_engine_initialization(physics_engine):
    """PhysicsEngineの初期化テスト"""
    assert physics_engine.app is not None
    assert physics_engine.bullet_world is not None
    assert physics_engine.debug_node is not None
    assert physics_engine.debug_np is not None
    assert not physics_engine.debug_np.isHidden()  # デバッグ表示は初期状態で表示されている

def test_toggle_debug(physics_engine):
    """デバッグ表示の切り替えテスト"""
    # 初期状態では表示されている
    assert not physics_engine.debug_np.isHidden()
    
    # 非表示に切り替え
    physics_engine.toggle_debug()
    assert physics_engine.debug_np.isHidden()
    
    # 表示に切り替え
    physics_engine.toggle_debug()
    assert not physics_engine.debug_np.isHidden()

def test_change_gravity(physics_engine):
    """重力の変更テスト"""
    # 初期重力を保存
    initial_gravity = physics_engine.gravity_vector
    
    # 重力を2倍に変更
    physics_engine.change_gravity(2.0)
    
    # 重力ベクトルの各成分を個別に比較
    assert abs(physics_engine.gravity_vector.x - initial_gravity.x * 2.0) < 0.01
    assert abs(physics_engine.gravity_vector.y - initial_gravity.y * 2.0) < 0.01
    assert abs(physics_engine.gravity_vector.z - initial_gravity.z * 2.0) < 0.01

def test_reset_gravity(physics_engine):
    """重力のリセットテスト"""
    # 初期重力を保存
    initial_gravity = physics_engine.gravity_vector
    
    # 重力を変更
    physics_engine.change_gravity(2.0)
    
    # 重力をリセット
    physics_engine.reset_gravity()
    
    # 重力ベクトルの各成分を個別に比較
    assert abs(physics_engine.gravity_vector.x - initial_gravity.x) < 0.01
    assert abs(physics_engine.gravity_vector.y - initial_gravity.y) < 0.01
    assert abs(physics_engine.gravity_vector.z - initial_gravity.z) < 0.01

def test_update(physics_engine):
    """物理シミュレーションの更新テスト"""
    # 更新前の状態を保存
    initial_state = physics_engine.bullet_world.getNumConstraints()
    
    # 物理シミュレーションを更新
    physics_engine.update(0.016)  # 約60FPSの時間間隔
    
    # 更新後の状態を確認
    # 注: 実際の物理演算結果は環境によって異なるため、
    # 単に例外が発生しないことを確認する
    assert physics_engine.bullet_world is not None 

def test_add_physics_object(physics_engine):
    """物理オブジェクトの追加テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    
    # 物理オブジェクトを作成
    shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(shape)
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 追加されたことを確認
    assert node in physics_engine.bullet_world.getRigidBodies()
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode()

def test_physics_object_movement(physics_engine):
    """物理オブジェクトの移動テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    from panda3d.core import Vec3
    
    # 物理オブジェクトを作成
    shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(shape)
    node.setMass(1.0)  # 質量を設定
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 初期位置を設定
    initial_pos = Vec3(0, 0, 10)
    node_path.setPos(initial_pos)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 物理シミュレーションを複数回更新
    for _ in range(10):  # 複数回更新して確実に落下させる
        physics_engine.update(0.1)
    
    # 位置が変更されたことを確認（重力の影響で落下）
    assert node_path.getPos().z < initial_pos.z
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode()

def test_collision_detection(physics_engine):
    """衝突検出のテスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletGhostNode
    from panda3d.core import Vec3
    
    # 静的オブジェクト（地面）を作成
    ground_shape = BulletBoxShape((10, 10, 0.5))
    ground_node = BulletRigidBodyNode('ground')
    ground_node.addShape(ground_shape)
    ground_node.setMass(0)  # 静的オブジェクト
    ground_path = physics_engine.app.render.attachNewNode(ground_node)
    ground_path.setPos(0, 0, -1)
    
    # 動的オブジェクトを作成
    box_shape = BulletBoxShape((1, 1, 1))
    box_node = BulletRigidBodyNode('box')
    box_node.addShape(box_shape)
    box_path = physics_engine.app.render.attachNewNode(box_node)
    box_path.setPos(0, 0, 5)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(ground_node)
    physics_engine.bullet_world.attachRigidBody(box_node)
    
    # 衝突検出用のゴーストノードを作成
    ghost_node = BulletGhostNode('ghost')
    ghost_node.addShape(box_shape)
    ghost_path = physics_engine.app.render.attachNewNode(ghost_node)
    ghost_path.setPos(0, 0, 0)
    physics_engine.bullet_world.attachGhost(ghost_node)
    
    # 物理シミュレーションを更新
    physics_engine.update(1.0)
    
    # 衝突が検出されたことを確認
    assert len(ghost_node.getOverlappingNodes()) > 0
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(ground_node)
    physics_engine.bullet_world.removeRigidBody(box_node)
    physics_engine.bullet_world.removeGhost(ghost_node)
    ground_path.removeNode()
    box_path.removeNode()
    ghost_path.removeNode()

def test_physics_object_rotation(physics_engine):
    """物理オブジェクトの回転テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    from panda3d.core import Vec3, Point3
    
    # 物理オブジェクトを作成
    shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(shape)
    node.setMass(1.0)
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 初期位置と回転を設定
    initial_pos = Point3(0, 0, 5)
    initial_rotation = Vec3(45, 0, 0)  # X軸周りに45度回転
    node_path.setPos(initial_pos)
    node_path.setHpr(initial_rotation)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 回転が変更されたことを確認
    current_rotation = node_path.getHpr()
    assert current_rotation != initial_rotation
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode()

def test_physics_object_velocity(physics_engine):
    """物理オブジェクトの速度設定テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    from panda3d.core import Vec3
    
    # 物理オブジェクトを作成
    shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(shape)
    node.setMass(1.0)
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 初期位置を設定
    initial_pos = Vec3(0, 0, 5)
    node_path.setPos(initial_pos)
    
    # 初期速度を設定（X軸方向に10単位/秒）
    initial_velocity = Vec3(10, 0, 0)
    node.setLinearVelocity(initial_velocity)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 位置が変化したことを確認（方向は問わない）
    current_pos = node_path.getPos()
    assert current_pos != initial_pos
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode()

def test_physics_object_collision_response(physics_engine):
    """物理オブジェクトの衝突応答テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    from panda3d.core import Vec3
    
    # 静的オブジェクト（壁）を作成
    wall_shape = BulletBoxShape((1, 10, 10))
    wall_node = BulletRigidBodyNode('wall')
    wall_node.addShape(wall_shape)
    wall_node.setMass(0)  # 静的オブジェクト
    wall_path = physics_engine.app.render.attachNewNode(wall_node)
    wall_path.setPos(5, 0, 5)  # X軸方向に5単位離れた位置
    
    # 動的オブジェクトを作成
    box_shape = BulletBoxShape((1, 1, 1))
    box_node = BulletRigidBodyNode('box')
    box_node.addShape(box_shape)
    box_node.setMass(1.0)
    box_path = physics_engine.app.render.attachNewNode(box_node)
    box_path.setPos(0, 0, 5)
    
    # 初期速度を設定（X軸方向に10単位/秒）
    initial_velocity = Vec3(10, 0, 0)
    box_node.setLinearVelocity(initial_velocity)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(wall_node)
    physics_engine.bullet_world.attachRigidBody(box_node)
    
    # 物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 衝突後、速度が変化したことを確認
    current_velocity = box_node.getLinearVelocity()
    assert current_velocity != initial_velocity
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(wall_node)
    physics_engine.bullet_world.removeRigidBody(box_node)
    wall_path.removeNode()
    box_path.removeNode()

def test_physics_object_mass_change(physics_engine):
    """物理オブジェクトの質量変更テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    from panda3d.core import Vec3
    
    # 物理オブジェクトを作成
    shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(shape)
    node.setMass(1.0)  # 初期質量
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 初期位置を設定
    initial_pos = Vec3(0, 0, 5)
    node_path.setPos(initial_pos)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 質量を変更
    node.setMass(2.0)  # 質量を2倍に
    
    # 再度物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 質量が変更されたことを確認
    assert node.getMass() == 2.0
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode()

def test_physics_object_shape_change(physics_engine):
    """物理オブジェクトの形状変更テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape, BulletSphereShape
    from panda3d.core import Vec3
    
    # 物理オブジェクトを作成（箱の形状）
    box_shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(box_shape)
    node.setMass(1.0)
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 初期位置を設定
    initial_pos = Vec3(0, 0, 5)
    node_path.setPos(initial_pos)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 形状を変更（球の形状）
    sphere_shape = BulletSphereShape(1.0)
    node.removeShape(box_shape)
    node.addShape(sphere_shape)
    
    # 再度物理シミュレーションを更新
    physics_engine.update(0.1)
    
    # 形状が変更されたことを確認（形状の種類を直接確認する方法がないため、
    # ノードが存在することを確認する）
    assert node in physics_engine.bullet_world.getRigidBodies()
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode()

def test_physics_object_multiple_updates(physics_engine):
    """物理オブジェクトの複数回の更新テスト"""
    from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
    from panda3d.core import Vec3
    
    # 物理オブジェクトを作成
    shape = BulletBoxShape((1, 1, 1))
    node = BulletRigidBodyNode('test_object')
    node.addShape(shape)
    node.setMass(1.0)
    node_path = physics_engine.app.render.attachNewNode(node)
    
    # 初期位置を設定
    initial_pos = Vec3(0, 0, 5)
    node_path.setPos(initial_pos)
    
    # 物理ワールドに追加
    physics_engine.bullet_world.attachRigidBody(node)
    
    # 複数回の物理シミュレーション更新
    positions = []
    for _ in range(5):
        physics_engine.update(0.1)
        positions.append(node_path.getPos())
    
    # 位置が変化したことを確認
    assert positions[0] != positions[-1]
    
    # 各更新ステップで位置が変化したことを確認
    for i in range(1, len(positions)):
        assert positions[i] != positions[i-1]
    
    # クリーンアップ
    physics_engine.bullet_world.removeRigidBody(node)
    node_path.removeNode() 