from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['post_count']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = '# Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'preview_image',
        'is_active',
        'created_on',
        'category_list',
        'view_on_site_link'
    ]
    list_filter = ['is_active', 'created_on', 'categories']
    search_fields = ['name', 'body']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories']
    date_hierarchy = 'created_on'
    readonly_fields = ['created_on', 'last_modified', 'preview_full_image']

    fieldsets = (
        ('Content', {
            'fields': ('name', 'slug', 'body')
        }),
        ('Media', {
            'fields': ('image', 'preview_full_image')
        }),
        ('Organization', {
            'fields': ('categories', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_on', 'last_modified'),
            'classes': ('collapse',)
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.image.url
            )
        return "-"
    preview_image.short_description = 'Image'

    def preview_full_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 500px; border-radius: 10px;" />',
                obj.image.url
            )
        return "-"
    preview_full_image.short_description = 'Image Preview'

    def category_list(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    category_list.short_description = 'Categories'

    def view_on_site_link(self, obj):
        if obj.is_active:
            return format_html(
                '<a href="{}" target="_blank" class="button">View Live</a>',
                obj.get_absolute_url()
            )
        return "-"
    view_on_site_link.short_description = 'View'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_on_short', 'body_preview']
    list_filter = ['created_on', 'post']
    search_fields = ['author', 'body', 'post__name']
    readonly_fields = ['created_on']
    date_hierarchy = 'created_on'

    def created_on_short(self, obj):
        return obj.created_on.strftime('%Y-%m-%d %H:%M')
    created_on_short.short_description = 'Date'
    created_on_short.admin_order_field = 'created_on'

    def body_preview(self, obj):
        return obj.body[:75] + '...' if len(obj.body) > 75 else obj.body
    body_preview.short_description = 'Comment'
