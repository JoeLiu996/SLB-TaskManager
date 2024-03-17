# make sure no tasks are in the database
import unittest
import json
from server import app

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_task(self):
        response = self.app.post('/tasks/add', data=json.dumps({
            'title': 'Task 1',
            'description': 'Description 1',
            'due_date': '2021-12-31',
            'status': 'TO DO'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Task 1')

    def test_create_task_invalid_data(self):
        response = self.app.post('/tasks/add', data=json.dumps({
            'title': 'Task 3',
            'description': 'Description 3',
            'due_date': '2021-12-31',
            'status': 'invalid'
        }), content_type='application/json')
        print(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))

    def test_get_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
    
    def test_get_task(self):
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Task 1')

    def test_get_task_not_found(self):
        response = self.app.get('/tasks/99999')
        self.assertEqual(response.status_code, 404)

    def test_update_task(self):
        response = self.app.put('/tasks/update/1', data=json.dumps({
            'title': 'Task 1 updated',
            'description': 'Description 1 updated',
            'due_date': '2021-12-31',
            'status': 'Completed'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Task 1 updated')

    def test_update_task_invalid_data(self):
        response = self.app.put('/tasks/update/1', data=json.dumps({
            'title': 'Task 1 updated',
            'description': 'Description 1 updated',
            'due_date': '2021-12-31',
            'status': 'invalid'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
    
    def test_update_task_not_found(self):
        response = self.app.put('/tasks/update/99999', data=json.dumps({
            'title': 'Task 3',
            'description': 'Description 3',
            'due_date': '2021-12-31',
            'status': 'TO DO'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_task(self):
        response = self.app.delete('/tasks/delete/1')
        self.assertEqual(response.status_code, 204)
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 404)

    def test_delete_task_not_found(self):
        response = self.app.delete('/tasks/delete/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(ServerTestCase('test_create_task'))
    suite.addTest(ServerTestCase('test_create_task_invalid_data'))
    suite.addTest(ServerTestCase('test_get_tasks'))
    suite.addTest(ServerTestCase('test_get_task'))
    suite.addTest(ServerTestCase('test_get_task_not_found'))
    suite.addTest(ServerTestCase('test_update_task'))
    suite.addTest(ServerTestCase('test_update_task_invalid_data')) 
    suite.addTest(ServerTestCase('test_update_task_not_found'))
    suite.addTest(ServerTestCase('test_delete_task'))
    suite.addTest(ServerTestCase('test_delete_task_not_found'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
   