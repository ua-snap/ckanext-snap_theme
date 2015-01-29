import ast
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

class SnapThemePlugin(plugins.SingletonPlugin):
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    # We use this to customize the dictionary that ships to the snippets.
    plugins.implements(plugins.IPackageController, inherit=True)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

        toolkit.add_resource('fanstatic', 'snap_theme')

    def before_view(context, pkg_dict):
        '''
        Adds any additional data fields to the package dictionary for custom display
        '''
        # Turn the stored string of credits back into a list 
        pkg_dict['credits'] = ast.literal_eval(helpers.get_pkg_dict_extra(pkg_dict, 'credits', ''))
        return pkg_dict
