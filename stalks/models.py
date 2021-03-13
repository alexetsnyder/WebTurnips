from django.db import models


class MergedTurnipRow:
    def __init__(self, turnip_count, turnip_price):
        self.turnip_count = turnip_count
        self.turnip_price = turnip_price


class StalkWeek (models.Model):
    start_date = models.DateField('Start of stalk week')
    end_date = models.DateField('End of stalk week')
    buy_price = models.IntegerField('Turnip buy price')

    def __str__(self):
        ret_str = 'Week: {:%B %d %Y} - {:%B %d %Y} -- '.format(self.start_date, self.end_date)
        ret_str += '{0} turnips, at {1} bells each, '.format(self.turnip_count(), self.buy_price)
        ret_str += '{0} total cost -- Profit: {1} Bells'.format(self.get_cost(), self.get_profit())
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
            total_price = turnip_stack.get_sales()
            temp_turnip_stacks = [stack for stack in all_turnip_stacks]
            all_turnip_stacks.clear()
            for stack in temp_turnip_stacks:
                if stack.sell_price == turnip_stack.sell_price:
                    total_count += stack.stack_size
                    total_price += stack.get_sales()
                else:
                    all_turnip_stacks.append(stack)
            merged_turnip_stacks.append((total_count, total_price))
        return merged_turnip_stacks

    def get_merged_turnips(self):
        return [MergedTurnipRow(count, price) for count, price in self.merge_turnips()]

    def get_cost(self):
        return self.turnip_count() * self.buy_price

    def get_profit(self):
        cost = self.get_cost()
        total_sales = sum([turnip_stack.get_sales() for turnip_stack in self.turnipstack_set.all()])
        return total_sales - cost


class DayPrices (models.Model):
    price_date = models.DateField('Day of week')
    sell_price_before_noon = models.IntegerField('Sell price before noon')
    sell_price_after_noon = models.IntegerField('Sell price after noon')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        return 'Date: {0} -- Sell Prices: Before noon: {1} After noon: {2}' \
            .format(self.price_date, self.sell_price_before_noon, self.sell_price_after_noon)


class TurnipStack (models.Model):
    stack_size = models.IntegerField('Turnips in a stack', default=10)
    sell_price = models.IntegerField('Price turnip sold at')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        return '10 turnips sold at {0}'.format(self.sell_price)

    def get_sales(self):
        return 10 * self.sell_price
