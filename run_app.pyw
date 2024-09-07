import sys
import logging
from main import TrayApp

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("Запуск приложения из run_app.pyw")

    app = TrayApp(sys.argv)
    sys.exit(app.exec())