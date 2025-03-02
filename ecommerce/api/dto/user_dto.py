from api.models.user import User

class UserDTO:
  def __init__(self, id=None, username=None, email=None,user_type=None, password=None):
    self.id = id
    self.username = username
    self.user_type = user_type
    self.email = email
    self.password = password

  @classmethod
  def from_model(cls, user: User):
    return cls(
      id=user.id,
      username=user.username,
      user_type=user.user_type,
     email=user.email,
      password=None  # لا يتم تضمين كلمة السر
    )

  def to_dict(self):
    return {
      "id": self.id,
      "username": self.username,
      "user_type": self.user_type,
     "email": self.email,
      "password": None  # كلمة السر لا يتم تضمينها في القاموس
    }
