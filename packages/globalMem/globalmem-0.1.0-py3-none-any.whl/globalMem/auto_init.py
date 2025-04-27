_registered_modules = []

def register_global_module(module_name: str):
    """
    Enregistre un module pour l'initialisation automatique.
    """
    if module_name not in _registered_modules:
        _registered_modules.append(module_name)

def auto_initialize_globals():
    """
    Importe dynamiquement tous les modules enregistrés.
    """
    for module_name in _registered_modules:
        __import__(module_name)
