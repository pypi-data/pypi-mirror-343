from django.utils.deprecation import MiddlewareMixin
from urllib.parse import parse_qs, urlencode
from django.http import HttpResponseRedirect
import re

class WagtailFilterPersistenceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only handle admin requests
        if not request.path.startswith('/admin/'):
            return None
            
        # Get current URL details
        path = request.path
        query_string = request.META.get('QUERY_STRING', '')
        
        # Pattern to match listing pages
        modeladmin_pattern = r'^/admin/(\w+)/$'
        modeladmin_results_pattern = r'^/admin/(\w+)/results/$'
        
        # Pattern to match edit/create pages
        edit_pattern = r'^/admin/(\w+)/edit/'
        create_pattern = r'^/admin/(\w+)/create/'
        
        # CASE 1: Store filters from listing pages with query parameters
        modeladmin_match = re.match(modeladmin_pattern, path) or re.match(modeladmin_results_pattern, path)
        if modeladmin_match and query_string:
            app_name = modeladmin_match.group(1)
            filter_key = f"wagtail_filters_{app_name}"
            request.session[filter_key] = parse_qs(query_string)
        
        # CASE 2: Apply filters on redirect to listing page without query parameters
        modeladmin_match = re.match(modeladmin_pattern, path) or re.match(modeladmin_results_pattern, path)
        if modeladmin_match and not query_string:
            app_name = modeladmin_match.group(1)
            filter_key = f"wagtail_filters_{app_name}"
            
            # Check if we have stored filters for this app
            if filter_key in request.session:
                stored_filters = request.session[filter_key]
                if stored_filters:
                    # Determine target redirect URL (prefer /results/ if that's what was stored)
                    if 'results' in filter_key or '/results/' in request.META.get('HTTP_REFERER', ''):
                        redirect_path = f"/admin/{app_name}/results/"
                    else:
                        redirect_path = path
                        
                    query_string = urlencode(stored_filters, doseq=True)
                    redirect_url = f"{redirect_path}?{query_string}"
                    return HttpResponseRedirect(redirect_url)
        
        # CASE 3: Special handling for POST redirect after edit/create
        if request.method == 'POST':
            referer = request.META.get('HTTP_REFERER', '')
            
            # Check if we're coming from an edit page
            edit_match = re.search(edit_pattern, referer) or re.search(create_pattern, referer)
            if edit_match:
                request.session['post_save_redirect'] = True
        
        # CASE 4: Handle the redirect after a POST save
        if request.session.pop('post_save_redirect', False):
            # Find which app we're in
            modeladmin_match = re.match(modeladmin_pattern, path)
            if modeladmin_match:
                app_name = modeladmin_match.group(1)
                filter_key = f"wagtail_filters_{app_name}"
                
                if filter_key in request.session:
                    stored_filters = request.session[filter_key]
                    if stored_filters:
                        # Try to redirect to results page first, fallback to regular page
                        try_paths = [f"/admin/{app_name}/results/", f"/admin/{app_name}/"]
                        redirect_path = try_paths[0]  # Prefer results page
                            
                        query_string = urlencode(stored_filters, doseq=True)
                        redirect_url = f"{redirect_path}?{query_string}"
                        return HttpResponseRedirect(redirect_url)
        
        return None