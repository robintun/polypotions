from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver")
def post_deliver_barrels(barrels_delivered: list[Barrel]):
    """ """
    print(barrels_delivered)

    total_cost = 0
    red_ml = 0
    green_ml = 0
    blue_ml = 0
    dark_ml = 0

    for barrel in barrels_delivered:
        total_cost += barrel.price * barrel.quantity
        if barrel.potion_type == [1, 0, 0, 0]:
            red_ml += barrel.ml_per_barrel * barrel.quantity
        elif barrel.potion_type == [0, 1, 0, 0]:
            green_ml += barrel.ml_per_barrel * barrel.quantity
        elif barrel.potion_type == [0, 0, 1, 0]:
            blue_ml += barrel.ml_per_barrel * barrel.quantity
        elif barrel.potion_type == [0, 0, 0, 1]:
            dark_ml += barrel.ml_per_barrel * barrel.quantity
        else:
            raise Exception("Invalid potion type")

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        SET num_red_ml = num_red_ml + :red_ml, 
            num_green_ml = num_green_ml + :green_ml,
            num_blue_ml = num_blue_ml + :blue_ml,
            gold = gold - :total_cost """),
        [{"red_ml": red_ml, "green_ml": green_ml, "blue_ml": blue_ml, "dark_ml": dark_ml, "total_cost": total_cost}])

        # Assignment 1
        # connection.execute(sqlalchemy.text(""" SELECT gold, num_red_ml FROM global_inventory """))
        # first_row = result.first()
        # my_new_gold = first_row.gold - cost
        # updated_red_ml = first_row.num_red_ml + red_ml

        # connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        # SET gold = '%s', num_red_ml = '%s' """ % (my_new_gold, updated_red_ml)))

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(f"barrel catalog: {wholesale_catalog}")

    # Assignment 1
    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT gold, num_red_potions FROM global_inventory """))
    #     first_row = result.first()
    #     red_potion_quan = first_row.num_red_potions
    #     my_gold = first_row.gold
        
    #     if red_potion_quan < 10 and my_gold > wholesale_catalog[0].price:
    #         lets_buy = int(my_gold / wholesale_catalog[0].price)

    # Attempt 1 for Assignment 2
    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT * FROM global_inventory """))
    # first_row = result.first()

    # red_potion = first_row.num_red_potions
    # red_ml = first_row.num_red_ml

    # green_potion = first_row.num_green_potions
    # green_ml = first_row.num_green_ml

    # blue_potion = first_row.num_blue_potions
    # blue_ml = first_row.num_blue_ml

    # my_gold = first_row.gold

    # for catalog in wholesale_catalog:

    # Assignment 2
    # plan = []
    # with db.engine.begin() as connection:
    #     for barrel in wholesale_catalog:
    #         result = connection.execute(sqlalchemy.text(""" SELECT gold FROM global_inventory """))
    #         first_row = result.first()
    #         my_gold = first_row.gold

    #         if my_gold >= barrel.price:
    #             plan.append(
    #                 {
    #                     "sku": barrel.sku,
    #                     "quantity": 1,
    #                 }
    #             )
    # return plan
    
    with db.engine.begin() as connection:
        global_inventory = connection.execute(sqlalchemy.text(""" SELECT gold FROM global_inventory """))  
    global_first_row = global_inventory.first()

    my_gold = global_first_row.gold
            
    my_plan = []
    quantity = {}
    counter = 0

    for barrel in wholesale_catalog:
        quantity[barrel.sku] = 0

    for barrel in wholesale_catalog:
        if (my_gold >= barrel.price):
            quantity[barrel.sku] += 1
            my_gold -= barrel.price
            barrel.quantity -= 1

    for barrel in wholesale_catalog:
        if ('MINI' in barrel.sku):
            if (quantity[barrel.sku] != 0):
                my_plan.append (
                    {
                        "sku": barrel.sku,
                        "quantity": quantity[barrel.sku]
                    }
                )
    print(f"my barrels plan: {my_plan}")
    return my_plan

    # return 
    #     {
    #         "sku": "SMALL_RED_BARREL",
    #         "quantity": lets_buy,
    #     }
    # ]
