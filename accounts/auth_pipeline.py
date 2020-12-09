from social_core.exceptions import AuthException

from accounts.models import Account


def check_email_exists(backend, details, uid, user=None, *args, **kwargs):
    email = details.get('email', '')
    provider = backend.name

    # check if social user exists to allow logging in (not sure if this is necessary)
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    # check if given email is in use
    exists = Account.objects.filter(email=email).exists()

    # user is not logged in, social profile with given uid doesn't exist
    # and email is in use
    if not user and not social and exists:
        raise AuthException(backend)