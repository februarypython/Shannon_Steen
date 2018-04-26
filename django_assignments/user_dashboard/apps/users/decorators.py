from django.shortcuts import redirect
# import .views

#ensure user is in session
def required_login(views_func):
    def _wrapped_views_func(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login_registration:homepage')
        else:
            return views_func(request, *args, **kwargs)
    return _wrapped_views_func