import uuid

from werkzeug.exceptions import BadRequest

from db import db
from managers.authentication import auth
from models import ComplaintsModel, RoleType, State, TransactionModel
from services.wise import WiseService


class ComplaintManager:
    @staticmethod
    def create_complaint(complaint_data):
        current_user = auth.current_user()
        complaint_data['user_id'] = current_user.id
        complaint = ComplaintsModel(**complaint_data)
        full_name = f'{current_user.first_name} {current_user.last_name}'
        amount = complaint_data['amount']
        iban = current_user.iban

        db.session.add(complaint)
        db.session.flush()

        complaint_id = complaint.id
        transfer = ComplaintManager.issue_transaction(amount, full_name, iban, complaint_id)

        db.session.add(transfer)
        db.session.flush()
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
        ComplaintManager._validate_status(complaint_id)
        wise_service = WiseService()
        transfer = TransactionModel.query.filter_by(complaint_id=complaint_id).first()
        wise_service.fund_transfer(transfer.transfer_id)
        ComplaintsModel.query.filter_by(id=complaint_id).update({'status': State.approved})
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintsModel.query.filter_by(id=complaint_id).update({'status': State.rejected})
        db.session.commit()

    @staticmethod
    def _validate_status(complaint_id):
        complaint = ComplaintsModel.query.filter_by(id=complaint_id).first()
        if not complaint:
            raise BadRequest('Complaint with this id does not exist')

        if complaint.status != State.pending:
            raise BadRequest("Complaint is already processed, can't change status")

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id):
        wise_service = WiseService()
        quote_id = wise_service.create_quota(amount)
        recipient_id = wise_service.create_recipient_account(full_name, iban)
        current_transfer_id = str(uuid.uuid4())
        transfer_id = wise_service.create_transfer(quote_id, recipient_id, current_transfer_id)
        transfer = TransactionModel(
            quote_id=quote_id,
            transfer_id=transfer_id,
            current_transfer_id=current_transfer_id,
            target_account_id=recipient_id,
            amount=amount,
            complaint_id=complaint_id
        )
        return transfer

role_mapper = {RoleType.complainer: ComplaintManager._get_complainer_complaints,
               RoleType.approver: ComplaintManager._get_approver_complaints,
               RoleType.admin: ComplaintManager._get_all_complaints,
}
