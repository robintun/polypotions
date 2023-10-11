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

    for potion in potions_delivered:
        red_potions += potion.quantity

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" SELECT num_red_ml, num_red_potions FROM global_inventory """))
        first_row = result.first()
        updated_red_potions = first_row.num_red_potions + red_potions
        updated_red_ml = first_row.num_red_ml - (red_potions * 100)

        connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        SET num_red_potions = '%s', num_red_ml = '%s' """ % (updated_red_potions, updated_red_ml)))

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

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" SELECT num_red_ml, 
        num_green_ml, num_blue_ml FROM global_inventory """))
        first_row = result.first()
        red_to_brew = int(first_row.num_red_ml / 100)
        green_to_brew = int(first_row.num_red_ml / 100)
        blue_to_brew = int(first_row.num_red_ml / 100)

        bottle_plan = []

    return [
            {
                "potion_type": [100, 0, 0, 0],
                "quantity": red_to_brew,
            }
        ]
