import matplotlib.pyplot as plt


def histogram(input, label, title, x_rotation=0):
    # Sets characteristics of the chart
    plt.title(title)
    plt.xlabel(label)

    valueRange = list(range(len(input.index)))  # Sets the value range
    plt.xticks(
        valueRange, input.index,
        rotation=x_rotation)  # Sets the ticks of the x axis to the browsers
    plt.bar(valueRange, input.values)  # Sets the value of the bars
    plt.show()
