import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

current_month = 9

ipc = pd.read_excel("IPC.xlsx", sheet_name="1. NACIONAL", skiprows=4)
ipc.dropna(inplace=True)
ipc = ipc[ipc["NIVEL"] == "Producto"]

months = [f"{mes[:3]}-{str(año)[-2:]}" for año in range(2018, 2024) for mes in ['ene', 'feb', 'mar', 
                                                                               'abr', 'may', 'jun',
                                                                               'jul', 'ago', 'sep',
                                                                               'oct', 'nov', 'dic']]

months = months[:-(12-current_month)]

tercer_meses_trimestre = [mes for i, mes in enumerate(months) if (i + 1) % 3 == 0]


# Melting del DataFrame
ipc_graph = pd.melt(ipc, id_vars="Descripción CCIF", value_vars=months)

# Create the data
# rs = np.random.RandomState(1979)
# x = rs.randn(500)
# g = np.tile(list("ABCDEFGHIJ"), 50)
# df = pd.DataFrame(dict(x=x, g=g))
# m = df.g.map(ord)
# df["x"] += m

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(rot=-.25, light=.7, as_cmap=True)
al = sns.cubehelix_palette(rot=-.25, light=.7)
g = sns.FacetGrid(ipc_graph, row="variable", hue="variable", aspect=25, height=.3, palette=al)


# g.map(plot_filtered_density, "value")
# Draw the densities in a few steps
g.map(sns.kdeplot, "value",
      bw_adjust=.5, clip_on=False,
      fill=True, alpha=1, linewidth=1.5, cmap= pal, shade=True)
g.map(sns.kdeplot, "value", clip_on=[False], color="w", lw=2, bw_adjust=.5)

# # # passing color=None to refline() uses the hue mapping
# g.refline(y=0, linewidth=1.5, linestyle="-", color=None, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "value")
# g.set(xlim=(-20, 20))

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.5)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)

plt.show()
