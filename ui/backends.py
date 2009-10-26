from crypt import crypt

from django.contrib.auth.models import User

from models import Bugs, Attachments, Profiles


class BugzillaBackend:

    def authenticate(self, username=None, password=None):
        try:
            bugzilla_user = Profiles.objects.get(login_name__exact=username)
        except Profiles.DoesNotExist:
            return
        pwd_valid = crypt(password, bugzilla_user.cryptpassword) == \
                bugzilla_user.cryptpassword
        if pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username, password=password)
            # make sure the password is in sync with bugzilla
            user.set_password(password)
            user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
