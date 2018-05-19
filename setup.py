from setuptools import setup

setup(
    name='yacmt',
    version='0.1',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacmt'],
    install_requires=['pyserial', 'click', 'filelock'],
    extras_require={'dev': ['line_profiler', 'pylint']},
    scripts=['bin/yacmt_bluetooth'],
    entry_points={'console_scripts': ['yacmt = yacmt.yacmt_cli:main']})
