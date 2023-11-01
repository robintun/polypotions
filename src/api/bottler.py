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
    print(f"potions_delivered: {potions_delivered}")

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
        # print(f"potions_delivered: {potions_delivered}")

        additional_potions = sum(potion.quantity for potion in potions_delivered)
        red_ml = sum(potion.quantity * potion.potion_type[0] for potion in potions_delivered)
        green_ml = sum(potion.quantity * potion.potion_type[1] for potion in potions_delivered)
        blue_ml = sum(potion.quantity * potion.potion_type[2] for potion in potions_delivered)
        dark_ml = sum(potion.quantity * potion.potion_type[3] for potion in potions_delivered)

        for potion_delivered in potions_delivered:
            # connection.execute(sqlalchemy.text(""" UPDATE potions 
            #                                        SET inventory = inventory + :additional_potions
            #                                        WHERE potion_type = :potion_type """),
            #                                 [{"additional_potions": potion_delivered.quantity,
            #                                 "potion_type": potion_delivered.potion_type}])
            
            # connection.execute(sqlalchemy.text(""" UPDATE global_inventory SET
            #                                        num_red_ml = num_red_ml - :red_ml,
            #                                        num_green_ml = num_green_ml - :green_ml,
            #                                        num_blue_ml = num_blue_ml - :blue_ml,
            #                                        num_dark_ml = num_dark_ml - :dark_ml """),
            #                 [{"red_ml": red_ml, "green_ml": green_ml, "blue_ml": blue_ml, "dark_ml": dark_ml}])
            connection.execute(sqlalchemy.text(""" INSERT INTO potions_ledger (change_of_potion, potion_id)
                                                   SELECT :change_of_potion, potions.id
                                                   FROM potions
                                                   WHERE potions.potion_type = :potion_type """),
                                            [{"change_of_potion": potion_delivered.quantity, "potion_type": potion_delivered.potion_type}])
            
        connection.execute(sqlalchemy.text(""" INSERT INTO ml_ledger (red_ml_change, green_ml_change, blue_ml_change, dark_ml_change)
                                               VALUES (:red_ml, :green_ml, :blue_ml, :dark_ml) """),
                                            [{"red_ml": -red_ml, "green_ml": -green_ml, "blue_ml": -blue_ml, "dark_ml": -dark_ml}])
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

    # Assignment 3
    # with db.engine.begin() as connection:
    #     global_inventory = connection.execute(sqlalchemy.text(""" SELECT num_red_ml, 
    #     num_green_ml, num_blue_ml, num_dark_ml FROM global_inventory """))
    #     my_potion = connection.execute(sqlalchemy.text(""" SELECT * FROM potions """))
    
    # global_first_row = global_inventory.first()
    
    # my_plan = []
    # inventory = 0

    # red_ml = global_first_row.num_red_ml
    # green_ml = global_first_row.num_green_ml
    # blue_ml = global_first_row.num_blue_ml
    # dark_ml = global_first_row.num_dark_ml

    # for potion in my_potion:
    #     if (potion.potion_type[0] <= red_ml and potion.potion_type[1] <= green_ml and potion.potion_type[2] <= blue_ml and potion.potion_type[3] <= dark_ml):
    #         my_plan.append(
    #             {
    #                 "potion_type": potion.potion_type,
    #                 "quantity": 1,
    #             }
    #         )
    #         red_ml -= potion.potion_type[0]
    #         green_ml -= potion.potion_type[1]
    #         blue_ml -= potion.potion_type[2]
    #         dark_ml -= potion.potion_type[3]
    # print(f"my bottler plan: {my_plan}")
    # return my_plan

    # Assignment 5
    # my_plan = []

    # with db.engine.begin() as connection:
    #     result = connection.execute(sqlalchemy.text(""" SELECT SUM(red_ml_change) AS red_ml, 
    #                                                            SUM(green_ml_change) AS green_ml, 
    #                                                            SUM(blue_ml_change) AS blue_ml, 
    #                                                            SUM(dark_ml_change) AS dark_ml 
    #                                                            FROM ml_ledger """)).first()
    #     red_ml = result.red_ml
    #     green_ml = result.green_ml
    #     blue_ml = result.blue_ml
    #     dark_ml = result.dark_ml

    #     my_potions = connection.execute(sqlalchemy.text(""" SELECT * FROM potions """))

    # for each_potion in my_potions:
    #     if (each_potion.potion_type[0] <= red_ml and each_potion.potion_type[1] <= green_ml and each_potion.potion_type[2] <= blue_ml and each_potion.potion_type[3] <= dark_ml):
    #         my_plan.append(
    #             {
    #                 "potion_type": each_potion.potion_type,
    #                 "quantity": 1,
    #             }
    #         )
    #         red_ml -= each_potion.potion_type[0]
    #         green_ml -= each_potion.potion_type[1]
    #         blue_ml -= each_potion.potion_type[2]
    #         dark_ml -= each_potion.potion_type[3]
    # print(f"my bottler plan: {my_plan}")
    # return my_plan

    # Logic 2

    bottles = []

    with db.engine.begin() as connection:
            
            # get potions' quantities and types
            result = connection.execute(sqlalchemy.text(""" SELECT potions.potion_type, SUM(potions_ledger.change_of_potion) AS quantity
                                                            FROM potions
                                                            JOIN potions_ledger ON potions.id = potions_ledger.potion_id
                                                            GROUP BY potions.potion_type """))       
            
            potions = result.fetchall()
            potion_types = len(potions)

            result = connection.execute(sqlalchemy.text(""" SELECT SUM(change_of_potion) AS total_potions FROM potions_ledger """))
            first_row = result.first()
            total_potions = first_row.total_potions

            print("potion types: ", potion_types)
            
            # get available ml
            ml = connection.execute(sqlalchemy.text(""" SELECT SUM(red_ml_change) AS red_ml, 
                                                               SUM(green_ml_change) AS green_ml, 
                                                               SUM(blue_ml_change) AS blue_ml, 
                                                               SUM(dark_ml_change) AS dark_ml
                                                        FROM ml_ledger """))
            
            ml = ml.first()
            red_ml = ml.red_ml
            green_ml = ml.green_ml
            blue_ml = ml.blue_ml
            dark_ml = ml.dark_ml

            print("in bottler, available mL: red: ", red_ml, " green: ", green_ml, " blue: ", blue_ml, " dark: ", dark_ml)
            total_ml = red_ml + green_ml + blue_ml + dark_ml
            max_bottles = (total_ml) // 100
            
            bottles_per_type = max_bottles//potion_types

            if bottles_per_type == 0 and max_bottles > 0:
                bottles_per_type = max_bottles
            elif red_ml > 0 and green_ml == 0 and blue_ml == 0:
                bottles_per_type = max_bottles
            elif green_ml > 0 and red_ml == 0 and blue_ml == 0:
                bottles_per_type = max_bottles
            elif blue_ml > 0 and green_ml == 0 and red_ml == 0:
                bottles_per_type = max_bottles  

            print("max bottles: ", max_bottles," bottles per type: ", bottles_per_type)
            
            for potion in potions:
                print(potion)
                bottled = 0

                
                while (total_potions < 300 and bottled < bottles_per_type and potion.potion_type[0] <= red_ml and potion.potion_type[1] <= green_ml and potion.potion_type[2] <= blue_ml and potion.potion_type[3] <= dark_ml):
                    
                    red_ml -= potion.potion_type[0]
                    green_ml -= potion.potion_type[1]
                    blue_ml -= potion.potion_type[2]
                    dark_ml -= potion.potion_type[3]
                    bottled += 1

                    total_potions += 1
                
                if bottled > 0:
                    bottle = {
                        "potion_type": potion.potion_type,
                        "quantity": bottled
                    }

                    bottles.append(bottle)                
            
    print(f"my bottler plan: {bottles}")

    return bottles
