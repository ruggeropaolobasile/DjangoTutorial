from django.contrib import admin
from django.utils import timezone

from .models import Choice, Membership, Person, Question


class PublicationStatusFilter(admin.SimpleListFilter):
    title = "publication status"
    parameter_name = "publication_status"

    def lookups(self, request, model_admin):
        return [
            ("published", "Published"),
            ("unpublished", "Unpublished"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "published":
            return queryset.filter(pub_date__lte=timezone.now())
        if self.value() == "unpublished":
            return queryset.filter(pub_date__gt=timezone.now())
        return queryset


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "owner", "pub_date", "was_published_recently"]
    list_filter = ["pub_date", PublicationStatusFilter]
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Person)
admin.site.register(Membership)

