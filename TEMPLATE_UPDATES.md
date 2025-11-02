# Django Template Updates for Optimized Images

## 📝 Template Changes Required

### **1. Update Header Template**
**File:** `home/templates/home/header.html`

```html
<!-- BEFORE -->
<img src="{% static 'images/profile-pic.png' %}" alt="Gero Zayas">

<!-- AFTER -->
<picture>
  <source srcset="{% static 'images/optimized/profile/profile-pic.webp' %}" type="image/webp">
  <img src="{% static 'images/optimized/profile/profile-pic.jpg' %}" 
       alt="Gero Zayas" 
       loading="lazy" 
       decoding="async"
       width="40" 
       height="40">
</picture>
```

### **2. Update About Template**
**File:** `home/templates/home/about.html`

```html
<!-- BEFORE -->
<img src="{% static 'images/New-Profile-Pic-Gero.jpg' %}" alt="Gero Zayas">

<!-- AFTER -->
<picture>
  <source srcset="{% static 'images/optimized/profile/about-pic.webp' %}" type="image/webp">
  <img src="{% static 'images/optimized/profile/about-pic.jpg' %}" 
       alt="Gero Zayas" 
       loading="lazy" 
       decoding="async"
       width="300" 
       height="300">
</picture>
```

### **3. Update Portfolio Templates**
**File:** `portfolio/templates/portfolio/portfolio_list.html`

```html
<!-- BEFORE -->
{% if project.image %}
<img src="{{ project.image.url }}" alt="{{ project.title }}">
{% endif %}

<!-- AFTER -->
{% if project.image %}
<picture>
  <source srcset="{{ project.image.url|replace:'images/':'images/optimized/projects/'|replace:'.png':'.webp'|replace:'.jpg':'.webp' }}" type="image/webp">
  <img src="{{ project.image.url|replace:'images/':'images/optimized/projects/' }}" 
       alt="{{ project.title }}" 
       loading="lazy" 
       decoding="async"
       width="400" 
       height="300">
</picture>
{% endif %}
```

### **4. Update Blog Templates**
**File:** `blog/templates/blog/blog_list.html`

```html
<!-- BEFORE -->
{% if post.image %}
<img src="{{ post.image.url }}" alt="{{ post.title }}">
{% endif %}

<!-- AFTER -->
{% if post.image %}
<picture>
  <source srcset="{{ post.image.url|replace:'images/':'images/optimized/blog/'|replace:'.png':'.webp'|replace:'.jpg':'.webp' }}" type="image/webp">
  <img src="{{ post.image.url|replace:'images/':'images/optimized/blog/' }}" 
       alt="{{ post.title }}" 
       loading="lazy" 
       decoding="async"
       width="800" 
       height="400">
</picture>
{% endif %}
```

### **5. Update Footer Template**
**File:** `home/templates/home/footer.html`

```html
<!-- BEFORE -->
<img src="{% static 'images/linkedin.png' %}" alt="LinkedIn">

<!-- AFTER -->
<picture>
  <source srcset="{% static 'images/optimized/social/linkedin.webp' %}" type="image/webp">
  <img src="{% static 'images/optimized/social/linkedin.jpg' %}" 
       alt="LinkedIn" 
       loading="lazy"
       width="24" 
       height="24">
</picture>
```

## 🔄 Django Model Updates

### **Update Image Field Paths**

**File:** `portfolio/models.py`

```python
# BEFORE
image = models.ImageField(upload_to="projects/")

# AFTER  
image = models.ImageField(
    upload_to="optimized/projects/",
    help_text="Upload optimized project images (max 150KB)"
)
```

**File:** `blog/models.py`

```python
# BEFORE
image = models.ImageField(upload_to="blog/%Y/%m/")

# AFTER
image = models.ImageField(
    upload_to="optimized/blog/",
    help_text="Upload optimized blog images (max 100KB)"
)
```

## 🛠️ Django Settings Updates

**File:** `config/settings.py`

```python
# Add these settings for image optimization

# Image validation
from django.core.exceptions import ValidationError

def validate_image_size(value):
    filesize = value.size
    
    if filesize > 2 * 1024 * 1024:  # 2MB limit
        raise ValidationError("Maximum file size is 2MB")

def validate_image_format(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    
    if not ext.lower() in valid_extensions:
        raise.ValidationError("Unsupported file format. Use JPG, PNG, or WebP")

# Update model fields with validation
# In your models.py:
# image = models.ImageField(
#     upload_to="optimized/projects/",
#     validators=[validate_image_size, validate_image_format],
#     help_text="Upload optimized images (JPG/PNG/WebP, max 2MB)"
# )

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

## 📊 Performance Monitoring

### **Add to Base Template**
**File:** `home/templates/home/base.html`

```html
<!-- Add before closing </head> tag -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.yourdomain.com">

<!-- Add performance monitoring -->
<script>
// Monitor Core Web Vitals
function reportWebVitals() {
  if ('PerformanceObserver' in window) {
    // Largest Contentful Paint
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        if (entry.element && entry.element.tagName === 'IMG') {
          console.log('LCP Image:', entry.element.src, entry.startTime);
        }
      }
    }).observe({entryTypes: ['largest-contentful-paint']});
    
    // Cumulative Layout Shift
    new PerformanceObserver((entryList) => {
      for (const entry of entryList.getEntries()) {
        console.log('CLS:', entry.value);
      }
    }).observe({entryTypes: ['layout-shift']});
  }
}

reportWebVitals();
</script>
```

## 🚀 Deployment Commands

```bash
# 1. Run optimization script
chmod +x optimize_portfolio_images.sh
./optimize_portfolio_images.sh

# 2. Update Django static files
python manage.py collectstatic --noinput --clear

# 3. Create database migrations for any model changes
python manage.py makemigrations
python manage.py migrate

# 4. Compress static files (if using django-compressor)
python manage.py compress --force

# 5. Test the application
python manage.py runserver
```

## 📈 Expected Performance Improvements

### **Before Optimization:**
- Total image size: ~12.5MB
- Page load time: 8-12 seconds
- LCP score: Poor (2.5-4.0s)
- CLS score: Poor (0.3+)

### **After Optimization:**
- Total image size: ~2.5MB (80% reduction)
- Page load time: 2-3 seconds
- LCP score: Good (1.0-2.5s)
- CLS score: Good (0.1-0.25)
- Better SEO rankings
- Improved user experience
- Reduced bandwidth costs

## 🔧 Maintenance Commands

```bash
# Weekly optimization check
python manage.py shell << EOF
from django.core.files.storage import default_storage
import os

# Check for oversized images
media_root = 'media'
for root, dirs, files in os.walk(media_root):
    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if size > 1:  # Larger than 1MB
                print(f"Large image found: {file_path} - {size:.2f}MB")
EOF

# Monthly cleanup
python manage.py collectstatic --clear --noinput
find static/ -name "*.gz" -delete  # Clear compressed cache
```

This comprehensive optimization will make your Django portfolio lightning-fast while maintaining excellent image quality! ⚡
