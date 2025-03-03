class UserDTO:
    def __init__(self, id=None, username=None, email=None, user_type=None, password=None):
        self.id = id
        self.username = username
        self.user_type = user_type
        self.email = email
        self.password = password  # password is kept for internal use, but not included in serialized output
    def to_dict(self):
        """Convert the UserDTO to a dictionary to make it JSON serializable."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type
        }