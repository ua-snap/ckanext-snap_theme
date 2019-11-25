import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers
import logging
log = logging.getLogger(__name__)

def get_showcases():
    '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    sc = toolkit.get_action('ckanext_showcase_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    # Truncate the list to the first 6.
    sc = sc[:6]

    return sc


class SnapThemePlugin(plugins.SingletonPlugin):
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    # We use this to customize the dictionary that ships to the snippets.
    plugins.implements(plugins.IPackageController, inherit=True)

    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        toolkit.add_resource('fanstatic', 'snap')


    def get_helpers(self):
        ''' Register template helper functions '''
        return {'snap_theme_get_showcases': get_showcases}
