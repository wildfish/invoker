from invoker import invoker


ns = invoker(
    apps=[
        {'path': 'example_tasks.context', 'envs': []},
        'example_tasks.context'
    ],
    envs=['prod', 'stage'],
)
