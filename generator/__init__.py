"""
pyFlies code generators transforms pyFlies experiment models to
different run-time platforms.

pygame_sl code generator transforms pygame_sl game models into


This module implements a part of code generation logic that should be the same
for all platforms (creating target folder structure, copying image and
sound files etc.).

Part of code generation that is specific for each platform is done in the
submodules named after target platform.
"""

import os