from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as f:
    required = f.readlines()
    required = [r.strip() for r in required]

setup(
    name='MicroA',
    version='1.4.0',
    summary=f'Django Microservice MicroA',
    author='Ali Mammadov',
    author_email='ali.mammadov@gmail.com',
    license='MA',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)