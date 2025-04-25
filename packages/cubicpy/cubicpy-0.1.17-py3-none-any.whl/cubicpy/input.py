from direct.showbase.ShowBase import ShowBase
from panda3d.core import ModifierButtons

class InputHandler:
    """入力処理を管理するクラス"""
    
    def __init__(self, base: ShowBase):
        """
        初期化
        
        Args:
            base: ShowBaseインスタンス
        """
        self.base = base
        self.key_map = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'jump': False
        }
        self.mouse_buttons = {
            'left': False,
            'right': False,
            'middle': False
        }
        self._setup_default_bindings()
        self._setup_input_handlers()
    
    def _setup_default_bindings(self):
        """デフォルトのキーバインドを設定"""
        self.key_bindings = {
            'forward': 'w',
            'backward': 's',
            'left': 'a',
            'right': 'd',
            'jump': 'space'
        }
    
    def _setup_input_handlers(self):
        """入力ハンドラーを設定"""
        self.base.accept('w', self._on_key_down, ['forward'])
        self.base.accept('w-up', self._on_key_up, ['forward'])
        self.base.accept('s', self._on_key_down, ['backward'])
        self.base.accept('s-up', self._on_key_up, ['backward'])
        self.base.accept('a', self._on_key_down, ['left'])
        self.base.accept('a-up', self._on_key_up, ['left'])
        self.base.accept('d', self._on_key_down, ['right'])
        self.base.accept('d-up', self._on_key_up, ['right'])
        self.base.accept('space', self._on_key_down, ['jump'])
        self.base.accept('space-up', self._on_key_up, ['jump'])
        
        # マウスボタンのハンドリング
        self.base.accept('mouse1', self._on_mouse_down, ['left'])
        self.base.accept('mouse1-up', self._on_mouse_up, ['left'])
        self.base.accept('mouse2', self._on_mouse_down, ['middle'])
        self.base.accept('mouse2-up', self._on_mouse_up, ['middle'])
        self.base.accept('mouse3', self._on_mouse_down, ['right'])
        self.base.accept('mouse3-up', self._on_mouse_up, ['right'])
    
    def _on_key_down(self, action):
        """キーが押された時の処理"""
        self.key_map[action] = True
    
    def _on_key_up(self, action):
        """キーが離された時の処理"""
        self.key_map[action] = False
    
    def _on_mouse_down(self, button):
        """マウスボタンが押された時の処理"""
        self.mouse_buttons[button] = True
    
    def _on_mouse_up(self, button):
        """マウスボタンが離された時の処理"""
        self.mouse_buttons[button] = False
    
    def is_key_pressed(self, action):
        """
        指定されたアクションのキーが押されているかどうかを確認
        
        Args:
            action: 確認するアクション名
            
        Returns:
            bool: キーが押されている場合はTrue
        """
        return self.key_map.get(action, False)
    
    def is_mouse_button_pressed(self, button):
        """
        指定されたマウスボタンが押されているかどうかを確認
        
        Args:
            button: 確認するボタン名（'left', 'right', 'middle'）
            
        Returns:
            bool: ボタンが押されている場合はTrue
        """
        return self.mouse_buttons.get(button, False)
    
    def update_key_bindings(self, new_bindings):
        """
        キーバインドを更新
        
        Args:
            new_bindings: 新しいキーバインドの辞書
        """
        # 古いバインドを解除
        for action, key in self.key_bindings.items():
            self.base.ignore(key)
            self.base.ignore(f"{key}-up")
        
        # 新しいバインドを設定
        self.key_bindings = new_bindings
        self._setup_input_handlers() 