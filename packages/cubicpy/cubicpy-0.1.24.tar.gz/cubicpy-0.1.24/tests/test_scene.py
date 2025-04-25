import pytest
from panda3d.core import NodePath, Point3, Vec3
from direct.showbase.ShowBase import ShowBase
from cubicpy.scene import SceneManager

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    yield base
    base.destroy()

@pytest.fixture
def scene(showbase):
    """テスト用のSceneManagerインスタンスを作成"""
    return SceneManager(showbase)

@pytest.fixture
def test_node(showbase):
    """テスト用のNodePathを作成"""
    return NodePath("test_node")

def test_scene_initialization(scene):
    """シーンマネージャーの初期化テスト"""
    assert isinstance(scene, SceneManager)
    assert scene.base is not None
    assert scene.scene_root is not None
    assert isinstance(scene.objects, dict)
    assert len(scene.objects) == 0

def test_add_object(scene, test_node):
    """オブジェクトの追加テスト"""
    # オブジェクトを追加
    added_node = scene.add_object("test", test_node)
    assert added_node is not None
    assert "test" in scene.objects
    assert scene.objects["test"] == added_node

def test_add_duplicate_object(scene, test_node):
    """重複オブジェクトの追加テスト"""
    # 最初のオブジェクトを追加
    scene.add_object("test", test_node)
    
    # 同じ名前のオブジェクトを追加しようとすると例外が発生
    with pytest.raises(ValueError):
        scene.add_object("test", test_node)

def test_remove_object(scene, test_node):
    """オブジェクトの削除テスト"""
    # オブジェクトを追加
    scene.add_object("test", test_node)
    assert "test" in scene.objects
    
    # オブジェクトを削除
    result = scene.remove_object("test")
    assert result is True
    assert "test" not in scene.objects

def test_remove_nonexistent_object(scene):
    """存在しないオブジェクトの削除テスト"""
    result = scene.remove_object("nonexistent")
    assert result is False

def test_get_object(scene, test_node):
    """オブジェクトの取得テスト"""
    # オブジェクトを追加
    scene.add_object("test", test_node)
    
    # オブジェクトを取得
    retrieved_node = scene.get_object("test")
    assert retrieved_node is not None
    assert retrieved_node == scene.objects["test"]

def test_get_nonexistent_object(scene):
    """存在しないオブジェクトの取得テスト"""
    retrieved_node = scene.get_object("nonexistent")
    assert retrieved_node is None

def test_move_object(scene, test_node):
    """オブジェクトの移動テスト"""
    # オブジェクトを追加
    scene.add_object("test", test_node)
    
    # オブジェクトを移動
    new_position = Point3(1, 2, 3)
    result = scene.move_object("test", new_position)
    assert result is True
    
    # 位置が正しく更新されたか確認
    pos = scene.objects["test"].getPos()
    assert abs(pos.x - new_position.x) < 1e-6
    assert abs(pos.y - new_position.y) < 1e-6
    assert abs(pos.z - new_position.z) < 1e-6

def test_rotate_object(scene, test_node):
    """オブジェクトの回転テスト"""
    # オブジェクトを追加
    scene.add_object("test", test_node)
    
    # オブジェクトを回転
    new_rotation = Vec3(45, 90, 180)
    result = scene.rotate_object("test", new_rotation)
    assert result is True
    
    # 回転が正しく更新されたか確認
    hpr = scene.objects["test"].getHpr()
    assert abs(hpr.x - new_rotation.x) < 1e-6
    assert abs(hpr.y - new_rotation.y) < 1e-6
    assert abs(hpr.z - new_rotation.z) < 1e-6

def test_get_all_objects(scene, test_node):
    """すべてのオブジェクト取得テスト"""
    # 複数のオブジェクトを追加
    scene.add_object("test1", test_node)
    scene.add_object("test2", test_node)
    
    # すべてのオブジェクト名を取得
    object_names = scene.get_all_objects()
    assert len(object_names) == 2
    assert "test1" in object_names
    assert "test2" in object_names

def test_clear_scene(scene, test_node):
    """シーンのクリアテスト"""
    # 複数のオブジェクトを追加
    scene.add_object("test1", test_node)
    scene.add_object("test2", test_node)
    assert len(scene.objects) == 2
    
    # シーンをクリア
    scene.clear_scene()
    assert len(scene.objects) == 0

def test_reset_scene(scene, test_node):
    """シーンのリセットテスト"""
    # オブジェクトを追加して位置を変更
    scene.add_object("test", test_node)
    scene.move_object("test", Point3(10, 10, 10))
    scene.rotate_object("test", Vec3(45, 45, 45))
    
    # シーンをリセット
    scene.reset_scene()
    assert len(scene.objects) == 0
    
    # シーンルートの位置と回転が初期化されたか確認
    pos = scene.scene_root.getPos()
    hpr = scene.scene_root.getHpr()
    assert abs(pos.x) < 1e-6
    assert abs(pos.y) < 1e-6
    assert abs(pos.z) < 1e-6
    assert abs(hpr.x) < 1e-6
    assert abs(hpr.y) < 1e-6
    assert abs(hpr.z) < 1e-6 