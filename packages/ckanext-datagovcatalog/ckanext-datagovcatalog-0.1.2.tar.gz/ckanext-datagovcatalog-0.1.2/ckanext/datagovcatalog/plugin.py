import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan import logic
from ckan.lib.base import config
from ckan.lib.navl.validators import not_empty

from ckanext.datagovcatalog.harvester.notifications import \
    harvest_get_notifications_recipients
from ckanext.datagovcatalog.helpers.packages import \
    update_tracking_info_to_package

from ckanext.tracking.plugin import TrackingPlugin
import types

toolkit.requires_ckan_version("2.9")

log = logging.getLogger(__name__)


class DatagovcatalogPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm, inherit=True)

    # IConfigurer
    def update_config(self, config):
        plugins.toolkit.add_public_directory(config, "../public")

        """
        Monkey-patch TrackingPlugin.after_dataset_search to improve API performance.
        Skips tracking summary lookups during /api/3/action/package_search requests,
        which speeds up responses when handling large CKAN datasets.
        """
        def safe_after_dataset_search(self, search_results, search_params):
            request = toolkit.request
            if request.path.startswith('/api'):
                log.info("Skipping tracking plugin for API call")
                return search_results

            # Call the original method if not API
            return safe_after_dataset_search.original(self, search_results, search_params)

        # Backup original method
        safe_after_dataset_search.original = TrackingPlugin.after_dataset_search

        # Apply patch
        TrackingPlugin.after_dataset_search = types.MethodType(
            safe_after_dataset_search, TrackingPlugin
        )

    # ITemplateHelpers
    def get_helpers(self):
        return {}

    def get_actions(self):
        return {
            "harvest_get_notifications_recipients": harvest_get_notifications_recipients
        }

    # IPackageController

    def before_dataset_view(self, pkg_dict):

        # Add tracking information just for datasets
        if pkg_dict.get("type", "dataset") == "dataset":
            if toolkit.asbool(
                config.get("ckanext.datagovcatalog.add_packages_tracking_info", True)
            ):
                # add tracking information.
                # CKAN by default hide tracking info for datasets

                # The pkg_dict received here could include some custom data
                # (like organization_type from GeoDataGov extension)
                # just get this new data and merge witgh previous pkg_dict version
                new_pkg_dict = toolkit.get_action("package_show")(
                    {}, {"include_tracking": True, "id": pkg_dict["id"]}
                )

                pkg_dict = update_tracking_info_to_package(pkg_dict, new_pkg_dict)

        return pkg_dict

    # Need to modify the schema to match import
    #  function that customizes tag validation
    def create_package_schema(self):
        # let's grab the default schema from CKAN
        schema = logic.schema.default_create_package_schema()
        schema["tags"].update({"name": [not_empty, string]})
        return schema

    def update_package_schema(self):
        # let's grab the default schema from CKAN
        schema = logic.schema.default_update_package_schema()
        schema["tags"].update({"name": [not_empty, string]})
        log.info("Trying to update package schema %s" % schema["tags"])
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # customizes tag validation (see above)
        return []


def string(value):
    return str(value)
