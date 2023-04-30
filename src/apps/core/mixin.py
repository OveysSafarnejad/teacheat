# -*- coding: utf-8 -*-
"""
core mixin module.
"""

from apps.core.exceptions import InvalidHookTypeError
from apps.core.structs import Hook


class HookMixin:
    """
    hook mixin class.

    every class that needs to provide hooks must inherit from this.
    """

    hook_type = Hook
    invalid_hook_type_error = InvalidHookTypeError

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of HookMixin.
        """

        super().__init__()
        self._hooks = []

    def _get_hooks(self):
        """
        gets all registered hooks.

        :rtype: list
        """

        return self._hooks

    def register_hook(self, instance):
        """
        registers the given instance into hooks.

        :param Hook instance: hook instance to be registered.

        :raises InvalidHookTypeError: invalid hook type error.
        """

        if not isinstance(instance, self.hook_type):
            raise self.invalid_hook_type_error('Input parameter [{instance}] is '
                                               'not an instance of [{hook}].'
                                               .format(instance=str(instance),
                                                       hook=self.hook_type))

        self._hooks.append(instance)
