"""Models."""
from django.db import models

from manage import init_django
from sqlitedb.utils import UserStatus

init_django()


class UserManager(models.Manager):  # type: ignore
    """Manager for the User model."""

    pass


class User(models.Model):
    """Model for storing user data.

    Attributes:
        id (int): The unique ID of the user.
        name (str or None): The name of the user, or None if no name was provided.
        telegram_id (int): The ID of the user.
        status (str): The current status of the user's account (active, suspended, or temporarily banned).
        joining_date (datetime): The date and time when the user was added to the database.
        last_updated (datetime): The date and time when the user's details were last updated.

    Managers:
        objects (UserManager): The custom manager for this model.

    Meta:
        db_table (str): The name of the database table used to store this model's data.

    Raises:
        IntegrityError: If the user's Telegram ID is not unique.
    """

    # User ID, auto-generated primary key
    id = models.AutoField(primary_key=True)

    # User name, max length of 255, can be null
    name = models.CharField(max_length=255, blank=True)

    # User Telegram ID, integer
    telegram_id = models.IntegerField(unique=True)

    # State of the user
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.name) for status in UserStatus],
        default=UserStatus.ACTIVE.value,
    )

    # Date and time when the user was added to the database, auto-generated
    joining_date = models.DateTimeField(auto_now_add=True)

    # Date and time when the user details was modified , auto-generated
    last_updated = models.DateTimeField(auto_now=True)

    # Conversation settings, stored as a JSON object
    settings = models.JSONField(default=dict)

    # Use custom manager for this model
    objects = UserManager()

    class Meta:
        # Database table name
        db_table = "user"

    def __str__(self) -> str:
        """Return a string representation of the user object."""
        return f"User(id={self.id}, name={self.name}, telegram_id={self.telegram_id}, status={self.status})"
