from setuptools import setup, find_packages

setup(
    name='pyapptest',
    version='0.1.0',
    description='A Streamlit-based API testing tool',
    author='RePromptsQuest',
    author_email='repromptsquest@gmail.com',
    url='https://github.com/reprompts/pyapptest',
    packages=find_packages(),  # finds backend and cli
    py_modules=['ui'],         # include the top-level ui.py
    install_requires=[
        'streamlit>=1.0',
        'click>=8.0',
        'fastapi>=0.65',
        'flask>=2.0',
        'django>=3.2',
        'faker',
    ],
    entry_points={
        'console_scripts': [
            'pyapptest=cli.main:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
