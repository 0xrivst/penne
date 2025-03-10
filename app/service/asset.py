"""
Asset Manager

This module contains a class for managing webpack assets.
"""

import os
import json
from flask import current_app


class AssetManager:
    """
    Class for managing webpack assets.
    """

    def __init__(self):
        self._assets = {}
        self._manifest_path = None

    def init_asset_manager(self):
        """
        Initialize the asset manager.
        """
        self._manifest_path = os.path.join(
            current_app.static_folder, "dist", "manifest.json"
        )
        self._get_webpack_assets(current_app)

        if current_app.config.get("DEBUG"):
            current_app.before_request(self.reload_webpack_assets)

        current_app.context_processor(lambda: {"asset": self})

    def url_for(self, file):
        """
        Get the URL for a webpack asset.
        """
        print(file, self._assets, self._assets.get(file))
        return self._assets.get(file)

    def reload_webpack_assets(self):
        """
        Reloads webpack assets.
        """
        self._get_webpack_assets(current_app)

    def _get_webpack_assets(self, app):
        with app.open_resource(self._manifest_path) as manifest:
            self._assets = json.load(manifest)
