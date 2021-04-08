from datetime import datetime

from kakaowork.models import (
    UserIdentificationField,
    UserField,
    ConversationType,
    ConversationField,
)


class TestUserField:
    def test_user_field_from_dict(self):
        data = {
            'avatar_url': None,
            'department': 'test',
            'id': '1234',
            'identifications': [{
                'type': 'email',
                'value': 'user@localhost'
            }],
            'mobiles': [],
            'name': 'noname',
            'nickname': None,
            'position': None,
            'responsibility': 'leader',
            'space_id': '123',
            'tels': [],
            'vacation_end_time': 1617889170,
            'vacation_start_time': 1617889170,
            'work_end_time': 1617889170,
            'work_start_time': 1617889170,
        }
        user = UserField.from_dict(data)

        assert user.avatar_url is None
        assert user.department == 'test'
        assert user.id == '1234'
        assert user.identifications == [UserIdentificationField(type='email', value='user@localhost')]
        assert user.mobiles == []
        assert user.name == 'noname'
        assert user.nickname is None
        assert user.position is None
        assert user.responsibility == 'leader'
        assert user.space_id == '123'
        assert user.tels == []
        assert user.vacation_end_time == datetime(2021, 4, 8, 22, 39, 30)
        assert user.vacation_start_time == datetime(2021, 4, 8, 22, 39, 30)
        assert user.work_end_time == datetime(2021, 4, 8, 22, 39, 30)
        assert user.work_start_time == datetime(2021, 4, 8, 22, 39, 30)


class TestConversationField:
    def test_conversation_field_from_dict(self):
        data = {
            'id': '1',
            'type': 'dm',
            'users_count': 2,
            'avatar_url': None,
            'name': 'noname',
        }
        conversation = ConversationField.from_dict(data)

        assert conversation.id == '1'
        assert conversation.type == ConversationType.DM
        assert conversation.users_count == 2
        assert conversation.avatar_url is None
        assert conversation.name == 'noname'
