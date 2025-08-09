import pytest

from pkg.interface_adapters.di.container import Container


class Repo:
    def get_all(self):
        return [1]


def test_container():
    Container.register('test', Repo, lambda: Repo())
    result = Container.resolve('test', Repo)

    assert isinstance(result, Repo)

    with pytest.raises(RuntimeError) as ex:
        Container.resolve('test1', Repo)

    assert str(ex.value) == f"No provider for key=\'test1\' / {Repo}"

    with pytest.raises(RuntimeError) as ex:
        Container.resolve(None, Repo)

    assert str(ex.value) == f"No provider for key=None / {Repo}"
