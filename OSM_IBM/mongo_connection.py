from pymongo import MongoClient 
mongo_url="mongodb+srv://srijitbhattacharjeegaddu_db_user:jkJXYNFJOrkrC0fU@cluster0.htdbxud.mongodb.net/"

client= MongoClient(mongo_url)

db=client["ecommerce_data"]
ecommerce_db=db["customer_order_collection"]
product_db=db["product_collection"]
print(client.admin.command("ping"))
 