from django.db import models


class StalkWeek(models.Model):
    start_date = models.DateField('Start of stalk week')
    end_date = models.DateField('End of stalk week')
    buy_price = models.IntegerField('Turnip buy price')

    def __str__(self):
        return '{0} to {1} -- {2} turnips bought at: {3}'.format(
            self.start_date,
            self.end_date,
            self.turnips(),
            self.buy_price)

    def turnips(self):
        return 10 * len(TurnipStack.objects.filter(stalk_week_id=self.id));


class DayPrices(models.Model):
    price_date = models.DateField('Day of week')
    sell_price_before_noon = models.IntegerField('Sell price before noon')
    sell_price_after_noon = models.IntegerField('Sell price after noon')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        return 'Date: {0} -- Sell Prices: Before noon: {1} After noon: {2}'\
            .format(self.price_date, self.sell_price_before_noon, self.sell_price_after_noon)


class TurnipStack(models.Model):
    sell_price = models.IntegerField('Price turnip sold at')
    stalk_week = models.ForeignKey(StalkWeek, on_delete=models.CASCADE)

    def __str__(self):
        return '10 turnips sold at {0}'.format(self.sell_price)
