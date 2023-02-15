from setuptools import setup

from civic_core import __version__

setup(
    name='civic-core',
    version=__version__,
    author='Muhamed Hassan',
    description='CIVICCore is used by all other microservices.',
    packages=['civic_core'],
    package_data={'civic_core': ['py.typed']},
    install_requires=[
        'fastapi==0.88.0',
        'psycopg2==2.9.5',
        'pydantic==1.10.2',
        'python-dotenv==0.21.0',
        'python-jose==3.3.0',
        'SQLAlchemy==1.4.45',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
