# URL Migration Guide - From PK to Slug-Based URLs

**Purpose:** Migrate blog and portfolio URLs from primary key (integer) based to slug-based URLs  
**Impact:** Better SEO, user-friendly URLs, but breaks existing links

---

## Overview

### Current URL Structure
```
/blog/1/              → Blog post with ID 1
/blog/2/              → Blog post with ID 2
/portfolio/5/         → Project with ID 5
```

### New URL Structure (After Migration)
```
/blog/my-first-post/         → Blog post with slug "my-first-post"
/blog/django-tips/           → Blog post with slug "django-tips"
/portfolio/portfolio-website/ → Project with slug "portfolio-website"
```

---

## Why This Change?

**Benefits:**
1. **SEO**: Search engines prefer descriptive URLs
2. **User-Friendly**: Easier to remember and share
3. **Security**: Doesn't expose database IDs
4. **Professional**: Industry standard practice

**Example:**
- **Bad**: `gerozayas.com/blog/123/`
- **Good**: `gerozayas.com/blog/building-django-portfolio/`

---

## Step-by-Step Migration Process

### PHASE 1: Preparation (DO THIS FIRST)

#### Step 1.1: Verify All Posts Have Slugs

Run this in Django shell:
```bash
python manage.py shell
```

```python
from blog.models import Post, Category
from portfolio.models import Project

# Check blog posts
posts_without_slug = Post.objects.filter(slug__isnull=True) | Post.objects.filter(slug='')
print(f"Posts without slug: {posts_without_slug.count()}")
for post in posts_without_slug:
    print(f"  - {post.id}: {post.name}")

# Check categories
categories_without_slug = Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug='')
print(f"Categories without slug: {categories_without_slug.count()}")
for cat in categories_without_slug:
    print(f"  - {cat.id}: {cat.name}")

# Check projects
projects_without_slug = Project.objects.filter(slug__isnull=True) | Project.objects.filter(slug='')
print(f"Projects without slug: {projects_without_slug.count()}")
for proj in projects_without_slug:
    print(f"  - {proj.id}: {proj.title}")
```

#### Step 1.2: Auto-Generate Missing Slugs

If any items are missing slugs, generate them:
```python
from django.template.defaultfilters import slugify

# Fix blog posts
for post in Post.objects.filter(slug__isnull=True) | Post.objects.filter(slug=''):
    post.slug = slugify(post.name)
    post.save()
    print(f"Generated slug for post {post.id}: {post.slug}")

# Fix categories
for cat in Category.objects.filter(slug__isnull=True) | Category.objects.filter(slug=''):
    cat.slug = slugify(cat.name)
    cat.save()
    print(f"Generated slug for category {cat.id}: {cat.slug}")

# Fix projects
for proj in Project.objects.filter(slug__isnull=True) | Project.objects.filter(slug=''):
    proj.slug = slugify(proj.title)
    proj.save()
    print(f"Generated slug for project {proj.id}: {proj.slug}")
```

#### Step 1.3: Create URL Mapping Document

Export current URLs to track the migration:
```python
import csv

# Export blog post mappings
with open('/tmp/blog_url_mapping.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Old URL', 'New URL', 'Post ID', 'Post Name'])
    for post in Post.objects.all():
        old_url = f"/blog/{post.id}/"
        new_url = f"/blog/{post.slug}/"
        writer.writerow([old_url, new_url, post.id, post.name])

print("Blog URL mapping saved to /tmp/blog_url_mapping.csv")

# Export portfolio mappings
with open('/tmp/portfolio_url_mapping.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Old URL', 'New URL', 'Project ID', 'Project Title'])
    for proj in Project.objects.all():
        old_url = f"/portfolio/{proj.id}/"
        new_url = f"/portfolio/{proj.slug}/"
        writer.writerow([old_url, new_url, proj.id, proj.title])

print("Portfolio URL mapping saved to /tmp/portfolio_url_mapping.csv")
```

---

### PHASE 2: Code Changes

#### Step 2.1: Update Blog URLs

**File:** `blog/urls.py`

**Current:**
```python
urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category"),
]
```

**New:**
```python
urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("category/<slug:category_slug>/", views.blog_category, name="blog_category"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),  # Must be last!
]
```

**⚠️ IMPORTANT:** The slug-based detail view MUST be last, otherwise it will catch category URLs!

#### Step 2.2: Update Blog Views

**File:** `blog/views.py`

Update `blog_detail`:
```python
def blog_detail(request, slug):  # Changed from pk to slug
    """Display single blog post with comments."""
    post = get_object_or_404(
        Post.objects.prefetch_related('categories'),
        slug=slug,  # Changed from pk=pk
        is_active=True
    )
    # ... rest of function stays the same
```

Update `blog_category`:
```python
def blog_category(request, category_slug):  # Changed from category
    """Display blog posts filtered by category with optimized queries."""
    posts = Post.objects.filter(
        categories__slug=category_slug,  # Changed from name__contains
        is_active=True
    ).prefetch_related('categories').order_by("-created_on")
    
    context = {"category": category_slug, "posts": posts}
    return render(request, "blog/blog_category.html", context)
```

#### Step 2.3: Update Blog Templates

**File:** `blog/templates/blog/blog_index.html`

Find and replace:
```html
<!-- OLD -->
<a href="{% url 'blog_detail' post.pk %}">{{post.name}}</a>
<a href="{% url 'blog_category' category.name %}">{{ category.name }}</a>

<!-- NEW -->
<a href="{% url 'blog_detail' post.slug %}">{{post.name}}</a>
<a href="{% url 'blog_category' category.slug %}">{{ category.name }}</a>
```

**File:** `blog/templates/blog/blog_detail.html`

Find and replace:
```html
<!-- OLD -->
<a href="{% url 'blog_category' category.name %}">{{ category.name }}</a>

<!-- NEW -->
<a href="{% url 'blog_category' category.slug %}">{{ category.name }}</a>
```

#### Step 2.4: Update Portfolio URLs

**File:** `portfolio/urls.py`

**Current:**
```python
urlpatterns = [
    path("", views.PortfolioView.as_view(), name="portfolio_index"),
    # Assuming you have detail view...
]
```

**New:**
```python
urlpatterns = [
    path("", views.ProjectListView.as_view(), name="portfolio_index"),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="project_detail"),
]
```

#### Step 2.5: Update Portfolio Templates

Search all portfolio templates for pk references and replace with slug.

---

### PHASE 3: Add Redirect Fallback (CRITICAL!)

To ensure old links still work, add a redirect view that catches old pk-based URLs and redirects to slugs.

#### Step 3.1: Create Redirect Views

**File:** `blog/views.py` (add these functions)

```python
from django.shortcuts import redirect
from django.http import Http404

def blog_detail_redirect(request, pk):
    """Redirect old pk-based URLs to new slug-based URLs."""
    try:
        post = Post.objects.only('slug').get(pk=pk)
        return redirect('blog_detail', slug=post.slug, permanent=True)
    except Post.DoesNotExist:
        raise Http404("Post not found")
```

#### Step 3.2: Add Redirect URLs

**File:** `blog/urls.py` (add at the end)

```python
urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("category/<slug:category_slug>/", views.blog_category, name="blog_category"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
    
    # Legacy redirects (keep these for backwards compatibility)
    path("id/<int:pk>/", views.blog_detail_redirect, name="blog_detail_old"),
]
```

**Update any external links to use:** `/blog/id/123/` instead of `/blog/123/`

This way:
- New slug URLs work: `/blog/my-post/` ✅
- Old pk URLs redirect: `/blog/id/123/` → `/blog/my-post/` ✅
- Invalid slugs show 404 ✅

---

### PHASE 4: Testing

#### Step 4.1: Test Old URLs (Before Changes)

Document current working URLs:
```bash
# Test these URLs in browser/curl BEFORE making changes:
http://localhost:8000/blog/1/
http://localhost:8000/blog/2/
http://localhost:8000/portfolio/1/
```

#### Step 4.2: Test New URLs (After Changes)

After deploying changes, test:
```bash
# New slug-based URLs
http://localhost:8000/blog/my-first-post/
http://localhost:8000/blog/category/technology/
http://localhost:8000/portfolio/my-project/

# Old pk-based URLs with redirect
http://localhost:8000/blog/id/1/  # Should redirect to slug URL

# Direct pk URLs should 404 (unless slug happens to match)
http://localhost:8000/blog/1/  # May 404 or match a slug literally named "1"
```

#### Step 4.3: Check All Templates

Search for any remaining pk references:
```bash
# From project root
grep -r "post.pk" blog/templates/
grep -r "project.pk" portfolio/templates/
grep -r "'blog_detail' post.pk" .
grep -r "'project_detail' project.pk" .
```

---

### PHASE 5: Deployment

#### Step 5.1: Development Testing
1. Make all code changes
2. Run migrations: `python manage.py migrate`
3. Test thoroughly in development
4. Check all blog posts load
5. Check all categories work
6. Verify redirects work

#### Step 5.2: Production Deployment

**Option A: Gradual Migration (Recommended)**
1. Deploy code with BOTH pk and slug support
2. Keep redirect URLs active
3. Monitor logs for 404s
4. Update external links gradually
5. After 30 days, remove pk redirects

**Option B: Immediate Migration**
1. Deploy all changes at once
2. Use Railway's deployment to push changes
3. Monitor errors in Railway dashboard
4. Fix issues immediately if they arise

#### Step 5.3: Railway Deployment Checklist
```bash
# Commit changes
git add .
git commit -m "Migrate to slug-based URLs with pk redirects"

# Push to GitHub (Railway will auto-deploy)
git push origin main

# Monitor Railway dashboard for:
# - Successful build
# - No 500 errors
# - Check logs for 404s
```

---

## Potential Issues & Solutions

### Issue 1: Duplicate Slugs

**Problem:** Two posts with same name create duplicate slugs.

**Solution:**
```python
# In blog/models.py Post.save()
def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
    super().save(*args, **kwargs)
```

### Issue 2: Empty/Invalid Slugs

**Problem:** Post name is all special characters → empty slug.

**Solution:** Add validation in admin:
```python
# In blog/admin.py
def save_model(self, request, obj, form, change):
    if not obj.slug or obj.slug.strip() == '':
        obj.slug = f"post-{obj.pk or 'new'}"
    super().save_model(request, obj, form, change)
```

### Issue 3: External Links Break

**Problem:** Other sites linking to your blog with old URLs.

**Solution:** Keep redirect URLs permanently:
- Google will eventually re-index new URLs
- Social media shares will still work via redirects
- Set redirect as `permanent=True` for SEO

---

## Rollback Plan

If something goes wrong:

### Quick Rollback (Revert URLs Only)
```bash
git revert HEAD
git push origin main
```

### Full Rollback (If Database Issues)
1. Restore database backup
2. Revert code changes
3. Redeploy

---

## Post-Migration Checklist

✅ All blog posts have slugs  
✅ All categories have slugs  
✅ All projects have slugs  
✅ Blog URLs updated  
✅ Blog views updated  
✅ Blog templates updated  
✅ Portfolio URLs updated  
✅ Portfolio views updated  
✅ Redirect views added  
✅ Tested in development  
✅ Created URL mapping CSV  
✅ Deployed to production  
✅ Verified no 404 errors  
✅ Updated external links (if any)  

---

## Questions?

If you encounter issues:
1. Check Railway logs for errors
2. Test specific URLs that fail
3. Verify slug field is populated in database
4. Check for duplicate slugs
5. Ask me for help!

---

## Timeline

- **Phase 1 (Preparation)**: 15 minutes
- **Phase 2 (Code Changes)**: 30 minutes
- **Phase 3 (Redirects)**: 15 minutes
- **Phase 4 (Testing)**: 20 minutes
- **Phase 5 (Deployment)**: 10 minutes

**Total: ~1.5 hours**

Let me know when you're ready to start, and we'll go through this step by step!
