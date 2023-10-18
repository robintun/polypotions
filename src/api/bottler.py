from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):
    """ """
    print(potions_delivered)

    # for potion in potions_delivered:
        # Assignment 1
        # if ((potion.potion_type)[0] == 100):
        #     with db.engine.begin() as connection:
        #         result = connection.execute(sqlalchemy.text(""" SELECT num_red_ml, num_red_potions FROM global_inventory """))
        #         first_row = result.first()
        #         updated_red_potions = first_row.num_red_potions + red_potions
        #         updated_red_ml = first_row.num_red_ml - (red_potions * 100)
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_red_potions = '%s', num_red_ml = '%s' """ % (updated_red_potions, updated_red_ml)))

        # Attempt 1 for Assignment 2
        # if ((potion.potion_type)[0] == 100):
        #     with db.engine.begin() as connection:
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_red_ml = num_red_ml - """ + str(potion.quantity * 100)))
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_red_potions = num_red_potions + """ + str(potion.quantity)))
        # elif ((potion.potion_type)[1] == 100):
        #     with db.engine.begin() as connection:
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_green_ml = num_green_ml - """ + str(potion.quantity * 100)))
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_green_potions = num_green_potions + """ + str(potion.quantity)))
        # elif ((potion.potion_type)[2] == 100):
        #     with db.engine.begin() as connection:
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_blue_ml = num_blue_ml - """ + str(potion.quantity * 100)))
        #         connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        #         SET num_blue_potions = num_blue_potions + """ + str(potion.quantity)))

        # Assignment 2
        # if (potion.potion_type == [100, 0, 0, 0]):
        #     with db.engine.begin() as connection:
        #         connection.execute(sqlalchemy.text(f""" UPDATE global_inventory 
        #         SET num_red_ml = num_red_ml - {potion.quantity * 100}""" ))
        #         connection.execute(sqlalchemy.text(f""" UPDATE global_inventory 
        #         SET num_red_potions = num_red_potions + {potion.quantity} """))
        
        # elif (potion.potion_type == [0, 100, 0, 0]):
        #     with db.engine.begin() as connection:
        #         connection.execute(sqlalchemy.text(f""" UPDATE global_inventory 
        #         SET num_green_ml = num_green_ml - {potion.quantity * 100} """))
        #         connection.execute(sqlalchemy.text(f""" UPDATE global_inventory 
        #         SET num_green_potions = num_green_potions + {potion.quantity} """))

        # elif (potion.potion_type == [0, 0, 100, 0]):
        #     with db.engine.begin() as connection:
        #         connection.execute(sqlalchemy.text(f""" UPDATE global_inventory 
        #         SET num_blue_ml = num_blue_ml - {potion.quantity * 100} """))
        #         connection.execute(sqlalchemy.text(f""" UPDATE global_inventory 
        #         SET num_blue_potions = num_blue_potions + {potion.quantity} """ ))
    with db.engine.begin() as connection:
        print(potions_delivered)

        additional_potions = sum(potion.quantity for potion in potions_delivered)
        red_ml = sum(potion.quantity * potion.potion_type[0] for potion in potions_delivered)
        green_ml = sum(potion.quantity * potion.potion_type[1] for potion in potions_delivered)
        blue_ml = sum(potion.quantity * potion.potion_type[2] for potion in potions_delivered)
        dark_ml = sum(potion.quantity * potion.potion_type[3] for potion in potions_delivered)

        for potion_delivered in potions_delivered:
            connection.execute(sqlalchemy.text(""" UPDATE potions 
                                                   SET inventory = inventory + :additional_potions
                                                   WHERE type = :potion_type """),
                                            [{"additional_potions": potion_delivered.quantity,
                                            "potion_type": potion_delivered.potion_type}])
            
            connection.execute(sqlalchemy.text(""" UPDATE global_inventory SET
                                                   red_ml = red_ml - :red_ml,
                                                   green_ml = green_ml - :green_ml,
                                                   blue_ml = blue_ml - :blue_ml,
                                                   dark_ml = dark_ml - :dark_ml """),
                            [{"red_ml": red_ml, "green_ml": green_ml, "blue_ml": blue_ml, "dark_ml": dark_ml}])

    return "OK"

# Gets called 4 times a day
@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    # Initial logic: bottle all barrels into red potions.

    # Assignment 2
    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT num_red_ml, 
    #     num_green_ml, num_blue_ml FROM global_inventory """))
    # first_row = result.first()
    # red_to_brew = int(first_row.num_red_ml / 100)
    # green_to_brew = int(first_row.num_red_ml / 100)
    # blue_to_brew = int(first_row.num_red_ml / 100)

    # bottle_plan = []
    # if (red_to_brew > 0):
    #     bottle_plan.append(
    #         {
    #             "potion_type": [100, 0, 0, 0],
    #             "quantity": red_to_brew,
    #         }
    #     )
    # if (green_to_brew > 0):    
    #     bottle_plan.append(
    #         {
    #             "potion_type": [0, 100, 0, 0],
    #             "quantity": green_to_brew,
    #         }
    #     )
    # if (blue_to_brew > 0):    
    #     bottle_plan.append(
    #         {
    #             "potion_type": [0, 0, 100, 0],
    #             "quantity": blue_to_brew,
    #         }
    #     )
    # return bottle_plan

    with db.engine.begin() as connection:
        global_inventory = connection.execute(sqlalchemy.text(""" SELECT num_red_ml, 
        num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory """))
        my_potion = connection.execute(sqlalchemy.text(""" SELECT * FROM potions """))
    
    global_first_row = global_inventory.first()
    
    my_plan = []
    inventory = 0

    red_ml = global_first_row.num_red_ml
    green_ml = global_first_row.num_green_ml
    blue_ml = global_first_row.num_blue_ml
    dark_ml = global_first_row.num_dark_ml

    for potion in my_potion:
        if (potion.potion_type[0] <= red_ml and potion.potion_type[1] <= green_ml and potion.potion_type[2] <= blue_ml and potion.potion_type[3] <= dark_ml):
            my_plan.append(
                {
                    "potion_type": potion.potion_type,
                    "quantity": 1,
                }
            )
            red_ml -= potion.potion_type[0]
            green_ml -= potion.potion_type[1]
            blue_ml -= potion.potion_type[2]
            dark_ml -= potion.potion_type[3]
    return my_plan
