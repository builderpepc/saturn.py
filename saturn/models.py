import asyncio
import aiohttp
import logging
from typing import Optional, List
import datetime

class Permissions:
    def __init__(
        self,
        admin: bool = False,
        owner: bool = False,
        waitlist: bool = False,
        employee: bool = False
    ):
        self._admin = admin
        self._owner = owner
        self._waitlist = waitlist
        self._employee = employee

    @property
    def admin(self) -> bool:
        return self._admin
    
    @property
    def owner(self) -> bool:
        return self._owner
    
    @property
    def waitlist(self) -> bool:
        return self._waitlist
    
    @property
    def employee(self) -> bool:
        return self._employee

class Media:
    def __init__(self, data: dict):
        self.id = data['id']
        self.content_type = data['content_type']
        self.metadata = data['metadata']
        self.resource_url: str = data['resource_url']
        self.size_urls: dict = data['size_urls']
        self.is_bitmoji: bool = data['is_bitmoji']

class Course:
    def __init__(self, data: dict):
        raise NotImplementedError()

class BaseUser:
    def __init__(self, data: dict, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        self._update(data)
    
    def _update(self, data: dict):
        self._created_at: str = data['created_at']
        self._updated_at: str = data['updated_at']
        self.id: int = data['id']
        self.first_name: str = data['first_name']
        self.last_name: str = data['last_name']
        self.grade: int = data['grade']
        self.public: bool = data['public']
        self.is_ambassador: bool = data['is_ambassador']
        self.cohort: Optional[str] = data['user_cohort']
        self.instagram: Optional[str] = data['user_instagram']
        self.tiktok: Optional[str] = data['user_tiktok']
        self.venmo: Optional[str] = data['user_venmo']
        self.vsco: Optional[str] = data['user_vsco']
        self.education: Optional[str] = data['user_education']
        self.city: Optional[str] = data['user_city'],
        self.workplace: Optional[str] = data['user_workplace']
        self.snapchat: Optional[str] = data['user_snapchat']
        self.bio: Optional[str] = data['bio']
        self.url: Optional[str] = data['url']
        self.tags: List[str] = data['tags']
        self.school_id: str = data['school_id']
        self.name: str = data['name']
        self._profile_picture: Optional[dict] = data['profile_picture']
        self.hidden: bool = data['hidden']
        self.ambassador_school: Optional[str] = data['ambassador_school'] # Type unknown
        self.description: str = data['description']
        self.affinity: int = data['affinity']
        self.school_title: str = data['school_title']
        self.waitlist_school: Optional[str] = data['waitlist_school']
        self._courses: List[dict] = data['courses']

    @property
    def created_at(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._created_at)

    @property
    def updated_at(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._updated_at)

    @property
    def profile_picture(self) -> Optional[Media]:
        if not self._profile_picture:
            return
        
        return Media(self._profile_picture)

    @property
    def courses(self) -> List[Course]:
        return [Course(x) for x in self._courses]

class ClientUser(BaseUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update(self, data: dict):
        super()._update(data)
        self.email: str = data['email']
        self.profile_pic_url: str = data['profile_pic_url']
        self._birthday: str = data['birthday']
        self.gender: Optional[str] = data['gender']
        self.gender_preference: Optional[str] = data['gender_preference']
        self.onboarded: bool = data['onboarded']
        self.phone_number: str = data['phone_number']
        self.phone_validated: bool = data['phone_validated']
        self.granted_scopes: List[str] = data['granted_scopes']
        self.referred_by = data['referred_by'] # Type unknown
        self.ambassador_school_id = data['ambassador_school_id'] # Type unknown
        self.schedule_type_response = data['schedule_type_response'] # Type unknown
        self.lite_to_live_completed = data['lite_to_live_completed'] # Type unknown
        self.gameball_id = data['gameball_id'] # Type unknown
        self.hashid: str = data['hashid']

    @property
    def birthday(self) -> datetime.date:
        return datetime.date().fromisoformat(data['birthday'])


class User(BaseUser):
    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)