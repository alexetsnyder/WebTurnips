from django.db import models
from .date_helper import OUTPUT_DATE_FORMAT


# class MergedTurnipRow:
#     def __init__(self, sell_date, turnip_count, single_price, turnip_price):
#         self.sell_date = sell_date
#         self.turnip_count = turnip_count
#         self.total_sales = turnip_price
#         self.single_price = single_price
#
#     def __str__(self):
#         ret_str = f'Turnips: {self.turnip_count:,} - Sold: {self.single_price} Bells Each'
#         ret_str += f' - Total: {self.total_sales:,} Bells'
#         if self.sell_date is not None:
#             ret_str = f'Date: {self.sell_date:{OUTPUT_DATE_FORMAT}} - {ret_str}'
#         return ret_str


class StalkWeek(models.Model):
    sunday = models.DateField('Start of stalk week')
    saturday = models.DateField('End of stalk week')
    buy_price = models.IntegerField('Turnip buy price')

    def __str__(self):
        date_f = OUTPUT_DATE_FORMAT
        ret_str = f'Week: {self.sunday:{date_f}} - {self.saturday:{date_f}} - Buy Price: {self.buy_price}'
        # ret_str += f' - Total Cost: {self.get_cost():,} - Profit: {self.get_profit()} Bells'
        return ret_str

    def get_card_header(self):
        return f'{self.sunday:{OUTPUT_DATE_FORMAT}} - {self.saturday:{OUTPUT_DATE_FORMAT}}'

    def get_card_content(self):
        return f'Turnip Stacks: {self.get_turnip_stacks():,} Buy Price: {self.buy_price} Bells Each'

    def get_turnip_stacks(self):
        return sum([stacks.turnip_stacks for stacks in self.turnipstacks_set.all()])

    def turnip_count(self):
        return sum([stacks.get_turnip_count() for stacks in self.turnipstacks_set.all()])

    #
    # def merge_turnips(self):
    #     all_turnip_stacks = list(self.turnipstack_set.all())
    #     merged_turnip_stacks = []
    #     while len(all_turnip_stacks) > 0:
    #         turnip_stack = all_turnip_stacks.pop()
    #         sell_date = turnip_stack.sell_date
    #         total_count = turnip_stack.stack_size
    #         single_price = turnip_stack.sell_price
    #         total_price = turnip_stack.get_sales()
    #         temp_turnip_stacks = [stack for stack in all_turnip_stacks]
    #         all_turnip_stacks.clear()
    #         for stack in temp_turnip_stacks:
    #             if stack.sell_date == sell_date and stack.sell_price == single_price:
    #                 total_count += stack.stack_size
    #                 total_price += stack.get_sales()
    #             else:
    #                 all_turnip_stacks.append(stack)
    #         merged_turnip_stacks.append((sell_date, total_count, single_price, total_price))
    #     return merged_turnip_stacks

    # def get_merged_turnips(self):
    #     return [MergedTurnipRow(date, count, single, price) for date, count, single, price in self.merge_turnips()]

    def get_cost(self):
        return self.turnip_count() * self.buy_price

    def get_sales(self):
        return sum([stack.get_sales() for stack in self.turnipstacks_set.all()])

    def get_profit(self):
        return self.get_sales() - self.get_cost()

    @staticmethod
    def get_latest_stalk_weeks():
        return StalkWeek.objects.order_by("sunday")[:5]


class DayPrices(models.Model):
    current_date = models.DateField('Day of week')
    first_sell_price = models.IntegerField('Sell price before noon')
    last_sell_price = models.IntegerField('Sell price after noon')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        ret_str = f'Date: {self.current_date:{OUTPUT_DATE_FORMAT}} - Price Before Noon: {self.first_sell_price} Bells'
        ret_str += f' - Price After Noon: {self.last_sell_price} Bells'
        return ret_str


class TurnipStacks(models.Model):
    turnip_stacks = models.IntegerField('Stacks of Turnips Sold')
    stack_size = models.IntegerField('Turnips in a stack', default=10)
    sell_date = models.DateField('Date turnips sold', null=True)
    sell_price = models.IntegerField('Price turnip sold at', default=0, )
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        ret_str = ''
        ret_str += f'Turnips: {self.get_turnip_count():,} - Sell Price: {self.sell_price} Bells - '
        ret_str += f'Total: {self.get_sales():,} Bells '
        ret_str += (lambda: f'Date: {self.sell_date:{OUTPUT_DATE_FORMAT}}', lambda: '')[self.sell_date is None]()
        return ret_str

    def get_sales(self):
        return self.turnip_stacks * self.stack_size * self.sell_price

    def get_turnip_count(self):
        return self.stack_size * self.turnip_stacks
