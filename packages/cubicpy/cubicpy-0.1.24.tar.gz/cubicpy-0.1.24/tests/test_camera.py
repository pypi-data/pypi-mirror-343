import pytest
from panda3d.core import Point3, Vec3, NodePath, Camera, PerspectiveLens
from direct.showbase.ShowBase import ShowBase
from cubicpy.camera import CameraControl

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    
    # カメラを手動で作成
    cam = Camera('test_camera', PerspectiveLens())
    base.camera = base.render.attachNewNode(cam)
    base.camera.setPos(0, 0, 0)
    
    # カメラレンズの種類を設定
    base.camera_lens = 'perspective'  # または 'orthographic'
    
    yield base
    base.destroy()

@pytest.fixture
def camera(showbase):
    """テスト用のカメラインスタンスを作成"""
    return CameraControl(showbase)

def test_camera_initialization(camera):
    """カメラの初期化テスト"""
    assert isinstance(camera, CameraControl)
    assert camera.camera_target is not None
    assert isinstance(camera.camera_target, NodePath)

def test_camera_position(camera):
    """カメラの位置設定テスト"""
    # カメラの位置が正しく設定されているか確認
    assert camera.camera_radius == camera.BASE_RADIUS
    assert camera.camera_theta == camera.BASE_THETA
    assert camera.camera_phi == camera.BASE_PHI

def test_camera_target(camera):
    """カメラのターゲット設定テスト"""
    # カメラのターゲットが正しく設定されているか確認
    target_pos = camera.camera_target.getPos()
    assert target_pos.x == 0
    assert target_pos.y == 0
    assert target_pos.z == 0

def test_camera_reset(camera):
    """カメラのリセットテスト"""
    # カメラの位置を変更
    camera.camera_radius = 100
    camera.camera_theta = 90
    camera.camera_phi = -45
    
    # リセット
    camera.reset_camera()
    
    # 元の位置に戻っているか確認
    assert camera.camera_radius == camera.BASE_RADIUS
    assert camera.camera_theta == camera.BASE_THETA
    assert camera.camera_phi == camera.BASE_PHI
    
    # ターゲットも原点に戻っているか確認
    target_pos = camera.camera_target.getPos()
    assert target_pos.x == 0
    assert target_pos.y == 0
    assert target_pos.z == 0

def test_camera_radius_change(camera):
    """カメラの距離変更テスト"""
    original_radius = camera.camera_radius
    camera.change_camera_radius(1.5)
    assert camera.camera_radius == original_radius * 1.5

def test_camera_angle_change(camera):
    """カメラの角度変更テスト"""
    original_theta = camera.camera_theta
    original_phi = camera.camera_phi
    
    camera.change_camera_angle(10, 5)
    
    assert camera.camera_theta == original_theta + 10
    assert camera.camera_phi == original_phi + 5 