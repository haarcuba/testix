import argparse
import pathlib
import importlib
import logging

def main():
    import testix
    root = pathlib.Path(testix.__file__).parent.parent
    logging.basicConfig(level=logging.INFO)
    for file in root.glob('testix/**/*.py'):
        if file.name == '__init__.py':
            continue
        relative = file.relative_to(root)
        package = str(relative.parent).replace('/', '.')
        module = relative.stem
        full_name = '{package}.{module}'.format(package=package, module=module)
        logging.info('importing {full_name}'.format(full_name=full_name))
        importlib.import_module(full_name)

    logging.info('all imports OK')

if __name__ == '__main__':
    main()
