# setup.py (updated to v0.1.2)
import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import py_compile

# read long description from README.md for PyPI
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

class CompileBeforeBuild(build_py):
    """Custom build command to compile Python files before building"""
    def run(self):
        # Compile all Python files first
        for root, _, files in os.walk('repmt'):
            for file in files:
                if file.endswith('.py'):
                    full_path = os.path.join(root, file)
                    try:
                        py_compile.compile(full_path, doraise=True)
                        print(f"Compiled {full_path}")
                    except Exception as e:
                        print(f"Error compiling {full_path}: {e}")
        # Run original build command
        super().run()

setup(
    name='repmt',
    version='0.1.2',  # bumped version
    description='A Streamlit-based CLI tool for testing API endpoints',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    package_data={
        'repmt': ['*.py', '*.pyc'],
    },
    include_package_data=True,
    cmdclass={
        'build_py': CompileBeforeBuild,
    },
    entry_points={
        'console_scripts': [
            'repmt=repmt.cli:main',
        ],
    },
    install_requires=[
        'streamlit>=1.30.0',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
