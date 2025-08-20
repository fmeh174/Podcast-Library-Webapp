from pathlib import Path

"""
For clearly and cleanly getting the project directory,
without each file having to import Path itself.
"""


def get_project_root() -> Path:
    return Path(__file__).parent.parent
