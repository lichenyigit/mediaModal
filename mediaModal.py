import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import QColor, QPainter, QPen, QPolygon, QCursor, QIcon

class OverlayWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # 设置窗口图标
            self.setWindowIcon(QIcon('modal.ico'))
            # 设置窗口无边框，但保留任务栏图标
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            # 设置窗口背景透明
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            # 优化拖动性能
            self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
            self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
            
            # 设置默认大小和位置
            screen = QApplication.primaryScreen().geometry()
            self.setGeometry(
                (screen.width() - 800) // 2,  # 水平居中
                screen.height() - 150,        # 距离底部50px (150 = 100高度 + 50距离)
                800,                          # 宽度
                50                           # 高度
            )
            
            # 创建关闭按钮
            self.close_button = QPushButton('×', self)
            self.close_button.setGeometry(self.width() - 30, 0, 30, 30)
            self.close_button.setStyleSheet("""
                QPushButton {
                    background-color: #000000;
                    color: #000000;
                    border: none;
                    font-size: 20px;
                    font-weight: bold;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #333333;
                }
                QPushButton:pressed {
                    background-color: #666666;
                }
            """)
            self.close_button.clicked.connect(self.close)
            
            # 用于窗口拖动的变量
            self.dragging = False
            self.drag_position = QPoint()
            self.last_mouse_pos = QPoint()
            
            # 用于调整大小的变量
            self.resizing = False
            self.resize_edge = None
            self.resize_margin = 10
            self.resize_indicator_size = 8
            
            # 启用鼠标追踪以获得更流畅的移动
            self.setMouseTracking(True)
        except Exception as e:
            QMessageBox.critical(None, "错误", f"初始化失败: {str(e)}")
            raise

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 255))
            
            if self.width() > 30 and self.height() > 30:
                indicator_points = QPolygon([
                    QPoint(self.width() - self.resize_indicator_size, self.height()),
                    QPoint(self.width(), self.height()),
                    QPoint(self.width(), self.height() - self.resize_indicator_size)
                ])
                painter.setPen(QPen(QColor(100, 100, 100), 1))
                painter.setBrush(QColor(150, 150, 150))
                painter.drawPolygon(indicator_points)
        except Exception as e:
            event.accept()

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.is_in_resize_area(event.pos()):
                    self.resizing = True
                    self.resize_edge = 'corner'
                    self.drag_position = event.pos()
                    self.start_geometry = self.geometry()
                else:
                    self.dragging = True
                    # 记录鼠标按下时的位置
                    self.last_mouse_pos = event.globalPosition().toPoint()
                    self.drag_position = self.frameGeometry().topLeft()
        except Exception as e:
            self.dragging = False
            self.resizing = False
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if self.dragging:
                # 计算鼠标移动的偏移量
                current_pos = event.globalPosition().toPoint()
                delta = current_pos - self.last_mouse_pos
                new_pos = self.drag_position + delta
                self.move(new_pos)
            elif self.resizing and hasattr(self, 'start_geometry'):
                delta = event.pos() - self.drag_position
                new_width = max(200, self.start_geometry.width() + delta.x())
                new_height = max(50, self.start_geometry.height() + delta.y())
                self.setGeometry(self.start_geometry.x(), self.start_geometry.y(), new_width, new_height)
                self.close_button.setGeometry(self.width() - 30, 0, 30, 30)
            else:
                # 更新鼠标光标
                if self.is_in_resize_area(event.pos()):
                    self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                else:
                    self.setCursor(Qt.CursorShape.ArrowCursor)
        except Exception as e:
            self.dragging = False
            self.resizing = False
            event.accept()

    def mouseReleaseEvent(self, event):
        try:
            self.dragging = False
            self.resizing = False
            self.resize_edge = None
            if hasattr(self, 'start_geometry'):
                delattr(self, 'start_geometry')
        except Exception as e:
            event.accept()

    def is_in_resize_area(self, pos):
        try:
            resize_rect = QRect(
                self.width() - self.resize_margin,
                self.height() - self.resize_margin,
                self.resize_margin,
                self.resize_margin
            )
            return resize_rect.contains(pos)
        except Exception as e:
            return False
        
    def enterEvent(self, event):
        try:
            if self.is_in_resize_area(event.pos()):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        except Exception as e:
            event.accept()
            
    def leaveEvent(self, event):
        try:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        except Exception as e:
            event.accept()
        
    def mouseDoubleClickEvent(self, event):
        try:
            if self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint:
                self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            else:
                self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.show()
        except Exception as e:
            event.accept()

    def resizeEvent(self, event):
        try:
            super().resizeEvent(event)
            self.close_button.setGeometry(self.width() - 30, 0, 30, 30)
        except Exception as e:
            event.accept()

def main():
    try:
        app = QApplication(sys.argv)
        
        # 设置应用程序图标（这会影响任务栏图标）
        app.setWindowIcon(QIcon('modal.ico'))
        
        window = OverlayWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "严重错误", f"程序发生严重错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 