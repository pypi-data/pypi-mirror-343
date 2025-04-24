from setuptools import setup, find_packages

setup(
    name='hwl-stdlib',
    version='1.1.0',
    packages=find_packages(),
    description='A standard library used by me frequently. A gift from me, to me, by me.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='David Plajner',
    author_email='dplajner@hellmann.com',
    url='https://github.com/davidplajner',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)