# -*- coding: utf-8 -*-
import vk_api
from typing import List


class VKApi:

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.vk_session = self.create_session(self.login, self.password)

    def create_session(self, login, token):
        vk_session = vk_api.VkApi(login=login, token=token)
        try:
            vk_session.auth(token_only=True)
            print("Соеденение с вк установленно")
        except vk_api.AuthError as error_connect:
            print(error_connect)
        return vk_session

    def upload_photo(self, photo_path: str, caption: str, album_id: str):
        upload = vk_api.VkUpload(self.vk_session)
        vk_photo = upload.photo(photos=[photo_path], album_id=album_id,
                                caption=[caption])[0]
        return f'photo{vk_photo["owner_id"]}_{vk_photo["id"]}'

    def post_wall(self, owner_id: int, text_message: str, vk_photos: List[str]):
        vk_photos_id = ",".join(vk_photos)
        vk_post = self.vk_session.method('wall.post', {
            'owner_id': -owner_id,
            'message': text_message,
            'attachments': vk_photos_id  # 'photo615022059_457240069,photo615022059_457240054'
        })
        print("Пост в вк готов")
        return vk_post

    def post_group_wall(self, photos_path: list, captions: list, album_id: str):
        vk_photos_id = [self.upload_photo(photo_path, caption, album_id)
                        for photo_path, caption in zip(photos_path, captions)]
        vk_post = self.post_wall(self.config.owner_id, self.config.text_message, vk_photos_id)
        return vk_post

    def get_album_id(self):
        photo_albums = self.vk_session.method('photos.getAlbums', {"owner_id": 615022059})
        vk_albums = photo_albums['items']
        for album in vk_albums:
            if album['title'] == self.config.album_name:
                print('Такой альбом уже имется')
                return album['id']
        album = self.vk_session.method('photos.createAlbum', {"title": self.config.album_name})
        print('Создал новый альбом')
        return album["id"]
