from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, Point3, Vec3
from typing import Dict, Optional, List

class SceneManager:
    """シーン管理を行うクラス"""
    
    def __init__(self, base: ShowBase):
        """
        初期化
        
        Args:
            base: ShowBaseインスタンス
        """
        self.base = base
        self.scene_root = self.base.render.attachNewNode("scene_root")
        self.objects: Dict[str, NodePath] = {}
        self._setup_default_scene()
    
    def _setup_default_scene(self):
        """デフォルトのシーン設定"""
        # シーンの初期設定
        self.scene_root.setPos(0, 0, 0)
        self.scene_root.setHpr(0, 0, 0)
    
    def add_object(self, name: str, node_path: NodePath) -> NodePath:
        """
        オブジェクトをシーンに追加
        
        Args:
            name: オブジェクトの名前
            node_path: 追加するNodePath
            
        Returns:
            NodePath: 追加されたオブジェクトのNodePath
        """
        if name in self.objects:
            raise ValueError(f"オブジェクト '{name}' は既に存在します")
        
        # シーンルートの子として追加
        new_node = self.scene_root.attachNewNode(name)
        new_node.setPos(node_path.getPos())
        new_node.setHpr(node_path.getHpr())
        new_node.setScale(node_path.getScale())
        self.objects[name] = new_node
        return new_node
    
    def remove_object(self, name: str) -> bool:
        """
        オブジェクトをシーンから削除
        
        Args:
            name: 削除するオブジェクトの名前
            
        Returns:
            bool: 削除に成功した場合はTrue
        """
        if name not in self.objects:
            return False
        
        node = self.objects[name]
        node.removeNode()
        del self.objects[name]
        return True
    
    def get_object(self, name: str) -> Optional[NodePath]:
        """
        オブジェクトを取得
        
        Args:
            name: 取得するオブジェクトの名前
            
        Returns:
            Optional[NodePath]: オブジェクトのNodePath。存在しない場合はNone
        """
        return self.objects.get(name)
    
    def move_object(self, name: str, position: Point3) -> bool:
        """
        オブジェクトを移動
        
        Args:
            name: 移動するオブジェクトの名前
            position: 新しい位置
            
        Returns:
            bool: 移動に成功した場合はTrue
        """
        if name not in self.objects:
            return False
        
        self.objects[name].setPos(position)
        return True
    
    def rotate_object(self, name: str, rotation: Vec3) -> bool:
        """
        オブジェクトを回転
        
        Args:
            name: 回転するオブジェクトの名前
            rotation: 回転角度（HPR）
            
        Returns:
            bool: 回転に成功した場合はTrue
        """
        if name not in self.objects:
            return False
        
        self.objects[name].setHpr(rotation)
        return True
    
    def get_all_objects(self) -> List[str]:
        """
        すべてのオブジェクト名を取得
        
        Returns:
            List[str]: オブジェクト名のリスト
        """
        return list(self.objects.keys())
    
    def clear_scene(self):
        """シーン内のすべてのオブジェクトを削除"""
        for name in list(self.objects.keys()):
            self.remove_object(name)
    
    def reset_scene(self):
        """シーンを初期状態にリセット"""
        self.clear_scene()
        self._setup_default_scene() 