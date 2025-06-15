from setuptools import setup, find_packages

setup(
    name="instagram-follower-audit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "plotly>=5.18.0",
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "typing-extensions>=4.9.0",
        "python-dateutil>=2.8.2",
        "pytz>=2024.1",
        "openai>=1.12.0",
        "aiohttp>=3.9.0",
        "streamlit-option-menu>=0.3.12",
        "pillow>=10.2.0",
        "streamlit-extras>=0.3.5"
    ],
) 