import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from firebase_admin import auth
from ninja.security import HttpBearer

User = get_user_model()
logger = logging.getLogger(__name__)


class FirebaseAuthentication(HttpBearer):
    def _create_user_instance(self, uid: str, email: str) -> User:
        user = User.objects.create(username=uid, email=email)
        return user

    def authenticate(self, request, token):
        # token = request.headers.get('Authorization')
        if not token:
            return None
        uid: int = cache.get(request.headers.get('UID'))
        if uid is None:
            try:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token["uid"]
                cache.set(uid, uid)
            except Exception as e:
                logger.error(e)
                return None

        try:
            user = User.objects.get(username=uid)
            return user, token
        except User.DoesNotExist:
            try:
                firebase_user = auth.get_user(uid)
                if firebase_user.email is None:
                    return None
                user = self._create_user_instance(uid=uid, email=firebase_user.email)
            except Exception as e:
                logger.error(e)
                return None
            return user, token
