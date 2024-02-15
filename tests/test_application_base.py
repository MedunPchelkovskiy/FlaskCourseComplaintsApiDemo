from models import RoleType
from tests.base import TestRestApiBase, generate_token
from tests.factory import UserFactory


class TestLoginRequired(TestRestApiBase):

    def test_get_complaints_auth_is_required(self):
        guarded_urls = [
            ('GET', '/complaints'),
            ('POST', '/complaints'),
            ('GET', '/complaints/1/approve'),
            ('GET', '/complaints/1/reject'),
        ]

        for method, url in guarded_urls:
            if method == 'GET':
                result = self.client.get('url')
            elif method == 'POST':
                result = self.client.post('url')
            elif method == 'PUT':
                result = self.client.put('url')
            elif method == 'DELETE':
                result = self.client.delete('url')

            assert result.status_code == 401
            assert result.json == {'message': 'Invalid or missing token'}

    def test_permission_required_create_complain_requires_complainer(self):
        user = UserFactory(role=RoleType.approver)
        token = generate_token(user)
        headers = {'Authorization': f'Bearer {token}'}

        result = self.client.post('/complaints', headers=headers)
        assert result.status_code == 403
        assert result.json == {'message': "You can't create complaint, no permission"}


        user = UserFactory(role=RoleType.admin)
        token = generate_token(user)
        headers = {'Authorization': f'Bearer {token}'}

        result = self.client.post('/complaints', headers=headers)
        assert result.status_code == 403
        assert result.json == {'message': "You can't create complaint, no permission"}


    
