from exposepy import expose, reexpose

# Simulate an external module defining this
@expose
def external_fn():
    return "hello"

# Now reexpose in this module
reexpose(external_fn)

def test_reexpose():
    import sys
    mod = sys.modules[__name__]
    assert "external_fn" in mod.__all__
    assert "external_fn" in dir(mod)
    assert external_fn() == "hello"

def test_cross_module_reexpose():
    from dummy_package import api

    assert hasattr(api, "public_func")
    assert api.public_func() == "core value"
    assert "public_func" in dir(api)
    assert "public_func" in api.__all__

