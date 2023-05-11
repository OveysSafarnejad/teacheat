# -*- coding: utf-8 -*-
"""
main celery module.
"""

import logging

from celery import Task


class ExtendedTask(Task):
    """
    extended celery task class.

    this class adds support for suppressing errors on rabbitmq connection failure.
    """

    LOGGER = logging.getLogger('celery.suppressed')

    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                    link=None, link_error=None, shadow=None, **options):
        """
        executes `.apply_async` method on task.

        it could suppress any error which occurs on connecting to rabbitmq.
        all extra keyword arguments of original `apply_async` method will be passed
        to underlying method.

        :param tuple args: the positional arguments to pass on to the task.
        :param dict kwargs: the keyword arguments to pass on to the task.
        :param str task_id: task id.
        :param kombu.Producer producer: custom producer to use when publishing the task.

        :param inspect.Signature link: a single, or a list of tasks signatures
                                       to apply if the task returns successfully.

        :param inspect.Signature link_error: a single, or a list of task signatures
                                             to apply if an error occurs while executing
                                             the task.

        :param str shadow: override task name used in logs/monitoring.

        :keyword bool suppress: suppress any error during execution of the task
                                and silently logs it. defaults to False if not provided.

        :returns: the `apply_async` result
        """

        suppress = options.pop('suppress', False)

        try:
            return super().apply_async(args=args, kwargs=kwargs, task_id=task_id,
                                       producer=producer, link=link, link_error=link_error,
                                       shadow=shadow, **options)

        except Exception as error:
            if suppress is not False:
                message = 'RabbitMQ connection failed silently: {error}'
                self.LOGGER.exception(message.format(error=str(error)))
                return None

            raise

    def delay(self, *args, **kwargs):
        """
        executes `.delay` method on task.

        it could suppress any error which occurs on connecting to rabbitmq.
        all extra keyword arguments of original `delay` method will be passed to
        underlying method.

        :param object args: the positional arguments to pass on to the task.
        :param object kwargs: the keyword arguments to pass on to the task.

        :keyword bool suppress: suppress any error during execution of the task
                                and silently logs it. defaults to False if not provided.

        :returns: the `delay` result
        """

        suppress = kwargs.pop('suppress', False)
        return self.apply_async(args=args, kwargs=kwargs, suppress=suppress)
