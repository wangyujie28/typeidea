from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Tag
from .adminforms import *
from typeidea.custom_site import custom_site
from django.contrib.admin.models import LogEntry
# Register your models here.


class BaseOwnerAdmin(admin.ModelAdmin):
    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(id=self.value())
        return queryset

class PostInline(admin.TabularInline): #stackedline样式不同
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):         #(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    #list_filter = [CategoryOwnerFilter]
    fields = ('name', 'status', 'is_nav')

    inlines = [PostInline]

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

    '''
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)
     '''

@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):                  #(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    '''
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)
    '''

@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):            #(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = []
    list_filter = ['category', ]
    search_fields = ['title', 'category__name']
    actions_on_top = False
    actions_on_bottom = True

    #编辑页面
    save_on_top = False

    #fields = (('category', 'title'), 'desc', 'status', 'content', 'tag')
    fieldsets = (
        (
             '基础配置', {
            'description' : '基础配置描述',
            'fields' : (('title', 'category'), 'status')
            }
        ),
       (
           '内容', {
               'fields' : ('desc', 'content'),
           }
       ),
       (
           '额外信息', {
               'classes': ('collapse', ),
               'fields' :('tag', ),
           }
       )
    )

    form = PostAdminForm

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '操作'

    '''
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner = request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
     '''
    class Media:
        css = {
            'all' : ("../typeidea/css/bootstrap.min.css"),
        }
        js = ('../typeidea/js/bootstrap.bundle.js')


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']

    def get_queryset(self, request):
        qs = super(LogEntryAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)