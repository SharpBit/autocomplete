import matplotlib.pyplot as plt

def bar_graph(stats, number, labels):
    """Easy function to quickly create a bargraph"""
    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(range(number), [w[1] for w in stats], align='center')
    ax.set_yticks(range(number))
    ax.set_yticklabels([w[0] for w in stats])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])

    plt.show()
