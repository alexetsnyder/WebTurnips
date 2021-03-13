from stalks.date_helper import DateHelper
from stalks.models import StalkWeek, TurnipStack, DayPrices


def create_turnip_stack(stalk_week_id, sell_price):
    return TurnipStack.objects.create(stalk_week_id=stalk_week_id, sell_price=sell_price)


def create_turnip_stacks(stalk_week_id, sell_price, turnip_stacks):
    for i in range(turnip_stacks):
        create_turnip_stack(stalk_week_id=stalk_week_id, sell_price=sell_price)


def create_stalk_week(current_date, buy_price):
    start_date = DateHelper.get_sunday(current_date)
    end_date = DateHelper.get_saturday(current_date)
    return StalkWeek.objects.create(start_date=start_date, end_date=end_date, buy_price=buy_price)


def create_day_price(stalk_week_id, current_date, sell_price_before_noon, sell_price_after_noon):
    return DayPrices.objects.create(
        stalk_week_id=stalk_week_id,
        price_date=current_date,
        sell_price_before_noon=sell_price_before_noon,
        sell_price_after_noon=sell_price_after_noon,
    )
