import os
from setuptools import setup, find_packages

setup(
    name="fs-comfyui-frontend-package",
    version=os.getenv("COMFYUI_FRONTEND_VERSION") or "1.18.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.9",
    author="FlowScale",  # Update with actual author name
    author_email="your.email@example.com",  # Update with actual email
    description="ComfyUI Frontend Package for web interface",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FlowScaleAI/comfyui_frontend",  # Update with actual repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
