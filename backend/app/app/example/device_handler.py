# from typing import Optional
#
# from sqlalchemy import desc
# from sqlalchemy.orm import Session
# from user_agents import parse
#
# from app.models import User
# from app.models.device import Device
# from app.models.firebase_token import FirebaseToken
#
#
# def _handle_device(
#             self,
#             db: Session,
#             owner: User,
#             host: Optional[str] = None,
#             x_real_ip: Optional[str] = None,
#             accept_language: Optional[str] = None,
#             user_agent: Optional[str] = None,
#             x_firebase_token: Optional[str] = None
#         ):
#
#         device = db.query(Device).filter(
#             Device.user == owner,
#             Device.ip_address == host,
#             Device.x_real_ip == x_real_ip,
#             Device.accept_language == accept_language,
#             Device.user_agent == user_agent
#         ).order_by(desc(Device.created)).first()
#
#         detected_os = None
#
#         if user_agent is not None:
#             ua_string = str(user_agent)
#             ua_object = parse(ua_string)
#
#             detected_os = ua_object.os.family
#             if detected_os is None or detected_os.lower() == 'other':
#                 if 'okhttp' in user_agent.lower():
#                     detected_os = 'Android'
#                 elif 'cfnetwork' in user_agent.lower():
#                     detected_os = 'iOS'
#                 else:
#                     detected_os = None
#
#         if device is None:
#             device = Device()
#             device.user = owner
#             device.ip_address = host
#             device.x_real_ip = x_real_ip
#             device.accept_language = accept_language
#             device.user_agent = user_agent
#             device.detected_os = detected_os
#         db.add(device)
#
#         if x_firebase_token is not None:
#             firebase_token = FirebaseToken()
#             firebase_token.device = device
#             firebase_token.value = x_firebase_token
#             db.add(firebase_token)
#
#         db.commit()
