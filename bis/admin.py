from django.contrib import admin

from .models import Hizlaria, ParteHartzea, Testua

class HizlariaAdmin(admin.ModelAdmin):
    list_display = ('abizenak', 'alderdia', 'generoa')
    search_fields = ['abizenak']
    list_filter = ['alderdia', 'generoa']

class ParteHartzeaAdmin(admin.ModelAdmin):
    list_display = ('data', 'p_ordena', 'hizlaria')
    search_fields = ['p_ordena', 'hizlaria__abizenak']
    date_hierarchy = 'data'

class TestuaAdmin(admin.ModelAdmin):
    list_display = ('parteHartzea', 't_ordena', 'hizkuntza','entitateak_ditu')#,'entitateak_stopwords_ditu','tf_idf_ditu')
    search_fields = ['parteHartzea__p_ordena', 't_ordena','entitateak']
    list_filter = ['hizkuntza']
    date_hierarchy = 'parteHartzea__data'

admin.site.register(Hizlaria, HizlariaAdmin)
admin.site.register(ParteHartzea, ParteHartzeaAdmin)
admin.site.register(Testua, TestuaAdmin)
