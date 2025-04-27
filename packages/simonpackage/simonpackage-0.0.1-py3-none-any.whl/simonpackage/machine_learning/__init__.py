import numpy as np
import matplotlib.pyplot as plt

def testModel(model, X_train, y_train, X_test, y_test, *args, **kwargs):
    model = model(*args, **kwargs)
    model.fit(X_train, y_train)
    model_score = model.score(X_test, y_test)
    print(f'score of {model} is {model_score}')
    return model_score

def plotMatrix(rows:int, cols:int, plots, plot_type:str='plot', *args, **kwargs):
    """
    plot rows * cols subplots
    :param rows:
    :param cols:
    :param plots: data to be plotted, can be sliced
    :param plot_type: "plot" "scatter" "imshow"
    :param args: args for the plot function
    :param kwargs: kwargs for the plot function
    :return:
    """
    fig, ax = plt.subplots(rows, cols, figsize=(8,10))
    total_plots = len(plots)
    for row in range(rows):
        for col in range(cols):
            axplot = eval(f'ax[row, col].{plot_type}')
            plot_index = row * col + col
            plot_index = plot_index if plot_index < total_plots else -1
            axplot(plots[plot_index], *args, **kwargs)
            ax[row, col].set_axis_off()

def plotDecisionBoundry(model, axis, cm=['#EF9A9A', '#FFF59D', '#90CAF9']):
    x0, x1 = np.meshgrid(
        np.linspace(axis[0], axis[1], int((axis[1] - axis[0]) * 100)).reshape(-1, 1),
        np.linspace(axis[2], axis[3], int((axis[3] - axis[2]) * 100)).reshape(-1, 1),
    )
    X_new = np.c_[x0.ravel(), x1.ravel()]
    y_predict = model.predict(X_new)
    zz = y_predict.reshape(x0.shape)
    from matplotlib.colors import ListedColormap
    custom_cmap = ListedColormap(cm)
    plt.contourf(x0, x1, zz, cmap=custom_cmap)

def findMisses(test, pred):
    """
    find the index list of the misclassifications
    :param test:
    :param pred:
    :return:
    """
    return [i for i, row in enumerate(test) if row != pred[i]]