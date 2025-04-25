from setuptools import setup, find_packages

setup(
    name="genai-security",
    version="0.0.0a",
    packages=find_packages(),
    install_requires=[],
    author="Lasso Security",
    author_email="research@lasso.security",
    description="A package for Generative AI security features",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lasso-security/prompt-guardrails",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
