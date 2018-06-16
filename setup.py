from setuptools import setup

setup(
    name='yacmt_core',
    version='0.4',
    author='Davide Masserut',
    author_email='d.masserut@gmail.com',
    packages=['yacmt_core'],
    install_requires=['pyserial', 'click', 'filelock'],
    extras_require={'dev': ['line_profiler', 'pylint']},
    scripts=['bin/yacmt_bluetooth'],
    entry_points={
        'console_scripts': [
            'yacmt_core = yacmt_core.yacmt_core:main',
            'yacmt_demo = yacmt_core.yacmt_demo:main'
        ]
    },
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ])
