import json

def export_config():
    try:
        with open("app/config.json", "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("Файл конфигурации не найден.")
        return {}
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON файла.")
        return {}

def get_config_value(key, default=None):
    config = export_config()
    return config.get(key, default)