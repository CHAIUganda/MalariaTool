from rolepermissions.roles import AbstractUserRole


class AdminRole(AbstractUserRole):
    available_permissions = {
        'add_implementing_partner': True,
        'add_document': True,
        'add_users': True,
    }


class IPUserRole(AbstractUserRole):
    available_permissions = {
        'add_task': True,
        'add_document': True,
    }
