from invoke import Context


class EnvContext(Context):
    def __getitem__(self, item):
        super_self = super(EnvContext, self)

        env = None
        if super_self.__contains__('env'):
            env = super_self.__getitem__('env')

        if (env and super_self.__contains__('envs') and env in super_self.__getitem__('envs') and item in super_self.__getitem__('envs')[env]):
            return super_self.__getitem__('envs')[env][item]
        else:
            return super_self.__getitem__(item)
