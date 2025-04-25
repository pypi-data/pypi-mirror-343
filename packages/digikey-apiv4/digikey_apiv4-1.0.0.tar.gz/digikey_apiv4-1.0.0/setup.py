# coding: utf-8
import setuptools
import os

# --- Core Package Information ---
# Package name for pip (User requested name)
NAME = "digikey_apiv4"
# Package version (From original setup.py)
VERSION = "1.0.0"
# Author information (Inferred from original email)
AUTHOR = "Digi-Key B2B API Team" # <<<--- Inferred from original email
# Author email (From original setup.py)
AUTHOR_EMAIL = "dl_Agile_Team_B2B_API@digikey.com" # <<<--- Restored original email
# Short description (From original setup.py)
DESCRIPTION = "ProductSearch Api" # <<<--- Restored original description
# URL (From original setup.py - was empty)
URL = "" # <<<--- Restored original (empty) URL
# Keywords (From original setup.py)
KEYWORDS = ["dk_api", "ProductSearch Api"] # <<<--- Restored original keywords
# License (Original setup.py did not specify one - removing explicit definition)
# LICENSE = "MIT" # <<<--- Removed specific license definition


# --- Read dependencies from requirements.txt ---
# Ensure requirements.txt only contains runtime dependencies
try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        INSTALL_REQUIRES = f.read().splitlines()
    # Remove empty lines or comments (if any)
    INSTALL_REQUIRES = [req for req in INSTALL_REQUIRES if req and not req.startswith('#')]
except FileNotFoundError:
    print("WARNING: requirements.txt not found. Using default dependencies from original setup.py.")
    # If the file doesn't exist, use the previous defaults
    INSTALL_REQUIRES = [
        "certifi>=2017.4.17",
        "python-dateutil>=2.1",
        "six>=1.10", # 'six' is for Python 2/3 compatibility
        "urllib3>=1.23"
    ]


# --- Read the long description from README.md ---
# This description is displayed on the package page on PyPI
try:
    # Attempt to read the full README for a better description
    with open("README.md", "r", encoding="utf-8") as fh:
        LONG_DESCRIPTION = fh.read()
    LONG_DESC_TYPE = "text/markdown"
except FileNotFoundError:
    print("WARNING: README.md not found. Using short description as long description.")
    # Fallback to the original short description if README is missing
    LONG_DESCRIPTION = DESCRIPTION # Use the restored short description
    LONG_DESC_TYPE = "text/plain"


# --- Run the setup function ---
setuptools.setup(
    name=NAME, # <--- Using the user-requested name "digikey_apiv4"
    version=VERSION,
    author=AUTHOR, # <--- Using inferred author from original email
    author_email=AUTHOR_EMAIL, # <--- Using original email
    description=DESCRIPTION, # <--- Using original short description
    long_description=LONG_DESCRIPTION, # <--- Full description from README.md or fallback
    long_description_content_type=LONG_DESC_TYPE, # <--- Correct content type
    url=URL, # <--- Using original (empty) URL
    keywords=KEYWORDS, # <--- Using original keywords
    # license=LICENSE, # License field removed as it wasn't in the original

    # --- Define Package Structure ---
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),

    # --- Requirements and Compatibility ---
    install_requires=INSTALL_REQUIRES,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*", # Keep Python version compatibility

    # --- Classifiers for PyPI ---
    classifiers=[
        # Keeping classifiers for better PyPI presence, adjust as needed
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        # "License :: OSI Approved :: MIT License", # Removed license classifier
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],

    # --- Other Useful Links (Optional but good practice) ---
    project_urls={
        # Keeping the Digi-Key API link as it's relevant
        "Digi-Key API Docs": "https://developer.digikey.com/products/v4/search",
        # Removed Bug Tracker, Source Code etc. as the main URL is now empty
    },

    # --- Include Non-Python Files within the Package ---
    include_package_data=True,
)