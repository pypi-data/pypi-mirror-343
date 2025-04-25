
from typing import Tuple, Type

# If these can be accessed, numpy will try to load the array from local memory,
# resulting in exceptions and/or segfaults, see #236:
MASKED_ATTRS = frozenset([
    '__array_struct__', '__array_interface__',
])

"""the set of attributes that are local to the netref object"""
LOCAL_ATTRS = frozenset([
    '____conn__', '____id_pack__', '____refcount__', '__class__', '__cmp__', '__del__', '__delattr__',
    '__dir__', '__doc__', '__getattr__', '__getattribute__', '__hash__', '__instancecheck__',
    '__init__', '__metaclass__', '__module__', '__new__', '__reduce__',
    '__reduce_ex__', '__repr__', '__setattr__', '__slots__', '__str__',
    '__weakref__', '__dict__', '__methods__', '__exit__',
    '__eq__', '__ne__', '__lt__', '__gt__', '__le__', '__ge__',
]) | MASKED_ATTRS


class ObjectId:

    __slots__ = ("type_module", "type_name", "type_id", "instance_id")

    def __init__(self, type_module: str, type_name: str, type_id: str, instance_id: str):
        self.type_module = type_module
        self.type_name = type_name
        self.type_id = type_id
        self.instance_id = instance_id
        return

    def __reduce__(self) -> Tuple[str, str, str, str]:
        rval = (self.type_module, self.type_name, self.type_id ,self.instance_id)
        return rval


class ObjectRefType(Type):
    """A *metaclass* used to customize the ``__repr__`` of ``netref`` classes.
    It is quite useless, but it makes debugging and interactive programming
    easier"""

    __slots__ = ()

    def __repr__(self):
        if self.__module__:
            return f"<ObjectRef class '{self.__module__}.{self.__name__}'>"
        else:
            return f"<ObjectRef class '{self.__name__}'>"

class ObejctRef(metaclass=ObjectRefType):
    """The base netref class, from which all netref classes derive. Some netref
    classes are "pre-generated" and cached upon importing this module (those
    defined in the :data:`_builtin_types`), and they are shared between all
    connections.

    The rest of the netref classes are created by :meth:`rpyc.core.protocol.Connection._unbox`,
    and are private to the connection.

    Do not use this class directly; use :func:`class_factory` instead.

    :param conn: the :class:`rpyc.core.protocol.Connection` instance
    :param id_pack: id tuple for an object ~ (name_pack, remote-class-id, remote-instance-id)
        (cont.) name_pack := __module__.__name__ (hits or misses on builtin cache and sys.module)
                remote-class-id := id of object class (hits or misses on netref classes cache and instance checks)
                remote-instance-id := id object instance (hits or misses on proxy cache)
        id_pack is usually created by rpyc.lib.get_id_pack
    """
    __slots__ = ["____conn__", "____id_pack__", "__weakref__", "____refcount__"]

    def __init__(self, conn, id_pack):
        self.____conn__ = conn
        self.____id_pack__ = id_pack
        self.____refcount__ = 1

    def __del__(self):
        try:
            asyncreq(self, consts.HANDLE_DEL, self.____refcount__)
        except Exception:
            # raised in a destructor, most likely on program termination,
            # when the connection might have already been closed.
            # it's safe to ignore all exceptions here
            pass

    def __getattribute__(self, name):
        if name in LOCAL_ATTRS:
            if name == "__class__":
                cls = object.__getattribute__(self, "__class__")
                if cls is None:
                    cls = self.__getattr__("__class__")
                return cls
            elif name == "__doc__":
                return self.__getattr__("__doc__")
            elif name in DELETED_ATTRS:
                raise AttributeError()
            else:
                return object.__getattribute__(self, name)
        elif name == "__call__":                          # IronPython issue #10
            return object.__getattribute__(self, "__call__")
        elif name == "__array__":
            return object.__getattribute__(self, "__array__")
        else:
            return syncreq(self, consts.HANDLE_GETATTR, name)

    def __getattr__(self, name):
        if name in DELETED_ATTRS:
            raise AttributeError()
        return syncreq(self, consts.HANDLE_GETATTR, name)

    def __delattr__(self, name):
        if name in LOCAL_ATTRS:
            object.__delattr__(self, name)
        else:
            syncreq(self, consts.HANDLE_DELATTR, name)

    def __setattr__(self, name, value):
        if name in LOCAL_ATTRS:
            object.__setattr__(self, name, value)
        else:
            syncreq(self, consts.HANDLE_SETATTR, name, value)

    def __dir__(self):
        return list(syncreq(self, consts.HANDLE_DIR))

    # support for metaclasses
    def __hash__(self):
        return syncreq(self, consts.HANDLE_HASH)

    def __cmp__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__cmp__')

    def __eq__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__eq__')

    def __ne__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__ne__')

    def __lt__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__lt__')

    def __gt__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__gt__')

    def __le__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__le__')

    def __ge__(self, other):
        return syncreq(self, consts.HANDLE_CMP, other, '__ge__')

    def __repr__(self):
        return syncreq(self, consts.HANDLE_REPR)

    def __str__(self):
        return syncreq(self, consts.HANDLE_STR)

    def __exit__(self, exc, typ, tb):
        return syncreq(self, consts.HANDLE_CTXEXIT, exc)  # can't pass type nor traceback

    def __reduce_ex__(self, proto):
        # support for pickling netrefs
        return pickle.loads, (syncreq(self, consts.HANDLE_PICKLE, proto),)

    def __instancecheck__(self, other):
        # support for checking cached instances across connections
        if isinstance(other, BaseNetref):
            if self.____id_pack__[2] != 0:
                raise TypeError("isinstance() arg 2 must be a class, type, or tuple of classes and types")
            elif self.____id_pack__[1] == other.____id_pack__[1]:
                if other.____id_pack__[2] == 0:
                    return False
                elif other.____id_pack__[2] != 0:
                    return True
            else:
                # seems dubious if each netref proxies to a different address spaces
                return syncreq(self, consts.HANDLE_INSTANCECHECK, other.____id_pack__)
        else:
            if self.____id_pack__[2] == 0:
                # outside the context of `__instancecheck__`, `__class__` is expected to be type(self)
                # within the context of `__instancecheck__`, `other` should be compared to the proxied class
                return isinstance(other, type(self).__dict__['__class__'].instance)
            else:
                raise TypeError("isinstance() arg 2 must be a class, type, or tuple of classes and types")