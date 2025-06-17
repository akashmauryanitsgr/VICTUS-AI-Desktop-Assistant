import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QGraphicsOpacityEffect, QDesktopWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer

class InputWindow(QWidget):
    
    def __init__(self,query):
        super().__init__()
        self.query = query
        self.setWindowTitle("Victus Input")
        self.setFixedSize(600, 280)  # Increased size
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                border-radius: 12px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                padding: 10px;
                font-size: 30px;
                border: 2px solid #3e3e55;
                border-radius: 8px;
                background-color: #2c2c3c;
                color: white;
            }
            QPushButton {
                background-color: #1abc9c;
                color: white;
                font-weight: bold;
                font-size: 20px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        self.user_input = None
        self.init_ui()
        self.center_window()
        self.animate_entry()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel(f"Enter your {self.query}:")
        self.label.setFont(QFont("Segoe UI", 18))
        self.label.setAlignment(Qt.AlignCenter)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Segoe UI", 30))

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.on_send)

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

    def center_window(self):
        screen = QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2 - 50  # Slightly higher for animation effect
        self.move(x, y)

    def animate_entry(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(600)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.start()

        start_pos = QPoint(self.x(), self.y() - 30)
        end_pos = QPoint(self.x(), self.y())
        self.move(start_pos)

        self.move_animation = QPropertyAnimation(self, b"pos")
        self.move_animation.setDuration(600)
        self.move_animation.setStartValue(start_pos)
        self.move_animation.setEndValue(end_pos)
        QTimer.singleShot(0, self.move_animation.start)

    def on_send(self):
        text = self.input_field.text().strip()
        if text:
            self.user_input = text
            self.close()
        else:
            QMessageBox.warning(self, "Empty", "Please enter something before sending.")

    def get_input(self):
        return self.user_input

# Function to call the window and get input
def get_user_input(query):
    app = QApplication(sys.argv)
    window = InputWindow(query=query)
    window.show()
    app.exec_()
    return window.get_input()

# Example usage
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "input"
    result = get_user_input(query=query)
    print(result)

