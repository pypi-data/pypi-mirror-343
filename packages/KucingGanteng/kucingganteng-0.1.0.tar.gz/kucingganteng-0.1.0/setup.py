from setuptools import setup, find_packages

setup(
    name='KucingGanteng',
    version='0.1.0',
    author='Adhityasar',
    author_email='adhityasar@gmail.com',
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
