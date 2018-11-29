import pytest
import run
import json

class TestCase:
    @pytest.fixture
    def client(self):
        test_client = run.server().test_client()
        return test_client

    def test_home(self, client):
        res = client.get('/')
        assert res.status_code == 200
        assert b"Welcome to iReporter" in res.data

    def test_getredflags(self, client):
        res = client.get('/api/v1/red-flags')
        assert res.status_code == 200
        assert b"data" in res.data

    def test_getredflag(self, client):
        res = client.get('/api/v1/red-flags/0')
        assert res.status_code == 200


    def test_create_red_flag(self, client):
        res = client.post('/api/v1/red-flags', content_type = 'application/json', data=json.dumps({
            "createdOn": '14/10/2018',
            "createdBy": 1,
            "type": 1,
            "location": "lat 0.00333 long 1.3456",
            "status": "Draft",
            "comment": "This is my comment."
        }))
        assert res.status_code == 200
        assert b'Created red-flag record' in res.data

    def test_redflag_not_found(self,client):
        res = client.get('/api/v1/red-flags/4')
        assert res.status_code == 400

    def test_edit_location(self,client):
        res = client.patch('/api/v1/red-flags/0/location', content_type='application/json', data=json.dumps(dict(
            location= "lat 0.44 long 1.23444"
        )
        ))
        assert res.status_code == 200
        assert b"Updated red-flag record's location" in res.data

    def test_edit_comment(self, client):
        res = client.patch('/api/v1/red-flags/0/comment', content_type='application/json',data=json.dumps(
            {
                'comment':'This is the updated comment'
            }
        ))
        assert res.status_code == 200
        assert b"Updated red-flag record's comment." in res.data

    def test_delete_redflag(self,client):
        res = client.delete('/api/v1/red-flags/0', data={'status':"complete"})
        assert res.status_code == 200
        assert b'Red-flag record deleted' in res.data

    def test_not_edited_comment(self,client):
        res = client.patch('/api/v1/red-flags/4/comment', content_type='application/json', data=json.dumps({
            'comment': 'This is the updated comment'
        }))
        assert res.status_code == 400
        assert b"Red-flag not updated" in res.data

    def test_not_edited_location(self,client):
        res = client.patch('/api/v1/red-flags/4/location', content_type='application/json', data=json.dumps({
            'location': "lat 0.44 long 1.23444"
        }))
        assert res.status_code == 400
        assert b"Red-flag record's location not updated" in res.data

    def test_redflag_not_deleted(self,client):
        res = client.delete('/api/v1/red-flags/0')
        assert res.status_code == 400
        assert b'Red-flag record not deleted' in res.data

    def test_redflag_not_found(self,client):
        res = client.get('/api/v1/red-flags/4')
        assert res.status_code == 400
        assert b'Red-flag does not exist.' in res.data