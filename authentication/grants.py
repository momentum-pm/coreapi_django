from authentication.groups import Groups
from authentication.actions import Actions
from authentication.models import Grant

grants = [
    Grant(group=Groups.admin, action=Actions.authentication),
]
