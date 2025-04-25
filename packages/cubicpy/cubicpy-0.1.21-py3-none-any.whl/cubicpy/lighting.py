from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    Point3,
    Vec3,
    NodePath,
    DirectionalLight,
    AmbientLight,
    PointLight,
    VBase4
)

class LightingManager:
    """ライティングを管理するクラス"""
    
    def __init__(self, base: ShowBase):
        """
        初期化
        
        Args:
            base: ShowBaseインスタンス
        """
        self.base = base
        self.lights = {}
        self._setup_default_lighting()
    
    def _setup_default_lighting(self):
        """デフォルトのライティングを設定"""
        # 環境光
        self.create_ambient_light("default_ambient", (0.2, 0.2, 0.2, 1.0))
        
        # 平行光源（太陽光）
        self.create_directional_light(
            "default_directional",
            (0.8, 0.8, 0.8, 1.0),
            Vec3(0, 0, -1)
        )
    
    def create_ambient_light(self, name: str, color: tuple) -> AmbientLight:
        """
        環境光を作成
        
        Args:
            name: 光源の名前
            color: RGBAカラー値
            
        Returns:
            AmbientLight: 作成された環境光
        """
        light = AmbientLight(name)
        light.setColor(VBase4(*color))
        light_np = self.base.render.attachNewNode(light)
        self.base.render.setLight(light_np)
        self.lights[name] = light_np
        return light
    
    def create_directional_light(
        self,
        name: str,
        color: tuple,
        direction: Vec3
    ) -> DirectionalLight:
        """
        平行光源を作成
        
        Args:
            name: 光源の名前
            color: RGBAカラー値
            direction: 光源の方向ベクトル
            
        Returns:
            DirectionalLight: 作成された平行光源
        """
        light = DirectionalLight(name)
        light.setColor(VBase4(*color))
        light_np = self.base.render.attachNewNode(light)
        light_np.setHpr(direction)
        self.base.render.setLight(light_np)
        self.lights[name] = light_np
        return light
    
    def create_point_light(
        self,
        name: str,
        color: tuple,
        position: Point3
    ) -> PointLight:
        """
        点光源を作成
        
        Args:
            name: 光源の名前
            color: RGBAカラー値
            position: 光源の位置
            
        Returns:
            PointLight: 作成された点光源
        """
        light = PointLight(name)
        light.setColor(VBase4(*color))
        light_np = self.base.render.attachNewNode(light)
        light_np.setPos(position)
        self.base.render.setLight(light_np)
        self.lights[name] = light_np
        return light
    
    def remove_light(self, name: str):
        """
        光源を削除
        
        Args:
            name: 削除する光源の名前
        """
        if name in self.lights:
            light_np = self.lights[name]
            self.base.render.clearLight(light_np)
            light_np.removeNode()
            del self.lights[name]
    
    def update_light_intensity(self, name: str, color: tuple):
        """
        光源の強度を更新
        
        Args:
            name: 更新する光源の名前
            color: 新しいRGBAカラー値
        """
        if name in self.lights:
            light = self.lights[name].node()
            light.setColor(VBase4(*color)) 