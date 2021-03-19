from django.db import models


class MergedTurnipRow:
    def __init__(self, turnip_count, single_price, turnip_price):
        self.turnip_count = turnip_count
        self.total_sales = turnip_price
        self.single_price = single_price

    def __str__(self):
        return 'Turnips: {0:,} -- Sold at: {1} Bells each -- Total: {2:,} Bells'\
                .format(self.turnip_count, self.single_price, self.total_sales)


class StalkWeek (models.Model):
    sunday = models.DateField('Start of stalk week')
    saturday = models.DateField('End of stalk week')
    buy_price = models.IntegerField('Turnip buy price')

    def __str__(self):
        ret_str = 'Week: {:%B %d %Y} - {:%B %d %Y} -- '.format(self.sunday, self.saturday)
        ret_str += '{0:,} turnips, at {1:,} bells each, '.format(self.turnip_count(), self.buy_price)
        ret_str += '{0:,} total cost -- Profit: {1:,} Bells'.format(self.get_cost(), self.get_profit())
        return ret_str

    def get_turnip_stacks(self):
        return self.turnipstack_set.all()

    def turnip_count(self):
        return 10 * len(self.get_turnip_stacks())

    def merge_turnips(self):
        all_turnip_stacks = list(self.turnipstack_set.all())
        merged_turnip_stacks = []
        while len(all_turnip_stacks) > 0:
            turnip_stack = all_turnip_stacks.pop()
            total_count = turnip_stack.stack_size
            single_price = turnip_stack.sell_price
            total_price = turnip_stack.get_sales()
            temp_turnip_stacks = [stack for stack in all_turnip_stacks]
            all_turnip_stacks.clear()
            for stack in temp_turnip_stacks:
                if stack.sell_price == turnip_stack.sell_price:
                    total_count += stack.stack_size
                    total_price += stack.get_sales()
                else:
                    all_turnip_stacks.append(stack)
            merged_turnip_stacks.append((total_count, single_price, total_price))
        return merged_turnip_stacks

    def get_merged_turnips(self):
        return [MergedTurnipRow(count, single, price) for count, single, price in self.merge_turnips()]

    def get_cost(self):
        return self.turnip_count() * self.buy_price

    def get_sales(self):
        return sum([stack.get_sales() for stack in self.turnipstack_set.all()])

    def get_profit(self):
        return self.get_sales() - self.get_cost()

    def get_latest_stalk_weeks(self):
        return StalkWeek.objects.order_by("-sunday")[:5]


class DayPrices (models.Model):
    current_date = models.DateField('Day of week')
    first_sell_price = models.IntegerField('Sell price before noon')
    last_sell_price = models.IntegerField('Sell price after noon')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        return 'Date: {0:%B %m %Y} -- Price before noon: {1} -- Price after noon: {2} Bells' \
            .format(self.current_date, self.first_sell_price, self.last_sell_price)


class TurnipStack (models.Model):
    stack_size = models.IntegerField('Turnips in a stack', default=10)
    sell_date = models.DateField('Date turnips sold')
    sell_price = models.IntegerField('Price turnip sold at')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def get_sales(self):
        return 10 * self.sell_price
