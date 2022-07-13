import datetime
import logging
from typing import Any, Dict, Optional, Union, Type, List, Tuple

import pytz
from app.getters.timestamp import to_timestamp
from app.models import Topic, LessonMember, Hug
from app.models.lesson_member import MemberStatus
from app.schemas.response import Paginator
from app.utils import pagination
from botocore.client import BaseClient
from coverage.annotate import os
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import File
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy import cast, String, or_, not_, and_, func, desc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_token, ALGORITHM
from app.crud.base import CRUDBase
from app.crud.crud_topic import topic as topic_crud
from app.crud.crud_story_attachment import story_attachment as attachment_crud
from app.models.story import Story
from app.models.group import Group
from app.models.personal_experience import PersonalExperience
from app.schemas.story import CreatingStory, UpdatingStory, UpdatingStory
from app.utils.security import generate_random_password
from ..email_senders import BaseEmailSender
from app.models.user import User

from ..models import Hashtag, StoryHashtag, StoryAttachment, View
from ..webinar_api.base import AbstractWebinarApi, EventSessionStartType, EventLang, MemberRole


class CRUDStory(CRUDBase[Story, CreatingStory, UpdatingStory]):
    def create_story_by_user(self, db, *, user: User, obj_in: CreatingStory):
        db_obj = Story()
        db_obj.user = user
        db_obj.text = obj_in.text
        db_obj.is_prof = user.is_prof
        db_obj.is_private = obj_in.is_private if obj_in.is_private is not None else None

        if obj_in.topic is not None:
            if topic_crud.get_by_id(db, id=obj_in.topic) is None:
                return None, -1, None

        db_obj.topic_id = obj_in.topic
        db.add(db_obj)

        attachments = []

        if obj_in.gallery is not None:
            not_found = []
            forbidden = []
            rebinding = []
            for index, attachment_id in enumerate(obj_in.gallery):
                attachment = attachment_crud.get_by_id(db, id=attachment_id)
                if attachment is None:
                    not_found.append(index)
                    continue
                if attachment.user != user:
                    forbidden.append(index)
                    continue
                if attachment.story is not None:
                    rebinding.append(index)
                    continue
                attachments.append(attachment)
            if len(not_found) > 0:
                return None, -2, not_found
            if len(forbidden) > 0:
                return None, -3, forbidden
            if len(rebinding) > 0:
                return None, -4, rebinding

        if obj_in.video is not None:
            attachment = attachment_crud.get_by_id(db, id=obj_in.video)
            if attachment is None:
                return None, -5, None
            if attachment.user != user:
                return None, -6, None
            if attachment.story is not None:
                return None, -7, None
            attachments.append(attachment)

        for attachment in attachments:
            attachment.story = db_obj
            db.add(attachment)

        for hashtag_text in obj_in.hashtags:
            hashtag = db.query(Hashtag).filter(Hashtag.text == hashtag_text).first()
            if hashtag is None:
                hashtag = Hashtag()
                hashtag.text = hashtag_text
                db.add(hashtag)
            story_hashtag = StoryHashtag()
            story_hashtag.story = db_obj
            story_hashtag.hashtag = hashtag
            db.add(story_hashtag)

        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def update(
        self,
        db: Session,
        *,
        db_obj: Story,
        obj_in:  Union[UpdatingStory, Dict[str, Any]]
    ):
        new_attachments = []
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if 'text' in update_data:
            db_obj.text = obj_in.text
        if 'is_private' in update_data:
            db_obj.is_private = obj_in.is_private if obj_in.is_private is not None else None
        db.add(db_obj)
        if 'topic' in update_data:
            if obj_in.topic is not None:
                if topic_crud.get_by_id(db, id=obj_in.topic) is None:
                    return None, -1, None
            db_obj.topic_id = obj_in.topic
        if 'gallery' in update_data:
            new_ids_in_gallery = update_data['gallery'] or []
            old_objs_in_gallery = db_obj.attachments.filter(StoryAttachment.is_image).all()
            old_ids_in_gallery = [item.id for item in old_objs_in_gallery]

            for_removing = []
            not_found = []
            forbidden = []
            rebinding = []

            for index, id_ in enumerate(old_ids_in_gallery):
                if id_ not in new_ids_in_gallery:
                    old_attachment = old_objs_in_gallery[index]
                    for_removing.append(old_attachment)
            for index, id_ in enumerate(new_ids_in_gallery):
                if id_ not in old_ids_in_gallery:
                    new_attachment = attachment_crud.get_by_id(db, id=id_)
                    if new_attachment is None:
                        not_found.append(index)
                    if new_attachment.user != db_obj.user:
                        forbidden.append(index)
                    if new_attachment.story is not None:
                        rebinding.append(index)
                    new_attachment.story = db_obj
                    db.add(new_attachment)

            if len(not_found) > 0:
                return None, -2, not_found
            if len(forbidden) > 0:
                return None, -3, forbidden
            if len(rebinding) > 0:
                return None, -4, rebinding

            for attachment in for_removing:
                db.delete(attachment)

        if 'video' in update_data:
            old_video = db_obj.attachments.filter(not_(StoryAttachment.is_image)).first()
            new_video_id = update_data['video']
            if old_video is not None and old_video.id != update_data['video']:
                old_video.story = None
            if new_video_id is not None:
                new_video = attachment_crud.get_by_id(db, id=new_video_id)
                if new_video is None:
                    return None, -5, None
                if new_video.user != db_obj.user:
                    return None, -6, None
                if new_video.story is not None:
                    return None, -7, None
                new_attachments.append(new_video)

        if 'hashtags' in update_data:
            old_hashtags = {
                hashtag_text: id_
                for hashtag_text, id_
                in db.query(Hashtag.text, StoryHashtag).join(StoryHashtag).filter(StoryHashtag.story == db_obj)
            }
            new_hashtags = update_data['hashtags']

            for hashtag_text, story_hashtag in old_hashtags.items():
                if hashtag_text not in new_hashtags:
                    db.delete(story_hashtag)
            for hashtag_text in new_hashtags:
                if hashtag_text not in old_hashtags:
                    hashtag = db.query(Hashtag).filter(Hashtag.text == hashtag_text).first()
                    if hashtag is None:
                        hashtag = Hashtag()
                        hashtag.text = hashtag_text
                        db.add(hashtag)
                    story_hashtag = StoryHashtag()
                    story_hashtag.story = db_obj
                    story_hashtag.hashtag = hashtag
                    db.add(story_hashtag)

        db.commit()
        db.refresh(db_obj)
        return db_obj, 0, None

    def get_stories_by_user(
        self,
        db: Session,
        *,
        user: User,
        page: Optional[int] = None,
    ) -> Tuple[List[Story], Paginator]:
        query = db.query(Story).filter(Story.user == user).order_by(desc(Story.created))

        return pagination.get_page(query, page)

    def get_stories(
            self,
            db,
            *,
            topic:
            Optional[Topic],
            hashtag: Optional[Hashtag],
            user: Optional[User],
            page: Optional[int]
    ) -> Tuple[List[Story], Paginator]:

        query = db.query(Story)
        now = datetime.datetime.utcnow()

        if user is not None:
            query = query.filter(Story.user == user)
        if hashtag is not None:
            query = query.join(StoryHashtag).filter(StoryHashtag.hashtag == hashtag)
        if topic is not None:
            query = query.filter(Story.topic == topic)

        query = query.filter(
            or_(
                and_(Story.is_prof, now - Story.created <= datetime.timedelta(days=90)),
                and_(not_(Story.is_prof), now - Story.created <= datetime.timedelta(days=10)),
            ),
        ).order_by(desc(Story.created)).distinct()

        return pagination.get_page(query, page)

    def mark_story_as_viewed(
            self,
            db,
            *,
            story: Story,
            user: User
    ):
        view = db.query(View).filter(View.story == story, View.user == user).first()
        if view is None:
            view = View()
            view.user = user
            view.story = story
            db.add(view)
            db.commit()

    def hug_story(
            self,
              db,
              *,
              story: Story,
              user: User,
              hugs: bool
    ):
        hug = db.query(Hug).filter(Hug.story == story, Hug.user == user).first()
        if hug is None and hugs:
            hug = Hug()
            hug.story = story
            hug.user = user
            db.add(hug)
            db.commit()
        elif hug is not None and not hugs:
            db.delete(hug)
            db.commit()


story = CRUDStory(Story)
