from matplotlib import pyplot as plt
import numpy as np

IDEAS_LIST = [
    "'the farmer returning alone'",
    "'the setup in the classic version being different'",
    "'the farmer's presence prevents adverse interactions'",
    "'the puzzle is unsolvable'",
    "'I'm confused'",
    "'the wolf and cabbage start on the left'",
    "'the solution seems too simple'",
    "7 numbered steps to solve the puzzle"
]

# data = {
#     "0.7": [46, 18, 39, 14, 17, 37, 19, 44],
#     "0.9": [49, 5, 45, 3, 5, 41, 13, 39],
#     "1.1": [46, 17, 48, 7, 13, 49, 29, 35],
#     "1.2": [43, 30, 45, 17, 27, 34, 31, 25],
#     "1.5": [43, 32, 45, 21, 29, 46, 38, 30],
# }

data = {
    "0.7": [39, 4, 10, 2, 9, 37, 3, 31],
    "0.9": [43, 4, 29, 7, 10, 38, 7, 26],
    "1.1": [36, 12, 31, 10, 22, 33, 16, 23],
    "1.2": [39, 20, 31, 3, 24, 32, 20, 14],
    "1.5": [27, 8, 22, 5, 15, 25, 16, 9],
}


IDEAS_LIST = [
    "'the farmer returning alone'",
    "'the setup in the classic version being different'",
    "'the farmer's presence prevents adverse interactions'",
    "'the puzzle is unsolvable'",
    "'I'm confused'",
    "'the wolf and cabbage start on the left'",
    "'the solution seems too simple'",
    "7 numbered steps to solve the puzzle"
]
data = {
    "0.7": [39, 4, 10, 2, 9, 37, 3, 31],
    "0.9": [43, 4, 29, 7, 10, 38, 7, 26],
    "1.1": [36, 12, 31, 10, 22, 33, 16, 23],
}
pleasant_order = [1, 7, 5, 0, 2, 4, 6, 3]

# Set up the plot
plt.figure(figsize=(10, 6))

data_normalized = {}
for key, value in data.items():
    sum_of_values = sum(value)
    data_normalized[key] = [x / sum_of_values for x in value]

# Convert data structure to be organized by idea number
temperatures = list(data.keys())
idea_data = []
for i in range(8):  # For each idea (0-7)
    idea_values = [data_normalized[temp][i] for temp in temperatures]
    idea_data.append(idea_values)

# Reorder to be in order indices [3, 6, 5, 0, 2, 7, 1, 4]
# pleasant_order = [1, 2, 5, 0, 7, 4, 6, 3]
pleasant_order = [1, 7, 5, 0, 2, 4, 6, 3]
idea_data = [idea_data[i] for i in pleasant_order]
ordered_ideas = [IDEAS_LIST[i] for i in pleasant_order]

print(idea_data)

# Define bar width and positions
bar_width = 0.1
index = np.arange(len(temperatures))  # position of each temperature on x-axis

# Plot bars for each idea with different colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

for i, idea_values in enumerate(idea_data):
    plt.bar(index + i * bar_width, idea_values, bar_width,
            label=ordered_ideas[i], color=colors[i], alpha=0.8)

# Customize the plot
plt.xlabel('Temperature')
plt.ylabel('Probability of Idea')
plt.title('Distribution of Ideas Across Temperatures')
plt.legend(loc='upper left', ncol=2)
plt.grid(True, alpha=0.3)

# Adjust x-axis ticks to be centered
plt.xticks(index + bar_width * (len(idea_data) - 1) / 2, temperatures)

plt.tight_layout()
plt.show()
