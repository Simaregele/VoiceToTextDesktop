import sys
import logging
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QStyle
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from app.background_app import BackgroundApp
from app.config import get_config_value
from app.utils import delete_all_files_in_directories


class TrayApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        logging.debug("Инициализация TrayApp")
        self.setQuitOnLastWindowClosed(False)
        self.background_app = BackgroundApp(argv)  # Изменено с self на argv

        # Создаем иконку в трее
        logging.debug("Создание иконки в трее")
        icon_path = "icon.png"
        if QIcon(icon_path).isNull():
            logging.warning(f"Файл иконки {icon_path} не найден. Используем стандартную иконку.")
            self.tray_icon = QSystemTrayIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon), self)
        else:
            self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)

        self.create_tray_menu()
        self.tray_icon.show()
        logging.debug("Иконка в трее создана и отображена")

        # Показываем сообщение о запуске
        QTimer.singleShot(100, self.show_startup_message)

    def create_tray_menu(self):
        logging.debug("Создание меню трея")
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.quit)
        self.tray_icon.setContextMenu(menu)
        logging.debug("Меню трея создано")

    def show_startup_message(self):
        logging.debug("Отображение стартового сообщения")
        hotkey = get_config_value('HOTKEY', 'ctrl+shift+alt+space')
        self.tray_icon.showMessage("Приложение запущено",
                                   f"Используйте {hotkey} для начала записи",
                                   QSystemTrayIcon.MessageIcon.Information)
        logging.debug("Стартовое сообщение отображено")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("Запуск приложения")

    app = TrayApp(sys.argv)

    temp_dirs = get_config_value('TEMP_DIRECTORIES', [])
    delete_all_files_in_directories(temp_dirs)

    logging.info("Приложение запущено")
    sys.exit(app.exec())