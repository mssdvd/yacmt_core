from setuptools import setup

setup(
    name='yacm',
    version='0.1',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacm'],
    install_requires=['pyserial'],
    extras_require={'dev': ['line_profiler', 'pylint']},
    scripts=['bin/yacm_bluetooth'])
