import pytest
from panda3d.core import NodePath, Vec3
from direct.showbase.ShowBase import ShowBase
from cubicpy.model_manager import ModelManager

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    yield base
    base.destroy()

@pytest.fixture
def model_manager(showbase):
    """テスト用のModelManagerインスタンスを作成"""
    return ModelManager(showbase)

def test_model_manager_initialization(model_manager):
    """ModelManagerの初期化テスト"""
    assert isinstance(model_manager, ModelManager)
    assert model_manager.app is not None
    assert isinstance(model_manager.cube_shapes, dict)
    assert isinstance(model_manager.sphere_shapes, dict)
    assert isinstance(model_manager.cylinder_shapes, dict)

def test_cube_model_loading(model_manager):
    """キューブモデルのロードテスト"""
    cube = model_manager.cube_model
    assert isinstance(cube, NodePath)
    
    # スケールの確認
    scale = cube.getScale()
    assert abs(scale.x - 1.0) < 1e-6
    assert abs(scale.y - 1.0) < 1e-6
    assert abs(scale.z - 1.0) < 1e-6

def test_sphere_model_loading(model_manager):
    """球体モデルのロードテスト"""
    sphere = model_manager.sphere_model
    assert isinstance(sphere, NodePath)
    
    # スケールの確認
    scale = sphere.getScale()
    assert abs(scale.x - 1.0) < 1e-6
    assert abs(scale.y - 1.0) < 1e-6
    assert abs(scale.z - 1.0) < 1e-6

def test_cylinder_model_loading(model_manager):
    """円柱モデルのロードテスト"""
    cylinder = model_manager.cylinder_model
    assert isinstance(cylinder, NodePath)
    
    # スケールの確認
    scale = cylinder.getScale()
    assert abs(scale.x - 1.0) < 1e-6
    assert abs(scale.y - 1.0) < 1e-6
    assert abs(scale.z - 1.0) < 1e-6

def test_model_reuse(model_manager):
    """モデルの再利用テスト"""
    # 同じモデルを複数回取得
    cube1 = model_manager.cube_model
    cube2 = model_manager.cube_model
    
    # 同じインスタンスであることを確認
    assert cube1 is cube2 