"""
Основной скрипт для запуска парсера данных из ВКонтакте.

Функциональность:
- Сбор информации о пользователях
- Получение последних постов пользователей
- Сбор сообществ, в которых состоят пользователи
- Обход социального графа с настраиваемой глубиной
- Асинхронные запросы для повышения производительности
- Сохранение прогресса и возможность возобновления работы

Вы можете использовать этот модуль через командную строку:
    $ vk-parser --config path/to/config.ini

Или импортировать в свой код:
    from vk_parser.main import run_parser
    await run_parser(config_path="config.ini", resume=True)
"""
import os
import sys
import asyncio
import argparse
import logging
from pathlib import Path

from vk_parser.config.settings import load_config
from vk_parser.collector import VKDataCollector
from vk_parser.utils.logging_setup import setup_logging, get_logger
from vk_parser.utils.state_manager import StateManager


def parse_args():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description='VK Data Parser')
    
    parser.add_argument(
        '--config', '-c',
        default='config.ini',
        help='Path to config file'
    )
    
    parser.add_argument(
        '--log', '-l',
        default=None,
        help='Path to log file'
    )
    
    parser.add_argument(
        '--log-dir', 
        default='logs',
        help='Directory for log files'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--resume', '-r',
        action='store_true',
        help='Resume collection from last saved state'
    )
    
    parser.add_argument(
        '--state-file', '-s',
        default='vk_parser_state.json',
        help='Path to state file for resume'
    )
    
    parser.add_argument(
        '--clear', 
        action='store_true',
        help='Clear saved state before starting'
    )
    
    return parser.parse_args()


async def run_parser(config_path="config.ini", log_file=None, log_dir="logs", 
                     debug=False, resume=False, state_file="vk_parser_state.json", 
                     clear=False):
    """
    Функция для запуска парсера из Python-кода.
    
    Args:
        config_path: Путь к файлу конфигурации
        log_file: Путь к файлу лога
        log_dir: Директория для логов
        debug: Включить режим отладки
        resume: Возобновить сбор данных с последнего состояния
        state_file: Путь к файлу состояния
        clear: Очистить сохраненное состояние перед запуском
    
    Returns:
        int: Код возврата (0 - успех, другое - ошибка)
    """
    # Настраиваем логирование
    log_level = logging.DEBUG if debug else logging.INFO
    log_file_path = setup_logging(log_file, log_level, log_dir)
    logger = get_logger(__name__)
    
    logger.info("Starting VK Parser")
    logger.info(f"Logs will be saved to: {log_file_path}")
    
    # Проверяем опции возобновления/очистки состояния
    state_manager = StateManager(state_file)
    
    if clear and state_manager.has_saved_state():
        state_manager.clear_state()
        logger.info("Saved state cleared")
    
    if resume and not state_manager.has_saved_state():
        logger.warning("Unable to resume: no saved state found")
        if not clear:
            logger.info("Starting new collection")
    
    try:
        # Загружаем конфигурацию
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            return 1
        
        config = load_config(config_path)
        logger.info(f"Config loaded from {config_path}")
        
        # Проверяем наличие токена и ID пользователя
        if config.access_token == "paste token from api" or config.access_token == "your_token_here":
            logger.error("Please set your access token in config.ini")
            return 1
        
        if config.start_user_id == "paste start user id" or config.start_user_id == "your_user_id_here":
            logger.error("Please set your start user ID in config.ini")
            return 1
        
        # Создаем и запускаем сборщик данных
        collector = VKDataCollector(
            config, 
            resume=resume, 
            state_file=state_file
        )
        await collector.run()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        return 0
    except Exception as e:
        logger.exception(f"Error: {e}")
        return 1


async def main():
    """Основная функция запуска приложения из командной строки."""
    args = parse_args()
    
    exit_code = await run_parser(
        config_path=args.config,
        log_file=args.log,
        log_dir=args.log_dir,
        debug=args.debug,
        resume=args.resume,
        state_file=args.state_file,
        clear=args.clear
    )
    
    sys.exit(exit_code)


def cli_main():
    """
    Точка входа для запуска из командной строки через pip-пакет.
    Эта функция используется в entrypoint в setup.py.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 