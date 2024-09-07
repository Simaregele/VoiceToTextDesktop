from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QGuiApplication

class FloatingStopButton(QWidget):
    def __init__(self, on_stop):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)

        layout = QVBoxLayout()
        self.stop_button = QPushButton("Стоп")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                min-width: 100px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.stop_button.clicked.connect(on_stop)
        layout.addWidget(self.stop_button)

        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                border-radius: 10px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def update_time(self, seconds):
        minutes, secs = divmod(seconds, 60)
        self.time_label.setText(f"{minutes:02d}:{secs:02d}")

    def showEvent(self, event):
        super().showEvent(event)
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def closeEvent(self, event):
        # Переопределяем метод закрытия, чтобы избежать проблем с отрисовкой
        self.hide()
        event.accept()

# class ConfirmRecordingWindow(QWidget):
#     def __init__(self, on_confirm, on_cancel):
#         super().__init__()
#         self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#
#         layout = QVBoxLayout()
#
#         self.label = QLabel("Начать запись?")
#         self.label.setStyleSheet("""
#             QLabel {
#                 color: white;
#                 background-color: rgba(0, 0, 0, 150);
#                 border-radius: 10px;
#                 padding: 10px;
#                 font-size: 16px;
#             }
#         """)
#         layout.addWidget(self.label)
#
#         button_layout = QVBoxLayout()
#
#         self.confirm_button = QPushButton("Да")
#         self.confirm_button.setStyleSheet("""
#             QPushButton {
#                 background-color: green;
#                 color: white;
#                 border-radius: 15px;
#                 font-size: 14px;
#                 min-width: 60px;
#                 min-height: 30px;
#             }
#             QPushButton:hover {
#                 background-color: darkgreen;
#             }
#         """)
#         self.confirm_button.clicked.connect(on_confirm)
#         button_layout.addWidget(self.confirm_button)
#
#         self.cancel_button = QPushButton("Нет")
#         self.cancel_button.setStyleSheet("""
#             QPushButton {
#                 background-color: red;
#                 color: white;
#                 border-radius: 15px;
#                 font-size: 14px;
#                 min-width: 60px;
#                 min-height: 30px;
#             }
#             QPushButton:hover {
#                 background-color: darkred;
#             }
#         """)
#         self.cancel_button.clicked.connect(on_cancel)
#         button_layout.addWidget(self.cancel_button)
#
#         layout.addLayout(button_layout)
#
#         self.setLayout(layout)
#
#     def showEvent(self, event):
#         super().showEvent(event)
#         # Центрируем окно на экране
#         screen = QScreen.availableGeometry(QScreen.primaryScreen())
#         size = self.geometry()
#         self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


