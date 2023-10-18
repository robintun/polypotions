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
    # Assignment 1 and 2
    # global card_id
    # card_id += 1
    # cart_dictonary[card_id] = {}

    with db.engine.begin() as connection:
        cart_id = connection.execute(sqlalchemy.text("""INSERT INTO carts (customer_name)
                                                        VALUES (:customer_name)
                                                        RETURNING cart_id"""),
                                        [{"customer_name": new_cart.customer}]).scalar_one()

    return {"cart_id": cart_id}


@router.get("/{cart_id}")
def get_cart(cart_id: int):
    """ """
    # Assignment 1 and 2
    # global cart_dictonary
    # cart = cart_dictonary[card_id]

    with db.engine.begin() as connection:
        cart = connection.execute(sqlalchemy.text(""" SELECT cart_id, potion_id, quantity FROM cart_items
                                                      WHERE cart_id = :cart_id """),
                                                [{"cart_id": card_id}])

    return cart


class CartItem(BaseModel):
    quantity: int


@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    """ """
    # Assignment 1 and 2
    # global cart_dictonary
    # cart = cart_dictonary[card_id]
    # cart[item_sku] = cart_item.quantity

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(""" INSERT INTO cart_items (cart_id, potion_id, quantity)
                                               SELECT :cart_id, potions.id, :quantity
                                               FROM potions WHERE potions.sku = :item_sku """),
                                    [{"cart_id": cart_id, "quantity": cart_item.quantity, "item_sku": item_sku}])
    
    return "OK"


class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """ """

    # Assignment 1
    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT num_red_potions,gold FROM global_inventory """))
    #     first_row = result.first()
    #     red_potion_quan = first_row.num_red_potions
    #     my_gold = first_row.gold

    #     red_going_to_buy = cart_dictonary[card_id]["RED_POTION_0"]
    #     total_price = red_buy * RED_PRICE

    #     if red_going_to_buy > red_potion_quan: 
    #         red_going_to_buy = 0
    #         total_price = 0
    #     else:
    #         new_red_potion_quan = red_potion_quan - red_going_to_buy
    #         new_gold = my_gold + total_price

    #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory
    #         SET num_red_potions = '%s', gold = '%s' """ % (new_red_potion_quan, new_gold)))

    # Assignment 2
    # global cart_dictonary
    # cart = cart_dictonary[card_id]
    # red_potions_buying = 0
    # green_potions_buying = 0
    # blue_potions_buying = 0

    # for item_sku in cart:
    #     if (item_sku == "RED_POTION_0"):
    #         red_potions_buying += cart[item_sku]
    #         with db.engine.begin() as connection:
    #             connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #             SET num_red_potions = num_red_potions - """ + str(red_potions_buying)))
    #             connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #             SET gold = gold + """ + str(red_potions_buying * 50))) 
    #     elif (item_sku == "GREEN_POTION_0"):
    #         green_potions_buying += cart[item_sku]
    #         with db.engine.begin() as connection:
    #             connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #             SET num_green_potions = num_green_potions - """ + str(green_potions_buying)))
    #             connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #             SET gold = gold + """ + str(green_potions_buying * 50)))    
    #     elif (item_sku == "BLUE_POTION_0"):
    #         blue_potions_buying += cart[item_sku]
    #         with db.engine.begin() as connection:
    #             connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #             SET num_blue_potions = num_blue_potions - """ + str(blue_potions_buying)))
    #             connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #             SET gold = gold + """ + str(blue_potions_buying * 50)))
    # total_potions_bought = red_potions_buying + green_potions_buying + blue_potions_buying

    total_potions_bought = 0
    total_gold_paid = 0

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(""" UPDATE potions
                                               SET inventory = potions.inventory - cart_items.quantity
                                               FROM cart_items
                                               WHERE potions.id = cart_items.potion_id and cart_items.cart_id = :cart_id """),
                                            [{"cart_id": card_id}])
        total_potions_bought = connection.execute(sqlalchemy.text(""" SELECT SUM(quantity) AS total_potions_bought
                                                                      FROM cart_items
                                                                      JOIN potions ON potions.id = cart_items.potion_id
                                                                      WHERE cart_id = :cart_id """),
                                                                [{"cart_id": card_id}]).scalar_one()
        total_gold_paid = connection.execute(sqlalchemy.text(""" SELECT SUM(quantity * price) AS total_gold_paid
                                                                      FROM cart_items
                                                                      JOIN potions ON potions.id = cart_items.potion_id
                                                                      WHERE cart_id = :cart_id """),
                                                                [{"cart_id": card_id}]).scalar_one()
        connection.execute(sqlalchemy.text(""" UPDATE global_inventory
                                               SET gold = gold + :gold_paid """),
                                            [{"gold_paid": total_gold_paid}])

    return {"total_potions_bought": total_potions_bought, "total_gold_paid": total_gold_paid}
