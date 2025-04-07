import numpy as np
import random
import time
import random
import os
import json
import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(42)
np.random.seed(42)

# Path
current_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.abspath(os.path.join(current_directory, '..'))
sys.path.append(root_directory)


def plot_heatmap(data, alphas, betas, alpha, beta, variable, colorbar_range=(0, 150), figsize=(7, 5)):
        """
        Plot a heatmap with specific configuration for colorbar and labels.

        Parameters:
            data (list of list of dict): Data containing 'alive' values.
            alphas (list): Labels for the y-axis.
            betas (list): Labels for the x-axis.
            colorbar_range (tuple): Min and max values for the colorbar.
            figsize (tuple): Figure size for the plot.
        """
        # Extract 'alive' values
        alive_values = np.array([[entry[variable] for entry in row] for row in data])
        
        # Set up plot
        fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor="white")
        im = ax.imshow(alive_values, vmin=colorbar_range[0], vmax=colorbar_range[1])
        
        # Colorbar
        cbar = fig.colorbar(im, ax=ax, label='UDs')
        #cbar.set_clim(*colorbar_range)
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(betas)))
        ax.set_yticks(np.arange(len(alphas)))
        ax.set_xticklabels([f'{round(beta, 3)}' for beta in betas])
        ax.set_yticklabels([f'{alpha:.1f}' for alpha in alphas])
        
        # Display values in the heatmap cells
        for i in range(len(alphas)):
            for j in range(len(betas)):
                ax.text(j, i, f'{alive_values[i, j]:.1f}', ha="center", va="center", color="w", fontsize=8)
        
        # Label axes
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        ax.set_ylabel(alpha)
        ax.set_xlabel(beta)
        
        #plt.show()
        return plt


n = 4
m = 40
malphas = np.linspace(1,n,n) # Average number of children: from 1 to n
mbetas = np.linspace(10,m,int(m/10)) # Initial UDs: from 10 to m
parent_folder = 'Outputs'
folder_name = os.path.join(parent_folder, 'results_validation', 'populational behavior', 'Dual Organization')
heat_std = os.path.join(folder_name, 'Dual_beta_fixed.npy')
mM_datos = np.load(heat_std, allow_pickle=True)
plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'alive', (0, 150))
plot.show()
# plot.savefig(os.path.join(folder_name, 'Dual_beta_fixed_mean.png'), dpi=300, bbox_inches="tight")
# print(f"Heatmap of the mean pop saved to: {os.path.join(folder_name, 'Dual_beta_fixed_mean.png')}")
plot = plot_heatmap(mM_datos, malphas, mbetas, 'Mean Children', 'Initial UDs', 'std', (0, 150))
plot.show()
# plot.savefig(os.path.join(folder_name, 'Dual_beta_fixed_std.png'), dpi=300, bbox_inches="tight")
# print(f"Heatmap of the mean std saved to: {os.path.join(folder_name, 'Dual_beta_fixed_std.png')}")


