from invoke import Collection

from .loader import get_apps


def invoker(apps=None, envs=None, context_processors=None):
    root_collection = Collection()

    # setup the collection for each environment
    env_collections = {env: Collection(env) for env in envs or []}
    for col in env_collections.values():
        root_collection.add_collection(col)

    # add each app to the root collection or each relevant env collection
    for app in get_apps(apps):
        if (app.envs is None and envs) or app.envs:
            for env in app.envs or envs or []:
                env_collections[env].add_collection(app.get_collection(env=env))
        else:
            root_collection.add_collection(app.get_collection())

    return root_collection
