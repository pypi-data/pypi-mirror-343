from setuptools import setup, find_packages

setup(
    name='fariz',
    version='0.1.0',
    author='fariz',
    author_email='fariz@contoh.com',
    description=' Ini COntoh upload Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
