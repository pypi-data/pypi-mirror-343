from math import sin, cos, radians
from panda3d.core import Point3, OrthographicLens, NodePath


class CameraControl:
  BASE_FILM_SIZE = (800, 600)
  BASE_RADIUS = 50
  BASE_THETA = 80
  BASE_PHI = -80
  MIN_PHI = 0.0000001
  LOOK_STEP = 2  # カメラの注視点移動量

  def __init__(self, app):
    self.app = app
    self.app.disableMouse()
    self.camera_radius = self.BASE_RADIUS
    self.camera_theta = self.BASE_THETA
    self.camera_phi = self.BASE_PHI

    # カメラの注視点用のノードを作成
    self.camera_target = NodePath("camera_target")
    self.camera_target.reparentTo(self.app.render)
    self.camera_target.setPos(0, 0, 0)

    self.camera_set_pos()

    # カメラを平行投影に変更
    if app.camera_lens == 'orthographic':
      print('Set OrthographicLens')
      self.lens = OrthographicLens()
      self.film_size = self.BASE_FILM_SIZE
      self.lens.setFilmSize(*self.film_size)  # 表示範囲のサイズを設定
      self.app.cam.node().setLens(self.lens)

    # 通常のカメラ角度制御
    self.app.accept('arrow_right', self.change_camera_angle, [0, 1])
    self.app.accept('arrow_left', self.change_camera_angle, [0, -1])
    self.app.accept('arrow_up', self.change_camera_angle, [-1, 0])
    self.app.accept('arrow_down', self.change_camera_angle, [1, 0])
    self.app.accept('arrow_right-repeat', self.change_camera_angle, [0, 1])
    self.app.accept('arrow_left-repeat', self.change_camera_angle, [0, -1])
    self.app.accept('arrow_up-repeat', self.change_camera_angle, [-1, 0])
    self.app.accept('arrow_down-repeat', self.change_camera_angle, [1, 0])

    # カメラの注視点移動をShift+W/S/A/D/Q/E組み合わせで統一
    # 左右移動
    self.app.accept('shift-a', self.move_camera_target, [-self.LOOK_STEP, 0, 0])  # 左
    self.app.accept('shift-d', self.move_camera_target, [self.LOOK_STEP, 0, 0])  # 右
    self.app.accept('shift-a-repeat', self.move_camera_target, [-self.LOOK_STEP, 0, 0])
    self.app.accept('shift-d-repeat', self.move_camera_target, [self.LOOK_STEP, 0, 0])

    # 前後移動
    self.app.accept('shift-w', self.move_camera_target, [0, self.LOOK_STEP, 0])  # 前
    self.app.accept('shift-s', self.move_camera_target, [0, -self.LOOK_STEP, 0])  # 後
    self.app.accept('shift-w-repeat', self.move_camera_target, [0, self.LOOK_STEP, 0])
    self.app.accept('shift-s-repeat', self.move_camera_target, [0, -self.LOOK_STEP, 0])

    # 上下移動
    self.app.accept('shift-e', self.move_camera_target, [0, 0, self.LOOK_STEP])  # 上
    self.app.accept('shift-q', self.move_camera_target, [0, 0, -self.LOOK_STEP])  # 下
    self.app.accept('shift-e-repeat', self.move_camera_target, [0, 0, self.LOOK_STEP])
    self.app.accept('shift-q-repeat', self.move_camera_target, [0, 0, -self.LOOK_STEP])

    self.app.accept('r', self.reset_camera)

    if app.camera_lens == 'orthographic':
      self.app.accept('wheel_up', self.change_film_size, [1.1])
      self.app.accept('wheel_down', self.change_film_size, [0.9])
    else:
      self.app.accept('wheel_up', self.change_camera_radius, [1.1])
      self.app.accept('wheel_down', self.change_camera_radius, [0.9])

  def change_camera_angle(self, theta, phi):
    self.camera_theta += theta
    self.camera_phi += phi
    if self.camera_theta <= 0:
      self.camera_theta = self.MIN_PHI
    if 180 <= self.camera_theta:
      self.camera_theta = 180 - self.MIN_PHI
    self.camera_set_pos()

  def change_camera_radius(self, ratio):
    self.camera_radius *= ratio
    self.camera_set_pos()

  def change_film_size(self, rate):
    self.film_size = tuple([int(size * rate) for size in self.film_size])
    self.lens.setFilmSize(*self.film_size)  # 表示範囲のサイズを設定
    self.app.cam.node().setLens(self.lens)

  def move_camera_target(self, dx, dy, dz):
    """カメラの注視点を移動する"""
    current_pos = self.camera_target.getPos()
    new_pos = Point3(current_pos.x + dx, current_pos.y + dy, current_pos.z + dz)
    self.camera_target.setPos(new_pos)
    self.camera_set_pos()  # カメラ位置を更新して新しい注視点を見るようにする

  def camera_set_pos(self):
    radius = self.camera_radius
    theta = self.camera_theta
    phi = self.camera_phi
    # 注視点を中心とした球面座標系でカメラ位置を計算
    target_pos = self.camera_target.getPos()
    cartesian_offset = self.convert_to_cartesian(radius, theta, phi)
    position = Point3(
      target_pos.x + cartesian_offset[0],
      target_pos.y + cartesian_offset[1],
      target_pos.z + cartesian_offset[2]
    )
    self.app.camera.setPos(position)
    # カメラを注視点に向ける
    self.app.camera.lookAt(self.camera_target)

  def reset_camera(self):
    """カメラをデフォルト設定にリセットする"""
    self.camera_radius = self.BASE_RADIUS
    self.camera_theta = self.BASE_THETA
    self.camera_phi = self.BASE_PHI
    # 注視点も原点にリセット
    self.camera_target.setPos(0, 0, 0)
    self.camera_set_pos()
    # レンズのリセットが必要な場合はコメントを外す
    # if hasattr(self, 'lens') and hasattr(self, 'film_size'):
    #     self.film_size = self.BASE_FILM_SIZE
    #     self.lens.setFilmSize(*self.BASE_FILM_SIZE)
    #     self.app.cam.node().setLens(self.lens)

  @staticmethod
  def convert_to_cartesian(r, theta, phi):
    rad_theta, rad_phi = radians(theta), radians(phi)
    x = r * sin(rad_theta) * cos(rad_phi)
    y = r * sin(rad_theta) * sin(rad_phi)
    z = r * cos(rad_theta)
    return x, y, z