import string
from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text

from invoker.context import EnvContext
from tests.strategies import namespace_names


class TestEnvContest(TestCase):
    @given(text(min_size=1, max_size=10, alphabet=string.ascii_letters),
           text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_env_is_not_present_in_the_context___param_from_the_root_context_is_returned(self, key, val):
        ctx = EnvContext({key: val})

        self.assertEqual(ctx[key], val)

    @given(text(min_size=1, max_size=10, alphabet=string.ascii_letters),
           text(min_size=1, max_size=10, alphabet=string.ascii_letters),
           namespace_names())
    def test_val_is_not_present_in_env_config___param_from_the_root_context_is_returned(self, key, val, env):
        ctx = EnvContext({
            key: val,
            'env': env,
            'envs': {key + 'extra': val + 'extra'},
        })

        self.assertEqual(ctx[key], val)

    @given(text(min_size=1, max_size=10, alphabet=string.ascii_letters),
           text(min_size=1, max_size=10, alphabet=string.ascii_letters),
           namespace_names(),
           text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_val_is_present_in_env_config___param_from_the_env_context_is_returned(self, key, val, env, env_val):
        ctx = EnvContext({
            key: val,
            'env': env,
            'envs': {
                env: {key: env_val}
            },
        })

        self.assertEqual(ctx[key], env_val)
