from resources.authentication import UserRegisterResource, UserLoginResource
from resources.complaint import ComplaintsResource, ComplaintApproveResource, ComplaintRejectResource
# from resources.images import FileResource

routes = (
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (ComplaintsResource, '/complaints'),
    (ComplaintApproveResource, '/complaints/<int:id>/approve'),
    (ComplaintRejectResource, '/complaints/<int:id>/reject'),
    # (FileResource, '/upload'),
)
