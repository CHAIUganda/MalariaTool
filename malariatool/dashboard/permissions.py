from rolepermissions.permissions import register_object_checker

from dashboard.roles import AdminRole, IPUserRole


@register_object_checker()
def add_users(role):
    if role == AdminRole:
        return True
    return False


@register_object_checker()
def add_implemting_partners(role):
    if role == AdminRole:
        return True
    return False


@register_object_checker()
def add_tasks(role):
    if role == IPUserRole or AdminRole:
        return True
    return False


@register_object_checker()
def add_document(role):
    if role == IPUserRole or AdminRole:
        return True
    return False


@register_object_checker()
def update_task(role):
    if role == IPUserRole:
        return True
    return False


@register_object_checker()
def add_notes(role):
    if role == IPUserRole or AdminRole:
        return True
    return False
