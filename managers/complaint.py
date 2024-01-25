from werkzeug.exceptions import BadRequest

from db import db
from managers.authentication import auth
from models import ComplaintsModel, RoleType, State


class ComplaintManager:
    @staticmethod
    def create_complaint(complaint_data):
        current_user = auth.current_user()
        complaint_data['user_id'] = current_user.id
        complaint = ComplaintsModel(**complaint_data)
        db.session.add(complaint)
        db.session.commit()
        return complaint

    @staticmethod
    def get_complaints():
        user = auth.current_user()
        role = user.role
        complaints = role_mapper[role]()
        return complaints

    @staticmethod
    def _get_complainer_complaints():
        user = auth.current_user()
        complaints = ComplaintsModel.query.filter_by(user_id=user.id).all()
        return complaints

    @staticmethod
    def _get_approver_complaints():
        complaints = ComplaintsModel.query.filter_by(status=State.pending).all()
        return complaints

    @staticmethod
    def _get_all_complaints():
        complaints = ComplaintsModel.query.all()
        return complaints

    @staticmethod
    def approve_complaint(complaint_id):
        ComplaintsModel.query.filter_by(id=complaint_id).update({'status': State.approved})
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintsModel.query.filter_by(id=complaint_id).update({'status': State.rejected})
        db.session.commit()

    @staticmethod
    def _validate_status(complaint_id):
        complaint = ComplaintsModel.query.filter_by(complaint_id).first()
        if not complaint:
            raise BadRequest('Complaint with this id does not exist')

        if complaint.status != State.pending:
            raise BadRequest("Complaint is already processed, can't change status")

role_mapper = {RoleType.complainer: ComplaintManager._get_complainer_complaints,
               RoleType.approver: ComplaintManager._get_approver_complaints,
               RoleType.admin: ComplaintManager._get_all_complaints,
}
