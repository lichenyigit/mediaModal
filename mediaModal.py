import sys
import json
import ctypes
from ctypes import wintypes
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QPoint, QRect, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QPolygon, QCursor, QIcon, QPainterPath

# Windows API函数
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def load_config():
    """加载配置文件"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载配置文件失败: {str(e)}")
        # 返回默认配置
        return {
            "front_detection": {
                "interval_ms": 100,
                "enabled": True,
                "log_enabled": True
            },
            "window": {
                "default_width": 800,
                "default_height": 50,
                "min_width": 200,
                "min_height": 50,
                "position": {
                    "x": "center",
                    "y": "bottom",
                    "margin_bottom": 50
                },
                "rounded_corners": {
                    "enabled": True,
                    "radius": 10
                }
            },
            "ui": {
                "close_button_size": 30,
                "resize_margin": 10,
                "resize_indicator_size": 8,
                "show_resize_indicator": True # 新增配置项
            }
        }

class OverlayWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            
            # 加载配置
            self.config = load_config()
            
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
            window_config = self.config["window"]
            ui_config = self.config["ui"]
            
            self.setGeometry(
                (screen.width() - window_config["default_width"]) // 2,  # 水平居中
                screen.height() - window_config["default_height"] - window_config["position"]["margin_bottom"],  # 距离底部
                window_config["default_width"],                          # 宽度
                window_config["default_height"]                         # 高度
            )
            
            # 创建关闭按钮
            self.close_button = QPushButton('×', self)
            close_button_size = ui_config["close_button_size"]
            
            # 获取圆角配置
            rounded_config = self.config["window"]["rounded_corners"]
            corner_radius = rounded_config["radius"] if rounded_config["enabled"] else 0
            
            # 调整关闭按钮位置，避免覆盖圆角
            button_x = self.width() - close_button_size - corner_radius
            button_y = corner_radius
            self.close_button.setGeometry(button_x, button_y, close_button_size, close_button_size)
            
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
            self.resize_margin = ui_config["resize_margin"]
            self.resize_indicator_size = ui_config["resize_indicator_size"]
            
            # 启用鼠标追踪以获得更流畅的移动
            self.setMouseTracking(True)
            
            # 初始化检测定时器
            self.init_front_detection()
        except Exception as e:
            QMessageBox.critical(None, "错误", f"初始化失败: {str(e)}")
            raise

    def init_front_detection(self):
        """初始化前台检测功能"""
        try:
            front_config = self.config["front_detection"]
            
            if front_config["enabled"]:
                # 创建定时器，使用配置的间隔时间
                self.front_detection_timer = QTimer()
                self.front_detection_timer.timeout.connect(self.check_if_frontmost)
                self.front_detection_timer.start(front_config["interval_ms"])
                
                # 记录当前窗口句柄
                self.window_handle = self.winId()
                self.is_frontmost = False
                self.log_enabled = front_config["log_enabled"]
            else:
                print("前台检测功能已禁用")
        except Exception as e:
            print(f"初始化前台检测失败: {str(e)}")

    def check_if_frontmost(self):
        """检测当前窗口是否在最前面"""
        try:
            # 获取当前前台窗口句柄
            foreground_hwnd = user32.GetForegroundWindow()
            
            # 获取当前窗口句柄
            current_hwnd = int(self.winId())
            
            # 检查是否是最前面的窗口
            is_front = (foreground_hwnd == current_hwnd)
            
            # 如果状态发生变化，输出日志
            if is_front != self.is_frontmost:
                self.is_frontmost = is_front
                if self.log_enabled:
                    if is_front:
                        print("=== 窗口已切换到前台 ===")
                    else:
                        print("=== 窗口已切换到后台 ===")
                    
        except Exception as e:
            print(f"检测前台状态失败: {str(e)}")

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            
            # 获取圆角配置
            rounded_config = self.config["window"]["rounded_corners"]
            ui_config = self.config["ui"]
            
            if rounded_config["enabled"]:
                # 创建圆角路径
                path = QPainterPath()
                radius = rounded_config["radius"]
                
                # 绘制圆角矩形
                path.addRoundedRect(self.rect(), radius, radius)
                
                # 填充背景
                painter.fillPath(path, QColor(0, 0, 0, 255))
                
                # 绘制调整大小指示器（如果启用）
                if ui_config.get("show_resize_indicator", False) and self.width() > 30 and self.height() > 30:
                    # 调整指示器位置以适应圆角，避免覆盖圆角区域
                    indicator_x = self.width() - self.resize_indicator_size - radius - 2
                    indicator_y = self.height() - self.resize_indicator_size - radius - 2
                    
                    # 确保指示器不会超出窗口边界
                    indicator_x = max(indicator_x, radius + 5)
                    indicator_y = max(indicator_y, radius + 5)
                    
                    indicator_points = QPolygon([
                        QPoint(indicator_x, self.height() - radius - 2),
                        QPoint(self.width() - radius - 2, self.height() - radius - 2),
                        QPoint(self.width() - radius - 2, indicator_y)
                    ])
                    painter.setPen(QPen(QColor(0, 0, 0), 1))
                    painter.setBrush(QColor(0, 0, 0))
                    painter.drawPolygon(indicator_points)
            else:
                # 原来的矩形绘制方式
                painter.fillRect(self.rect(), QColor(0, 0, 0, 255))
                
                # 绘制调整大小指示器（如果启用）
                if ui_config.get("show_resize_indicator", False) and self.width() > 30 and self.height() > 30:
                    indicator_points = QPolygon([
                        QPoint(self.width() - self.resize_indicator_size, self.height()),
                        QPoint(self.width(), self.height()),
                        QPoint(self.width(), self.height() - self.resize_indicator_size)
                    ])
                    painter.setPen(QPen(QColor(0, 0, 0), 1))
                    painter.setBrush(QColor(0, 0, 0))
                    painter.drawPolygon(indicator_points)
        except Exception as e:
            event.accept()

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.is_in_resize_area(event.position().toPoint()):
                    self.resizing = True
                    self.resize_edge = 'corner'
                    self.drag_position = event.position().toPoint()
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
                delta = event.position().toPoint() - self.drag_position
                new_width = max(200, self.start_geometry.width() + delta.x())
                new_height = max(50, self.start_geometry.height() + delta.y())
                self.setGeometry(self.start_geometry.x(), self.start_geometry.y(), new_width, new_height)
                self.update_close_button_position()
            else:
                # 更新鼠标光标
                if self.is_in_resize_area(event.position().toPoint()):
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

    def update_close_button_position(self):
        """更新关闭按钮位置以适应圆角"""
        try:
            ui_config = self.config["ui"]
            close_button_size = ui_config["close_button_size"]
            rounded_config = self.config["window"]["rounded_corners"]
            corner_radius = rounded_config["radius"] if rounded_config["enabled"] else 0
            
            # 调整关闭按钮位置，避免覆盖圆角
            button_x = self.width() - close_button_size - corner_radius
            button_y = corner_radius
            self.close_button.setGeometry(button_x, button_y, close_button_size, close_button_size)
        except Exception as e:
            print(f"更新关闭按钮位置失败: {str(e)}")

    def is_in_resize_area(self, pos):
        try:
            # 获取圆角配置
            rounded_config = self.config["window"]["rounded_corners"]
            corner_radius = rounded_config["radius"] if rounded_config["enabled"] else 0
            
            # 调整调整大小区域，避免与圆角重叠
            margin = self.resize_margin + corner_radius
            resize_rect = QRect(
                self.width() - margin,
                self.height() - margin,
                margin,
                margin
            )
            return resize_rect.contains(pos)
        except Exception as e:
            return False
        
    def enterEvent(self, event):
        try:
            if self.is_in_resize_area(event.position().toPoint()):
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
            self.update_close_button_position()
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