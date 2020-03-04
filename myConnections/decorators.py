from django.http import HttpResponseForbidden


def person_required(f):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    def user_is_person(request, *args, **kwargs):
        if not request.user.is_person:
            return HttpResponseForbidden("<h1 style='font-weight: bolder;'>FORBIDDEN</h1>")
        return f(request, *args, **kwargs)
    
    return user_is_person


def organisation_required(f):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    def user_is_organisation(request, *args, **kwargs):
        if not request.user.is_organisation:
            return HttpResponseForbidden("<h1 style='font-weight: bolder;'>FORBIDDEN</h1>")
        return f(request, *args, **kwargs)

    return user_is_organisation