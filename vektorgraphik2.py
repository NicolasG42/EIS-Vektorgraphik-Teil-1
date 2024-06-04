from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QKeySequence, QImage, QPainter, QColor
from PySide6.QtWidgets import QApplication, QMenuBar, QToolBar, QWidget, QFileDialog, QMainWindow, QMessageBox, QVBoxLayout
import sys
import math
from abc import ABC ,abstractmethod
# Datenstrukturen für Vektorgrafik
##!Geändert mit oberklasse "Shape", allerdings noch keine "draw funktion"(unsicher wie wir das umsetzen,
#  da die bei uns im renderer sind..., noch nicht eingabefenster überarbeitet)
class Shape(ABC):
    def __init__(self, x, y, fill_color, border_color, border_width):
        self.x = x
        self.y = y
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width

    @abstractmethod
    def painter(self):
        pass

##! Haben alle jetzt "border width" 
class Rectangle(Shape):
    def __init__(self, x, y, width, height, fill_color, border_color, border_width):
        super().__init__(x,y,fill_color, border_color, border_width)
        self.width = width
        self.height = height

    def contains(self, point):
        return self.x <= point.x() <= self.x + self.width and self.y <= point.y() <= self.y + self.height

class Circle:
    def __init__(self, x, y, radius, fill_color, border_color, border_width):
        super().__init__(x,y,fill_color, border_color, border_width)
        self.radius = radius

    def contains(self, point):
        return (self.x - point.x())**2 + (self.y - point.y())**2 <= self.radius**2

class Star:
    def __init__(self, x, y, radius, points, fill_color, border_color, border_width):
        super().__init__(x,y,fill_color, border_color, border_width)
        self.radius = radius
        self.points = points

    def contains(self, point):
        # A simple bounding box check for demonstration purposes
        return self.x - self.radius <= point.x() <= self.x + self.radius and self.y - self.radius <= point.y() <= self.y + self.radius

class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

class MyPaintArea(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        self.image: QImage = QImage(640, 480, QImage.Format_RGB32)
        self.image.fill(QColor(255, 255, 255))
        self.scene = Scene()
        self.selected_object = None
        self.last_mouse_position = QPointF()

    def load_image(self, filename):
        self.image = QImage(filename)
        self.update()

    def paintEvent(self, event):
        painter: QPainter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.render_scene(painter, QRectF(0, 0, self.width(), self.height()), QRectF(0, 0, 640, 480))

    def render_scene(self, painter, viewport, world_rect):
        painter.setRenderHint(QPainter.Antialiasing)

        scale_x = viewport.width() / world_rect.width()
        scale_y = viewport.height() / world_rect.height()
        scale = min(scale_x, scale_y)

        painter.scale(scale, scale)
        painter.translate(-world_rect.left(), -world_rect.top())

        for obj in self.scene.objects:
            if isinstance(obj, Rectangle):
                painter.setBrush(QColor(*obj.fill_color))
                painter.setPen(QColor(*obj.border_color))
                painter.drawRect(obj.x, obj.y, obj.width, obj.height)
            elif isinstance(obj, Circle):
                painter.setBrush(QColor(*obj.fill_color))
                painter.setPen(QColor(*obj.border_color))
                painter.drawEllipse(obj.x - obj.radius, obj.y - obj.radius, 2 * obj.radius, 2 * obj.radius)
            elif isinstance(obj, Star):
                painter.setBrush(QColor(*obj.fill_color))
                painter.setPen(QColor(*obj.border_color))
                self.draw_star(painter, obj)

    def draw_star(self, painter, star):
        points = []
        angle = math.pi / star.points  # Winkel für einen Sternzacken

        for i in range(2 * star.points):
            r = star.radius if i % 2 == 0 else star.radius / 2
            theta = i * angle
            x = star.x + r * math.cos(theta)
            y = star.y + r * math.sin(theta)
            points.append(QPointF(x, y))
        
        painter.drawPolygon(points)

    def rectangle(self):
        self.scene.add_object(Rectangle(50, 50, 100, 150, (255, 0, 0), (0, 0, 0)))
        self.update()
    
    def circle(self):
        self.scene.add_object(Circle(400, 200, 80, (255, 255, 0), (0, 0, 0)))
        self.update()

    def star(self):
        self.scene.add_object(Star(550, 300, 70, 7, (255, 0, 255), (0, 0, 0), 1402))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected_object = self.find_object_at(event.position())
            self.last_mouse_position = event.position()

    def mouseMoveEvent(self, event):
        if self.selected_object:
            dx = event.position().x() - self.last_mouse_position.x()
            dy = event.position().y() - self.last_mouse_position.y()
            self.last_mouse_position = event.position()

            if isinstance(self.selected_object, (Rectangle, Circle, Star)):
                self.selected_object.x += dx
                self.selected_object.y += dy

            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected_object = None

    def find_object_at(self, position):
        for obj in self.scene.objects:
            if obj.contains(position):
                return obj
        return None

class MyWindow(QMainWindow):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.paint_area: MyPaintArea = MyPaintArea(self)
        layout = QVBoxLayout()
        layout.addWidget(self.paint_area)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        #menüs und aktionen
        self.file_menu: QMenuBar = self.menuBar().addMenu("File")
        self.help_menu: QMenuBar = self.menuBar().addMenu("Help")
        self.open_action = self.file_menu.addAction("Open File")
        self.open_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_O))
        self.saveAs_action = self.file_menu.addAction("Save As...")
        self.saveAs_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_S))
        self.quit_action = self.file_menu.addAction("Quit")
        self.quit_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Q))
        self.info_action = self.help_menu.addAction("Info")
        self.info_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_I))

        self.open_action.triggered.connect(self.load_file)
        self.saveAs_action.triggered.connect(self.save_file)
        self.info_action.triggered.connect(self.show_info)
        self.quit_action.triggered.connect(self.show_quit_warning)
        
        #toolbar
        self.nice_toolbar: QToolBar = self.addToolBar("Some Nice Tools")
        self.nice_toolbar.addAction("Open", self.load_file)
        self.nice_toolbar.addAction("Save", self.save_file)
        self.nice_toolbar.addAction("Info", self.show_info)
        self.nice_toolbar.addAction("Quit", self.show_quit_warning)
        self.nice_toolbar.addAction("Rectangle", self.paint_area.rectangle)
        self.nice_toolbar.addAction("Circle", self.paint_area.circle)
        self.nice_toolbar.addAction("Star", self.paint_area.star)

    def show_quit_warning(self):
        ret = QMessageBox.question(self, "Ufpasse!", "Möchtest Du das Programm wirklich schließen? :(", QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.close()
        else:
            print("Programm wird fortgesetzt")
    
    def show_info(self):
        QMessageBox.information(self, "Info", "Eine super nützliche Information...", QMessageBox.Ok)

    def load_file(self):
        file_name, selected_filter = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG Files (*.png)")
        if file_name:
            self.paint_area.load_image(file_name)

    def save_file(self):
        file_name, selected_filter = QFileDialog.getSaveFileName(self, "Save As", "picture", "PNG Files (*.png)")
        if file_name:
            self.paint_area.image.save(file_name)

if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    main_window: MyWindow = MyWindow(None)
    main_window.setWindowTitle("Vektorgraphik Editor")
    main_window.show()
    app.exec()
