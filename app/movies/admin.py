from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = (
        'person',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'type', 'creation_date', 'rating', 'get_genres',
        'get_director', 'get_writer', 'get_actor'
    )
    list_filter = ('type', 'creation_date',)
    search_fields = ('title', 'description', 'id')
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_prefetch_related = ('persons', 'genres', 'person_filmwork')

    def get_director(self, obj):
        return ','.join(
            [
                item.person.full_name
                for item in obj.person_filmwork.filter(role='director')
            ]
        )

    get_director.short_description = 'Режиссеры фильма'

    def get_writer(self, obj):
        return ','.join(
            [
                item.person.full_name
                for item in obj.person_filmwork.filter(role='writer')
            ]
        )

    get_writer.short_description = 'Авторы фильма'

    def get_actor(self, obj):
        return ','.join(
            [
                item.person.full_name
                for item in obj.person_filmwork.filter(role='actor')
            ]
        )

    get_actor.short_description = 'Актёры фильма'

    def get_queryset(self, request):
        queryset = (
                    super()
                    .get_queryset(request)
                    .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    ordering = ['created_at']
    search_fields = ['full_name']
