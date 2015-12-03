from rolepermissions.permissions import register_object_checker

from dashboard.roles import Admin, IPUser


@register_object_checker()
def add_users(role):
    if role == Admin:
        return True
    return False


@register_object_checker()
def add_implemting_partners(role):
    if role == Admin:
        return True
    return False


@register_object_checker()
def add_tasks(role):
    if role == IPUser:
        return True
    return False


@register_object_checker()
def add_document(role):
    if role == IPUser or Admin:
        return True
    return False
