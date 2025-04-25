from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletCylinderShape
from . import get_position_offset


class Cylinder:
    def __init__(self, app, cylinder, parent_node=None):
        # print(cylinder)
        self.app = app
        self.type = 'cylinder'

        # スケール・色・質量の設定
        self.node_scale = Vec3(cylinder['scale']) if 'scale' in cylinder else (1, 1, 1)
        self.node_color = cylinder['color'] if 'color' in cylinder else (0.5, 0.5, 0.5)
        self.node_mass = cylinder['mass'] if 'mass' in cylinder else 1
        self.node_hpr = Vec3(cylinder['hpr']) if 'hpr' in cylinder else Vec3(0, 0, 0)
        self.color_alpha = cylinder['color_alpha'] if 'color_alpha' in cylinder else 1
        # 配置するときの位置基準 (0: 原点に近い角が基準, 1: 底面の中心が基準, 2: 立方体の重心が基準)
        self.base_point = cylinder['base_point'] if 'base_point' in cylinder else 0
        self.remove_selected = cylinder['remove'] if 'remove' in cylinder else False
        # 初速度ベクトルの設定を追加
        self.velocity = Vec3(cylinder['velocity']) if 'velocity' in cylinder else Vec3(0, 0, 0)

        # 配置位置の計算
        self.node_pos = Vec3(cylinder['pos']) + get_position_offset(self)

        # 物理形状（スケールを適用）
        if cylinder['scale'] in self.app.model_manager.cylinder_shapes:
            self.cylinder_shape = self.app.model_manager.cylinder_shapes[cylinder['scale']]
        else:
            self.cylinder_shape = BulletCylinderShape(0.5, 1)
            self.app.model_manager.cylinder_shapes[cylinder['scale']] = self.cylinder_shape

        # Bullet剛体ノード
        self.rigid_cylinder = BulletRigidBodyNode('Cylinder')
        self.rigid_cylinder.setMass(self.node_mass)
        self.rigid_cylinder.addShape(self.cylinder_shape)
        self.rigid_cylinder.setRestitution(self.app.restitution)
        self.rigid_cylinder.setFriction(self.app.friction)
        self.app.physics.bullet_world.attachRigidBody(self.rigid_cylinder)
        # 速度ベクトルがある場合は、剛体を適切に設定
        if self.velocity != Vec3(0, 0, 0):
            self.rigid_cylinder.setDeactivationEnabled(False)

        # ノードパス - 親ノードが指定されている場合はその下に配置
        if parent_node:
            self.model_node = parent_node.attachNewNode(self.rigid_cylinder)
        else:
            self.model_node = self.app.world_node.attachNewNode(self.rigid_cylinder)

        self.model_node.setPos(self.node_pos)
        self.model_node.setScale(self.node_scale)
        self.model_node.setColor(*self.node_color, self.color_alpha)
        self.model_node.setHpr(self.node_hpr)
        self.app.model_manager.cylinder_model.copyTo(self.model_node)

        if self.color_alpha < 1:
            self.model_node.setTransparency(1)  # 半透明を有効化

        # スペースボタンを表示
        if self.velocity != Vec3(0, 0, 0):
            self.app.space_button_text.show()

        # Xボタンを表示
        if self.remove_selected:
            self.app.x_button_text.show()

    def update(self):
        """ 物理エンジンの位置を更新 """
        self.model_node.setPos(self.model_node.node().getPos())

    def remove(self):
        """ ボックスを削除 """
        self.app.physics.bullet_world.removeRigidBody(self.model_node.node())
        self.model_node.removeNode()
        del self.model_node
        del self.cylinder_shape  # 削除処理

    def apply_velocity(self):
        """オブジェクトに初速を与える"""
        if self.velocity != Vec3(0, 0, 0):
            # 剛体をアクティブ化
            self.model_node.node().setActive(True)
            # 寝ている状態からの自動移行を無効化
            self.model_node.node().setDeactivationEnabled(False)
            # 連続衝突検出の設定
            self.model_node.node().setCcdMotionThreshold(1e-7)
            self.model_node.node().setCcdSweptSphereRadius(0.5)
            # 速度を設定
            self.model_node.node().setLinearVelocity(self.velocity)

    def has_moved(self, tolerance=0.01):
        """オブジェクトが初期位置から動いたかどうかを確認します"""
        # 現在の位置を取得
        current_pos = self.model_node.getPos()

        # 初期位置との差を計算
        dx = abs(current_pos.x - self.node_pos.x)
        dy = abs(current_pos.y - self.node_pos.y)
        dz = abs(current_pos.z - self.node_pos.z)

        # いずれかの軸で許容誤差より大きく動いていたら、動いたと判断
        return dx > tolerance or dy > tolerance or dz > tolerance