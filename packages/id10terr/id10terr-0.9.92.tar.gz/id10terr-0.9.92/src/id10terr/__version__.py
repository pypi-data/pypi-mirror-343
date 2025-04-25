"""Module information."""

import os

# The title and description of the package
__title__ = "id10terr"
__description__ = """
    ID10T python library
"""

# The version and build number
# Without specifying a unique number, you cannot overwrite packages in the PyPi repo
__version__ = os.getenv("RELEASE_NAME", "1.0.0")

# Author and license information
__author__ = "Scheibling Consulting"
__author_email__ = "itsec@scheibling.se"
__license__ = "GPL-3.0-or-later"

# URL to the project
__url__ = f"https://github.com/scheiblingco/{__title__}"