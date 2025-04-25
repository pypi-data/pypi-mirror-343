from math import degrees, atan2, sqrt
from direct.gui.DirectGui import OnscreenText
from panda3d.core import TextNode, PandaNode


class Draw2DText(OnscreenText):
    def __init__(self, font, parent, text='', scale=0.1, pos=(0.05, -0.1), fg=(1, 1, 1, 1), frame=None):


        super().__init__(font=font, parent=parent, text=text, scale=scale, pos=pos, frame=frame,
                         fg=fg, align=TextNode.ALeft, mayChange=True)


class Draw3DText(OnscreenText):
    def __init__(self, font, parent, text='', scale=5, pos=(0, 0), fg=(1, 1, 1, 1)):
        self.label_node = parent.attachNewNode(PandaNode('label_node'))
        super().__init__(font=font, parent=self.label_node, text=text, scale=scale, pos=pos,
                         fg=fg)

    def look_at_origin(self, x, y, z):
        # ラベルを回転させて原点の方向に向ける
        h = degrees(atan2(y, x)) - 90  # Z軸方向の回転角度（°）
        p = degrees(atan2(z, sqrt(x ** 2 + y ** 2)))  # X軸方向の回転角度（°）
        r = 0  # Y軸中心の回転角度（°）
        self.label_node.setHpr(h, p, r)
