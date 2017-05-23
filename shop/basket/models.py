from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.partner.strategy import Selector


class Basket(AbstractBasket):
    _strategy = Selector().strategy()

from oscar.apps.basket.models import *  # noqa
