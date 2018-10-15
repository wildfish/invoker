import string

from hypothesis.strategies import text, sampled_from


def namespace_names():
    return text(min_size=1, max_size=10, alphabet=string.ascii_letters)


def apps():
    return sampled_from([
        ('bare-tasks', 'tests.examples.bare_tasks'),
        ('ns-tasks', 'tests.examples.ns_tasks'),
    ])
