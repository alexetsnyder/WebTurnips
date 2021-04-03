from django import forms
from .date_helper import DateHelper
from .models import StalkWeek, TurnipStacks, DayPrices
from .widgets import CustomDatePicker
from .date_helper import OUTPUT_DATE_FORMAT


class DefaultDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super(DefaultDateField, self).__init__(
            *args,
            input_formats=[OUTPUT_DATE_FORMAT],
            widget=CustomDatePicker(),
            **kwargs
        )


class ModelForm(forms.Form):
    class ModelInfo:
        model = None
        fields = []
        extra = []

    def __init__(self, *args, **kwargs):
        self._info = self.ModelInfo()
        self.extra = {key: kwargs.pop(key, None) for key in self._info.extra}
        super(ModelForm, self).__init__(*args, **kwargs)

    def get_parameters(self):
        return {**self.extra, **{key: self.cleaned_data[key] for key in self._info.fields}}

    def save(self):
        if self._info.model is not None:
            return self._info.model.objects.create(**self.get_parameters())


class AddStalkWeekForm(ModelForm):
    primary_key = forms.IntegerField(required=False, initial=None, widget=forms.HiddenInput())
    current_date = DefaultDateField(label='Create Date')
    buy_price = forms.IntegerField(label='Buy Price:', min_value=90)

    class ModelInfo:
        model = StalkWeek
        fields = ['sunday', 'saturday', 'buy_price']
        extra = []

    def get_sunday_date(self):
        return DateHelper.get_sunday(self.cleaned_data['current_date'])

    def get_saturday_date(self):
        return DateHelper.get_saturday(self.cleaned_data['current_date'])

    def clean_current_date(self):
        current_date = self.cleaned_data['current_date']
        sunday = self.get_sunday_date()
        saturday = self.get_saturday_date()
        duplicate_sunday = StalkWeek.objects.filter(sunday=sunday).first()
        if duplicate_sunday:
            self.add_error('current_date', f'Week with sunday={sunday:{OUTPUT_DATE_FORMAT}} already exists.')
        self.cleaned_data['sunday'] = sunday
        self.cleaned_data['saturday'] = saturday
        return current_date

    def save(self):
        pk = self.cleaned_data['primary_key']
        if pk is None:
            return super().save()
        else:
            return StalkWeek.objects.filter(pk=pk).update(self.get_parameters())


class AddDayPriceForm(ModelForm):
    primary_key = forms.IntegerField(required=False, initial=None, widget=forms.HiddenInput())
    current_date = DefaultDateField(label='Current Date:')
    first_sell_price = forms.IntegerField(label='Price Before Noon:', min_value=2)
    last_sell_price = forms.IntegerField(label='Price After Noon:', min_value=2)

    class ModelInfo:
        model = DayPrices
        fields = ['current_date', 'first_sell_price', 'last_sell_price']
        extra = ['stalk_week_id']

    def save(self, stalk_week_id):
        self.extra['stalk_week_id'] = stalk_week_id
        pk = self.cleaned_data['primary_key']
        if pk is None:
            return super().save()
        else:
            return DayPrices.objects.filter(pk=pk).update(self.get_parameters())


class AddTurnipStacksForm(ModelForm):
    primary_key = forms.IntegerField(initial=None, required=False, widget=forms.HiddenInput())
    sell_date = DefaultDateField(label='Sell Date:', required=False)
    sell_price = forms.IntegerField(label='Sell Price:', initial=0)
    turnip_stacks = forms.IntegerField(label='Stacks of 10 turnips')

    class ModelInfo:
        model = TurnipStacks
        fields = ['turnip_stacks', 'sell_date', 'sell_price']
        extra = ['stalk_week_id']

    def save(self, stalk_week_id):
        self.extra['stalk_week_id'] = stalk_week_id
        pk = self.cleaned_data['primary_key']
        if pk is None:
            return super().save()
        else:
            turnip_stacks_model = TurnipStacks.objects.get(pk=pk)
            turnip_stacks_database = turnip_stacks_model.turnip_stacks
            turnip_stacks_form = self.cleaned_data['turnip_stacks']
            turnip_stacks_model.save(self.get_parameters())
            if turnip_stacks_form < turnip_stacks_database:
                TurnipStacks.objects.create({'turnip_stacks': turnip_stacks_database - turnip_stacks_form})


        # if self._info.model is not None:
        #     for i in range(self.cleaned_data['turnip_stacks']):
        #         self._info.model.objects.create(**self.get_parameters())


# class SellTurnipStacksForm(ModelForm):
#     sell_date = DefaultDateField(label='Sell Date:')
#     sell_price = forms.IntegerField(label='Sell Price')
#     turnip_stacks = forms.IntegerField(label='Stacks of 10 turnips')
#     turnip_count = forms.IntegerField(label='Number of turnips', disabled=True, required=False)
#
#     class ModelInfo:
#         model = TurnipStack
#         fields = ['sell_date', 'sell_price']
#         extra = ['stalk_week_id']
#
#     def save(self):
#         if self._info.model is not None:
#             stacks = self.cleaned_data['turnip_stacks']
#             stack_list = TurnipStack.objects.filter(sell_price=0, stalk_week_id=self.extra['stalk_week_id'])[:stacks]
#             update_list = []
#             for stack in stack_list:
#                 stack.sell_date = self.cleaned_data['sell_date']
#                 stack.sell_price = self.cleaned_data['sell_price']
#                 update_list.append(stack)
#             TurnipStack.objects.bulk_update(update_list, ['sell_date', 'sell_price'])
