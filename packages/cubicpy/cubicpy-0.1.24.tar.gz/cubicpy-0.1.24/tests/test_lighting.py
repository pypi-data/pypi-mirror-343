import pytest
from panda3d.core import Point3, Vec3, NodePath, DirectionalLight, AmbientLight, PointLight
from direct.showbase.ShowBase import ShowBase
from cubicpy.lighting import LightingManager

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    yield base
    base.destroy()

@pytest.fixture
def lighting(showbase):
    """テスト用のライティングマネージャーインスタンスを作成"""
    return LightingManager(showbase)

def test_lighting_initialization(lighting):
    """ライティングマネージャーの初期化テスト"""
    assert isinstance(lighting, LightingManager)
    assert lighting.base is not None
    assert lighting.lights is not None
    assert isinstance(lighting.lights, dict)

def test_ambient_light_creation(lighting):
    """環境光の作成テスト"""
    light = lighting.create_ambient_light("test_ambient", (0.5, 0.5, 0.5, 1.0))
    assert isinstance(light, AmbientLight)
    assert light.getName() == "test_ambient"
    assert "test_ambient" in lighting.lights

def test_directional_light_creation(lighting):
    """平行光源の作成テスト"""
    light = lighting.create_directional_light("test_directional", (1, 1, 1, 1), Vec3(0, 0, -1))
    assert isinstance(light, DirectionalLight)
    assert light.getName() == "test_directional"
    assert "test_directional" in lighting.lights

def test_point_light_creation(lighting):
    """点光源の作成テスト"""
    light = lighting.create_point_light("test_point", (1, 1, 1, 1), Point3(0, 0, 10))
    assert isinstance(light, PointLight)
    assert light.getName() == "test_point"
    assert "test_point" in lighting.lights

def test_light_removal(lighting):
    """光源の削除テスト"""
    # 光源を作成
    light = lighting.create_ambient_light("test_light", (0.5, 0.5, 0.5, 1.0))
    assert "test_light" in lighting.lights
    
    # 光源を削除
    lighting.remove_light("test_light")
    assert "test_light" not in lighting.lights

def test_light_intensity_update(lighting):
    """光源の強度更新テスト"""
    # 光源を作成
    light = lighting.create_ambient_light("test_light", (0.5, 0.5, 0.5, 1.0))
    
    # 強度を更新
    lighting.update_light_intensity("test_light", (0.8, 0.8, 0.8, 1.0))
    
    # 強度が正しく更新されたか確認
    color = light.getColor()
    assert abs(color.x - 0.8) < 1e-6
    assert abs(color.y - 0.8) < 1e-6
    assert abs(color.z - 0.8) < 1e-6
    assert abs(color.w - 1.0) < 1e-6 