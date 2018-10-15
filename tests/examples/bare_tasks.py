from invoke import task


@task()
def noop(ctx):
    return ctx
