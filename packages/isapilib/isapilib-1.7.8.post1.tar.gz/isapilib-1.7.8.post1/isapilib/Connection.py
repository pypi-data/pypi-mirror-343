from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connections

from isapilib.exceptions import SepaException


def add_conn(username, gwmbac=None, idbranch=None):
    try:
        user_model_path = getattr(settings, 'AUTH_USER_MODEL', 'isapilib.UserAPI')
        branch_model_path = getattr(settings, 'BRANCH_MODEL', 'isapilib.SepaBranch')
        permission_model_path = getattr(settings, 'PERMISSION_MODEL', 'isapilib.SepaBranchUsers')

        user_model = apps.get_model(user_model_path, require_ready=False)
        branch_model = apps.get_model(branch_model_path, require_ready=False)
        permission_model = apps.get_model(permission_model_path, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError as e:
        if settings.AUTH_USER_MODEL in str(e):
            raise ImproperlyConfigured(
                f"AUTH_USER_MODEL refers to model '{settings.AUTH_USER_MODEL}' that has not been installed"
            )
        elif settings.BRANCH_MODEL in str(e):
            raise ImproperlyConfigured(
                f"BRANCH_MODEL refers to model '{settings.BRANCH_MODEL}' that has not been installed"
            )
        elif settings.PERMISSION_MODEL in str(e):
            raise ImproperlyConfigured(
                f"PERMISSION_MODEL refers to model '{settings.PERMISSION_MODEL}' that has not been installed"
            )
        else:
            raise e

    user = branch = None
    try:
        user = user_model.objects.get(usuario=username)
        permissions = permission_model.objects.filter(iduser=user)

        if gwmbac:
            branch = branch_model.objects.filter(gwmbac=gwmbac)
        if idbranch:
            branch = branch_model.objects.filter(pk=idbranch)

        if not branch or not branch.exists():
            raise branch_model.DoesNotExist

        try:
            branch = branch.get(id__in=permissions.values_list('idbranch', flat=True))
        except branch_model.DoesNotExist:
            raise permission_model.DoesNotExist

        conn = f'external-{branch.id}'
        connections.databases[conn] = create_conn(branch)
        return conn
    except user_model.DoesNotExist:
        raise SepaException('The user does not exist')
    except branch_model.DoesNotExist:
        raise SepaException('The agency does not exist', user)
    except permission_model.DoesNotExist:
        raise SepaException('You do not have permissions on the agency', user, branch)


def get_version(version=6000):
    version = version or 6000

    if 5000 > version >= 4000:
        return '4000'

    return '6000'


def create_conn(_branch):
    return {
        'ENGINE': 'mssql',
        'NAME': _branch.conf_db if _branch.conf_db else '',
        'USER': _branch.conf_user if _branch.conf_user else '',
        'PASSWORD': _branch.conf_pass if _branch.conf_pass else '',
        'HOST': _branch.conf_ip_ext if _branch.conf_ip_ext else '',
        'PORT': _branch.conf_port if _branch.conf_port else '',
        'INTELISIS_VERSION': get_version(_branch.version),
        'TIME_ZONE': None,
        'CONN_HEALTH_CHECKS': None,
        'CONN_MAX_AGE': None,
        'ATOMIC_REQUESTS': None,
        'AUTOCOMMIT': True,
        'OPTIONS': settings.DATABASES['default'].get('OPTIONS')
    }
