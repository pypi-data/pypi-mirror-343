"""Alexandria: Library for Knowledge for AI Agents."""


from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import tomllib


try:
    __version__: str = version(distribution_name='Alexandria-AI')

except PackageNotFoundError:
    with open(file=Path(__file__).parent.parent / 'pyproject.toml', mode='rb') as f:
        __version__: str = tomllib.load(f)['tool']['poetry']['version']
