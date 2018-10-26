from unittest import TestCase

import six
from hypothesis import given, assume

from invoker import invoker
from tests.strategies import namespace_names, apps


class TestInvoker(TestCase):
    @given(apps())
    def test_no_env_is_given___tasks_are_added_to_the_root(self, app):
        ns = invoker(
            apps=[app[1]]
        )

        self.assertIn(app[0], list(ns.collections.keys()))
        self.assertIn('noop', ns.collections[app[0]].tasks)

    @given(apps(), namespace_names(), namespace_names())
    def test_envs_are_given___tasks_are_added_to_the_envs(self, app, first, second):
        assume(first != second)

        ns = invoker(
            apps=[app[1]],
            envs=[first, second],
        )

        self.assertEqual(list(sorted([first, second])), list(sorted(ns.collections.keys())))
        self.assertIn('noop', ns.collections[first].collections[app[0]].tasks)
        self.assertIn('noop', ns.collections[second].collections[app[0]].tasks)

    @given(apps(), namespace_names(), namespace_names())
    def test_envs_are_given_and_specified_for_the_app___tasks_are_added_to_the_specified_envs(self, app_name, first, second):
        assume(first != second)

        ns = invoker(
            apps=[{'path': app_name[1], 'envs': [first]}],
            envs=[first, second],
        )

        self.assertEqual(list(sorted([first, second])), list(sorted(ns.collections.keys())))
        self.assertIn('noop', ns.collections[first].collections[app_name[0]].tasks)
        self.assertNotIn(app_name[0], ns.collections[second].collections)

    def test_path_is_not_specified___value_error_is_raised(self):
        with six.assertRaisesRegex(self, ValueError, 'Each app specified must be a string or a dictionary containing a path') as ex:
            invoker(
                apps=[{'envs': ['first']}],
                envs=['first', 'second'],
            )

    @given(apps(), namespace_names(), namespace_names(), namespace_names())
    def test_app_has_an_overridden_namespace___tasks_are_added_to_the_envs_with_specified_env(self, app_name, first, second, custom):
        assume(first != second)

        ns = invoker(
            apps=[{'path': app_name[1], 'envs': [first], 'namespace': custom}],
            envs=[first, second],
        )

        self.assertEqual(list(sorted([first, second])), list(sorted(ns.collections.keys())))
        self.assertIn('noop', ns.collections[first].collections[custom].tasks)
        self.assertNotIn(custom, ns.collections[second].collections)

    @given(apps(), namespace_names())
    def test_env_name_is_added_to_namespace_configuration(self, app_name, env_name):
        ns = invoker(
            apps=[app_name[1]],
            envs=[env_name],
        )

        self.assertEqual(env_name, ns.collections[env_name].configuration()['env'])
