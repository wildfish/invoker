from unittest import TestCase
from invoke import Context

from invoker import invoker
from invoker.context import EnvContext


def test_processor(ctx):
    ctx['foo'] = 'bar'
    return ctx


class ContextProcessors(TestCase):
    def test_task_is_bare_task___context_is_converted_to_env_context(self):
        ns = invoker(
            apps=[
                'tests.examples.bare_tasks',
            ]
        )

        res = ns.collections['bare-tasks'].tasks['noop'](Context({}))

        self.assertIsInstance(res, EnvContext)

    def test_task_is_ns_task___context_is_converted_to_env_context(self):
        ns = invoker(
            apps=[
                'tests.examples.ns_tasks',
            ]
        )

        res = ns.collections['ns-tasks'].tasks['noop'](Context({}))

        self.assertIsInstance(res, EnvContext)

    def test_task_is_bare_task___context_is_converted_to_env_context_with_extra_processors(self):
        ns = invoker(
            apps=[
                'tests.examples.bare_tasks',
            ],
            context_processors=['tests.test_context_processors.test_processor']
        )

        res = ns.collections['bare-tasks'].tasks['noop'](Context({}))

        self.assertIsInstance(res, EnvContext)
        self.assertEqual(res['foo'], 'bar')

    def test_task_is_ns_task___context_is_converted_to_env_context_with_extra_processors(self):
        ns = invoker(
            apps=[
                'tests.examples.ns_tasks',
            ],
            context_processors=['tests.test_context_processors.test_processor']
        )

        res = ns.collections['ns-tasks'].tasks['noop'](Context({}))

        self.assertIsInstance(res, EnvContext)
        self.assertEqual(res['foo'], 'bar')
