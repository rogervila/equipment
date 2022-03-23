#!/usr/bin/env python

from equipment.framework import equipment
import matplotlib.pyplot as plt
import numpy as np

app = equipment()

app.log().info(
    f'''

    Welcome to {app.config().get('APP', 'name')}

    Do you to work with matplotlib?

    Go to the root folder and run:

    $ pip install matplotlib
    $ pip install numpy
    $ rm main.py && mv examples/example_matplotlib.py main.py
    $ py main.py
    '''
)

# Create CSV with data
app.storage().write(
    'data.csv',
    '''1, 5
2, 3
3, 4
4, 7
5, 4
6, 3
7, 5
8, 7
9, 4
10, 4'''
)

x, y = np.loadtxt(app.storage().path('data.csv'), delimiter=',', unpack=True)

plt.plot(x, y, label='Example')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Matplotlib example')
plt.legend()
plt.show()
