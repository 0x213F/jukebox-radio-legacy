
from proj.core.messages import BaseMessage


class UserMessage(BaseMessage):

    NOT_AUTHENTICATED = 'User is not authenticated'
    ALREADY_AUTHENTICATED = 'User is already authenticated'
    USERNAME_TAKEN = "A User already exists with that username"
    MISSING_USERNAME = "Must choose a username to continue"
    MISSING_AGREE = 'Must agree to Privacy Policy to continue'
