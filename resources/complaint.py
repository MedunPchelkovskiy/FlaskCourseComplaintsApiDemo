from flask import request
from flask_restful import Resource

from helpers.decorators import validate_schema, permission_required
from managers.authentication import auth
from managers.complaint import ComplaintManager
from models import RoleType
from schemas.request.complaints import ComplaintsRequestSchema
from schemas.response.complaints import CreateComplaintResponseSchema, GetComplaintResponseSchema


class ComplaintsResource(Resource):
    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintsRequestSchema)
    def post(self):
        data = request.get_json()
        complaint = ComplaintManager.create_complaint(data)
        return CreateComplaintResponseSchema().dump(complaint), 201

    @auth.login_required
    def get(self):
        complaints = ComplaintManager.get_complaints()
        return GetComplaintResponseSchema(many=True).dump(complaints), 201

class ComplaintResource(Resource): #TODO: for homework
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass #return 204 status, no content after delete


class ComplaintApproveResource(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def get(self,id):
        ComplaintManager.approve_complaint(id)


class ComplaintRejectResource(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def get(self, id):
        ComplaintManager.reject_complaint(id)
