import time

from flask import current_app
import requests


class ThreadsPublisher:

    def __init__(self):
        config = current_app.config
        self.main_url = config["THREADS_MAIN_URL"]
        self.access_token = config["THREADS_ACCESS_TOKEN"]
        self.user_id = config["THREADS_USER_ID"]
        self.version = config["THREADS_VERSION"]

    def _create_container(self, img_url, text=''):
        params = {
            'media_type':'IMAGE',
            'image_url': img_url,
            'text': text,
            'access_token': self.access_token
    }

        res = requests.post(f'{self.main_url}/{self.user_id}/threads', data=params)
        if res.status_code != 200:
            raise RuntimeError(f"Failed to create container: {res.status_code} {res.text}")
        print(res.status_code)
        print(res.json())
        container = res.json()
        return container
    
    def get_container_id(self,  img_url, text=''):
        """

        """
        container = self._create_container(img_url, text)
        return container['id']
    
    def _wait_until_ready(self, container_id, timeout=120):
        """
        メディアコンテナが公開可能（FINISHED）になるまで待機する。

        Args:
            container_id (str): /media で作成したメディアコンテナID
            timeout (int): 最大待機秒数（1秒間隔でポーリング）

        Raises:
            RuntimeError: ステータス確認APIがエラーを返した場合、または処理が ERROR になった場合
            TimeoutError: timeout 秒待っても FINISHED にならなかった場合
        """
        
        url = f'{self.main_url}/{self.version}/{container_id}'

        for i in range(timeout):
            res = requests.get(
                url,
                params={
                    "fields": "status",
                    "access_token": self.access_token
                },
                timeout=10
            )

            result = res.json()
            status = result.get('status')
            print(f"[{i+1}s] status={status}")

            if status == "FINISHED":
                print(res.text)
                return
            if status == "ERROR":
                raise RuntimeError(f"Media processing failed: {result}")

            time.sleep(1)

        raise TimeoutError("Media processing timeout")
    
    def publish_media(self, img_url, text=''):
        """
        作成済みのメディアコンテナをInstagramに公開（投稿確定）する。

        Args:
            img_url (str): Instagramに投稿する画像のURL
            caption (str, optional): 投稿時のキャプション。省略可。

        Raises:
            RuntimeError: メディアの公開に失敗した場合
        """
        container_id = self.get_container_id(img_url, text)
        
        self._wait_until_ready(container_id)

        data = {
                'creation_id': container_id,
                'access_token': self.access_token
        }
        res = requests.post(f'{self.main_url}/{self.version}/{self.user_id}/threads_publish',data=data)
        if res.status_code != 200:
            raise RuntimeError(
                f"Failed to publish media: {res.status_code} {res.text}"
            )
        print(res.status_code)
        print(res.text)
        print('投稿完了')