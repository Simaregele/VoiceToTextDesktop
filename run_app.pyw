import os
import sys
import logging

# Устанавливаем текущую директорию в директорию скрипта
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Добавляем текущую директорию в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Запуск приложения из run_app.pyw")

from main import TrayApp

if __name__ == "__main__":
    app = TrayApp(sys.argv)
    sys.exit(app.exec())