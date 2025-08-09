from typing import List, Callable, Type, Any, Tuple

from pkg.frameworks_drivers.di import DIRegister


def auto_di_register(
    depends: List[Tuple[str, Type[Any], Callable[[], Any]]],
    register_func: Callable[[dict], None],
) -> None:
    processed = {}
    for d in depends:
        processed.update(DIRegister.depends_factory(*d))
    register_func(processed)
