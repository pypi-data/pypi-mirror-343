from django.utils.deprecation import MiddlewareMixin
from urllib.parse import urlparse, parse_qs, urlencode
from django.http import HttpResponseRedirect

class WagtailFilterPersistenceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if this is a Wagtail admin request
        if not request.path.startswith('/admin/'):
            return None
            
        # Store filter params when viewing a listing
        if 'modeladmin' in request.path and not request.path.endswith('/create/') and not '/edit/' in request.path:
            query_params = parse_qs(request.META.get('QUERY_STRING', ''))
            if query_params:
                request.session['wagtail_filters_' + request.path] = query_params
        
        # Get the current page's "base path" (without query string)
        current_path = request.path
        
        # Check if we're on a listing page with no query params but have stored filters
        # This handles direct navigation or redirects after save
        if (not request.META.get('QUERY_STRING') and 
            'modeladmin' in current_path and 
            not current_path.endswith('/create/') and 
            not '/edit/' in current_path):
            
            # Check if we have stored filters for this page
            if 'wagtail_filters_' + current_path in request.session:
                stored_params = request.session.get('wagtail_filters_' + current_path)
                if stored_params:
                    # Redirect to the same URL but with the stored parameters
                    query_string = urlencode(stored_params, doseq=True)
                    redirect_url = current_path + '?' + query_string
                    return HttpResponseRedirect(redirect_url)
        
        # Additionally, check if we're coming from an edit page (post-save)
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            parsed_referer = urlparse(referer)
            referer_path = parsed_referer.path
            
            # Check if referer was an edit page and current is a listing
            is_from_edit = '/edit/' in referer_path
            is_listing_page = 'modeladmin' in current_path and not '/edit/' in current_path and not current_path.endswith('/create/')
            
            if is_from_edit and is_listing_page and not request.META.get('QUERY_STRING'):
                # Find the stored filters for the current path
                if 'wagtail_filters_' + current_path in request.session:
                    stored_params = request.session.get('wagtail_filters_' + current_path)
                    if stored_params:
                        # Redirect to apply the stored filters
                        query_string = urlencode(stored_params, doseq=True)
                        redirect_url = current_path + '?' + query_string
                        return HttpResponseRedirect(redirect_url)
                
        return None