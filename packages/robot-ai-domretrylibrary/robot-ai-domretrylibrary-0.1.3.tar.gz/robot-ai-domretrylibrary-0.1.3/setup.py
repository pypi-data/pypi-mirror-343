from setuptools import setup, find_packages

setup(
    name="robot-ai-domretrylibrary",
    version="0.1.3",
    description="A Robot Framework library with AI fallback for locators using OpenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kristijan Plaushku",
    author_email="info@plaushkusolutions.com",
    url="https://github.com/plaushku/robot-ai-domretrylibrary",
    packages=["robot_ai_domretrylibrary"],
    py_modules=["dom_retry_library"],
    package_dir={"robot_ai_domretrylibrary": "."},
    package_data={
        "robot_ai_domretrylibrary": ["*.json"],
    },
    include_package_data=True,
    entry_points={
        "robotframework.libraries": [
            "DomRetryLibrary=dom_retry_library:DomRetryLibrary",
        ],
    },
    install_requires=[
        "robotframework>=6.0",
        "robotframework-seleniumlibrary>=6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",
        "webdriver-manager>=4.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Robot Framework :: Library",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
    ],
    keywords="robotframework testing automation ai openai",
) 