from contextlib import contextmanager


def safe_update(init_func, old_kwargs, new_kwargs):
    name = init_func.__name__
    old_repr = ', '.join(f'{k} = {v}' for k, v in old_kwargs.items())

    try:
        old = init_func(**old_kwargs)

    except FileNotFoundError:
        print(f"{name}({old_repr}) does not exist: Create new one")
        new = init_func(**new_kwargs)
        new.dump()

    except Exception as e:
        raise e

    else:
        new = init_func(**new_kwargs)
        if old == new:
            print(f"{name}({old_repr}) exist and valid")
        else:
            print(f"{name}({old_repr}) exist, but outdated. Rewrite new one")
            new.dump()


@contextmanager
def swap_item(x, i, new):
    """x[i] should not be mutable"""
    old = x[i]
    try:
        x[i] = new
        yield
    finally:
        x[i] = old
