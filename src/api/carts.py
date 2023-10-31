from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from enum import Enum



router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

class search_sort_options(str, Enum):
    customer_name = "customer_name"
    item_sku = "item_sku"
    line_item_total = "line_item_total"
    timestamp = "timestamp"

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"   

@router.get("/search/", tags=["search"])
def search_orders(
    customer_name: str = "",
    potion_sku: str = "",
    search_page: str = "",
    sort_col: search_sort_options = search_sort_options.timestamp,
    sort_order: search_sort_order = search_sort_order.desc,
):
    """
    Search for cart line items by customer name and/or potion sku.

    Customer name and potion sku filter to orders that contain the 
    string (case insensitive). If the filters aren't provided, no
    filtering occurs on the respective search term.

    Search page is a cursor for pagination. The response to this
    search endpoint will return previous or next if there is a
    previous or next page of results available. The token passed
    in that search response can be passed in the next search request
    as search page to get that page of results.

    Sort col is which column to sort by and sort order is the direction
    of the search. They default to searching by timestamp of the order
    in descending order.

    The response itself contains a previous and next page token (if
    such pages exist) and the results as an array of line items. Each
    line item contains the line item id (must be unique), item sku, 
    customer name, line item total (in gold), and timestamp of the order.
    Your results must be paginated, the max results you can return at any
    time is 5 total line items.
    """

    # if search_page == "":
    #     search_page = 0
    # else:
    #     search_page = int(search_page)

    # if sort_order is search_sort_order.desc:
    #     if sort_col is search_sort_options.customer_name:
    #         order_by = sqlalchemy.desc(db.carts.c.customer)

    #     elif sort_col is search_sort_options.item_sku:
    #         order_by = sqlalchemy.desc(db.potions.c.sku)

    #     elif sort_col is search_sort_options.line_item_total:
    #         order_by = sqlalchemy.desc(db.cart_items.c.quantity)

    #     elif sort_col is search_sort_options.timestamp:
    #         order_by = sqlalchemy.desc(db.cart_items.c.created_at)

    # elif sort_order is search_sort_order.asc:
    #     if sort_col is search_sort_options.customer_name:
    #         order_by = sqlalchemy.asc(db.carts.c.customer)

    #     elif sort_col is search_sort_options.item_sku:
    #         order_by = sqlalchemy.asc(db.potions.c.sku)

    #     elif sort_col is search_sort_options.line_item_total:
    #         order_by = sqlalchemy.asc(db.cart_items.c.quantity)

    #     elif sort_col is search_sort_options.timestamp:
    #         order_by = sqlalchemy.asc(db.cart_items.c.created_at)

    # else:
    #     assert False

    # stmt = (sqlalchemy.select(db.carts.c.customer,
    #                           db.cart_items.c.id,
    #                           db.potions.c.sku,
    #                           (db.cart_items.c.quantity * db.potions.c.price).label("total_gold_paid"),
    #                           db.cart_items.c.created_at)
    #                         .join(db.carts, db.carts.c.cart_id == db.cart_items.c.cart_id)
    #                         .join(db.potions, db.potions.c.id == db.cart_items.c.potion_id)
    #                         .offset(search_page)
    #                         .limit(5)
    #                         .order_by(order_by, db.cart_items.c.id))

    # if customer_name != "":
    #     stmt = stmt.where(db.carts.c.customer.ilike(f"%{customer_name}%"))

    # if potion_sku != "":
    #     stmt = stmt.where(db.potions.c.sku.ilike(f"%{sku}%"))

    # with db.engine.connect() as conn:

    #     result = conn.execute(stmt)

    #     json = []
    #     for each_row in result:
    #         json.append(
    #             {
    #                 "line_item_id": each_row.id,
    #                 "item_sku": each_row.sku,
    #                 "customer_name": each_row.customer,
    #                 "line_item_total": each_row.total,
    #                 "timestamp": each_row.created_at,
    #             }
    #         )

    # prev = ""
    # next = ""

    # if search_page-5 >= 0:
    #     prev = str(search_page-5)

    # if search_page+5 < count:
    #     next = str(search_page+5)

    # return {"previous": prev, "next": next, "results": json}

    limit = 5
    if search_page == "":
        offset = 0
    else:
        offset = int(search_page)

    with db.engine.connect() as connection:

        if sort_order is search_sort_order.desc:
            order = "DESC"
        else:
            order = "ASC"

        if sort_col is search_sort_options.customer_name:
            order_by = "carts.customer_name"
        elif sort_col is search_sort_options.item_sku:
            order_by = "potions.sku"
        elif sort_col is search_sort_options.timestamp:
            order_by = "cart_items.created_at"
        elif sort_col is search_sort_options.line_item_total:
            order_by = "potions.price * cart_items.quantity"
        else:
            assert False

        result = connection.execute(
            sqlalchemy.text(
                f"""
                SELECT carts.cart_id AS cart_id, carts.customer_name AS name, cart_items.created_at AS time, 
                    cart_items.potion_id AS item_id, cart_items.quantity AS quantity,
                    potions.sku AS sku, potions.price AS price
                FROM carts
                JOIN cart_items ON cart_items.cart_id = carts.cart_id
                JOIN potions ON potions.id = cart_items.potion_id
                WHERE carts.customer_name ILIKE :name
                AND potions.sku ILIKE :sku
                ORDER BY {order_by} {order}
                LIMIT :limit OFFSET :offset
                """
            ),({'name':f"%{customer_name}%", 'limit':limit, 'offset':offset,'sku':f"%{potion_sku}%"})).all()

        results = []
        global line_id
        for row in result:
            line_id += 1
            results.append({
                    "line_item_id": line_id,
                    "item_sku": f"{row.quantity} {row.sku} POTION",
                    "customer_name": row.name,
                    "line_item_total": row.quantity*row.price,
                    "timestamp": row.time,
                }) 
    
    if offset == 0:
        prev = ""
    else:
        prev = str(offset - 5)
    
    if results == [] or len(results) < 5:
        next = ""
    else:
        next = str(offset + 5)

    json = {"previous": prev, "next": next,"results": results}

    return json
    # return {
    #     "previous": "",
    #     "next": "",
    #     "results": [
    #         {
    #             "line_item_id": 1,
    #             "item_sku": "1 oblivion potion",
    #             "customer_name": "Scaramouche",
    #             "line_item_total": 50,
    #             "timestamp": "2021-01-01T00:00:00Z",
    #         }
    #     ],
    # }

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

    # Assignment 3
    # total_potions_bought = 0
    # total_gold_paid = 0

    # with db.engine.begin() as connection:
    #     connection.execute(sqlalchemy.text(""" UPDATE potions
    #                                            SET inventory = potions.inventory - cart_items.quantity
    #                                            FROM cart_items
    #                                            WHERE potions.id = cart_items.potion_id and cart_items.cart_id = :cart_id """),
    #                                         [{"cart_id": cart_id}])
    #     total_potions_bought = connection.execute(sqlalchemy.text(""" SELECT SUM(quantity) AS total_potions_bought
    #                                                                   FROM cart_items
    #                                                                   JOIN potions ON potions.id = cart_items.potion_id
    #                                                                   WHERE cart_id = :cart_id """),
    #                                                             [{"cart_id": cart_id}]).scalar_one()
    #     total_gold_paid = connection.execute(sqlalchemy.text(""" SELECT SUM(quantity * price) AS total_gold_paid
    #                                                                   FROM cart_items
    #                                                                   JOIN potions ON potions.id = cart_items.potion_id
    #                                                                   WHERE cart_id = :cart_id """),
    #                                                             [{"cart_id": cart_id}]).scalar_one()
    #     connection.execute(sqlalchemy.text(""" UPDATE global_inventory
    #                                            SET gold = gold + :gold_paid """),
    #                                         [{"gold_paid": total_gold_paid}])

    with db.engine.begin() as connection:
        total_potions_bought = connection.execute(sqlalchemy.text(""" SELECT SUM(quantity) AS total_potions_bought
                                                                      FROM cart_items
                                                                      JOIN potions ON potions.id = cart_items.potion_id
                                                                      WHERE cart_id = :cart_id """),
                                                                [{"cart_id": cart_id}]).scalar_one()
        
        total_gold_paid = connection.execute(sqlalchemy.text(""" SELECT SUM(cart_items.quantity * potions.price) AS total_gold_paid
                                                                 FROM cart_items
                                                                 JOIN potions ON potions.id = cart_items.potion_id
                                                                 WHERE cart_id = :cart_id """),
                                                                [{"cart_id": cart_id}]).scalar_one()
        
        connection.execute(sqlalchemy.text(""" INSERT INTO gold_ledger (change_of_gold)
                                               VALUES (:total_gold) """),
                                        [{"total_gold": total_gold_paid}])

        connection.execute(sqlalchemy.text(""" INSERT INTO potions_ledger (potion_id, change_of_potion)
                                               SELECT cart_items.potion_id, (cart_items.quantity * -1)
                                               FROM cart_items
                                               WHERE cart_id = :cart_id """),
                                        [{"cart_id": cart_id}])

    return {"total_potions_bought": total_potions_bought, "total_gold_paid": total_gold_paid}
