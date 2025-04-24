"""
Модели данных для пользователей VK.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class VKUser:
    """Модель данных пользователя VK."""
    id: str
    first_name: str
    last_name: str
    is_closed: bool = False
    posts: List[Dict[str, Any]] = field(default_factory=list)
    communities: List[Dict[str, Any]] = field(default_factory=list)
    
    # Дополнительные поля профиля
    bdate: Optional[str] = None
    city: Optional[Dict[str, Any]] = None
    country: Optional[Dict[str, Any]] = None
    photo_max: Optional[str] = None
    photo_id: Optional[str] = None
    followers_count: Optional[int] = None
    sex: Optional[int] = None
    occupation: Optional[Dict[str, Any]] = None
    interests: Optional[str] = None
    education: Optional[Dict[str, Any]] = None
    universities: Optional[List[Dict[str, Any]]] = None
    schools: Optional[List[Dict[str, Any]]] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    last_seen: Optional[Dict[str, Any]] = None
    relation: Optional[int] = None
    personal: Optional[Dict[str, Any]] = None
    connections: Optional[Dict[str, Any]] = None
    activities: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'VKUser':
        """
        Создает объект пользователя из ответа API.
        
        Args:
            data: Словарь с данными пользователя из API
            
        Returns:
            VKUser: Объект пользователя
        """
        # Копируем базовые поля
        user_data = {
            'id': str(data.get('id')),
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'is_closed': data.get('is_closed', False),
        }
        
        # Копируем дополнительные поля если они есть
        optional_fields = [
            'bdate', 'city', 'country', 'photo_max', 'photo_id', 
            'followers_count', 'sex', 'occupation', 'interests', 
            'education', 'universities', 'schools', 'domain', 
            'status', 'last_seen', 'relation', 'personal', 
            'connections', 'activities'
        ]
        
        for field in optional_fields:
            if field in data:
                user_data[field] = data[field]
        
        # Добавляем посты если они есть
        if 'posts' in data:
            user_data['posts'] = data['posts']
        
        # Добавляем сообщества если они есть
        if 'communities' in data:
            user_data['communities'] = data['communities']
        
        return cls(**user_data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект в словарь для сериализации.
        
        Returns:
            Dict[str, Any]: Словарь с данными пользователя
        """
        return {k: v for k, v in self.__dict__.items() if v is not None} 