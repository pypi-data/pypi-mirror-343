import builtins
from typing import Any, Optional

class GlobalRegistrationError(Exception):
    """Exception levée lorsqu'un conflit de nom survient dans builtins."""
    pass

def Global(obj: Any = None, *, specificName: Optional[str] = None) -> Any:
    """
    Déclare un élément dans builtins pour un accès global sans import.

    Args:
        obj (Any): L'élément à rendre global.
        specificName (Optional[str]): Nom alternatif pour l'injection.

    Raises:
        GlobalRegistrationError: Si le nom est déjà occupé.
        ValueError: Si l'objet n'a pas de nom identifiable.

    Returns:
        Any: L'objet injecté inchangé.
    """
    def wrapper(o: Any) -> Any:
        name = specificName if specificName else getattr(o, '__name__', None)
        if not name:
            raise ValueError("Impossible de déterminer le nom de l'objet.")
        if hasattr(builtins, name):
            raise GlobalRegistrationError(f"L'attribut '{name}' existe déjà dans builtins.")
        setattr(builtins, name, o)
        return o

    return wrapper(obj) if obj is not None else wrapper
