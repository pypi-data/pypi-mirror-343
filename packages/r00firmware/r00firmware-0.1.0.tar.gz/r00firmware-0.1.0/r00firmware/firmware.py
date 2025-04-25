import time
from pathlib import Path

from adb import adb_utils
from adb.helpers.exceptions import ADBConnectionError
from logger import log
from system import run
from dialoger import msg
from adb import exceptions

class Firmware:
    def process_stock(self, source: str):
        srcdir = Path(source)
        if not srcdir.is_dir():
            raise ValueError(f"Указанный путь '{source}' не является директорией.")

        found_files = {}
        search_patterns = {
            "AP": "AP_*.tar.md5",
            "BL": "BL_*.tar.md5",
            "CP": "CP_*.tar.md5",
            "CSC": "CSC_*.tar.md5",
        }

        # Поиск каждого типа файла
        for file_type, pattern in search_patterns.items():
            log.trace(f"Ищем файл типа {file_type} с паттерном '{pattern}' в '{srcdir}'")
            matches = list(srcdir.glob(pattern))

            if not matches:
                log.error(f"Не найден необходимый файл для {file_type} по паттерну '{pattern}' в директории '{srcdir}'")
                raise FileNotFoundError(f"Не найден файл {file_type} (паттерн: '{pattern}') в '{srcdir}'")
            elif len(matches) > 1:
                log.warning(
                    f"Найдено несколько файлов для {file_type} по паттерну '{pattern}': {matches}")
                raise ValueError(f"Найдено несколько подходящих файлов для {file_type} (паттерн: '{pattern}')")
            else:
                log.debug(f"Найден файл для {file_type}: {Path(matches[0]).name}")
                found_files[file_type] = matches[0]

        # Убедимся, что все 4 файла были найдены (хотя предыдущий цикл уже должен был выбросить ошибку, если какой-то не найден)
        if len(found_files) != len(search_patterns):
            missing_types = [ftype for ftype in search_patterns if ftype not in found_files]
            log.critical(f"Не удалось найти все необходимые типы файлов. Отсутствуют: {missing_types}")
            raise FileNotFoundError(f"Не удалось найти все необходимые файлы прошивки. Отсутствуют: {missing_types}")

        log.info("Все необходимые файлы прошивки успешно найдены.")

        # Получаем найденные пути для каждого файла
        ap_file = found_files["AP"]
        bl_file = found_files["BL"]
        cp_file = found_files["CP"]
        csc_file = found_files["CSC"]

        command = (
            f"odin4 -a \"{ap_file}\" "
            f"-b \"{bl_file}\" "
            f"-c \"{cp_file}\" "
            f"-s \"{csc_file}\""
        )

        try:
            log.info("Начинаем прошивать телефон на сток...")
            run(command, timeout=2000)
            log.info("✨✨✨ Прошивка успешно выполнена! ✨✨✨")
        except Exception as e:
            log.error(e)
            raise

    @staticmethod
    def process_custom(device: str = None, local: str = None, format_data: bool = False):
        adb_utils.restart_server()
        status = adb_utils.get_status_device()
        if status == 'device':
            adb_utils.reboot(recovery_mode=True, sleep_after_reboot=15)
        elif status == 'recovery':
            log.trace("Телефон в режиме recovery")
        else:
            raise ADBConnectionError("Не удалось найти телефон. Проверь соединение")

        adb = adb_utils.connect_device()

        if format_data:
            log.info("Форматируем телефон...")
            adb.twrp.wipe()
            adb.twrp.format_data()
            adb.twrp.mount('data')

        if local:
            log.info("Пушим прошивку...")
            adb.push(local, '/sdcard/firmware.zip', timeout=1500)
            device = '/sdcard/firmware.zip'

        log.info("Устанавливаем прошивку...")
        adb.twrp.install_zip(device)

    @staticmethod
    def process_recovery(recovery):
        mode = adb_utils.get_samsung_mode_device()

        if mode == 'no_connect':
            raise exceptions.ADBConnectionError("Не удалось найти телефон. Проверь соединение")

        if not mode == 'download':
            adb_utils.reboot(download_mode=True)

        recovery_tar = Path(recovery)
        if not recovery_tar.is_file():
            raise FileNotFoundError(f"Файл прошивки не найден: {recovery_tar}")

        message = "Зажимай bixby + volume up + power"
        log.warning(message)
        run(f"odin4 -a \"{recovery_tar}\"")
        msg(message)


if __name__ == '__main__':
    f = Firmware()
    exit()
    # f.process_recovery(
    #     recovery='/media/user/Android/Devices/GalaxyS8/TWRP/twrp-3.5.2_9-0-dreamlte.img.tar'
    # )

    f.process_custom(
        local='/media/user/Android/Devices/GalaxyS8/Fireware/Android_9.0_SDK28/horizon_rom/original/firmware.zip'
    )
