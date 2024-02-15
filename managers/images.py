from managers.authentication import auth
from models.images import ImagesModel


class ImageManager:
    @staticmethod
    def upload_image(image_data):
        current_user = auth.current_user()
        image_data['user_id'] = current_user.id
        image = ImagesModel(**image_data)

