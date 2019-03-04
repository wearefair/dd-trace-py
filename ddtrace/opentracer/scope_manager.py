from opentracing.scope_managers import ThreadLocalScopeManager

from .utils import get_context_provider_for_scope_manager


class DDTraceAwareThreadLocalScopeManager(ThreadLocalScopeManager):
    def __init__(self, dd_context_provider=None):
        super().__init__()
        self._dd_context_provider = (dd_context_provider or
                                     get_context_provider_for_scope_manager(self))

    def activate(self, span, finish_on_close):
        val = super().activate(span, finish_on_close)
        dd_context = span._dd_context
        if dd_context is not None:
            self._dd_context_provider.activate(dd_context)
        return val

    @property
    def dd_context_provider(self):
        return self._dd_context_provider
