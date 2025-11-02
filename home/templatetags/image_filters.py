from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from urllib.parse import unquote
import logging

# Import our new configuration system
from config.image_config import get_image_config

register = template.Library()

# Configure logging
logger = logging.getLogger(__name__)

@register.filter
def optimized_image(image_url):
    """
    Convert old image paths to optimized paths using configuration system
    Example: /static/images/Projects/OpenAI_Language_Learning_Assistant_COVER.png
    Becomes: /static/images/optimized/projects/openai-assistant.jpg
    
    Performance improvements:
    - O(1) lookup instead of O(n) iteration
    - Cached configuration
    - Pattern-based matching for dynamic resolution
    """
    if not image_url:
        return image_url
    
    try:
        # Get image configuration (cached, efficient)
        image_config = get_image_config()
        
        # Extract path after /static/images/
        if '/static/images/' not in image_url:
            return image_url
        
        image_path = image_url.replace('/static/images/', '')
        
        # Get optimized path using efficient lookup
        optimized_path = image_config.get_mapping(image_path)
        
        if optimized_path:
            return static(optimized_path)
        else:
            # Log missing mapping for debugging
            logger.warning(f"No mapping found for: {image_path}")
            return image_url
            
    except Exception as e:
        # Graceful error handling
        logger.error(f"Error in optimized_image filter: {e}")
        return image_url

@register.filter
def webp_fallback(image_url):
    """
    Generate WebP fallback URL for optimized images
    Simplified logic with better error handling
    """
    if not image_url:
        return image_url
    
    # If it's already an optimized image, replace .jpg with .webp
    if '/images/optimized/' in image_url and image_url.endswith('.jpg'):
        return image_url.replace('.jpg', '.webp')
    
    return image_url

@register.simple_tag
def optimized_image_tag(image_url, alt_text, css_class="", loading="lazy"):
    """
    Generate optimized image tag with improved error handling and validation
    Performance optimizations:
    - Early returns for invalid inputs
    - Efficient static URL generation
    - Graceful fallbacks
    """
    if not image_url:
        # Return placeholder div for missing images
        return mark_safe(
            f'<div class="{css_class} flex items-center justify-center bg-gray-200 text-gray-400 text-4xl">📁</div>'
        )
    
    try:
        # Get optimized URL using our efficient filter
        optimized_url = optimized_image(image_url)
        
        # If no optimization was possible, use original
        if optimized_url == image_url:
            logger.info(f"Using original image (no optimization): {image_url}")
        
        # Generate optimized img tag with modern attributes
        img_tag = (
            f'<img src="{optimized_url}" '
            f'alt="{alt_text}" '
            f'class="{css_class}" '
            f'loading="{loading}" '
            f'decoding="async">'
        )
        
        return mark_safe(img_tag)
        
    except Exception as e:
        # Error fallback: show original image with error logging
        logger.error(f"Error generating image tag for {image_url}: {e}")
        
        fallback_tag = (
            f'<img src="{image_url}" '
            f'alt="{alt_text}" '
            f'class="{css_class}" '
            f'loading="{loading}" '
            f'decoding="async">'
        )
        
        return mark_safe(fallback_tag)

@register.simple_tag
def validate_image_mappings():
    """
    Debug tag to validate image mappings
    Returns summary of valid/invalid mappings
    """
    try:
        image_config = get_image_config()
        
        # Get Django static root
        from django.conf import settings
        static_root = getattr(settings, 'STATIC_ROOT', 'staticfiles')
        
        total, valid = image_config.validate_mappings(static_root)
        
        if total == valid:
            return mark_safe(f'<span class="text-green-600">✅ All {total} mappings valid</span>')
        else:
            return mark_safe(
                f'<span class="text-yellow-600">⚠️ {valid}/{total} mappings valid</span>'
            )
            
    except Exception as e:
        return mark_safe(f'<span class="text-red-600">❌ Error: {e}</span>')