import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load the CSV file
df = pd.read_csv('data.csv')

# Display the first few rows of the dataframe
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# MongoDB Schema + Load
uri = "mongodb+srv://manish:lemoncherrygelato@v0.b0xcqmc.mongodb.net/?retryWrites=true&w=majority&appName=v0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['v0']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

collection = db['company_profiles']

# Process each row in the dataframe and insert into MongoDB
for index, row in df[df['Batch'] == 'W24'].iterrows():
    company_profile = {
        "company_name": row['Company'],
        "website": row['Website'],
        "description": row['One line'],
        "size": row['Size'],
        "sector": row['Sector'],
        "status": row['Status'],
        "phase": row['Phase']
    }
    collection.insert_one(company_profile)

print("Data inserted successfully into MongoDB")

