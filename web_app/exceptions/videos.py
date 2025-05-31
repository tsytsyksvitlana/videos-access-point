from web_app.exceptions.base import ObjectNotFoundException


class VideoIdNotFoundException(ObjectNotFoundException):
    def __init__(self, user_id: int):
        super().__init__(object_type="User", field=f"ID {user_id}")
