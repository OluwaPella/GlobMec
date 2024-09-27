from flask import request
import uuid
from auth import AUTH
from models import Session, db
from datetime import datetime

class session(AUTH):
    """this logic session management"""

    def session_cookie(self, request=None):
        """this logic retieve session cookie from request"""
        if request is None:
            return None
        return request.cookie.get(session)
    
    def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        new_session = Session(user_id=user_id, session_id=session_id, create_at=datetime.utcnow())
        db.session.add(new_session)
        db.session.commit()
        return session_id
    
    def destroy_session(self, request=None) -> bool:
        """destroys the session for the current user."""
        if request is None:
            return False
        get_session = self.session_cookie(request)
        if get_session is None:
            return False
        deL_session = Session.query.filter_by(get_session).frist()
        if deL_session is None:
            return False
        
        db.session.delete(deL_session)
        db.session.commit()

        return True