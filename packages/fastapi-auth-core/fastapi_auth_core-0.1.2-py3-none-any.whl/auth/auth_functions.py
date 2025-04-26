from datetime import datetime, UTC
from typing import Callable, Any


class AuthFunctions:
    def  __init__(self, db_session: Callable[...,Any], User:any):
        """
        Args:
            db_session (Callable[..., Session]): A function that returns a SQLAlchemy session.
            User (any): The SQLAlchemy model class representing the user table
        """
        self.db = db_session
        self.User = User
    
    async def update_user_refresh_token(self, user_id: int, refresh_token: str):
        """
        Updates the refresh token for a user in the database.

        Args:
            user_id (int): The ID of the user.
            refresh_token (str): The new refresh token to be updated.

        Raises:
            Exception: Rolls back the transaction if an error occurs.
        """

        with self.db() as session:
            try:
                user = session.query(self.User).filter(self.User.id == user_id).first()

                if user:
                    user.refresh_token = refresh_token
                    user.updated_at = datetime.now(UTC)

            except Exception as e:
                raise e
    

    def get_user_by_attribute(self,attribute: str, value: str):
        """
        Get a user by an attribute.

        Args:
            attribute (str): The attribute to get the user by.
            value (str): The value of the attribute.
        
        Returns:
            User: The user object if found, otherwise None.
        """
        with self.db() as session:
            try:
                if not hasattr(self.User, attribute):
                    raise ValueError(f"Attribute {attribute} does not exist on the User model")
                
                return session.query(self.User).filter(getattr(self.User, attribute) == value).first()
            
            except Exception as e:
                raise e
