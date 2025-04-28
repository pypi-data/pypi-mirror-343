from setuptools import setup, find_packages

setup(
    name='securepasslib',
    version='1.0.3',
    packages=find_packages(),
    description='Secure password validation, strength analysis, generation, and breach checking library',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Tuan Nguyen',
    author_email='nguyenhuutuan1306@gmail.com',
    url='https://github.com/mituso89/securepass',  # replace with your GitHub repo
    project_urls={
        'Documentation': 'https://github.com/mituso89/securepass/blob/main/docs/usage.md',
        'Source': 'https://github.com/mituso89/securepass',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'securepass=securepasslib.cli:cli',
        ],
    },
)
