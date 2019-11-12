import unittest
from test.support import EnvironmentVarGuard

from app import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.env = EnvironmentVarGuard()
        self.env.set('CELERY_BROKER_URL',
                     'amqp://pyizcpcy:i8-DLpC9lKVReHWD0--fNDPT_QOJzNCJ@orangutan.rmq.cloudamqp.com/pyizcpcy')

        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_calculate(self):
        with self.env:
            res = self.app.get('/calculate/3.1/2.1')
            self.assertEqual(res.status_code, 200)

            self.assertTrue(res.is_json)
            self.assertDictEqual(res.json, {'x': 3.1, 'y': 2.1})

    def test_callback(self):
        with self.env:
            res = self.app.get('/callback/21.2')
            self.assertEqual(res.status_code, 200)

            self.assertTrue(res.is_json)
            self.assertDictEqual(res.json, {'result': 21.2})


if __name__ == '__main__':
    unittest.main()
