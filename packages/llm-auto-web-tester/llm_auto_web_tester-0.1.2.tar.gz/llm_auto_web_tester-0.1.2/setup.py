from setuptools import setup, find_packages
from llm_auto_web_tester import __version__

setup(
    name="llm-auto-web-tester",
    version=__version__,
    author="Lucas Custodio",
    author_email="lucas.custodio@stefanini.com",
    description="Automated UI testing tool using Playwright MCP and OpenAI GPT agents.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/stefanini-applications/llm-auto-web-tester",
    packages=find_packages(),
    install_requires=[
        "openai-agents",
        "python-dotenv",
        "openai",
        "playwright",
        "rich",
        "requests",
        "asyncio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "llm-web-test=llm_auto_web_tester.llm_auto_web_tester:run_test_suite",
        ],
    },
)
