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

    print(f"gold paid: {total_cost} red_ml: {red_ml} blue_ml: {blue_ml} green_ml: {green_ml} dark_ml: {dark_ml}")

    # with db.engine.begin() as connection:
    #     connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
    #     SET num_red_ml = num_red_ml + :red_ml, 
    #         num_green_ml = num_green_ml + :green_ml,
    #         num_blue_ml = num_blue_ml + :blue_ml,
    #         gold = gold - :total_cost """),
    #     [{"red_ml": red_ml, "green_ml": green_ml, "blue_ml": blue_ml, "dark_ml": dark_ml, "total_cost": total_cost}])

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(""" INSERT INTO gold_ledger (change_of_gold)
                                               VALUES (:gold_paid) """),
                                            [{"gold_paid": -total_cost}])

        connection.execute(sqlalchemy.text(""" INSERT INTO ml_ledger (red_ml_change, green_ml_change, blue_ml_change, dark_ml_change)
                                               VALUES (:red_ml, :green_ml, :blue_ml, :dark_ml) """),
                                            [{"red_ml": red_ml, "green_ml": green_ml, "blue_ml": blue_ml, "dark_ml": dark_ml}])

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
    
    # Assignment 3
    # with db.engine.begin() as connection:
    #     global_inventory = connection.execute(sqlalchemy.text(""" SELECT gold FROM global_inventory """))  
    # global_first_row = global_inventory.first()

    # my_gold = global_first_row.gold

    # Working
    # with db.engine.begin() as connection:
    #     gold = connection.execute(sqlalchemy.text(""" SELECT SUM(change_of_gold) 
    #                                                      FROM gold_ledger """)).scalar_one()  
            
    # my_gold = gold
    # my_plan = []
    # quantity = {}
    # iteration = 0

    # for barrel in wholesale_catalog:
    #     quantity[barrel.sku] = 0

    # while (my_gold > 0 and iteration < 10):
    #     iteration += 1
    #     for barrel in wholesale_catalog:
    #         if (my_gold >= barrel.price):
    #             if ('MINI' in barrel.sku):
    #                 quantity[barrel.sku] += 1
    #                 my_gold -= barrel.price
    #                 barrel.quantity -= 1

    # for barrel in wholesale_catalog:
    #     if (quantity[barrel.sku] != 0):
    #         my_plan.append (
    #             {
    #                 "sku": barrel.sku,
    #                 "quantity": quantity[barrel.sku]
    #             }
    #         )
    # print(f"my barrels plan: {my_plan}")
    # return my_plan

    # Logic 1
    # my_plan = []

    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT COALESCE(SUM(change_of_gold),0) FROM gold_ledger """))
    #     gold = result.scalar_one()

    # for barrel in wholesale_catalog:
    #     if gold >= barrel.price and barrel.ml_per_barrel <= 500:
    #         my_plan.append(
    #             {
    #             "sku": barrel.sku,
    #             "quantity": 1,
    #             })
    #         gold = gold - barrel.price

    # print(f"my barrels plan: {my_plan}")
    # return my_plan

    # Logic 2

    with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(""" SELECT SUM(red_ml_change) AS red_ml, 
                                                                  SUM(green_ml_change) AS green_ml, 
                                                                  SUM(blue_ml_change) AS blue_ml 
                                                            FROM ml_ledger """))
            first_row = result.first()

            red_ml = first_row.red_ml
            green_ml = first_row.green_ml
            blue_ml = first_row.blue_ml
            print("IN BARRELS PLAN, ml in inventory: red: ", red_ml, " green: ", green_ml, " blue: ", blue_ml)
    
            result = connection.execute(sqlalchemy.text(""" SELECT SUM(change_of_gold) AS gold
                                                            FROM gold_ledger """)) 
            
            first_row = result.first()
            my_gold = first_row.gold
            print("IN BARRELS PLAN, gold: ", my_gold)


            result = connection.execute(sqlalchemy.text(""" SELECT SUM(change_of_potion) AS total_potions
                                                            FROM potions_ledger """)) 
            
            first_row = result.first()
            total_potions = first_row.total_potions
            print("IN BARRELS PLAN, potions in inventory: ", total_potions) 

    barrels = [] # to return

    total_ml = red_ml + green_ml + blue_ml

    potential_potions = total_ml // 100
    total_potions += potential_potions

    potions_to_make = 300 - total_potions

    ml_to_buy = potions_to_make * 100

    # red_to_buy = ml_to_buy // 3 
    # green_to_buy = ml_to_buy // 3 
    # blue_to_buy = ml_to_buy // 3 

    red_to_buy = 1000
    green_to_buy = 1000
    blue_to_buy = 1000

    print("total_potions: ", total_potions, " potions to make: ", potions_to_make, " ml_to_buy: ", ml_to_buy, " ml_per_color: ", red_to_buy)

    if total_potions < 300:
        for barrel in wholesale_catalog:
            print(barrel)
            barrels_to_purchase = 0

            if barrel.potion_type == [1, 0, 0, 0]: # initial amount of ml less that 1000
                # buy if gold available and until I buy 1000 ml
                while red_to_buy > 0 and my_gold >= barrel.price and barrels_to_purchase < barrel.quantity:
                    barrels_to_purchase += 1
                    #red_ml += barrel.ml_per_barrel
                    my_gold -= barrel.price
                    red_to_buy -= barrel.ml_per_barrel

            elif barrel.potion_type == [0, 1, 0, 0]:
                # buy if gold available and until I buy 1000 ml
                while green_to_buy > 0 and my_gold >= barrel.price and barrels_to_purchase < barrel.quantity:
                    barrels_to_purchase += 1
                    #green_ml += barrel.ml_per_barrel
                    my_gold -= barrel.price
                    green_to_buy -= barrel.ml_per_barrel

            elif barrel.potion_type == [0, 0, 1, 0]:
                # buy if gold available and until I buy 1000 ml
                while blue_to_buy > 0 and my_gold >= barrel.price and barrels_to_purchase < barrel.quantity:
                    barrels_to_purchase += 1
                    #blue_ml += barrel.ml_per_barrel
                    my_gold -= barrel.price
                    blue_to_buy -= barrel.ml_per_barrel


            if barrels_to_purchase > 0:
                barrel = {
                    "sku": barrel.sku,
                    "quantity": barrels_to_purchase
                }

                barrels.append(barrel) 

    print("barrels planning to purchase: ")
    print(barrels)

    return barrels

    # return 
    #     {
    #         "sku": "SMALL_RED_BARREL",
    #         "quantity": lets_buy,
    #     }
    # ]
