import datetime
from typing import Optional

from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, status

from app.db.session import get_session

from app.models.verif_code import VerifCode

from app.exceptions import UnprocessableEntity

from app.schemas.verif_code import VerifCodeSaveOnBase, CheckCode
from sqlalchemy import desc

# from app import db
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.exceptions import UnfoundEntity

from app.schemas.verif_code import UsedVerifCode

TIME_IS_AVAILABLE_VERIF_CODE = 1111


class VerifCodesServices(CRUDBase[VerifCode, VerifCodeSaveOnBase, CheckCode]):
    def get_code(self, db: Session, *, tel: str, code: str) -> Optional[VerifCode]:
        verif = (db.query(VerifCode).filter(VerifCode.tel == tel, VerifCode.value == code)
                 .order_by(desc(VerifCode.id)).first())
        return verif

    def check_code_test(self, db: Session, *, tel: str, code: str) -> VerifCode:
        # Сортировка номером
        if not (db.query(VerifCode).filter_by(tel=tel).first()):
            return None, -1, None

        # Сортировка кодом
        if not (db.query(VerifCode).filter_by(tel=tel, value=code).first()):
            return None, -2, None

        # Сортировка номером, кодом, актуальностью
        if not (db.query(VerifCode).filter_by(tel=tel, value=code, actual=True).first()):
            return None, -3, None

        # Сортировка номером, кодом, актуальностью, Временем
        time_now = datetime.datetime.utcnow()
        five_minutes_ago = time_now - datetime.timedelta(minutes=TIME_IS_AVAILABLE_VERIF_CODE)
        if not db.query(VerifCode).filter(VerifCode.actual,
                                          VerifCode.value == code, VerifCode.tel == tel,
                                          VerifCode.created_at > five_minutes_ago).all():
            return None, -4, None
        good_verif_code = (db.query(VerifCode).filter(VerifCode.actual, VerifCode.value == code,
                                                      VerifCode.tel == tel, VerifCode.created_at > five_minutes_ago)
                           .order_by(desc(VerifCode.id)).first())
        return good_verif_code, 0, None

    def update_actual(self, db: Session, *, db_obj, obj_in: UsedVerifCode):
        db_obj.actual = obj_in.actual
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


verif_codes_service = VerifCodesServices(VerifCode)

# поверяет в базе корректность данных введенных пользователем ТЕЛЕФОНОМ КОДОМ АКТУАЛЬНОСТЬ И ВРЕМЯ
# def check_actual(self, db: Session, *, tel: str, code: str) -> VerifCode:
#     # Сортировка номером
#     if not (db.query(VerifCode).filter_by(tel=tel).first()):
#         raise UnprocessableEntity(
#             message="Нет такого номера!"
#             )
#     # Сортировка кодом
#     if not(db.query(VerifCode).filter_by(value=code).first()):
#         raise UnprocessableEntity(
#             message="Неправильно введенный код!"
#             )
#     # Сортировка номером, кодом, актуальностью
#     if not (db.query(VerifCode).filter_by(tel=tel, value=code, actual=True).first()):
#         raise UnprocessableEntity(
#             message="Код уже использовался! Запросите новый!"
#             )
#     # Сортировка номером, кодом, актуальностью, Временем
#     time_now = datetime.datetime.utcnow()
#     five_minutes_ago = time_now - datetime.timedelta(minutes=TIME_IS_AVAILABLE_VERIF_CODE)
#     # Добавить сюда tei, code, actual
#     if not db.query(VerifCode).filter(VerifCode.actual,
#                                       VerifCode.value == code, VerifCode.tel == tel,
#                                       VerifCode.created_at > five_minutes_ago).all():
#         raise UnprocessableEntity(
#             message="Время истекло, запросите новый код!"
#         )
#
#     verif_code_instance = (db.query(VerifCode).
#                            filter(VerifCode.actual,
#                                   VerifCode.value == code, VerifCode.tel == tel,
#                                   VerifCode.created_at > five_minutes_ago).order_by(desc(VerifCode.id)).
#                            first())
#     return verif_code_instance
