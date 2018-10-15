invoker
=======

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

