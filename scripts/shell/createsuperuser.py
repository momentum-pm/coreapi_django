from authentication.models import User, Membership
from authentication.groups import Groups, Group


def run(username, password):
    (user, created) = User.objects.get_or_create(
        username=username, defaults={"username": username}
    )
    if not created:
        print("User with username already exists")
    user.is_superuser = True
    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.set_password(password)
    user.save()
    admin_group = Groups.admin
    group = Group.objects.get(key=admin_group.key)
    Membership.objects.create(user=user, group=group)
    print("User is ready with given credentials")
    return True
