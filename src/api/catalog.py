from fastapi import APIRouter

import sqlalchemy
from src import database as db

router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """
    # Assignment 2
    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT num_red_potions,
    #     num_green_potions, num_blue_potions FROM global_inventory """))
    # first_row = result.first()

    # # Can return a max of 20 items.

    # my_catalog = []
    # if (first_row.num_red_potions > 0):
    #     my_catalog.append(
    #         {
    #             "sku": "RED_POTION_0",
    #             "name": "red potion",
    #             "quantity": first_row.num_red_potions,
    #             "price": 50,
    #             "potion_type": [100, 0, 0, 0],
    #         }
    #     )
    # if (first_row.num_green_potions > 0):
    #     my_catalog.append(
    #         {
    #             "sku": "GREEN_POTION_0",
    #             "name": "green potion",
    #             "quantity": first_row.num_green_potions,
    #             "price": 50,
    #             "potion_type": [0, 100, 0, 0],
    #         }
    #     )
    # if (first_row.num_blue_potions > 0):
    #     my_catalog.append(
    #         {
    #             "sku": "BLUE_POTION_0",
    #             "name": "blue potion",
    #             "quantity": first_row.num_blue_potions,
    #             "price": 50,
    #             "potion_type": [0, 0, 100, 0],
    #         }
    #     )
    # return my_catalog

    my_catalog = []

    with db.engine.begin() as connection:
        # result = connection.execute(sqlalchemy.text(""" SELECT sku,
        # price,inventory,potion_type FROM potions """))
        result = connection.execute(sqlalchemy.text(""" SELECT sku,
                                                        SUM(potions_ledger.change_of_potion) AS inventory, price, potion_type 
                                                        FROM potions
                                                        JOIN potions_ledger ON potions_ledger.potion_id = potions.id
                                                        GROUP BY potions.id """))

    for each_potion in result:
        if (each_potion.inventory > 0):
            my_catalog.append(
                {
                    "sku": each_potion.sku,
                    "name": each_potion.sku,
                    "quantity": each_potion.inventory,
                    "price": each_potion.price,
                    "potion_type": each_potion.potion_type,
                }
            )
    print(f"my catalog: {my_catalog}")
    return my_catalog
