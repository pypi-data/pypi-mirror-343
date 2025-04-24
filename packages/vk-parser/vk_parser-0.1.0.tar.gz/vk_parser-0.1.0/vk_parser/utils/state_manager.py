"""
Менеджер состояния для сохранения и восстановления прогресса сбора данных.
"""
import os
import json
import logging
from typing import Dict, List, Set, Any, Optional

logger = logging.getLogger(__name__)


class StateManager:
    """Класс для управления состоянием сбора данных."""
    
    def __init__(self, state_file: str = "vk_parser_state.json"):
        """
        Инициализирует менеджер состояния.
        
        Args:
            state_file: Путь к файлу для сохранения состояния
        """
        self.state_file = state_file
        self.default_state = {
            "used_users": [],
            "unique_users": [],
            "last_user_id": None,
            "batch_index": 1,
            "users_counter": 0,
            "in_progress_users": []
        }
    
    def save_state(self, 
                  used_users: Set[str], 
                  unique_users: Set[str], 
                  last_user_id: Optional[str],
                  batch_index: int,
                  users_counter: int,
                  in_progress_users: List[str]) -> None:
        """
        Сохраняет текущее состояние сбора данных.
        
        Args:
            used_users: Множество обработанных пользователей
            unique_users: Множество уникальных пользователей
            last_user_id: ID последнего обрабатываемого пользователя
            batch_index: Текущий индекс пакета
            users_counter: Счетчик собранных пользователей
            in_progress_users: Список пользователей, обработка которых не завершена
        """
        state = {
            "used_users": list(used_users),
            "unique_users": list(unique_users),
            "last_user_id": last_user_id,
            "batch_index": batch_index,
            "users_counter": users_counter,
            "in_progress_users": in_progress_users
        }
        
        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
            logger.info(f"State saved to {self.state_file}")
        except Exception as e:
            logger.error(f"Error saving state to {self.state_file}: {e}")
    
    def load_state(self) -> Dict[str, Any]:
        """
        Загружает сохраненное состояние сбора данных.
        
        Returns:
            Dict[str, Any]: Данные состояния или состояние по умолчанию
        """
        if not os.path.exists(self.state_file):
            logger.info(f"State file {self.state_file} not found, using default state")
            return self.default_state
        
        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                state = json.load(file)
            logger.info(f"State loaded from {self.state_file}")
            
            # Преобразуем списки обратно в множества для оптимальной работы
            state["used_users"] = set(state.get("used_users", []))
            state["unique_users"] = set(state.get("unique_users", []))
            
            return state
        except Exception as e:
            logger.error(f"Error loading state from {self.state_file}: {e}")
            return self.default_state
    
    def has_saved_state(self) -> bool:
        """
        Проверяет наличие сохраненного состояния.
        
        Returns:
            bool: True если есть сохраненное состояние, иначе False
        """
        return os.path.exists(self.state_file)
    
    def clear_state(self) -> None:
        """Удаляет файл сохраненного состояния."""
        if os.path.exists(self.state_file):
            try:
                os.remove(self.state_file)
                logger.info(f"State file {self.state_file} removed")
            except Exception as e:
                logger.error(f"Error removing state file {self.state_file}: {e}")
    
    def backup_state(self) -> None:
        """Создает резервную копию файла состояния."""
        if os.path.exists(self.state_file):
            try:
                backup_file = f"{self.state_file}.bak"
                with open(self.state_file, "r", encoding="utf-8") as src:
                    with open(backup_file, "w", encoding="utf-8") as dst:
                        dst.write(src.read())
                logger.info(f"State backup created: {backup_file}")
            except Exception as e:
                logger.error(f"Error creating state backup: {e}") 