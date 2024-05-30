import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *


class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.transform_matrix = np.identity(4, dtype=np.float32)
        self.update()

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.5, 0.5, 1.0])
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)

    def paintGL(self):
        self.render()

    def render(self, **kwargs):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMultMatrixf(self.transform_matrix)
        self.draw_shape()
        self.swapBuffers()

    def draw_shape(self):
        glBegin(GL_QUADS)

        # Нижняя грань
        glNormal3f(0.0, 0.0, -1.0)
        glColor3f(1.0, 0.0, 0.0)  # RED
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)

        # Верхняя грань
        glNormal3f(0.0, 0.0, 1.0)
        glColor3f(0.0, 1.0, 0.0)  # GREEN
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.3, 0.5, 0.5)
        glVertex3f(-0.3, 0.5, 0.5)

        # Передняя грань
        glNormal3f(0.0, 1.0, 0.0)
        glColor3f(0.0, 0.0, 1.0)  # BLUE
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(0.3, 0.5, 0.5)
        glVertex3f(-0.3, 0.5, 0.5)

        # Задняя грань
        glNormal3f(0.0, -1.0, 0.0)
        glColor3f(1.0, 1.0, 0.0)  # YELLOW
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)

        # Левая грань
        glNormal3f(-1.0, 0.0, 0.0)
        glColor3f(1.0, 0.0, 1.0)  # MAGENTA
        glVertex3f(-0.5, -0.5, 0.0)
        glVertex3f(-0.5, 0.5, 0.0)
        glVertex3f(-0.3, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)

        # Правая грань
        glNormal3f(1.0, 0.0, 0.0)
        glColor3f(0.0, 1.0, 1.0)  # LIGHT BLUE
        glVertex3f(0.5, -0.5, 0.0)
        glVertex3f(0.5, 0.5, 0.0)
        glVertex3f(0.3, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glEnd()
        self.update()
        self.update()
    def translate(self, dx, dy):
        self.transform_matrix = np.dot(self.transform_matrix, self.create_translation_matrix(dx, dy, 0))
        self.update()

    def scale(self, sx, sy):
        self.transform_matrix = np.dot(self.transform_matrix, self.create_scale_matrix(sx, sy, 1.0))
        self.update()

    def rotate(self, angle, axis):
        self.transform_matrix = np.dot(self.transform_matrix, self.create_rotation_matrix(angle, axis))
        self.update()

    def reflect(self, x_axis, y_axis):
        reflect_matrix = np.identity(4, dtype=np.float32)
        if x_axis:
            reflect_matrix[0, 0] = -1
        if y_axis:
            reflect_matrix[1, 1] = -1
        self.transform_matrix = np.dot(self.transform_matrix, reflect_matrix)
        self.update()

    def reflect_y_equals_x(self):
        reflect_matrix = np.array([
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.transform_matrix = np.dot(self.transform_matrix, reflect_matrix)
        self.update()

    def reset_transformations(self):
        self.transform_matrix = np.identity(4, dtype=np.float32)
        self.update()

    def create_translation_matrix(self, dx, dy, dz):
        return np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.update()
    def create_scale_matrix(self, sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)
        self.update()
    def create_rotation_matrix(self, angle, axis):
        axis = np.array(axis, dtype=np.float32)
        axis = axis / np.linalg.norm(axis)
        c = np.cos(np.radians(angle))
        s = np.sin(np.radians(angle))
        t = 1 - c
        x, y, z = axis
        return np.array([
            [t * x * x + c, t * x * y - s * z, t * x * z + s * y, 0],
            [t * x * y + s * z, t * y * y + c, t * y * z - s * x, 0],
            [t * x * z - s * y, t * y * z + s * x, t * z * z + c, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.glWidget = GLWidget(self)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        layout.addWidget(self.glWidget)

        self.add_buttons(layout)

        self.setWindowTitle("Индивидуальное задание 2")
        self.setGeometry(100, 100, 800, 600)
        self.update()
    def add_buttons(self, layout):
        translate_button = QPushButton("Translate")
        translate_button.clicked.connect(lambda: self.glWidget.translate(0.1, 0.1))
        layout.addWidget(translate_button)

        scale_button = QPushButton("Scale")
        scale_button.clicked.connect(lambda: self.glWidget.scale(1.1, 1.1))
        layout.addWidget(scale_button)

        rotate_x_button = QPushButton("Rotate X")
        rotate_x_button.clicked.connect(lambda: self.glWidget.rotate(10.0, [1, 0, 0]))
        layout.addWidget(rotate_x_button)

        rotate_y_button = QPushButton("Rotate Y")
        rotate_y_button.clicked.connect(lambda: self.glWidget.rotate(10.0, [0, 1, 0]))
        layout.addWidget(rotate_y_button)

        rotate_z_button = QPushButton("Rotate Z")
        rotate_z_button.clicked.connect(lambda: self.glWidget.rotate(10.0, [0, 0, 1]))
        layout.addWidget(rotate_z_button)

        reflect_x_button = QPushButton("Reflect X")
        reflect_x_button.clicked.connect(lambda: self.glWidget.reflect(True, False))
        layout.addWidget(reflect_x_button)

        reflect_y_button = QPushButton("Reflect Y")
        reflect_y_button.clicked.connect(lambda: self.glWidget.reflect(False, True))
        layout.addWidget(reflect_y_button)

        reflect_y_equals_x_button = QPushButton("Reflect Y=X")
        reflect_y_equals_x_button.clicked.connect(lambda: self.glWidget.reflect_y_equals_x())
        layout.addWidget(reflect_y_equals_x_button)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(lambda: self.glWidget.reset_transformations())
        layout.addWidget(reset_button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
