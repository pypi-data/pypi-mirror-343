from setuptools import setup, find_packages

setup(
    name="llm-security",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Lasso Security",
    author_email="research@lasso.security",
    description="A package for LLM security features",
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
