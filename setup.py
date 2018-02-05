from setuptools import setup

setup(
    name='yacm',
    version='0.1',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacm'],
    install_requires=['pyserial', 'click'],
    extras_require={'dev': ['line_profiler', 'pylint']},
    scripts=['bin/yacm_bluetooth'],
    entry_points={
        'console_scripts': ['yacm = yacm.yacm_cli:main']
    })
