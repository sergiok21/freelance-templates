from pkg.interface_adapters.di.container import Container
from pkg.interface_adapters.di.provider import inject


class Empty:
    ...


def test_provider():
    @inject
    def func(a, test: Empty = 'empty'):
        return a, test

    @inject
    def func_with_container(a, test: Empty = 'test'):
        return a, test

    Container.register('test', Empty, lambda: Empty())

    result_a, cls = func(1)

    assert result_a == 1
    assert cls == 'empty'

    result_a, cls = func_with_container(1)

    assert result_a == 1
    assert cls != 'test'
    assert isinstance(cls, Empty)
