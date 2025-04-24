"""
Модуль для работы с настройками парсера.
"""
from dataclasses import dataclass
from configparser import ConfigParser
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

@dataclass
class VKConfig:
    """Конфигурация для парсера VK."""
    access_token: str
    start_user_id: str
    max_depth: int = 5
    max_users: int = 20000
    batch_size: int = 25
    request_delay: float = 0.35
    save_interval: int = 5000


def load_config(config_path: str = "config.ini") -> VKConfig:
    """Загружает конфигурацию из INI файла.
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        VKConfig: Объект конфигурации
    """
    config = ConfigParser()
    
    # Проверяем существование файла конфигурации
    if not os.path.exists(config_path):
        logger.error(f"Config file not found: {config_path}")
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    try:
        # Читаем файл с явным указанием кодировки UTF-8
        with open(config_path, 'r', encoding='utf-8') as f:
            config.read_file(f)
        
        logger.info(f"Config loaded from {config_path}")
        
        return VKConfig(
            access_token=config["VK"]["access_token"],
            start_user_id=config["VK"]["start_user_id"],
            max_depth=int(config.get("Settings", "max_depth", fallback=5)),
            max_users=int(config.get("Settings", "max_users", fallback=20000)),
            batch_size=int(config.get("Settings", "batch_size", fallback=25)),
            request_delay=float(config.get("Settings", "request_delay", fallback=0.35)),
            save_interval=int(config.get("Settings", "save_interval", fallback=5000))
        )
    except UnicodeDecodeError as e:
        # Если возникла ошибка с UTF-8, пробуем другие кодировки
        logger.warning(f"Failed to read config with UTF-8 encoding, trying cp1251: {e}")
        try:
            with open(config_path, 'r', encoding='cp1251') as f:
                config.read_file(f)
            
            logger.info(f"Config loaded from {config_path} with cp1251 encoding")
            
            return VKConfig(
                access_token=config["VK"]["access_token"],
                start_user_id=config["VK"]["start_user_id"],
                max_depth=int(config.get("Settings", "max_depth", fallback=5)),
                max_users=int(config.get("Settings", "max_users", fallback=20000)),
                batch_size=int(config.get("Settings", "batch_size", fallback=25)),
                request_delay=float(config.get("Settings", "request_delay", fallback=0.35)),
                save_interval=int(config.get("Settings", "save_interval", fallback=5000))
            )
        except Exception as e2:
            logger.error(f"Failed to load config: {e2}")
            raise
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise 