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

    cost = 0
    red_ml = 0

    for barrel in barrels_delivered:
        cost += barrel.price
        red_ml += barrel.ml_per_barrel

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" SELECT gold, num_red_ml FROM global_inventory """))
        
        first_row = result.first()
        my_new_gold = first_row.gold - cost
        updated_red_ml = first_row.num_red_ml + red_ml

        connection.execute(sqlalchemy.text(""" UPDATE global_inventory 
        SET gold = '%s', num_red_ml = '%s' """ % (my_new_gold, updated_red_ml)))

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    """ """
    print(wholesale_catalog)

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(""" SELECT gold, num_red_potions FROM global_inventory """))
        first_row = result.first()
        red_potion_quan = first_row.num_red_potions
        my_gold = first_row.gold
        
        if red_potion_quan < 10 and my_gold > wholesale_catalog[0].price:
            # transverse 
            lets_buy = int(my_gold / wholesale_catalog[0].price)
            # Use all gold to buy?
            
    return [
        {
            "sku": "SMALL_RED_BARREL",
            "quantity": lets_buy,
        }
    ]
