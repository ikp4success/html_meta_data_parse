from setuptools import setup, find_packages

setup(
    name='html_meta_data_parse',
    version='0.0.1',
    python_requires='>=3.8',
    packages=find_packages(exclude=['tests']),
    package_data={},
    install_requires=[
        'beautifulsoup4==4.10.0',
        'requests>=2.26.0'
        'parsel==1.6.0'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==3.3.0',
        'flake8==3.6.0',
        'requests-mock==1.5.2',
        'pyflakes==2.1.1',
        'pytest-flakes==4.0.0'
    ],
    entry_points='''
    ''',
)
