#!/usr/bin/env python

from equipment.framework import equipment

app = equipment()

app.log().info(
    f'''

    Welcome to {app.config().get('APP', 'name')}

    This example shows how to read and write
    files with the storage module.
    '''
)

file = 'test.txt'

app.storage().write(file, 'test')

if not app.storage().exists(file):
    raise RuntimeError(f'{file} has not been created!')

if app.storage().read(file) != 'test':
    raise RuntimeError(f'{file} has not been read!')

if not app.storage().remove(file):
    raise RuntimeError(f'{file} has not been deleted!')
