from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/inventory")
def get_inventory():
    """ """
    # Assignement 2
    # with db.engine.begin() as connection:
    #     global_inventory = connection.execute(sqlalchemy.text(""" SELECT * FROM global_inventory """))
    # first_row = result.first()

    # total_potions = first_row.num_red_potions + first_row.num_green_potions + first_row.num_blue_potions
    # total_ml = first_row.num_red_ml + first_row.num_green_ml + first_row.num_blue_ml
    # my_gold = first_row.gold

    # return {"number_of_potions": total_potions, "ml_in_barrels": total_ml, "gold": my_gold}

    with db.engine.begin() as connection:
        global_inventory = connection.execute(sqlalchemy.text(""" SELECT * FROM global_inventory """))
        my_catalog = connection.execute(sqlalchemy.text(""" SELECT inventory FROM potions """))

    total_potions = 0
    for each_potion in my_catalog:
        total_potions += each_potion.inventory
        
    total_ml = global_inventory.num_red_ml + global_inventory.num_green_ml + global_inventory.num_blue_ml
    my_gold = global_inventory.gold

    return {"number_of_potions": total_potions, "ml_in_barrels": total_ml, "gold": my_gold}

class Result(BaseModel):
    gold_match: bool
    barrels_match: bool
    potions_match: bool

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return "OK"
