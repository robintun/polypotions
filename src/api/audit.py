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

    # with db.engine.begin() as connection:
    #     global_inventory = connection.execute(sqlalchemy.text(""" SELECT * FROM global_inventory """))
    #     my_catalog = connection.execute(sqlalchemy.text(""" SELECT inventory FROM potions """))

    # global_first_row = global_inventory.first()
    # total_potions = 0
    # for each_potion in my_catalog:
    #     total_potions += each_potion.inventory

    # total_ml = global_first_row.num_red_ml + global_first_row.num_green_ml + global_first_row.num_blue_ml
    # my_gold = global_first_row.gold

    # return {"number_of_potions": total_potions, "ml_in_barrels": total_ml, "gold": my_gold}

    with db.engine.begin() as connection:
        my_gold = connection.execute(sqlalchemy.text(""" SELECT SUM(change_of_gold)
                                                         FROM gold_ledger """)).scalar_one()
        my_red_ml = connection.execute(sqlalchemy.text(""" SELECT SUM(red_ml_change)
                                                         FROM ml_ledger """)).scalar_one()
        my_green_ml = connection.execute(sqlalchemy.text(""" SELECT SUM(green_ml_change)
                                                         FROM ml_ledger """)).scalar_one()
        my_blue_ml = connection.execute(sqlalchemy.text(""" SELECT SUM(blue_ml_change)
                                                         FROM ml_ledger """)).scalar_one() 
        my_dark_ml = connection.execute(sqlalchemy.text(""" SELECT SUM(dark_ml_change)
                                                         FROM ml_ledger """)).scalar_one()
        total_potions = connection.execute(sqlalchemy.text(""" SELECT SUM(change_of_potion) 
                                                               FROM potions_ledger """)).scalar_one()

    total_ml = my_red_ml + my_green_ml + my_blue_ml + my_dark_ml
    
    print(f"audit_gold: {my_gold}, audit_potions: {total_potions}, audit_ml: {total_ml}")

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
