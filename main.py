

from typing import Optional, Any
from dataclasses import dataclass

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore

store = JsonStore('storage.json')
STORE_NAME = "values"

HEIGHT = 800
WIDTH = 1000


@dataclass
class StoreData:
    money: int
    energy: int
    happy: int
    food: int


class CatGame(Widget):
    pass


def create_store():
    store.put(STORE_NAME, money=0, energy=100, happy=100, food=100)


def storage_get(name: str) -> int:
    money_exist = store.exists(STORE_NAME)

    if not money_exist:
        create_store()

    return store.get(STORE_NAME)[name]


def storage_get_multi() -> StoreData:
    money_exist = store.exists(STORE_NAME)

    if not money_exist:
        create_store()

    data = store.get(STORE_NAME)
    return StoreData(**data)


def update_value(
        money: Optional[int] = None,
        energy: Optional[int] = None,
        happy: Optional[int] = None,
        food: Optional[int] = None
):
    money_exist = store.exists(STORE_NAME)

    if not money_exist:
        create_store()

    values = store.get(STORE_NAME)

    if money:
        values["money"] = money

    if energy:
        values["energy"] = energy

    if food:
        values["food"] = food

    if happy:
        values["happy"] = happy

    store.put(STORE_NAME, **values)


class CatIcon(Widget):
    money = ObjectProperty(storage_get("money"))
    energy = ObjectProperty(storage_get("energy"))
    happy = ObjectProperty(storage_get("happy"))
    food = ObjectProperty(storage_get("food"))

    def update(self):
        values = storage_get_multi()

        self.money = values.money
        self.energy = values.energy
        self.happy = values.happy
        self.food = values.food

    def add_money(self):
        values = storage_get_multi()

        update_value(
            money=values.money+1,
            happy=values.happy - 1,
            energy=values.energy - 1,
            food=values.food - 1,
        )

        self.update()

    def add_energy(self):
        values = storage_get_multi()

        if values.money <= 25:
            popup = Popup(
                title='Нет денег',
                content=Label(text="Для счастливого сна нужно минимум 26 монет"),
                size_hint=(None, None), size=(400, 400)
            )
            popup.open()
            return

        update_value(
            food=values.food - 10,
            money=values.money - 25,
            energy=100,
            happy=values.happy - 20
        )

        self.update()

    def add_eat(self):
        values = storage_get_multi()

        if values.money <= 10:
            popup = Popup(
                title='Нет денег',
                content=Label(text="Для покупки еды нужно минимум 11 монет"),
                size_hint=(None, None), size=(400, 400)
            )
            popup.open()
            return

        if values.food + 50 > 100:
            values.food = 100

        else:
            values.food += 50

        update_value(
            food=values.food,
            money=values.money-10
        )

        self.update()

    def add_happy(self):
        values = storage_get_multi()

        if values.happy + 20 > 100:
            values.happy = 100

        else:
            values.happy += 20

        update_value(
            happy=values.happy,
            food=values.food - 10,
            energy=values.energy - 10
        )

        self.update()


class CatApp(App):
    width: Any
    height: Any

    def build(self):
        self.width = Window.width
        self.height = Window.height

        self.title = "Raspy"

        return CatGame()


if __name__ == '__main__':
    Config.set('graphics', 'width', "800")
    Config.set('graphics', 'height', '1200')
    Config.write()

    CatApp().run()
