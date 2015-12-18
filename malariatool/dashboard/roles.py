from rolepermissions.roles import AbstractUserRole


class AdminRole(AbstractUserRole):
    available_permissions = {
        'add_implementing_partner': True,
        'add_document': True,
        'add_users': True,
        'add_tasks': True,
        'add_notes': True,
        'add_meetings': True

    }


class IPUserRole(AbstractUserRole):
    available_permissions = {
        'add_document': True,
        'update_tasks': True,
        'update_notes': True,
    }
