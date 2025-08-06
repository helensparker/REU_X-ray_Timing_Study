import matplotlib.pyplot as plt

def returnPlot():
    xlist = [1,1,3,4,3]
    ylist = [1,2,3,4,5]
    _, ax = plt.subplots()
    ax.plot(xlist, ylist)
    return ax


returnPlot().figure.savefig(f'figureReturn.png')