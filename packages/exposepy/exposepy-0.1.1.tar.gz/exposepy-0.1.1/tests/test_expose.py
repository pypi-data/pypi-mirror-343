from exposepy import expose

@expose
def foo():
    return 42

@expose(name="bar_alias")
def bar():
    return 99

def test_expose_basic():
    import sys
    mod = sys.modules[foo.__module__]
    assert "foo" in mod.__all__
    assert "bar_alias" in mod.__all__
    assert "bar_alias" in dir(mod)
    assert foo() == 42
    assert bar() == 99

