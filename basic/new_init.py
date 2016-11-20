#!/usr/bin/env python


class config(object):

    def __init__(self, *args, **kwargs):
        print("config __init__")


#    def __new__(cls, *args, **kwargs):
#        print("config __new__")


class server(config):

    def __init__(self, ip, host):
        self.ip = ip
        self.host = host
        print("server __init__")



#    def __new__(cls, *args, **kwargs):
#        print("server __new__")



c = config()
s = server("192.168.241.12", "invoker")
print(s.ip, s.host)


class A(object):

    __impl_class = None
    __impl_kwargs = None

    def __new__(cls, *args, **kwargs):

        print("A __new__")
        base = cls.config_base()
        init_kwargs = {}
        if cls is base:
            impl = cls.config_class()
            if base.__impl_kwargs:
                init_kwargs.update(base.__impl_kwargs)
        else:
            impl = cls
        init_kwargs.update(kwargs)
        instance = super(A, cls).__new__(impl)
        instance.initialize(*args, **init_kwargs)
        return instance


    @classmethod
    def config_base(cls):
        raise NotImplementedError()

    @classmethod
    def config_default(cls):
        raise NotImplementedError()

    @classmethod
    def config_class(cls):
        base = cls.config_base()
        if cls.__impl_class is None:
            base.__impl_class  = cls.config_default()
        return base.__impl_class



class B(A):
    def __init__(self, *args, **kwargs):
        print("B __init__")
        pass

#    def __new__(cls, *args, **kwargs):
#        print("B __new__")

    def initialize(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age


    @classmethod
    def config_base(cls):
        return B

    @classmethod
    def config_default(cls):
        return B


u = B()
u.initialize("fzeng","male", 23)
print(u.name)
