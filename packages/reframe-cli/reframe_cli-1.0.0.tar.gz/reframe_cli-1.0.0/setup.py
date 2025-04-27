from setuptools import setup, find_packages
import os

setup(
    name="reframe-cli",
    version="1.0.0",
    description="ReFrame-CLI A great tool to boost your productivity in video and image manipulation tasks. Ideal for preparing image datasets for training machine learning models, including generative AI and diffusion models.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Gour4v",
    author_email="chatgai.note@gmail.com",
    url="https://github.com/ForgeL4bs/ReFrame",
    license="MIT",
    packages=find_packages(include=["ReFrame", "ReFrame.*"]),
    install_requires=[
        "opencv-python",
        "pillow",
        "imageio",
        "pillow-heif",
    ],
    entry_points={
        "console_scripts": [
            "reframe=ReFrame.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
