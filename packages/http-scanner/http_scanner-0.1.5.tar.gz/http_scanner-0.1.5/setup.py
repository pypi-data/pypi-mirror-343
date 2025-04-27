from setuptools import setup, find_packages

setup(
    name='http-scanner',
    version='0.1.5',
    author='dotcomrow',
    author_email='your-email@example.com',
    description='A modular, plugin-based HTTP scanning framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dotcomrow/http-scanner',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'PyYAML',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'http-scanner=core.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
