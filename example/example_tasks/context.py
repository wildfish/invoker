from __future__ import print_function

from invoke import task, Collection

from invoker.context import EnvContext


@task(default=True, help={'param': 'The name of the param to display from the context'})
def get(ctx, param):
    """
    Prints the value of the supplied context variable.
    """
    ctx = EnvContext(ctx)

    if ctx.get('env'):
        print('The environment is set to:', ctx['env'])
    else:
        print('The environment is not set')

    if param in ctx:
        print(param, '=', ctx[param])
    else:
        print(param, 'is not present in the context')


ns = Collection(
    'context',
    get,
)
