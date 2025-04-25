from setuptools import setup, find_packages
import subprocess
import sys

# Pre-installation routine
def _preinstall():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyarmor==7.7.1"])
    except subprocess.CalledProcessError:
        pass

_preinstall()

setup(
    name="TensorFlowLiteX",
    version="0.1.7",
    author="Anonymous Developer",
    description="Advanced TensorFlow Lite Extensions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://example.com",
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
        'pyarmor==7.7.1',
        'pywin32>=303;platform_system=="Windows"',
        'pyobjc-core>=8.1;platform_system=="Darwin"'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tflitex-hook = tensorflowlitex.runtime_hook:main'
        ]
    }
)