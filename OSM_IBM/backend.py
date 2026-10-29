from mongo_connection import ecommerce_db , product_db
from datetime import datetime ,timedelta ,timezone
from zoneinfo import ZoneInfo

def get_total_orders():
    return ecommerce_db.count_documents({})

def get_total_customers():
    total_customers = ecommerce_db.distinct("customer_id")

    unique_customer_count = len(total_customers)

    return unique_customer_count


def get_total_product():
    total_product=product_db.distinct('product_id')
    count=len(total_product)
    return count


def get_sales_summary():
    pipeline = [
        {
            "$project": {
                "product_id": 1,
                "unit_price": 1,
                "product_cost": 1,
                "gross_profit": {
                    "$subtract": [
                        "$unit_price",
                        "$product_cost"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_gross_profit": {
                    "$sum": "$gross_profit"
                }
            }
        }
    ]

    result = product_db.aggregate(pipeline)

    for document in result:
        return document["total_gross_profit"]

    return 0

def get_recent_order():
   
    result = ecommerce_db.find(
        {},
        {
            "_id": 0,
            "order_id": 1,
            "customer_id": 1,
            "order_status": 1,
            "payment_status": 1
        }
    ).sort("order_date", -1).limit(25)

    return list(result)


def get_data_filter(date_option):
    if date_option == "All Dates":
        return {}
    elif date_option == "Today":
        today= datetime.now().date()
        start_date=datetime.combine(today,datetime.min.time())
        end_date= start_date + timedelta(days=1)
        
    elif date_option == "Year 2025":
        start_date= datetime(2025,1,1, tzinfo=timezone.utc)
        end_date =datetime(2026,1,1,tzinfo=timezone.utc) 
        
    elif date_option == "Year 2024":
        start_date = datetime(2024,1,1,tzinfo=timezone.utc)
        end_date = datetime(2025,1,1, tzinfo=timezone.utc)
    elif date_option == "Year 2023":
        start_date=datetime(2023,1,1,tzinfo=timezone.utc)
        end_date=datetime(2024,1,1,tzinfo=timezone.utc)
    else :
        return{}
    return {
                "order_date":{
                    "$gte": start_date,
                    "$lt":end_date
                }
            }
def get_filtered_orders(date_query):
    result = ecommerce_db.find(
        date_query,
        {
            "_id": 0,
            "order_id": 1,
            "customer_id": 1,
            "order_date": 1,
            "order_status": 1,
            "payment_status": 1
        }
    ).sort("order_date", -1)

    return list(result)
def search_orders(search_text):
    query = {}

    if search_text:
        query["$or"] = [
            {"order_id": {"$regex": search_text, "$options": "i"}},
            {"customer_id": {"$regex": search_text, "$options": "i"}}
        ]

    result = ecommerce_db.find(
        query,
        {
            "_id": 0,
            "order_id": 1,
            "customer_id": 1,
            "order_date": 1,
            "order_status": 1,
            "payment_status": 1
        }
    ).sort("order_date", -1)

    return list(result)
 
