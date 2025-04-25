from setuptools import setup, find_packages

setup(
    name='danuyaa',
    version='0.1.0',
    author='Nama Kamu',
    author_email='email@contoh.com',
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
