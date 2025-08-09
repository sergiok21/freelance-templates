middlewares_container = []
outer_middlewares_container = []
callback_middlewares_container = []
callback_outer_middlewares_container = []


def register_middleware_class(cls):
    middlewares_container.append(cls)
    return cls


def register_outer_middleware_class(cls):
    outer_middlewares_container.append(cls)
    return cls


def register_callback_middleware_class(cls):
    callback_middlewares_container.append(cls)
    return cls


def register_callback_outer_middleware_class(cls):
    callback_outer_middlewares_container.append(cls)
    return cls
