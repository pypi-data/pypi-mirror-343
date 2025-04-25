import pytest
from panda3d.core import NodePath, GeomNode, GeomVertexData, GeomTriangles, GeomLines
from cubicpy.geom_utils import create_line_node, create_geom, draw_line, draw_circumference, draw_triangle

class TestGeomUtils:
    @pytest.fixture
    def mock_parent(self):
        # テスト用の親ノードを作成
        return NodePath("test_parent")

    def test_create_line_node(self):
        # 線のノードが正しく作成されることをテスト
        start = (0, 0, 0)
        end = (1, 1, 1)
        color = (1, 0, 0)
        thickness = 2

        node = create_line_node(start, end, color, thickness)
        assert isinstance(node, NodePath)
        assert isinstance(node.getNode(0), GeomNode)

    def test_create_geom_triangle(self, mock_parent):
        # 三角形のジオメトリが正しく作成されることをテスト
        vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        color = (1, 0, 0)

        node = create_geom(mock_parent, vertices, color)
        assert isinstance(node, NodePath)
        assert isinstance(node.getNode(0), GeomNode)

        # 頂点データが正しく設定されていることを確認
        geom = node.getNode(0).getGeom(0)
        vdata = geom.getVertexData()
        assert vdata.getNumRows() == 3

    def test_create_geom_line(self, mock_parent):
        # 線のジオメトリが正しく作成されることをテスト
        vertices = [(0, 0, 0), (1, 1, 1)]
        color = (1, 0, 0)

        node = create_geom(mock_parent, vertices, color)
        assert isinstance(node, NodePath)
        assert isinstance(node.getNode(0), GeomNode)

        # 頂点データが正しく設定されていることを確認
        geom = node.getNode(0).getGeom(0)
        vdata = geom.getVertexData()
        assert vdata.getNumRows() == 2

    def test_draw_line(self, mock_parent):
        # 線の描画関数が正しく動作することをテスト
        point1 = (0, 0, 0)
        point2 = (1, 1, 1)
        color = (1, 0, 0)

        node = draw_line(mock_parent, point1, point2, color)
        assert isinstance(node, NodePath)
        assert isinstance(node.getNode(0), GeomNode)

    def test_draw_circumference(self, mock_parent):
        # 円周の描画関数が正しく動作することをテスト
        radius = 1
        color = (1, 0, 0)
        segs = 32

        node = draw_circumference(mock_parent, radius, color, segs=segs)
        assert isinstance(node, NodePath)
        assert isinstance(node.getNode(0), GeomNode)

        # 頂点データが正しく設定されていることを確認
        geom = node.getNode(0).getGeom(0)
        vdata = geom.getVertexData()
        assert vdata.getNumRows() == segs + 1

    def test_draw_triangle(self, mock_parent):
        # 三角形の描画関数が正しく動作することをテスト
        point1 = (0, 0, 0)
        point2 = (1, 0, 0)
        point3 = (0, 1, 0)
        color = (1, 0, 0)

        node = draw_triangle(mock_parent, point1, point2, point3, color)
        assert isinstance(node, NodePath)
        assert isinstance(node.getNode(0), GeomNode)

        # 頂点データが正しく設定されていることを確認
        geom = node.getNode(0).getGeom(0)
        vdata = geom.getVertexData()
        assert vdata.getNumRows() == 3 