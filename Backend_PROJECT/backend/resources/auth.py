from  flask import request
from typing import List, TypeVar
import re
from models import User
from session import session


class AUTH(session):
    """logic auth"""
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """this logic check if auth is requred or not"""
        if path  is None or excluded_path is None or  len(excluded_path) == 0:
            return True
        for excluded_pths in excluded_path:
            excluded_path = excluded_pths.strip()
            checked =''
            if excluded_path[-1] == '*':
                checked = '{}.*'.format(excluded_path[:-1])
            elif excluded_path[-1] == '/':
                checked = '{}/*'.format(excluded_path[:-1])
            else:
                checked = '{}/*'.format(excluded_path)
            if re.match(checked, path):
                return False
            
            return True
        
    def authorization_header(self,request=None) -> str:
            """this logic check auth header"""
            if request is None:
                return None
            return request.headers.get('Authorization', None)
    def user_id_for_session_id(self,session_id:str) -> str:
            """this logic retrieve session_id"""
            if session_id is None:
                return None
            if not isinstance(session_id, str):
                return None
            else:
                found_id = self.user_id_by_session_id.get(session_id)
                return found_id
        
    def current_user(self,request=None) -> TypeVar('User'):
            """this logic identify current user"""
            session = self.session_cookie(request)
            if request is None:
                 return None
            user_id = self.user_id_for_session_id(session)
            if user_id is None:
                return None
            return User.query.get(user_id) 
