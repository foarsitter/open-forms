from functools import partial
from typing import Callable


def get_default(value) -> str:
    return str(value)


def runtime_gettext(literal) -> Callable[[], str]:
    """
    Generate a callable for migration defaults resolving to a translated literal.

    When using literal :func:`gettext` or :func:`gettext_lazy` default values in
    migrations, the defaults are evaluated and frozen in the migration files.

    By using a callable, we can defer this, see
    https://docs.djangoproject.com/en/2.2/topics/migrations/#serializing-values
    """
    func = partial(get_default, literal)
    return func
