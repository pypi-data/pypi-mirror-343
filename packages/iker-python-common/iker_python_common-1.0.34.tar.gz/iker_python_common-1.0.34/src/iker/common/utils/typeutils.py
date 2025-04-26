import types
import typing


def print_type(t: type):
    def print_typing_indent(t: type, indent: int = 0):
        origin = type_origin(t)
        if origin:
            print(" " * indent, t, origin)
        else:
            print(" " * indent, t)
        for arg in type_args(t):
            print_typing_indent(arg, indent + 2)

    print_typing_indent(t)


def type_origin(t: type) -> type | None:
    return t.__origin__ if hasattr(t, "__origin__") else None


def type_args(t: type) -> list[type]:
    return t.__args__ if hasattr(t, "__args__") else []


def is_union_type(t: type) -> bool:
    return type(t) is types.UnionType or type_origin(t) in {typing.Union}


def is_optional_type(t: type) -> bool:
    if not is_union_type(t):
        return False
    return types.NoneType in type_args(t)


def is_identical_union_type(a: type, b: type) -> bool:
    a_args = type_args(a)
    b_args = type_args(b)

    if len(a_args) != len(b_args):
        return False
    for arg_a, arg_b in zip(sorted(a_args, key=str), sorted(b_args, key=str)):
        if not is_identical_type(arg_a, arg_b):
            return False
    return True


def is_identical_type(a: type, b: type) -> bool:
    if is_union_type(a) and is_union_type(b):
        return is_identical_union_type(a, b)
    elif is_union_type(a) ^ is_union_type(b):
        return False

    a_origin = type_origin(a)
    b_origin = type_origin(b)

    if a_origin is not None and b_origin is not None:
        if a_origin != b_origin:
            return False
    elif a != b:
        return False

    a_args = type_args(a)
    b_args = type_args(b)

    if len(a_args) != len(b_args):
        return False
    for arg_a, arg_b in zip(a_args, b_args):
        if not is_identical_type(arg_a, arg_b):
            return False
    return True
