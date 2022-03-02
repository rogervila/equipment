import sys
from setuptools import setup

install_requires = []

with open('equipment/console/requirements.txt', 'r', encoding='utf-8') as f:
    install_requires.extend(f.read().splitlines())

with open('equipment/framework/requirements.txt', 'r', encoding='utf-8') as f:
    install_requires.extend(f.read().splitlines())

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='equipment',
    packages=['equipment'],
    version='CURRENT_VERSION',
    license='MIT',
    description='The root of your next python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Roger Vilà',
    author_email='rogervila@me.com',
    url='https://github.com/rogervila/equipment',
    download_url='https://github.com/rogervila/equipment/archive/CURRENT_VERSION.tar.gz',
    keywords=['equipment', 'application scaffolding', 'framework'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        # Install a script as "equipment", and as "equipment3", and as "equipment3.x"
        'console_scripts': [
            #pylint: disable=consider-using-f-string
            'equipment = equipment.console:main',
            'equipment%d = equipment.console:main' % sys.version_info[:1],
            'equipment%d.%d = equipment.console:main' % sys.version_info[:2],
            #pylint: enable=consider-using-f-string
        ],
    },
)
