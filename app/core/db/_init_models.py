from importlib import import_module


__all__ = ["init_models"]


def init_models():
    from core.settings import settings
    for entity in settings.entities:
        import_module(f'{entity}.models')
