from django.shortcuts import redirect, render
from django.urls import reverse

from social_core.exceptions import AuthAlreadyAssociated

class GitHubAuthAlreadyAssociatedMiddleware(SocialAuthExceptionMiddleware):
    """Redirect users to desired-url when AuthAlreadyAssociated exception occurs."""
    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            if request.backend.name == "github":
                message = "This email is already in use."
                if message in str(exception):
                    # Add logic if required

                    # User is redirected to any url you want
                    # in this case to "app_name:url_name"
                    # return redirect(reverse("app_name:url_name"))
                    return render(request,'messages.html', {'messsgae': message})