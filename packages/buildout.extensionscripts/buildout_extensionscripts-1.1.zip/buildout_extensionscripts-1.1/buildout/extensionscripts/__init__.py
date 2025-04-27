def extension(buildout=None):
    import os

    try:
        from imp import load_source
    except ImportError:
        import importlib

        def load_source(modname, filename):
            loader = importlib.machinery.SourceFileLoader(modname, filename)
            spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
            module = importlib.util.module_from_spec(spec)
            # The module is always executed and not cached in sys.modules.
            # Uncomment the following line to cache the module.
            # sys.modules[module.__name__] = module
            loader.exec_module(module)
            return module

    scripts = buildout.get(
        'buildout', {}).get(
            'extension-scripts', '').split('\n')
    for script in scripts:
        if not script.strip():
            continue
        filename, function = script.split(':')
        filename = os.path.abspath(filename.strip())
        module = load_source('script', filename)
        getattr(module, function.strip())(buildout)
