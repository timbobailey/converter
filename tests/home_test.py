import unittest
import json
import os
import shutil
from web import create_app
app = create_app()
APP_PATH = os.environ.get('APP_PWD')


class HomeTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.tester = app.test_client(self)

    def test_config(self):
        assert not create_app().testing

    def test_home(self):
        response = self.tester.get('/', content_type='html/text')
        assert response.status_code == 200

    def test_404(self):
        response = self.tester.get('/not_found', content_type='html/text')
        assert response.status_code == 404

    def test_popular(self):
        # remove cache
        shutil.rmtree(APP_PATH+'/cache')
        response = self.tester.get('/popular', content_type='html/text')
        assert response.status_code == 200

    def test_convert(self):
        import websockets
        import asyncio
        from server import start_server, stop_server
        # start_server()

        async def notify(payload):
            uri = 'ws://localhost:5678'
            async with websockets.connect(uri) as websocket:
                await websocket.send(str(payload).encode())

        data = {
            'name': 'Tester'
        }
        asyncio.run(notify(data))

        payload = dict(
            urls='https://www.youtube.com/watch?v=qbrgk2oCNFA',
            audio_quality='192',
            name=data['name'])

        response = self.tester.post('/convert', data=json.dumps(payload),
                                    content_type='application/json')
        assert response.status_code == 200
        # stop_server()

    def test_get_duration(self):
        payload = dict(
            yt_video_url='https://www.youtube.com/watch?v=_wdKCdWfTaY&list=PLWN4RVLXtxVAcmVrlfqWkUXbdplV-1KCi&index=6')

        response = self.tester.post('/get_duration', data=json.dumps(payload),
                                    content_type='application/json')
        assert response.status_code == 200
        assert b'305' in response.data


if __name__ == '__main__':
    unittest.main()