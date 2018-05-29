from django.apps import AppConfig


class WwwConfig(AppConfig):
    name = 'www'


class PermissionApplicationConfig(AppConfig):
    """
    A runner that creates and deletes permission based on the permissions.py file data. Is used to keep permissions
    synced between the endpoints and the database.
    """
    name = 'www.apps'
    label = 'permission_updater'
    verbose_name = 'Updater for endpoint permissions'

    def ready(self):
        from crm.models import SwipePermission
        from www.permissions import PERMISSION_LIST
        try:
            all_permissions = SwipePermission.objects.all()  # type: list[SwipePermission]
            if all_permissions.count() != len(PERMISSION_LIST):
                permission_map = {}
                string_set = set(PERMISSION_LIST)
                for perm in all_permissions:
                    if perm.name not in string_set:
                        perm.delete()
                    else:
                        permission_map[perm.name] = perm
                for perm_string in PERMISSION_LIST:
                    if not permission_map.get(perm_string):
                        new_permission = SwipePermission(name=perm_string)
                        new_permission.save()
        except Exception as e:
            pass
