import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from psqlextra.indexes import UniqueIndex


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created_at')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('updated_at')
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('title'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class MovieTypes(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(verbose_name=_('creation_date'))
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(
        verbose_name=_('type'),
        max_length=10,
        choices=MovieTypes.choices,
        blank=False, null=False
    )
    genres = models.ManyToManyField(
        Genre, through='GenreFilmwork', verbose_name=_('genres')
    )
    persons = models.ManyToManyField(
        Person, through='PersonFilmwork',
        verbose_name=_('persons')
    )
    file_path = models.FileField(
        _('file'), blank=True, null=True, upload_to='movies/'
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('movie')
        verbose_name_plural = _('movies')
        indexes = [
            models.Index(
                fields=['creation_date'],
                name='film_work_creation_date_idx'
            ),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork, on_delete=models.CASCADE, verbose_name=_('movie')
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name=_('genre')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('creation_date')
    )

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            UniqueIndex(
                fields=['film_work_id', 'genre_id'],
                name='film_work_genre_idx'),
        ]


class PersonFilmwork(UUIDMixin):
    class RoleTypes(models.TextChoices):
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')
        ACTOR = 'actor', _('actor')
    film_work = models.ForeignKey(
        Filmwork, on_delete=models.CASCADE,
        verbose_name=_('movie'), related_name='person_filmwork'
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name=_('person')
    )
    role = models.TextField(_('role'), null=True, choices=RoleTypes.choices,)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('creation_date')
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            UniqueIndex(
                fields=['film_work_id', 'person_id', 'role'],
                name='film_work_person_idx'
            ),
        ]
