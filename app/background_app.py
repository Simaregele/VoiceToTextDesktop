import logging
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, QObject, pyqtSlot, pyqtSignal
import keyboard
import pyperclip
from app.voice_recorder import VoiceRecorderThread
from app.ui_components import FloatingStopButton
from app.config import get_config_value
import win32gui
import win32api
import win32con
import win32process

class WindowHandler(QObject):
    show_window_signal = pyqtSignal(QObject)

    def __init__(self):
        super().__init__()
        self.show_window_signal.connect(self.show_window)

    @pyqtSlot(QObject)
    def show_window(self, window):
        if window:
            window.show()
            logging.debug(f"Окно {type(window).__name__} показано")
            QTimer.singleShot(100, lambda: self.check_window_visibility(window))
        else:
            logging.error("window is None в show_window")

    def check_window_visibility(self, window):
        if window:
            visible = window.isVisible()
            logging.debug(f"Видимость окна {type(window).__name__}: {visible}")
            if not visible:
                logging.warning(f"Окно {type(window).__name__} не видимо, пробуем показать снова")
                window.show()
        else:
            logging.error("window is None в check_window_visibility")


class BackgroundApp(QApplication):
    close_button_signal = pyqtSignal()

    def __init__(self, argv):
        super().__init__(argv)
        logging.debug("Инициализация BackgroundApp")
        self.tray_icon = QSystemTrayIcon(QIcon("../icon.png"), self)
        self.create_tray_menu()
        self.tray_icon.show()

        self.recording = False
        self.recorder_thread = None
        self.floating_button = None
        self.is_processing = False
        self.is_stopping = False
        self.recording_duration = 0

        self.hotkey = get_config_value('HOTKEY', 'ctrl+shift+alt+space')
        self.setup_hotkey()

        self.window_handler = WindowHandler()
        self.window_handler.moveToThread(self.thread())

        self.close_button_signal.connect(self.close_floating_button)

        # Новые атрибуты для отслеживания активного окна и позиции каретки
        self.active_window_handle = None
        self.caret_position = None

        self.tray_icon.showMessage("Приложение запущено", f"Используйте {self.hotkey} для начала записи",
                                   QSystemTrayIcon.MessageIcon.Information)
        logging.info("Приложение инициализировано")


    def create_tray_menu(self):
        logging.debug("Создание меню трея")
        menu = QMenu()
        test_action = menu.addAction("Проверка горячих клавиш")
        test_action.triggered.connect(self.test_hotkey)
        exit_action = menu.addAction("Выход")
        exit_action.triggered.connect(self.quit)
        self.tray_icon.setContextMenu(menu)

    def setup_hotkey(self):
        logging.debug(f"Настройка горячей клавиши: {self.hotkey}")
        try:
            keyboard.add_hotkey(self.hotkey, self.toggle_recording)
            logging.info(f"Горячая клавиша {self.hotkey} успешно настроена")
        except Exception as e:
            logging.error(f"Ошибка при настройке горячей клавиши: {e}")
            self.tray_icon.showMessage("Ошибка", f"Не удалось настроить горячую клавишу {self.hotkey}",
                                       QSystemTrayIcon.MessageIcon.Warning)

    def test_hotkey(self):
        logging.debug("Тестирование горячей клавиши")
        self.tray_icon.showMessage("Тест горячих клавиш", f"Нажмите {self.hotkey}",
                                   QSystemTrayIcon.MessageIcon.Information)

    def toggle_recording(self):
        logging.debug("Вызван метод toggle_recording")
        if self.is_processing:
            logging.debug("Предыдущий вызов еще обрабатывается, игнорируем")
            return

        self.is_processing = True
        logging.debug("Горячая клавиша нажата")

        try:
            if not self.recording:
                self.start_recording()
            else:
                self.stop_recording()
        finally:
            self.is_processing = False
            logging.debug("Завершена обработка в toggle_recording")

    def init_recorder_thread(self):
        self.recorder_thread = VoiceRecorderThread()
        self.recorder_thread.finished.connect(self.on_recording_finished)
        self.recorder_thread.update_time.connect(self.update_recording_time)

    def start_recording(self):
        logging.debug("Начало записи")
        self.recording = True
        self.save_active_window_info()
        self.init_recorder_thread()
        self.recorder_thread.start()

        self.floating_button = FloatingStopButton(self.stop_recording)
        self.window_handler.show_window_signal.emit(self.floating_button)

        self.tray_icon.showMessage("Запись", "Начата запись голоса", QSystemTrayIcon.MessageIcon.Information)
        logging.info("Запись начата")

    def stop_recording(self):
        if self.is_stopping:
            logging.debug("Остановка уже в процессе")
            return

        self.is_stopping = True
        logging.debug("Начало остановки записи")
        if self.recording:
            self.recording = False
            if self.recorder_thread:
                logging.debug("Остановка потока записи")
                self.recorder_thread.stop()
                if not self.recorder_thread.wait(30000):  # Ждем максимум 30 секунд
                    logging.error("Не удалось остановить поток записи")
                    self.recorder_thread.terminate()
                logging.debug("Поток записи остановлен")

            self.close_button_signal.emit()

            self.tray_icon.showMessage("Запись", f"Запись остановлена. Длительность: {self.recording_duration} сек",
                                       QSystemTrayIcon.MessageIcon.Information)
            logging.info(f"Запись остановлена. Длительность: {self.recording_duration} сек")
        else:
            logging.warning("Попытка остановить запись, когда она не идет")
        self.is_stopping = False

    def save_active_window_info(self):
        self.active_window_handle = win32gui.GetForegroundWindow()
        _, thread_id = win32process.GetWindowThreadProcessId(self.active_window_handle)
        self.caret_position = win32gui.GetCaretPos()
        logging.debug(f"Сохранена информация об активном окне: handle={self.active_window_handle}, caret={self.caret_position}")

    def on_recording_finished(self, text):
        logging.debug("Запись завершена, обработка результата")
        try:
            print(f"Транскрибированный текст (длительность {self.recording_duration} сек):")
            print(text)  # Вывод в консоль
            pyperclip.copy(text)  # Копирование в буфер обмена

            self.insert_text_at_caret(text)

            self.tray_icon.showMessage("Транскрипция",
                                       f"Текст (длительность {self.recording_duration} сек) скопирован в буфер обмена и вставлен в активное окно",
                                       QSystemTrayIcon.MessageIcon.Information)
            logging.info("Транскрипция завершена, скопирована в буфер обмена и вставлена в активное окно")
        except Exception as e:
            logging.error(f"Ошибка при обработке результата записи: {e}")

    def insert_text_at_caret(self, text):
        if self.active_window_handle and win32gui.IsWindow(self.active_window_handle):
            win32gui.SetForegroundWindow(self.active_window_handle)
            keyboard.write(text)
            logging.debug(f"Текст вставлен в активное окно")
        else:
            logging.warning("Не удалось вставить текст: активное окно недоступно")

    def update_recording_time(self, seconds):
        self.recording_duration = seconds
        if self.floating_button:
            self.floating_button.update_time(seconds)

    @pyqtSlot()
    def close_floating_button(self):
        logging.debug("Закрытие кнопки остановки")
        if self.floating_button:
            try:
                self.floating_button.hide()  # Сначала скрываем кнопку
                QTimer.singleShot(100, self.floating_button.deleteLater)  # Затем удаляем ее через небольшую задержку
                self.floating_button = None
                logging.debug("Кнопка остановки закрыта")
            except Exception as e:
                logging.error(f"Ошибка при закрытии кнопки остановки: {e}")