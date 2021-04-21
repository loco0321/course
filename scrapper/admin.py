from django.contrib import admin

from scrapper.models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'rating']
    search_fields = ['name']
    list_filter = ['year']


admin.site.register(Movie, MovieAdmin)
