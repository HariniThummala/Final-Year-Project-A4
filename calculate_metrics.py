import pandas as pd

# Load CSV file
df = pd.read_csv("evaluation_results.csv")

# Total number of queries
total_queries = len(df)

# Count correct answers (1's)
correct_answers = df["correct"].sum()

# Calculate accuracy
accuracy = (correct_answers / total_queries) * 100

print("Total Queries:", total_queries)
print("Correct Responses:", correct_answers)
print("Chatbot Accuracy:", round(accuracy, 2), "%")

# Response time metrics
avg_time = df["response_time"].mean()
max_time = df["response_time"].max()
min_time = df["response_time"].min()

print("Average Response Time:", round(avg_time, 3), "seconds")
print("Max Response Time:", round(max_time, 3), "seconds")
print("Min Response Time:", round(min_time, 3), "seconds")