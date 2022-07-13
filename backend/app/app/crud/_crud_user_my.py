# import os
# import shutil
#
# from jose import jwt, JWTError
#
# from typing import Optional
#
# from fastapi import Depends, UploadFile
# from sqlalchemy import desc
#
# from app.db.session import SessionLocal, get_session
# from app.models.user_my import UserMy
#
# from app.exceptions import UnfoundEntity, InaccessibleEntity
# from app.schemas.user_my import DataToCreateUser, UserBasicUpdate
#
#
# from ..exceptions import UnfoundEntity, InaccessibleEntity
#
# SECRET_JWT = "AXAS"
#
#
# class UserService:
#     def __init__(self, session: SessionLocal = Depends(get_session)):
#         self.session = session
#
#     def _get(self, tel: str) -> Optional[int]:  # в метод предается id, если объект есть в таблице
#         user = (self.session.query(UserMy.id).filter_by(tel=tel).order_by(desc(UserMy.id)).first())
#         if not user:
#             return None
#         return user.id
#
#     def create_user(self, user_data: DataToCreateUser,) -> UserMy:
#         user = UserMy()
#         for attr, value in user_data.dict().items():
#             if hasattr(user, attr):
#                 setattr(user, attr, value)
#         self.session.add(user)
#         self.session.commit()
#         return user
#
#     def update(self, id_user: int, user_data: UserBasicUpdate) -> None:
#         tab = UserMy
#         tab = self.session.query(tab).filter(tab.id == id_user).order_by(desc(tab.id)).first()
#         for attr, value in user_data.dict().items():
#             if hasattr(tab, attr):
#                 setattr(tab, attr, value)
#         self.session.add(tab)
#         self.session.commit()
#         # return self.session.query(tables.Users.id, tables.Users.tel, tables.Users.first_name, tables.Users.last_name,
#         #                           tables.Users.location).filter(tables.Users.id == id_user).first()
#         return self.session.query(UserMy).filter(UserMy.id == id_user).first()
#
#     # СТАРЫЙ РАБОЧИЙ КОД
#     # def update(self, id_user: int, user_data: UserBasicUpdate) -> None:
#     #     tab = tables.Users
#     #     tab = self.session.query(tab).filter(tab.id == id_user).order_by(desc(tab.id)).first()
#     #     for attr, value in user_data.dict().items():
#     #         if hasattr(tab, attr):
#     #             setattr(tab, attr, value)
#     #     self.session.add(tab)
#     #     self.session.commit()
#     #     return self.session.query(tables.Users.id, tables.Users.tel, tables.Users.first_name, tables.Users.last_name,
#     #                               tables.Users.location).filter(tables.Users.id == id_user).first()
#
#     def get_user(self, id_user: int) -> UserMy:  # Вот тут надо оптимизировать код
#         # user = (self.session.query(UserMy.id, UserMy.tel, UserMy.first_name, UserMy.last_name,
#         #                            UserMy.location, UserMy.photo_main, UserMy.photo_1,
#         #                            UserMy.photo_2, UserMy.basic_about_me, UserMy.job_title,
#         #                            UserMy.company, UserMy.about_me, UserMy.contact_phone,
#         #                            UserMy.telegram).filter_by(id=id_user).
#         #         order_by(desc(UserMy.id)).first())
#
#         user = self.session.query(UserMy).get(id_user)
#
#         # НАДО ДОПИСАТЬ ТАКИМ ОБРАЗОМ ЧТОБЫ ВЫВОДИЛИСЬ ВСЕ ДАННЫЕ
#         # user = (self.session.query(tables.Users.id, tables.Users.tel).filter_by(id=id_user).
#         # order_by(desc(tables.Users.id)).first())
#         if not user:
#             raise UnfoundEntity(
#                 message="Нет такого пользователя!"
#             )
#         return user
#
#     def get_id_user_by_tel(self, user_data: str) -> UserMy.id:
#         return self._get(user_data)
#
#     # Зашифровываем токен
#     def token_encode(self, id_user: int):
#         try:
#             token = jwt.encode({"id": id_user}, SECRET_JWT, algorithm="HS256")
#             return token
#         except JWTError as e:
#             raise InaccessibleEntity(message="Неправильный токен")
#
#     # расшифровывание токена
#     def token_decode(self, token: str):
#         try:
#             token = jwt.decode(token, SECRET_JWT, algorithms=["HS256"])
#             return token
#         except JWTError as e:
#             raise InaccessibleEntity(message="Неправильный токен")
#
#     #  Добавляет аватарку если нет, а если есть заменяет
#     def adding_photo(self, num, id_user: int, file: Optional[UploadFile] ):
#     # def adding_photo(self,
#     #                  num,
#     #                  id_user: int,
#     #                  file: UploadFile | None = None,
#     #                  ):
#
#         if file is None:
#             self.session.query(UserMy).filter(UserMy.id == id_user).update({f'photo_{num}': None})
#             return {"photo": None}
#
#         filename = file.filename
#         path_name = f'{os.getcwd()}/Mediafile/Photo_users/{id_user}/{num}/'
#         if not os.path.exists(path_name):
#             os.makedirs(path_name)
#
#         with open(path_name + filename, "wb") as wf:
#             shutil.copyfileobj(file.file, wf)
#             file.file.close()  # удаляет временный
#         path_name = path_name + filename
#         self.session.query(UserMy).filter(UserMy.id == id_user).update({f'photo_{num}': path_name})
#         self.session.commit()
#         if not file:
#             raise UnfoundEntity(message="Не отправлен загружаемый файл")
#         else:
#             return {"photo": path_name}
