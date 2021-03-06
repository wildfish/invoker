invoker
=======

.. image:: https://travis-ci.org/wildfish/invoker.svg?branch=master
    :target: https://travis-ci.org/wildfish/invoker

.. image:: https://codecov.io/gh/wildfish/invoker/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/wildfish/invoker

A wrapper around `invoke <http://www.pyinvoke.org/>`_ to help
facilitate sharing tasks and specifying multiple environments
to run tasks against for instance running tasks against staging
and production environments.

Configuration
-------------

The simplest configuration is to specify a set of task files to
import::

    from invoker import invoker

    ns = invoker(
        apps=['path.to.my.tasks'],
    )

This should be stored in your ``tasks.py`` file. To add environments
you can specify them in the ``invoker`` call::

    from invoker import invoker

    ns = invoker(
        apps=['path.to.my.tasks'],
        envs=['stage', 'prod'],
    )

The environment name will be added to the tasks context as ``env``.
As well as the app paths you can also specify other options by
supplying a dictionary for each app that requires additional
options::

    from invoker import invoker

    ns = invoker(
        apps=[
            {'path': 'path.to.my.tasks', 'envs': ['stage'], 'namespace': 'foo'}
        ],
        envs=['stage', 'prod'],
    )

In this example the tasks at ``path.to.my.tasks`` will be loaded
into the ``stage`` environment under the ``foo`` namespace, these
tasks can be called using::

    inv stage.foo.<task>

The only required parameter is ``path``, all other parameters are
optional. These are described below.

* **envs** - A list of environments to add the applications tasks
  to. If this is not supplied the tasks will be added to all
  specified environments. Each environment specified on an app must
  be present in the main ``envs`` setting.
* **namespace** - Specifies a namespace to load the namespace tasks
  into. If this is not set the name of the module is used.
* **context_processors** - Specifies paths to a list of functions to
  apply to the context before running the task (see
  `Context Processors <#context-processors>`_).

The invoke config can remain the same. However it is possible to
configure each environment separately in the ``'envs'`` section.
If a key is present in the environment specific config that value
will be used over the entry from the root config provided
``EnvConfig`` if used in the task. To specify environment specific
configurations your conig file may look something like this::

    {
        'key': 'value',
        'envs': {
            'stage': {
                'key': 'stage val',
            },
            'prod': {
                'key': 'prod val',
            }
        }
    }

Apps
----

Apps are packages that specify which tasks to include under the
namespace. These are normal invoke task files, for example you may
have an app in ``bash.py``::

    from invoke import task, run

    @task()
    def echo(ctx, message):
        run('echo {}'.format(message))

To add extra configuration options you can specify an invoke
collection called ``ns``::

    from invoke import task, run, Collection

    @task()
    def echo(ctx, message):
        run('echo {}'.format(message))

    ns = Collection()
    ns.add_task(echo)
    ns.configure({
        'param': 'default value'
    })


EnvContext
----------

The context supplied to each of your tasks will behave similarly
to the normal invoke context however it has be changed to handle
environments better, for example, with the following config::

    {
        'key': 'value',
        'envs': {
            'stage': {
                'key': 'stage val',
            },
            'prod': {
                'other': 'other val',
            }
        }
    }

In the ``prod`` environment calling using ``ctx['key']`` will
return ``'value'`` as there is no ``'key'`` entry in the ``'prod'``
specific config. In the ``stage`` environment using ``ctx['key']``
will return ``'stage val'``.

Context Processors
------------------

A context processor if a function that takes a single argument (the
current context) and returns a modified context. For example::

    def add_foo(ctx):
        ctx['foo'] = 'bar'
        return ctx

Will add ``foo`` with a value ``'bar'`` to the context.

Context processors can be configured in 2 ways, by setting
``'context_processors'`` on an app spec to a list of paths of functions
to call or by passing the list to the ``invoker`` call::

    invoker(
        ...
        context_processors=['foo.bar.func']
    )

Any context processors added as an argument to ``invoker`` will be added
to all apps where as those passed as part of the app spec will only be
added to the relevant app.

**NOTE:** ``invoker.context_processors.make_env_context`` is always added
to the context processors to ensure the environment specific context is
always available.
