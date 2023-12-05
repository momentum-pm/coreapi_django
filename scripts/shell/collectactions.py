from django.apps import apps
import importlib
from authentication.groups import Groups, Group
from authentication.models import Grant


def run():
    insert_groups = []
    for attr_name in dir(Groups):
        attr = getattr(Groups, attr_name)
        if isinstance(attr, Group):
            group = attr
            if not Group.objects.filter(key=group.key).exists():
                insert_groups.append(group)
    Group.objects.bulk_create(insert_groups)
    for name, app in apps.app_configs.items():
        actions = getattr(app, "actions", False)
        from authentication.models import Action

        if actions:
            actions_module = importlib.__import__(app.name + ".actions")
            actions_file = getattr(actions_module, "actions")
            Actions = getattr(actions_file, "Actions")
            attribute_names = dir(Actions)
            registration_list = []

            for attribute_name in attribute_names:
                attribute = getattr(Actions, attribute_name)
                attribute_class = attribute.__class__
                if attribute_class == Action:
                    attribute.is_visible = True
                    registration_list.append(attribute)
            print(f"Actions of {name}:")
            Action.register_actions(registration_list, True)
    for name, app in apps.app_configs.items():
        actions = getattr(app, "actions", False)
        from authentication.models import Action

        if actions:
            try:
                grants_module = importlib.__import__(app.name + ".grants")
                grants_file = getattr(grants_module, "grants")
                grants = getattr(grants_file, "grants")
                insert_grants = []
                for grant in grants:
                    group_key = grant.group.key
                    action_path = grant.action.path
                    if not Grant.objects.filter(
                        group__key=group_key, action__path=action_path
                    ).exists():
                        group = Group.objects.get(key=group_key)
                        action = Action.objects.get(path=action_path)
                        grant = Grant(action=action, group=group)
                        insert_grants.append(grant)

                Grant.objects.bulk_create(insert_grants)
            except ModuleNotFoundError:
                pass
    return True
