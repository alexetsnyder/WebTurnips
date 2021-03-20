from django import forms
from .date_helper import DateHelper
from .models import StalkWeek, TurnipStack, DayPrices
from .widgets import CustomDatePicker


class DefaultDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        super(DefaultDateField, self).__init__(
            *args,
            input_formats=['%B %d %Y'],
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

    def get_create_parameters(self):
        return {**self.extra, **{key: self.cleaned_data[key] for key in self._info.fields}}

    def save(self):
        if self._info.model is not None:
            return self._info.model.objects.create(**self.get_create_parameters())


class AddStalkWeekForm(ModelForm):
    current_date = DefaultDateField(label='Create Date')
    buy_price = forms.IntegerField(label='Buy Price:', min_value=90)
    turnip_stacks = forms.IntegerField(label='Stacks of 10 Turnips')
    turnip_count = forms.IntegerField(label='Total turnip count', disabled=True, required=False)

    class ModelInfo:
        model = StalkWeek
        fields = ['sunday', 'saturday', 'buy_price']
        extra = []

    def get_start_date(self):
        return DateHelper.get_sunday(self.cleaned_data['current_date'])

    def get_end_date(self):
        return DateHelper.get_saturday(self.cleaned_data['current_date'])

    def save(self):
        self.cleaned_data['sunday'] = self.get_start_date()
        self.cleaned_data['saturday'] = self.get_end_date()
        stalk_week = super().save()
        if self._info.model is not None:
            for i in range(self.cleaned_data['turnip_stacks']):
                TurnipStack.objects.create(
                    stalk_week_id=stalk_week.id,
                    sell_date=self.cleaned_data['current_date'],
                    sell_price=0,
                )
        return stalk_week


class AddDayPriceForm(ModelForm):
    current_date = DefaultDateField(label='Current Date:')
    first_sell_price = forms.IntegerField(label='Price Before Noon:', min_value=2)
    last_sell_price = forms.IntegerField(label='Price After Noon:', min_value=2)

    class ModelInfo:
        model = DayPrices
        fields = ['current_date', 'first_sell_price', 'last_sell_price']
        extra = ['stalk_week_id']


class AddTurnipStacksForm(ModelForm):
    sell_date = DefaultDateField(label='Sell Date:')
    sell_price = forms.IntegerField(label='Sell Price:')
    turnip_stacks = forms.IntegerField(label='Stacks of 10 turnips')
    turnip_count = forms.IntegerField(label='Number of turnips', disabled=True, required=False)

    class ModelInfo:
        model = TurnipStack
        fields = ['sell_date', 'sell_price']
        extra = ['stalk_week_id']

    def save(self):
        if self._info.model is not None:
            for i in range(self.cleaned_data['turnip_stacks']):
                self._info.model.objects.create(**self.get_create_parameters())


class SellTurnipStacksForm(ModelForm):
    sell_date = DefaultDateField(label='Sell Date:')
    sell_price = forms.IntegerField(label='Sell Price')
    turnip_stacks = forms.IntegerField(label='Stacks of 10 turnips')
    turnip_count = forms.IntegerField(label='Number of turnips', disabled=True, required=False)

    class ModelInfo:
        model = TurnipStack
        fields = ['sell_date', 'sell_price']
        extra = ['stalk_week_id']

    def save(self):
        if self._info.model is not None:
            stacks = self.cleaned_data['turnip_stacks']
            stack_list = TurnipStack.objects.filter(sell_price=0, stalk_week_id=self.extra['stalk_week_id'])[:stacks]
            update_list = []
            for stack in stack_list:
                stack.sell_price = self.cleaned_data['sell_price']
                update_list.append(stack)
            TurnipStack.objects.bulk_update(update_list, ['sell_price'])
