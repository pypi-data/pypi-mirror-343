import pytest
from panda3d.core import WindowProperties, ModifierButtons
from direct.showbase.ShowBase import ShowBase
from cubicpy.input import InputHandler

@pytest.fixture
def showbase():
    """テスト用のShowBaseインスタンスを作成"""
    base = ShowBase(windowType='offscreen')
    yield base
    base.destroy()

@pytest.fixture
def input_handler(showbase):
    """テスト用の入力ハンドラーインスタンスを作成"""
    return InputHandler(showbase)

def test_input_initialization(input_handler):
    """入力ハンドラーの初期化テスト"""
    assert isinstance(input_handler, InputHandler)
    assert input_handler.base is not None
    assert input_handler.key_map is not None
    assert input_handler.mouse_buttons is not None

def test_key_mapping(input_handler):
    """キーマッピングのテスト"""
    # デフォルトのキーマッピングを確認
    assert 'forward' in input_handler.key_map
    assert 'backward' in input_handler.key_map
    assert 'left' in input_handler.key_map
    assert 'right' in input_handler.key_map
    assert 'jump' in input_handler.key_map

def test_mouse_button_mapping(input_handler):
    """マウスボタンマッピングのテスト"""
    # デフォルトのマウスボタンマッピングを確認
    assert 'left' in input_handler.mouse_buttons
    assert 'right' in input_handler.mouse_buttons
    assert 'middle' in input_handler.mouse_buttons

def test_key_state_tracking(input_handler):
    """キーの状態追跡テスト"""
    # キーが押されていない状態を確認
    assert not input_handler.is_key_pressed('forward')
    assert not input_handler.is_key_pressed('backward')
    
    # キーを押した状態をシミュレート
    input_handler.key_map['forward'] = True
    assert input_handler.is_key_pressed('forward')
    
    # キーを離した状態をシミュレート
    input_handler.key_map['forward'] = False
    assert not input_handler.is_key_pressed('forward')

def test_mouse_button_state_tracking(input_handler):
    """マウスボタンの状態追跡テスト"""
    # ボタンが押されていない状態を確認
    assert not input_handler.is_mouse_button_pressed('left')
    assert not input_handler.is_mouse_button_pressed('right')
    
    # ボタンを押した状態をシミュレート
    input_handler.mouse_buttons['left'] = True
    assert input_handler.is_mouse_button_pressed('left')
    
    # ボタンを離した状態をシミュレート
    input_handler.mouse_buttons['left'] = False
    assert not input_handler.is_mouse_button_pressed('left')

def test_key_binding_update(input_handler):
    """キーバインドの更新テスト"""
    # 新しいキーバインドを設定
    new_bindings = {
        'forward': 'w',
        'backward': 's',
        'left': 'a',
        'right': 'd',
        'jump': 'space'
    }
    input_handler.update_key_bindings(new_bindings)
    
    # バインドが正しく更新されたか確認
    assert input_handler.key_bindings['forward'] == 'w'
    assert input_handler.key_bindings['backward'] == 's'
    assert input_handler.key_bindings['left'] == 'a'
    assert input_handler.key_bindings['right'] == 'd'
    assert input_handler.key_bindings['jump'] == 'space' 