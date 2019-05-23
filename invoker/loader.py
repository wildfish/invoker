from __future__ import absolute_import

import importlib
import inspect

import six
from invoke import Collection, Task
from chainmap import ChainMap


_app_spec_defaults = {
    'namespace': None,
    'envs': None
}


class App:
    default_context_processors = [
        'invoker.context_processors.add_env_context'
    ]

    def __init__(self, path=None, namespace=None, envs=None, context_processors=None):
        self.path = path
        self.namespace = namespace
        self.envs = envs

        self.context_processors = [
            self.load_context_processor(p)
            for p in self.default_context_processors + (context_processors or [])
        ]

    def get_namespace_name(self):
        return self.namespace or self.path.rsplit('.')[-1]

    def get_module(self):
        return importlib.import_module(self.path)

    def load_context_processor(self, path):
        _split = path.split('.')
        module = importlib.import_module('.'.join(_split[:-1]))
        return getattr(module, _split[-1])

    def add_context_processors_to_task(self, task):
        _orig_body = task.body

        def _body(ctx, *args, **kwargs):
            for fn in self.context_processors:
                ctx = fn(ctx)

            return _orig_body(ctx, *args, **kwargs)

        _body.__signature__ = inspect.signature(_orig_body)
        task.body = _body
        return task

    def add_context_processor_to_collection(self, collection):
        for task in collection.tasks.values():
            self.add_context_processors_to_task(task)
        return collection

    def get_tasks(self):
        module = self.get_module()

        props = (getattr(module, name) for name in dir(module))
        for obj in props:
            if isinstance(obj, Task):
                yield obj

    def get_collection(self, env=None):
        module = self.get_module()

        if getattr(module, 'ns', None) and isinstance(module.ns, Collection):
            # if a namespace is exposed use that
            collection = self.add_context_processor_to_collection(module.ns)
            collection.name = self.get_namespace_name()
        else:
            # if no namespace is exposed gather each task and add those
            collection = Collection(self.get_namespace_name())

            for t in self.get_tasks():
                collection.add_task(self.add_context_processors_to_task(t))

        return collection


def get_app_spec(app):
    if isinstance(app, six.string_types):
        return ChainMap({'path': app}, _app_spec_defaults)
    else:
        if 'path' not in app:
            raise ValueError(
                'Each app specified must be a string or a dictionary containing a path'
            )

        return ChainMap(app, _app_spec_defaults)


def get_apps(apps, context_processors):
    return [App(**get_app_spec(app_spec), context_processors=context_processors) for app_spec in apps]
