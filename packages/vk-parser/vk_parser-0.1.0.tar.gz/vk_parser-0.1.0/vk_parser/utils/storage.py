"""
Утилиты для хранения данных.
"""
import os
import json
import shutil
import logging
from typing import Dict, List, Any, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class DataStorage:
    """Класс для работы с хранилищем данных."""
    
    def __init__(self, temp_folder: str = "batch_temp", data_folder: str = "data"):
        """
        Инициализирует хранилище данных.
        
        Args:
            temp_folder: Путь к временной папке
            data_folder: Путь к папке для сохранения данных
        """
        self.temp_folder = temp_folder
        self.data_folder = data_folder
        os.makedirs(temp_folder, exist_ok=True)
        os.makedirs(data_folder, exist_ok=True)
    
    def save_temp_batch(self, data: Dict[str, Any], batch_name: str) -> str:
        """
        Сохраняет временный пакет данных.
        
        Args:
            data: Данные для сохранения
            batch_name: Имя пакета
            
        Returns:
            str: Путь к сохраненному файлу
        """
        filename = os.path.join(self.temp_folder, f"{batch_name}.json")
        return self._save_json(data, filename)
    
    def save_batch(self, data: List[Dict[str, Any]], batch_index: int) -> str:
        """
        Сохраняет пакет данных пользователей.
        
        Args:
            data: Список данных пользователей
            batch_index: Индекс пакета
            
        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем директорию для данных если она не существует
        os.makedirs(self.data_folder, exist_ok=True)
        
        # Формируем имя файла и сохраняем в директорию data
        filename = os.path.join(self.data_folder, f"friends_{batch_index}.json")
        return self._save_json(data, filename)
    
    def _save_json(self, data: Union[Dict[str, Any], List[Dict[str, Any]]], filename: str) -> str:
        """
        Сохраняет данные в JSON файл.
        
        Args:
            data: Данные для сохранения
            filename: Имя файла
            
        Returns:
            str: Путь к сохраненному файлу
        """
        # Убедимся, что директория для файла существует
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving data to {filename}: {e}")
            raise
    
    def load_json(self, filename: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Загружает данные из JSON файла.
        
        Args:
            filename: Имя файла
            
        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: Загруженные данные
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error loading data from {filename}: {e}")
            raise
    
    def cleanup_temp(self) -> None:
        """Очищает временную папку."""
        try:
            if os.path.exists(self.temp_folder):
                shutil.rmtree(self.temp_folder)
                logger.info(f"Temporary folder '{self.temp_folder}' cleaned")
                os.makedirs(self.temp_folder, exist_ok=True)
        except Exception as e:
            logger.error(f"Error cleaning temporary folder: {e}")
            raise 