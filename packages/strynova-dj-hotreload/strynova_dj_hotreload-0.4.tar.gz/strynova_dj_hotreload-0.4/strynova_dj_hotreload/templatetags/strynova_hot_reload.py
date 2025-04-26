from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def hot_reload_js(ws_host=None, ws_port=None):
    """
    Template tag to include the hot reload JavaScript client.
    
    Usage:
        {% load strynova_hot_reload %}
        {% hot_reload_js %}
        
    With custom WebSocket host and port:
        {% hot_reload_js ws_host="localhost" ws_port="9000" %}
    """
    # Only include in debug mode by default
    if not getattr(settings, 'DEBUG', False) and not getattr(settings, 'STRYNOVA_HOT_RELOAD_FORCE', False):
        return ''
    
    # Get host and port from settings if not provided
    if ws_host is None:
        ws_host = getattr(settings, 'STRYNOVA_HOT_RELOAD_HOST', '127.0.0.1')
    
    if ws_port is None:
        ws_port = getattr(settings, 'STRYNOVA_HOT_RELOAD_PORT', 8765)
    
    # Create the script tag with data attributes for configuration
    script_tag = (
        f'<script src="{settings.STATIC_URL}strynova_dj_hotreload/js/hot-reload.js" '
        f'data-ws-host="{ws_host}" data-ws-port="{ws_port}"></script>'
    )
    
    return mark_safe(script_tag)