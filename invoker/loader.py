import importlib

import six
from invoke import Collection, Task
from chainmap import ChainMap


_app_spec_defaults = {
    'namespace': None,
    'envs': None
}


class App:
    def __init__(self, path=None, namespace=None, envs=None):
        self.path = path
        self.namespace = namespace
        self.envs = envs

    def get_namespace_name(self):
        return self.namespace or self.path.rsplit('.')[-1]

    def get_module(self):
        return importlib.import_module(self.path)

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
            collection = module.ns
            collection.name = self.get_namespace_name()
        else:
            # if no namespace is exposed gather each task and add those
            collection = Collection(self.get_namespace_name())

            for t in self.get_tasks():
                collection.add_task(t)

        if env:
            collection.configure({'env': env})

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


def get_apps(apps):
    return [App(**get_app_spec(app_spec)) for app_spec in apps]
