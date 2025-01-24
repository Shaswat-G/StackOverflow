import pymongo
import json
from bson import json_util
from datetime import datetime


# Connect to the MongoDB cluster
myclient = pymongo.MongoClient("mongodb+srv://mzamponi:iM97jgMYeYgUQMVi@cluster0.q761myr.mongodb.net/?tls=true")
mydb = myclient["stack_overflow"]
mycol = mydb["google_match_datadump"]
print("Connected to the MongoDB cluster")

# Get a sample document from the collection
sample_document = mycol.find_one()
print(sample_document.keys())

# Get the number of documents in the collection
document_count = mycol.count_documents({})
print("Number of Documents:", document_count)

# Save the sample document to a JSON file
file_path = "sample_document.json"
with open(file_path, "w") as file:
    json.dump(sample_document, file, default=json_util.default, indent=4)

print(f"Sample document saved to {file_path}")