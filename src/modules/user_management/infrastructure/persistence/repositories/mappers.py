from modules.user_management.domain.entities.user import User
from modules.user_management.domain.value_objects.email import Email
from ..models import UserModel

def to_entity(model: UserModel) -> User:
        """
        Convert ORM model to domain entity.
        
        Args:
            model: User ORM model
            
        Returns:
            User domain entity
        """
        user = User(
            email=Email(model.email),
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
            id=model.id
        )
        
        # Set internal timestamps from model
        user._created_at = model.created_at
        user._updated_at = model.updated_at
        user._is_deleted = model.is_deleted
        
        return user
    
def to_model(entity: User) -> UserModel:
    """
    Convert domain entity to ORM model.
    
    Args:
        entity: User domain entity
        
    Returns:
        User ORM model
    """
    return UserModel(
        id=entity.id,
        email=entity.email.value,
        username=entity.username,
        first_name=entity.first_name,
        last_name=entity.last_name,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        is_deleted=entity.is_deleted
    )