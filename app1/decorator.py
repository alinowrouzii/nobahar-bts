

def check_bearer(func):
    def wrap(request, *args, **kwargs):
        try:
            HTTP_AUTHORIZATION = request.META['HTTP_AUTHORIZATION']
            if not str(HTTP_AUTHORIZATION).startswith("Bearer"):
                request.META['HTTP_AUTHORIZATION'] = "Bearer " + HTTP_AUTHORIZATION
            return func(request, *args, **kwargs)
        except Exception:
            return func(request, *args, **kwargs)
    return wrap
