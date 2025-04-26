from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='yadisk-fetch',
    version='0.1.3',  # BUMP the version (very important!)
    py_modules=['yadisk_fetch'],
    entry_points={
        'console_scripts': ['yadisk-fetch=yadisk_fetch:fetch_yadisk'],
    },
    install_requires=['requests'],
    author='YourName',
    description='Download Yandex.Disk folders easily by faking mobile browser headers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
