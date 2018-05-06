from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


class SwipeLoginRequired(LoginRequiredMixin):
    """
    The Swipe implementation of checking if the user who tried to access an endpoint was logged in. Any view that
    should be protected by user authentication should inherit from this class FIRSTLY. If done later in the inheritance
    chain it might be skipped.
    """

    def __init__(self):
        super(SwipeLoginRequired, self).__init__()
        self.raise_exception = True

    def handle_no_permission(self):
        if self.raise_exception:
            return HttpResponse('401 Unauthorized', status=401)
