def validate_wrapper(validation_func):
    def real_decorator(func):
        def wrapper_arg_dict(*args, **kwargs):
            validation_func(*args, **kwargs)
            func(*args, **kwargs)
        return wrapper_arg_dict
    return real_decorator
