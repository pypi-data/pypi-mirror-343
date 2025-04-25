from django.conf import settings
from wagtail import hooks

@hooks.register('register_admin_middleware')
def register_filter_persistence_middleware():
    from .middleware import WagtailFilterPersistenceMiddleware
    return WagtailFilterPersistenceMiddleware