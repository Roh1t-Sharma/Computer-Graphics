import matplotlib.pyplot as plt

# Values to be represented in the pie chart
values = [25, 35, 15, 25, 45]

def calculate_percentages(values):
    total = sum(values)
    percentages = [(value / total) * 100 for value in values]
    return percentages

def add_value(values, new_value):
    values.append(new_value)
    return calculate_percentages(values)

# Initial percentages
percentages = calculate_percentages(values)

def plot_pie_chart(percentages):
    # Create a pie chart based on the percentages
    fig, ax = plt.subplots()
    ax.pie(percentages, labels=[f'{p:.2f}%' for p in percentages], startangle=90, counterclock=False)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart
    plt.show()

# Plot initial pie chart
plot_pie_chart(percentages)

# Function to update the pie chart with a new value
def update_pie_chart(new_value):
    updated_percentages = add_value(values, new_value)
    plot_pie_chart(updated_percentages)

# For demonstration, add a new value to the pie chart
update_pie_chart(20)
