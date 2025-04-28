import setuptools
import distutils.core

setuptools.setup(
    name='mime-extension',
    version="1.1.0",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='Return the file extension for a mimetype on Linux',
    license='MIT',
    keywords='mime,extension,cli',
    url='https://github.com/talwrii/mime-extension',
    packages=["mime_extension"],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['mime-extension=mime_extension.main:main']
    },
    install_requires=["lxml"],
    classifiers=[
    ],
    test_suite='nose.collector'
)
