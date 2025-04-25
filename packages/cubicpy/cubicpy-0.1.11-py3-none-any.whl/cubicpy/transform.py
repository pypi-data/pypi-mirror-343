from panda3d.core import NodePath, TransformState


class TransformManager:
    """座標変換を管理するクラス - Processingスタイルの座標系操作を実現"""

    def __init__(self, app):
        self.app = app

        # 変換ノードのスタック
        self.transform_stack = []

        # 現在の変換ノード（ワールドノードの子として作成）
        self.current_node = self.app.world_node.attachNewNode("transform_root")

    def push_matrix(self):
        """現在の変換状態をスタックに保存し、新しい変換ノードを作成"""
        # 現在のノードをスタックに保存
        self.transform_stack.append(self.current_node)

        # 新しい変換ノードを作成（現在のノードの子として）
        new_node = self.current_node.attachNewNode(f"transform_{len(self.transform_stack)}")
        self.current_node = new_node

        return self.current_node

    def pop_matrix(self):
        """スタックから変換状態を復元"""
        if not self.transform_stack:
            print("警告: 空のトランスフォームスタックをポップしようとしました")
            return None

        # 現在のノードを削除（必要なければコメントアウト）
        # self.current_node.removeNode()

        # スタックから前の変換ノードを取得
        self.current_node = self.transform_stack.pop()

        return self.current_node

    def translate(self, x, y, z):
        """指定した位置に移動"""
        self.current_node.setPos(self.current_node, x, y, z)
        return self.current_node

    def rotate_hpr(self, h, p, r):
        """HPR（Heading-Pitch-Roll）で回転"""
        self.current_node.setHpr(self.current_node, h, p, r)
        return self.current_node

    def reset_matrix(self):
        """変換をリセット"""
        # すべてのスタックをクリア
        self.transform_stack = []

        # ルートノードを削除して再作成
        self.current_node.removeNode()
        self.current_node = self.app.world_node.attachNewNode("transform_root")

        return self.current_node

    def get_current_node(self):
        """現在の変換ノードを取得"""
        return self.current_node