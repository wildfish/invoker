# Example

This is an example invoker setup that can be used to inspect the
environment specific context.

## Setup

The only requirement is to install invoker into your virtualenv::

    pip install ..
    
## Commands

The example only gives one command `context`. This is available in
each of the envs (``prod`` and ``stage``) as well as at the root.

    $ inv --list
    Available tasks:
    
      context.get (context)               Prints the value of the supplied context variable.
      prod.context.get (prod.context)     Prints the value of the supplied context variable.
      stage.context.get (stage.context)   Prints the value of the supplied context variable.

The config for the context can be found in the `invoke.yml` file.

We can then run the command on each env to get the values for the 
supplied context variables::

    $ inv context foo context bar
    The environment is not set
    foo = abc
    The environment is not set
    bar = 123
    
    $ inv stage.context foo stage.context bar
    The environment is set to: stage
    foo = abc
    The environment is set to: stage
    bar = stage's bar value

    $ inv prod.context foo prod.context bar
    The environment is set to: prod
    foo = prod's foo value
    The environment is set to: prod
    bar = 123

## More examples

More examples of tasks apps will be provided soon...