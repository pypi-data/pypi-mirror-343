from setuptools import setup, find_packages

setup(
    name='latihan-api-cihuy',
    version='0.1.0',
    author='Muhammad Agam Nasywaan',
    author_email='agamnasy28@gmail.com',
    description=' Ini Contoh upload Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
