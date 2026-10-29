from pathlib import Path
import pandas as pd

raw_folder=Path("data/raw")
procssed_folder=Path("data/processed_data")

procssed_folder.mkdir(parents=True,exist_ok=True)




selected_columns = {
    "order_items.csv": [
        "order_id",
        "product_id",
        "quantity",
        "unit_price"
        ],   
    "customer_master.csv": [
         "customer_id",
         "customer_name",
         "gender",
         "customer_city",
         "customer_state",
         
        ],
     "ecommerce_sales.csv":[
          "shipping_method",
          "warehouse",
          "delivery_days",
          "estimated_delivery_days",
          "delivery_status",
          "customer_rating",
          "review_sentiment"

         
     ],
    "product_catalog.csv" : [
    
               "brand",
               "supplier",
               "unit_price",
               "product_cost",
               "product_rating"
]

    
}



csv_files=list(raw_folder.glob("*.csv"))


for file in csv_files:
    if file.name in selected_columns:
        columns=selected_columns[file.name]
        df=pd.read_csv(file,usecols=columns)
        output_folder=procssed_folder/file.name
        df.to_csv(output_folder,index=False)
