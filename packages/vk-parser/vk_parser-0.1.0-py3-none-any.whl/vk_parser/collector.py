"""
Основной модуль сборщика данных из ВКонтакте.
"""
import logging
import asyncio
import signal
import time
from typing import List, Dict, Set, Any, Optional

from vk_parser.config.settings import VKConfig
from vk_parser.api.vk_client import VKClient
from vk_parser.utils.storage import DataStorage
from vk_parser.utils.state_manager import StateManager
from vk_parser.models.user import VKUser


logger = logging.getLogger(__name__)


class VKDataCollector:
    """Основной класс для сбора данных из ВКонтакте.
    
    Собирает информацию о пользователях, их постах и сообществах, в которых они состоят.
    Выполняет сбор данных с помощью асинхронных запросов к API ВКонтакте.
    Поддерживает возобновление сбора данных с точки остановки.
    """
    
    def __init__(self, config: VKConfig, resume: bool = False, state_file: str = "vk_parser_state.json"):
        """
        Инициализирует сборщик данных.
        
        Args:
            config: Конфигурация для сборщика
            resume: Флаг возобновления сбора данных
            state_file: Путь к файлу состояния
        """
        self.config = config
        self.api_client = VKClient(config.access_token, config.request_delay)
        self.storage = DataStorage()
        self.state_manager = StateManager(state_file)
        
        # Флаг для индикации потребности сохранить состояние
        self.need_save_state = False
        self.last_state_save = time.time()
        self.state_save_interval = 10  # Сохраняем состояние каждые 10 секунд
        
        # Загружаем сохраненное состояние или инициализируем новое
        if resume and self.state_manager.has_saved_state():
            state = self.state_manager.load_state()
            self.used_users = state["used_users"]
            self.unique_users = state["unique_users"]
            self.batch_data = []  # Всегда начинаем с пустых данных
            self.batch_index = state["batch_index"]
            self.users_counter = state["users_counter"]
            self.in_progress_users = state.get("in_progress_users", [])
            logger.info(f"Resuming collection from {self.users_counter} users, batch {self.batch_index}")
        else:
            # Наборы для отслеживания пользователей
            self.used_users: Set[str] = set()
            self.unique_users: Set[str] = set()
            self.in_progress_users: List[str] = []
            
            # Данные текущего пакета
            self.batch_data: List[Dict[str, Any]] = []
            self.batch_index: int = 1
            self.users_counter: int = 0
        
        # Устанавливаем обработчик сигналов для корректного сохранения состояния
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Настраивает обработчики сигналов для корректного завершения."""
        # Только для *nix систем
        try:
            signal.signal(signal.SIGINT, self._handle_exit)
            signal.signal(signal.SIGTERM, self._handle_exit)
        except (AttributeError, ValueError):
            # Windows не поддерживает SIGTERM
            pass
    
    def _handle_exit(self, signum, frame):
        """Обрабатывает сигналы завершения."""
        logger.info(f"Received signal {signum}, saving state and exiting...")
        self.need_save_state = True
        raise KeyboardInterrupt
    
    def filter_friends(self, friends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Фильтрует только открытые профили.
        
        Args:
            friends: Список профилей друзей
            
        Returns:
            List[Dict[str, Any]]: Отфильтрованный список профилей
        """
        return [f for f in friends if not f.get("is_closed", True)]
    
    def _save_current_state(self, last_user_id: Optional[str] = None):
        """
        Сохраняет текущее состояние сбора данных.
        
        Args:
            last_user_id: ID последнего обрабатываемого пользователя
        """
        self.state_manager.save_state(
            self.used_users,
            self.unique_users,
            last_user_id,
            self.batch_index,
            self.users_counter,
            self.in_progress_users
        )
    
    def _check_periodic_state_save(self):
        """Периодически сохраняет состояние, чтобы не потерять прогресс."""
        current_time = time.time()
        if current_time - self.last_state_save > self.state_save_interval:
            self._save_current_state()
            self.last_state_save = current_time
    
    async def collect_friends(self, user_id: str, depth: int = 1) -> None:
        """
        Асинхронно собирает информацию о друзьях, их постах и сообществах.
        
        Для каждого пользователя собирается:
        - Профиль с основной информацией
        - Последние посты со стены
        - Список сообществ, в которых состоит пользователь
        
        Args:
            user_id: ID пользователя для начала сбора
            depth: Текущая глубина рекурсии
        """
        # Периодически сохраняем состояние
        self._check_periodic_state_save()
        
        # Проверяем условия остановки рекурсии
        if (
            user_id in self.used_users
            or depth > self.config.max_depth
            or self.users_counter >= self.config.max_users
        ):
            return
        
        # Добавляем пользователя в список обрабатываемых
        if user_id not in self.in_progress_users:
            self.in_progress_users.append(user_id)
        
        try:
            # Отмечаем пользователя как обработанного
            self.used_users.add(user_id)
            
            # Получаем список ID друзей
            friends_ids = await self.api_client.get_friends_ids(user_id)
            logger.info(f"User {user_id} has {len(friends_ids)} friends")
            
            # Получаем информацию о друзьях
            friends_info = await self.api_client.get_users_info(friends_ids)
            filtered_friends = self.filter_friends(friends_info)
            logger.info(f"Open profiles: {len(filtered_friends)}")
            
            # Получаем посты друзей
            posts = await self.api_client.get_posts_batch([f["id"] for f in filtered_friends])
            
            # Получаем сообщества друзей
            communities = await self.api_client.get_communities_batch([f["id"] for f in filtered_friends])
            
            # Обрабатываем каждого друга
            for friend in filtered_friends:
                if friend["id"] in self.unique_users or self.users_counter >= self.config.max_users:
                    continue
                
                # Получаем посты друга
                friend_posts = posts.get(friend["id"], [])
                if not friend_posts:
                    continue
                
                # Получаем сообщества друга
                friend_communities = communities.get(friend["id"], [])
                
                # Создаем объект пользователя
                friend_data = friend.copy()
                friend_data["posts"] = friend_posts
                friend_data["communities"] = friend_communities
                
                # Можно использовать объект VKUser для валидации данных
                # user = VKUser.from_api_response(friend_data)
                # self.batch_data.append(user.to_dict())
                
                # Сейчас добавляем сырой словарь
                self.batch_data.append(friend_data)
                self.unique_users.add(friend["id"])
                self.users_counter += 1
                
                # Сохраняем пакет по достижении лимита
                if self.users_counter % self.config.save_interval == 0:
                    self.storage.save_batch(self.batch_data, self.batch_index)
                    self.storage.cleanup_temp()
                    self.batch_data = []
                    self.batch_index += 1
                    
                    # Сохраняем состояние после сохранения пакета
                    self._save_current_state(user_id)
                
                # Проверяем достижение общего лимита
                if self.users_counter >= self.config.max_users:
                    logger.info(f"Reached maximum users limit: {self.users_counter}")
                    return
            
            # Рекурсивно обрабатываем следующий уровень друзей
            if depth < self.config.max_depth and self.users_counter < self.config.max_users:
                tasks = []
                for friend in filtered_friends:
                    task = self.collect_friends(friend["id"], depth + 1)
                    tasks.append(task)
                await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            logger.warning(f"Task for user {user_id} was cancelled")
            raise
        except Exception as e:
            logger.error(f"Error processing user {user_id}: {e}")
        finally:
            # Удаляем пользователя из списка обрабатываемых
            if user_id in self.in_progress_users:
                self.in_progress_users.remove(user_id)
    
    async def run(self) -> None:
        """Запускает процесс сбора данных."""
        logger.info("Starting data collection...")
        
        # Если есть незавершенные пользователи, обрабатываем их первыми
        start_users = self.in_progress_users.copy() if self.in_progress_users else [self.config.start_user_id]
        
        try:
            tasks = []
            for user_id in start_users:
                task = self.collect_friends(user_id)
                tasks.append(task)
            
            await asyncio.gather(*tasks)
            
            # Сохраняем оставшиеся данные
            if self.batch_data:
                self.storage.save_batch(self.batch_data, self.batch_index)
            
            logger.info(f"Collection completed. Total users collected: {self.users_counter}")
            
            # Очищаем состояние после успешного завершения
            self.state_manager.clear_state()
            
        except KeyboardInterrupt:
            logger.warning("Collection interrupted by user")
            # Сохраняем состояние для возможности продолжения
            self._save_current_state()
        except Exception as e:
            logger.error(f"Error during data collection: {e}")
            # Сохраняем состояние для возможности продолжения
            self._save_current_state()
            raise
        finally:
            # Очищаем временные файлы в любом случае
            self.storage.cleanup_temp()
            
            # Принудительно сохраняем состояние если флаг установлен
            if self.need_save_state:
                self._save_current_state() 