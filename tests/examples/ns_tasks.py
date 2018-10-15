from invoke import task, Collection


@task()
def noop(ctx):
    return ctx


ns = Collection()
ns.add_task(noop)
