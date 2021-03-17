from stalks.date_helper import DateHelper
from stalks.models import StalkWeek, TurnipStack, DayPrices


def create_turnip_stack(stalk_week_id, sell_date, sell_price):
    return TurnipStack.objects.create(stalk_week_id=stalk_week_id, sell_date=sell_date, sell_price=sell_price)


def create_turnip_stacks(stalk_week_id, sell_date, sell_price, turnip_stacks):
    for i in range(turnip_stacks):
        create_turnip_stack(stalk_week_id=stalk_week_id, sell_date=sell_date, sell_price=sell_price)


def create_stalk_week(current_date, buy_price):
    sunday = DateHelper.get_sunday(current_date)
    saturday = DateHelper.get_saturday(current_date)
    return StalkWeek.objects.create(sunday=sunday, saturday=saturday, buy_price=buy_price)


def create_day_price(stalk_week_id, current_date, sell_price_before_noon, sell_price_after_noon):
    return DayPrices.objects.create(
        stalk_week_id=stalk_week_id,
        current_date=current_date,
        first_sell_price=sell_price_before_noon,
        last_sell_price=sell_price_after_noon,
    )
