from typing import Dict, Any, Optional, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, \
    IntegerIDMixin, InvalidPasswordException
from fastapi_users.authentication import \
    AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from .utils import get_user_db
from .models import User
from .schemas import UserCreate
from .mail import send_email


SECRET = "SECRET"
APP_DOMAIN = '127.0.0.1'


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    MIN_PASSWORD_LENGTH = 5

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < UserManager.MIN_PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason="Password should be at least {} characters".format(
                    UserManager.MIN_PASSWORD_LENGTH
                )
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def on_after_register(self, user: User,
                                request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_update(
        self,
        user: User,
        update_dict: Dict[str, Any],
        request: Optional[Request] = None,
    ):
        print(f"User {user.id} has been updated with {update_dict}.")

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        print(f"User {user.id} logged in.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. \
              Verification token: {token}")

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has been verified")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

        reset_url = f"https://{APP_DOMAIN}/reset-password?token={token}"
        subject = "Password Reset Request"
        content = f"Click the link below to reset your password:\n\n{reset_url}"

        await send_email(user.email, subject, content)

    async def on_after_reset_password(self, user: User,
                                      request: Optional[Request] = None):
        print(f"User {user.id} has reset their password.")

    async def on_before_delete(self, user: User,
                               request: Optional[Request] = None):
        print(f"User {user.id} is going to be deleted")

    async def on_after_delete(self, user: User,
                              request: Optional[Request] = None):
        print(f"User {user.id} is successfully deleted")


async def get_user_manager(user_db: SQLAlchemyUserDatabase =
                           Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
