class ApiMethod:
    """オブジェクト作成と操作のためのAPIメソッド"""

    def __init__(self, app):
        self.app = app
        self.object_data = []  # リセット用にオブジェクトデータを保存
        # 変換マネージャーへの参照
        self.transform_manager = None

    def add_cube(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, hpr=(0, 0, 0),
                 base_point=0, remove=False, velocity=(0, 0, 0)):
        """箱を追加"""
        # 現在の変換ノードを取得（設定されている場合）
        parent_node = self._get_parent_node()

        cube_data = {
            'type': 'cube',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha,
            'hpr': hpr,
            'base_point': base_point,
            'remove': remove,
            'velocity': velocity,
            'parent_node': parent_node
        }
        self.object_data.append(cube_data)
        return cube_data

    def add_sphere(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1,
                   hpr=(0, 0, 0),
                   base_point=0, remove=False, velocity=(0, 0, 0)):
        """球を追加"""
        # 現在の変換ノードを取得（設定されている場合）
        parent_node = self._get_parent_node()

        sphere_data = {
            'type': 'sphere',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha,
            'hpr': hpr,
            'base_point': base_point,
            'remove': remove,
            'velocity': velocity,
            'parent_node': parent_node
        }
        self.object_data.append(sphere_data)
        return sphere_data

    def add_cylinder(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1,
                     hpr=(0, 0, 0),
                     base_point=0, remove=False, velocity=(0, 0, 0)):
        """円柱を追加"""
        # 現在の変換ノードを取得（設定されている場合）
        parent_node = self._get_parent_node()

        cylinder_data = {
            'type': 'cylinder',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha,
            'hpr': hpr,
            'base_point': base_point,
            'remove': remove,
            'velocity': velocity,
            'parent_node': parent_node
        }
        self.object_data.append(cylinder_data)
        return cylinder_data

    def add_ground(self, color=(0, 1, 0), color_alpha=0.3):
        """平面の地面を追加"""
        # 地面は必ずワールド座標系に配置
        ground_data = {
            'type': 'cube',
            'pos': (-500, -500, -1),
            'scale': (1000, 1000, 1),
            'color': color,
            'mass': 0,
            'color_alpha': color_alpha,
            'parent_node': None  # 常にワールドの子
        }
        self.object_data.append(ground_data)
        return ground_data

    def add(self, obj_type, **kwargs):
        """汎用オブジェクト追加メソッド"""
        position = kwargs.get('position', kwargs.get('pos', (0, 0, 0)))
        scale = kwargs.get('scale', (1, 1, 1))
        color = kwargs.get('color', (0.5, 0.5, 0.5))
        mass = kwargs.get('mass', 1)
        color_alpha = kwargs.get('color_alpha', 1)
        hpr = kwargs.get('hpr', (0, 0, 0))
        base_point = kwargs.get('base_point', 0)
        remove = kwargs.get('remove', False)
        velocity = kwargs.get('velocity', (0, 0, 0))

        if obj_type in ['cube', 'box']:
            return self.add_cube(position, scale, color, mass, color_alpha, hpr, base_point, remove, velocity)
        elif obj_type == 'sphere':
            return self.add_sphere(position, scale, color, mass, color_alpha, hpr, base_point, remove, velocity)
        elif obj_type == 'cylinder':
            return self.add_cylinder(position, scale, color, mass, color_alpha, hpr, base_point, remove, velocity)
        else:
            raise ValueError(f"未知のオブジェクトタイプ: {obj_type}")

    def from_body_data(self, body_data):
        """body_dataリストからオブジェクトを作成"""
        for data in body_data:
            data_copy = data.copy()  # 元のデータを変更しないようにコピー
            obj_type = data_copy.pop('type', 'cube')
            self.add(obj_type, **data_copy)
        return self

    def clear_data(self):
        """保存したオブジェクトデータをクリア"""
        self.object_data = []

    def get_object_data(self):
        """保存したオブジェクトデータのコピーを取得"""
        return self.object_data.copy()

    # 変換操作のためのメソッド
    def push_matrix(self):
        """現在の変換状態をスタックに保存"""
        if self.transform_manager:
            return self.transform_manager.push_matrix()
        return None

    def pop_matrix(self):
        """スタックから変換状態を復元"""
        if self.transform_manager:
            return self.transform_manager.pop_matrix()
        return None

    def translate(self, x, y, z):
        """指定した位置に移動"""
        if self.transform_manager:
            return self.transform_manager.translate(x, y, z)
        return None

    def rotate_hpr(self, h, p, r):
        """HPR（Heading-Pitch-Roll）で回転"""
        if self.transform_manager:
            return self.transform_manager.rotate_hpr(h, p, r)
        return None

    def reset_matrix(self):
        """変換をリセット"""
        if self.transform_manager:
            return self.transform_manager.reset_matrix()
        return None

    def _get_parent_node(self):
        """現在の変換ノードを取得（なければNone）"""
        if self.transform_manager:
            return self.transform_manager.get_current_node()
        return None