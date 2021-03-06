import ast
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers
from datetime import datetime

class SnapThemePlugin(plugins.SingletonPlugin):
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    # We use this to customize the dictionary that ships to the snippets.
    plugins.implements(plugins.IPackageController, inherit=True)

    # Implementing the IFacets interface lets us hide the organization and groups facets.
    plugins.implements(plugins.IFacets)

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

    def before_view(context, pkg_dict):
        '''
        Adds any additional data fields to the package dictionary for custom display
        '''

        # Attach URL "download bucket" endpoint to package
        pkg_dict['preview_url'] = helpers.get_pkg_dict_extra(pkg_dict, 'download-url', '')

        # Turn the stored string of credits back into a list 
        credits = helpers.get_pkg_dict_extra(pkg_dict, 'credits', '');
        if credits:
            pkg_dict['credits'] = ast.literal_eval(credits)

        # If temporal extent, format the dates.
        temporal_start = helpers.get_pkg_dict_extra(pkg_dict, 'temporal-extent-begin')
        temporal_end = helpers.get_pkg_dict_extra(pkg_dict, 'temporal-extent-end')
        if temporal_start and temporal_end:
            # Unfortunately, the datetime library won't handle years before 1900, so a bit
            # of manual parsing is needed here.
            start_year = temporal_start[:4]
            start_month = temporal_start[5:7]
            end_year = temporal_end[:4]
            end_month = temporal_end[5:7]
            try:
                pkg_dict['temporal_start'] = "{0} {1}".format(datetime.strptime(start_month, '%m').strftime('%B'), start_year)
                pkg_dict['temporal_end'] = "{0} {1}".format(datetime.strptime(end_month, '%m').strftime('%B'), end_year)
            except ValueError:
                # Swallow and ignore if the date parsing failed.
                pass
        
        spatial_resolution = helpers.get_pkg_dict_extra(pkg_dict, 'spatial-resolution')
        spatial_resolution_units = helpers.get_pkg_dict_extra(pkg_dict, 'spatial-resolution-units')
        if spatial_resolution and spatial_resolution_units:
            pkg_dict['spatial_resolution'] = "{0} {1}".format(spatial_resolution, spatial_resolution_units)

        return pkg_dict

    def _facets(self, facets_dict):
        '''
        Hide the Organization and Group facets.
        '''
        if 'groups' in facets_dict:
            del facets_dict['groups']
        if 'organization' in facets_dict:
            del facets_dict['organization']
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return self._facets(facets_dict)
    def group_facets(self, facets_dict, group_type, package_type):
        return self._facets(facets_dict)
    def organization_facets(self, facets_dict, organization_type, package_type):
        return self._facets(facets_dict)
