import argparse
from .firmware import Firmware

def handle_stock_command(args):
    firmware_instance = Firmware()
    firmware_instance.process_stock(source=args.source)

def handle_recovery_command(args):
    firmware_instance = Firmware()
    firmware_instance.process_recovery(recovery=args.recovery_filepath)

def handle_custom_command(args):
    if not args.device and not args.local:
        raise ValueError("Укажите путь к файлу прошивки на устройстве или локально.")

    firmware_instance = Firmware()
    if args.device:
        firmware_instance.process_custom(device=args.device, format_data=args.format)
    else:
        firmware_instance.process_custom(local=args.local, format_data=args.format)


def create_parser():
    parser = argparse.ArgumentParser(description="Инструмент для работы с прошивкой телефона.", )
    # parser.add_argument(
    #     "-v", "--verbose",
    #     action="store_true",
    #     help="Включить подробный вывод (применимо ко всем командам)."
    # )

    # Создаем контейнер для субпарсеров (команд)
    # 'dest' сохранит имя выбранной команды в атрибут 'command' объекта args
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        title="Доступные команды",
        description="Выберите одну из команд для выполнения.",
        help="Используйте 'firmware <command> -h' для справки по конкретной команде."
    )
    # Субпарсер для команды 'stock'
    parser_stock = subparsers.add_parser(
        "stock",
        help="Работа со стоковой прошивкой.",
        description="Выполняет операции со стоковой прошивкой для указанной модели."  # Справка для 'firmware stock -h'
    )
    parser_stock.add_argument(
        "--source", '-s',
        type=str,
        required=True,  # <--- Модель обязательна для команды 'stock'
        help="Папка с tar файлами оригинальной прошивки"
    )
    # Устанавливаем функцию-обработчик для этой команды
    parser_stock.set_defaults(func=handle_stock_command)



    # Субпарсер для команды 'custom'
    parser_custom = subparsers.add_parser(
        "custom",
        help="Работа с кастомной прошивкой.",
        description="Устанавливает кастомную прошивку из указанного источника."
    )

    parser_custom.add_argument(
        "--device", '-d',
        type=str,
        required=False,
        help="Путь к файлу .zip на устройстве"
    )

    parser_custom.add_argument(
        "--local", '-l',
        type=str,
        required=False,
        help="Путь к файлу .zip на компьюторе"
    )

    parser_custom.add_argument(
        "--format",
        action='store_true',
        help="Форматирование телефона перед установкой прошивки (true/false). По умолчанию: false."
    )

    parser_custom.set_defaults(func=handle_custom_command)


    # Субпарсер для команды 'recovery'
    parser_recovery = subparsers.add_parser(
        "recovery",
        help="Прошивка кастомного рекавери.",
        description="Устанавливает кастомное рекавери из указанного источника."
    )

    parser_recovery.add_argument('recovery_filepath', type=str, help="Путь к файлу .tar на хосте")

    # Устанавливаем функцию-обработчик для этой команды
    parser_recovery.set_defaults(func=handle_recovery_command)

    return parser