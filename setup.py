from setuptools import setup # type: ignore
from pathlib import Path

readme = Path('.') / 'README.md'

setup(
    long_description=readme.read_text(),
    long_description_content_type='text/markdown'
)
