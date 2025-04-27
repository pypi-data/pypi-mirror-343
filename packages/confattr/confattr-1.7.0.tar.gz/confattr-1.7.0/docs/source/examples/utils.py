#!/usr/bin/env python3

import os
import importlib
import contextlib
import io

def run(fn: str, *, main: bool = True, nextto: 'str|None' = None) -> None:
    if main:
        name = '__main__'
    else:
        name = os.path.splitext(os.path.split(fn)[1])[0]
    if nextto:
        fn = os.path.join(os.path.dirname(nextto), fn)
    spec = importlib.util.spec_from_file_location(name, fn)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

def run_and_get_stdout(fn: str, nextto: 'str|None' = None, no_system_exit: bool = False) -> str:
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        if no_system_exit:
            try:
                run(fn, nextto=nextto)
            except SystemExit:
                pass
        else:
            run(fn, nextto=nextto)
    return stdout.getvalue()

def force_import_quickstart() -> None:
    import confattr.quickstart
    importlib.reload(confattr.quickstart)

def raise_error(msg: object) -> None:
    raise AssertionError(msg)  # pragma: no cover
