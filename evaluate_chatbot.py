import requests
import time
import pandas as pd

API_URL = "http://127.0.0.1:5000/ask"

data = pd.read_csv("test_queries.csv")

total = len(data)
correct = 0
times = []

for i,row in data.iterrows():

    query = row["query"]
    expected = row["expected"]

    start = time.time()

    r = requests.post(API_URL,json={"question":query})
    answer = r.json()["answer"].lower()

    end = time.time()

    response_time = end-start
    times.append(response_time)

    if expected in answer:
        correct += 1
    if "sorry" not in answer:
    answered += 1

coverage = answered/total

accuracy = correct/total
avg_time = sum(times)/len(times)

print("Total Queries:",total)
print("Correct:",correct)
print("Accuracy:",accuracy)
print("Query Coverage:",coverage)

print("Average Response Time:",avg_time)