from django import forms
from django.contrib import admin
from django.contrib.admin import AllValuesFieldListFilter, ChoicesFieldListFilter, \
    RelatedFieldListFilter

from django_filters import Filter


class IntegerFilter(Filter):
    field_class = forms.IntegerField


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (key, value)
            for key, value in changelist.get_filters_params().items()
            if key != self.parameter_name
        )
        yield all_choice


class IDFilter(InputFilter):
    parameter_name = 'id'
    title = 'id'

    def queryset(self, request, queryset):
        if self.value() is not None and self.value() != '':
            return queryset.filter(
                id=self.value()
            )

        return queryset.all()


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'admin/drop_down_filter.html'


class DropDownFilter(AllValuesFieldListFilter):
    template = 'admin/drop_down_filter.html'


class ChoiceDropDownFilter(ChoicesFieldListFilter):
    template = 'admin/drop_down_filter.html'
