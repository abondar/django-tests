from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from tests.models import *
from nested_inline.admin import  NestedStackedInline, NestedModelAdmin


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        count = 0
        right_count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
                    if form.cleaned_data['is_right']:
                        right_count += 1

            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 2:
            raise ValidationError('Вопрос должен иметь по крайней мере два ответа')
        elif right_count == count:
            raise ValidationError('Все ответы на вопрос не могут быть правльными')


class AnswerInline(NestedStackedInline):
    model = Answer
    formset = AnswerInlineFormSet


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = [AnswerInline]


class TestAdmin(NestedModelAdmin):
    model = Test
    inlines = [QuestionInline]


admin.site.register(Test, TestAdmin)
