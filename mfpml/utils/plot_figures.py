import numpy as np
import pandas as pd
from typing import Tuple, Any
from matplotlib import pyplot as plt
from mfpml.base import Functions


def plot_sf_sampling(samples: np.ndarray,
                     responses: np.ndarray,
                     function: Functions = None,
                     save_figure: bool = False) -> None:
    """
    Visualize the 1D case, set the y axis as Zero
    Parameters
    ----------
    save_figure: bool
        save figure
    samples : np.ndarray
        original data for visualization
    responses: np.ndarray
        responses of samples
    function:
        the original function

    Returns
    -------

    """
    num_dim = samples.shape[1]
    if num_dim == 1:
        x_plot = np.linspace(start=function.low_bound[0],
                             stop=function.high_bound[0],
                             num=1000)
        x_plot = x_plot.reshape((-1, 1))
        y_plot = function.f(x=x_plot)
        y_plot.reshape((-1, 1))
        with plt.style.context(['ieee', 'science']):
            fig, ax = plt.subplots()
            ax.plot(samples[:, 0], responses[:, 0], '*', label='Samples')
            ax.plot(x_plot, y_plot, label=f'{function.__class__.__name__}')
            ax.legend()
            ax.set(xlabel=r'$x$')
            ax.set(ylabel=r'$y$')
            ax.autoscale(tight=True)
            if save_figure is True:
                fig.savefig(function.__class__.__name__, dpi=300)
            plt.show(block=True)
            plt.interactive(False)
    elif num_dim == 2:
        num_plot = 200
        x1_plot = np.linspace(start=function.__class__.low_bound[0],
                              stop=function.__class__.high_bound[0],
                              num=num_plot)
        x2_plot = np.linspace(start=function.__class__.low_bound[1],
                              stop=function.__class__.high_bound[1],
                              num=num_plot)
        X1, X2 = np.meshgrid(x1_plot, x2_plot)
        Y = np.zeros([len(X1), len(X2)])
        # get the values of Y at each mesh grid
        for i in range(len(X1)):
            for j in range(len(X1)):
                xy = np.array([X1[i, j], X2[i, j]])
                xy = np.reshape(xy, (1, 2))
                Y[i, j] = function.f(x=xy)
        with plt.style.context(['ieee', 'science']):
            fig, ax = plt.subplots()
            plt.scatter(samples[:, 0], samples[:, 1], s=15, color='orangered',
                        label='Samples')
            cs = ax.contour(X1, X2, Y, 15)
            plt.colorbar(cs)
            ax.set(xlabel=r'$x_1$')
            ax.set(ylabel=r'$x_2$')
            plt.legend(loc='upper center', bbox_to_anchor=(1, -0.05), edgecolor='k')
            # plt.clabel(cs, inline=True)
            if save_figure is True:
                fig.savefig(function.__class__.__name__, dpi=300)
            plt.show(block=True)
            plt.interactive(False)


def plot_1d_model_prediction(data: dict,
                             model: Any,
                             function: Functions = None,
                             name: str = 'figure',
                             save: bool = False) -> None:
    """

    Parameters
    ----------
    model: Any
        machine learning models
    data:  dict
        samples generated by design_of_experiment
    function: Functions
        real function
    name:str
        name of the figure
    save: bool
        save the figure or not

    Returns
    -------

    """
    x_plot = np.linspace(start=function.low_bound[0],
                         stop=function.high_bound[0],
                         num=1000)
    x_plot = x_plot.reshape((-1, 1))
    y_plot = function(x=x_plot, fidelity='high')
    y_plot.reshape((-1, 1))
    y_pred, y_sigma = model.predict(x_plot, return_std=True)
    with plt.style.context(['ieee', 'science']):
        fig, ax = plt.subplots()
        ax.plot(data['inputs'].iloc[:, 0], data['outputs'].iloc[:, 0], '*', label='Samples')
        ax.plot(x_plot, y_plot, label=f'{function.__class__.__name__}')
        ax.plot(x_plot, y_pred, '--', label='prediction')
        ax.fill_between(x_plot.ravel(),
                        (y_pred + 2 * y_sigma).ravel(),
                        (y_pred - 2 * y_sigma).ravel(),
                        color='forestgreen',
                        alpha=0.3,
                        label='confidence interval')
        ax.legend()
        ax.set(xlabel=r'$x$')
        ax.set(ylabel=r'$y$')
        ax.autoscale(tight=True)
        if save is True:
            fig.savefig(name, dpi=300)
        plt.show(block=True)
        plt.interactive(False)