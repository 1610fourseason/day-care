import time

from flask import current_app
import requests


class InstagramPublisher:
    def __init__(self):
        config = current_app.config
        self.main_url = config["INSTAGRAM_MAIN_URL"]
        self.access_token = config["INSTAGRAM_ACCESS_TOKEN"]
        self.instagram_id = config["INSTAGRAM_USER_ID"]
        self.version = config["INSTAGRAM_VERSION"]

    def _create_container(self, img_url, caption=''):
        """
        インスタに投稿するためのコンテナを作成
        Args:
            img_url(str): Instagramに投稿する画像のURL
        Returns:
            dict: Graph APIのレスポンスJSON（例: {"id": "..."} など）
        Raises:
            RuntimeError: APIリクエストが失敗した場合
        """
        params = {
        'image_url': img_url,
        'caption': caption,
        'access_token': self.access_token
    }
        res = requests.post(f'{self.main_url}/{self.version}/{self.instagram_id}/media', data=params)
        print(res.status_code)
        print(res.text)
        if res.status_code != 200:
            
            raise RuntimeError(f"Failed to create container: {res.status_code} {res.text}")
        container = res.json()
        return container

    def get_container_id(self,  img_url, caption=''):
        """
        画像URLとキャプションからInstagram投稿用の
        メディアコンテナIDを取得する。

        Args:
            img_url (str): Instagramに投稿する画像のURL
            caption (str, optional): 投稿時のキャプション。省略可。

        Returns:
            str: 作成されたメディアコンテナID
        """
        container = self._create_container(img_url, caption)
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
                    "fields": "status_code",
                    "access_token": self.access_token
                },
                timeout=10
            )

            result = res.json()
            status = result.get('status_code')
            print(f"[{i+1}s] status_code={status}")

            if status == "FINISHED":
                print(res.text)
                return
            if status == "ERROR":
                raise RuntimeError(f"Media processing failed: {result}")

            time.sleep(1)

        raise TimeoutError("Media processing timeout")


    
    def publish_media(self, img_url, caption=''):
        """
        作成済みのメディアコンテナをInstagramに公開（投稿確定）する。

        Args:
            img_url (str): Instagramに投稿する画像のURL
            caption (str, optional): 投稿時のキャプション。省略可。

        Raises:
            RuntimeError: メディアの公開に失敗した場合
        """
        container_id = self.get_container_id(img_url, caption)
        
        self._wait_until_ready(container_id)

        data = {
                'creation_id': container_id,
                'access_token': self.access_token
        }
        res = requests.post(f'{self.main_url}/{self.version}/{self.instagram_id}/media_publish',data=data)
        if res.status_code != 200:
            raise RuntimeError(
                f"Failed to publish media: {res.status_code} {res.text}"
            )
        print(res.status_code)
        print(res.text)
        print('投稿完了')

