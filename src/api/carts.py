from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)


class NewCart(BaseModel):
    customer: str

cart_dictonary = {}
card_id = 0 

@router.post("/")
def create_cart(new_cart: NewCart):
    """ """

    global card_id
    card_id += 1
    cart_dictonary[card_id] = {}

    return {"cart_id": card_id}


@router.get("/{cart_id}")
def get_cart(cart_id: int):
    """ """

    global cart_dictonary
    cart = cart_dictonary[card_id]

    return cart


class CartItem(BaseModel):
    quantity: int


@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    """ """

    global cart_dictonary
    cart = cart_dictonary[card_id]
    cart[item_sku] = cart_item.quantity

    return "OK"


class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """ """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" SELECT num_red_potions,gold FROM global_inventory """))
        first_row = result.first()
        red_potion_quan = first_row.num_red_potions
        my_gold = first_row.gold

        red_going_to_buy = cart_dictonary[card_id]["RED_POTION_0"]
        total_price = red_buy * RED_PRICE

        if red_going_to_buy > red_potion_quan: 
            red_going_to_buy = 0
            total_price = 0
        else:
            new_red_potion_quan = red_potion_quan - red_going_to_buy
            new_gold = my_gold + total_price

            connection.execute(sqlalchemy.text(""" UPDATE global_inventory
            SET num_red_potions = '%s', gold = '%s' """ % (new_red_potion_quan, new_gold)))

    return {"total_potions_bought": red_going_to_buy, "total_gold_paid": total_price}
