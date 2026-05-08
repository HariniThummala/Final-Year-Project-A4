import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("evaluation_results.csv")

plt.plot(df["response_time"])
plt.title("Chatbot Response Time")
plt.xlabel("Query Number")
plt.ylabel("Response Time (seconds)")
plt.show()