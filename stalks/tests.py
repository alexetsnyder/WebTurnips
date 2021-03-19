from django.test import TestCase
from django.utils import timezone
import factory


class StalkWeekModel(TestCase):
    def test_merge_turnips_no_stacks(self):
        stalk_week = factory.create_stalk_week(timezone.now(), 90)
        turnip_stacks = stalk_week.merge_turnips()
        self.assertEqual(turnip_stacks, [])

    def test_merge_turnips_one_stack(self):
        stalk_week = factory.create_stalk_week(timezone.now(), 90)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=0)
        turnip_stacks = stalk_week.merge_turnips()
        self.assertEqual(turnip_stacks, [(10, 0, 0)])

    def test_merge_turnips_many_stacks(self):
        stalk_week = factory.create_stalk_week(timezone.now(), 90)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=100)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=100)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=100)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=100)
        self.assertEqual(stalk_week.merge_turnips(), [(40, 100, 4000)])

    def test_merge_turnips_many_different_stacks(self):
        stalk_week = factory.create_stalk_week(timezone.now(), 90)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=100)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=100)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=120)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=120)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=0)
        factory.create_turnip_stack(stalk_week_id=stalk_week.id, sell_date=timezone.now(), sell_price=0)
        turnip_stacks = stalk_week.merge_turnips()
        self.assertIn((20, 100, 2000), turnip_stacks)
        self.assertIn((20, 120, 2400), turnip_stacks)
        self.assertIn((20, 0, 0), turnip_stacks)
        self.assertEqual(len(turnip_stacks), 3)
