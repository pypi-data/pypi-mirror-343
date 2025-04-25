import pytest
from panda3d.core import Point3, Vec3, NodePath
from direct.showbase.ShowBase import ShowBase
from cubicpy.transform import TransformManager

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    base.world_node = base.render.attachNewNode("world")
    yield base
    base.destroy()

@pytest.fixture
def transform(showbase):
    """テスト用の変換マネージャーインスタンスを作成"""
    return TransformManager(showbase)

def test_transform_initialization(transform):
    """変換マネージャーの初期化テスト"""
    assert isinstance(transform, TransformManager)
    assert transform.current_node is not None
    assert isinstance(transform.current_node, NodePath)
    assert len(transform.transform_stack) == 0

def test_push_matrix(transform):
    """変換スタックのプッシュテスト"""
    original_node = transform.current_node
    new_node = transform.push_matrix()
    
    assert new_node is not None
    assert new_node != original_node
    assert len(transform.transform_stack) == 1
    assert transform.transform_stack[0] == original_node

def test_pop_matrix(transform):
    """変換スタックのポップテスト"""
    # スタックにノードをプッシュ
    original_node = transform.current_node
    transform.push_matrix()
    
    # スタックからポップ
    popped_node = transform.pop_matrix()
    
    assert popped_node == original_node
    assert len(transform.transform_stack) == 0

def test_translate(transform):
    """平行移動テスト"""
    transform.translate(1, 2, 3)
    pos = transform.current_node.getPos()
    assert pos.x == 1
    assert pos.y == 2
    assert pos.z == 3

def test_rotate_hpr(transform):
    """回転テスト"""
    transform.rotate_hpr(90, 45, 30)
    hpr = transform.current_node.getHpr()
    assert hpr.x == 90
    assert hpr.y == 45
    assert hpr.z == 30

def test_reset_matrix(transform):
    """変換のリセットテスト"""
    # 変換を適用
    transform.translate(1, 2, 3)
    transform.rotate_hpr(90, 45, 30)
    transform.push_matrix()
    
    # 変換前のノードを保存
    original_node = transform.current_node
    
    # リセット
    reset_node = transform.reset_matrix()
    
    # 新しいノードが作成されているか確認
    assert reset_node is not None
    assert reset_node.getName() == "transform_root"
    
    # 位置と回転がリセットされているか確認
    pos = reset_node.getPos()
    assert pos.x == 0
    assert pos.y == 0
    assert pos.z == 0
    
    hpr = reset_node.getHpr()
    assert hpr.x == 0
    assert hpr.y == 0
    assert hpr.z == 0 