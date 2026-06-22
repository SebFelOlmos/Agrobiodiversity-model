import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx

# ── colour palette ────────────────────────────────────────────────────────────
COLORS = {
    # ENDOGAMOUS (greens)
    'Endo-Parallel':  '#66C2A4',
    'Endo-Cross-33':  '#41AE76',
    'Endo-Cross-66':  '#238B45',
    'Endo-Cross-100': '#005A32',

    # DUAL (gold/yellow)
    'Dual-Parallel':  '#FDD049',
    'Dual-Cross-33':  '#E6AB02',
    'Dual-Cross-66':  '#C98A00',
    'Dual-Cross-100': '#8C510A',

    # Comparison colours
    'clan':           '#D62728',
    'community':      '#1F77B4',
}

FUNC_MAP = {
    'Endo-Parallel':  'simul_paralel_EN',

    'Endo-Cross-33':  'simul_cross_33_EN',
    'Endo-Cross-66':  'simul_cross_66_EN',
    'Endo-Cross-100': 'simul_cross_100_EN',

    'Dual-Parallel':  'simul_paralel_DU',

    'Dual-Cross-33':  'simul_cross_33_DU',
    'Dual-Cross-66':  'simul_cross_66_DU',
    'Dual-Cross-100': 'simul_cross_100_DU',
}

# ── helpers ───────────────────────────────────────────────────────────────────

def _get(df, func_label, n):
    fname = FUNC_MAP[func_label]
    return df[(df['func'] == fname) & (df['n'] == n)]


def _plot_series(ax, df, func_label, n, col, label=None, color=None, linestyle='-'):
    """Plot mean ± std for a single (func, n, col) combination."""
    data = _get(df, func_label, n)
    if col not in data.columns or data[col].isna().all():
        ax.text(0.5, 0.5, 'N/A', transform=ax.transAxes,
                ha='center', va='center', fontsize=13, color='gray', alpha=0.5)
        return
    grp  = data.groupby('time')[col]
    mean = grp.mean()
    std  = grp.std()
    lbl  = label or func_label
    clr  = color or COLORS.get(func_label, 'gray')
    ax.plot(mean, label=lbl, color=clr, linewidth=1.8, linestyle=linestyle)
    ax.fill_between(mean.index, mean - std, mean + std, alpha=0.13, color=clr)


def _style(ax):
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=13)


def _legend(ax, **kw):
    ax.legend(frameon=False, fontsize=13, **kw)


def _savekw():
   return dict(bbox_inches='tight', dpi=100)

# ─--────────────────────────────────────────────────────────────────────────────
#  n = 1  PLOTS
# ─────────────────────────────────────────────────────────────────────────────

def plot_n1_community_richness(df_final, save_path=None, configs=['Endo-Parallel', 'Endo-Cross-100','Dual-Parallel', 'Dual-Cross-100',]):
    """
    n=1 · Compare community richness (div_com_0 == div_total for n=1)
    across all four configurations in one panel.
    """
    df = df_final[df_final['n'] == 1]

    fig, ax = plt.subplots(figsize=(9, 5))

    for cfg in configs:
        _plot_series(ax, df, cfg, n=1, col='div_total',
                     label=cfg, color=COLORS[cfg])

    _style(ax)
    _legend(ax, loc='upper right', ncol=2)

    ax.set_xlabel('Generations', fontsize=18)
    ax.set_ylabel('Community richness', fontsize=18)
    #ax.set_title('Community richness — All Configurations', fontsize=17, pad=10)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, **_savekw())
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
#  n > 1  PLOT 1 — community measures, four configurations
# ─────────────────────────────────────────────────────────────────────────────

def _jaccard_cols_for_n(n):
    """Return the list of pairwise jaccard column names valid for a given n."""
    if n < 2:
        return []
    cols = ['jaccard_com_0_1']
    if n >= 3:
        cols += ['jaccard_com_0_2', 'jaccard_com_1_2']
    return cols


def plot_community_measures(df_final, communities=(2, 3), save_path=None, configs=['Endo-Parallel', 'Endo-Cross-100','Dual-Parallel', 'Dual-Cross-100']):
    """
    Community measures for all configurations.

    Rows = communities (n values)
    Cols = alpha_com | beta_com | jaccard_com_0_1
    """

    all_measures = [
        ('alpha_com',       'Alpha community'),
        ('beta_com',        'Beta community'),
        ('jaccard_com_0_1', 'Jaccard community'),
    ]

    ncols = len(all_measures)
    nrows = len(communities)

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(15, 8),
        sharex=True
    )

    if nrows == 1:
        axes = axes[np.newaxis, :]

    # Column titles
    for c, (_, meas_label) in enumerate(all_measures):
        axes[0, c].set_title(
            meas_label,
            fontsize=18,
            fontweight='medium',
            pad=8
        )

    # Panels
    for r, n in enumerate(communities):

        for c, (col, _) in enumerate(all_measures):

            ax = axes[r, c]

            for cfg in configs:
                _plot_series(
                    ax,
                    df_final,
                    cfg,
                    n,
                    col,
                    color=COLORS[cfg]
                )

            _style(ax)

        axes[r, 0].set_ylabel(
            f'n = {n}',
            fontsize=18,
            color='gray'
        )

    # Global legend
    handles = [
        plt.Line2D([0], [0],
                   color=COLORS['Endo-Parallel'],
                   linewidth=2,
                   label='Endo-P'),

        plt.Line2D([0], [0],
                   color=COLORS['Endo-Cross-100'],
                   linewidth=2,
                   label='Endo-100'),

        plt.Line2D([0], [0],
                   color=COLORS['Dual-Parallel'],
                   linewidth=2,
                   label='Dual-P'),

        plt.Line2D([0], [0],
                   color=COLORS['Dual-Cross-100'],
                   linewidth=2,
                   label='Dual-100'),
    ]

    fig.legend(
        handles=handles,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.98),
        ncol=4,
        frameon=False,
        fontsize=16
    )

    fig.text(
        0.5,
        0.04,
        'Time',
        ha='center',
        fontsize=18
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.92])

    if save_path:
        fig.savefig(save_path, **_savekw())

    plt.show()

def plot_clan_measures(df_final, communities=(1, 2, 3), save_path=None):
    """
    Clan measures for Dual configurations only.

    Rows = communities (n values)
    Cols = alpha_clan | beta_clan | jaccard_clan
    """

    configs = [
        'Dual-Parallel',
        'Dual-Cross-33',
        'Dual-Cross-66',
        'Dual-Cross-100'
    ]

    all_measures = [
        ('alpha_clan',   'Alpha clan'),
        ('beta_clan',    'Beta clan'),
        ('jaccard_clan', 'Jaccard clan'),
    ]

    ncols = len(all_measures)
    nrows = len(communities)

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(14, 11),
        sharex=True
    )

    if nrows == 1:
        axes = axes[np.newaxis, :]

    # Column titles
    for c, (_, meas_label) in enumerate(all_measures):
        axes[0, c].set_title(
            meas_label,
            fontsize=14,
            fontweight='medium',
            pad=8
        )

    # Panels
    for r, n in enumerate(communities):

        for c, (col, _) in enumerate(all_measures):

            ax = axes[r, c]

            for cfg in configs:
                _plot_series(
                    ax,
                    df_final,
                    cfg,
                    n,
                    col,
                    color=COLORS[cfg]
                )

            _style(ax)

        axes[r, 0].set_ylabel(
            f'n = {n}',
            fontsize=15,
            color='gray'
        )

    # Global legend
    handles = [
        plt.Line2D(
            [0], [0],
            color=COLORS['Dual-Parallel'],
            linewidth=1.8,
            label='Parallel'
        ),
        plt.Line2D(
            [0], [0],
            color=COLORS['Dual-Cross-33'],
            linewidth=1.8,
            label='Cross-33'
        ),
        plt.Line2D(
            [0], [0],
            color=COLORS['Dual-Cross-66'],
            linewidth=1.8,
            label='Cross-66'
        ),
        plt.Line2D(
            [0], [0],
            color=COLORS['Dual-Cross-100'],
            linewidth=1.8,
            label='Cross-100'
        ),
    ]

    fig.legend(
        handles=handles,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.98),
        ncol=4,
        frameon=False,
        fontsize=12
    )

    fig.text(
        0.5,
        0.04,
        'Time',
        ha='center',
        fontsize=16
    )

    # fig.suptitle(
    #     'Clan measures — Dual configurations',
    #     fontsize=18,
    #     y=1.03
    # )

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])

    if save_path:
        fig.savefig(save_path, **_savekw())

    plt.show()

# ─────────────────────────────────────────────────────────────────────────────
#  n > 1  PLOT 2a — community vs clan, one Dual configuration per figure
# ─────────────────────────────────────────────────────────────────────────────

def plot_com_vs_clan_dual(df_final, dual_config='Dual-Parallel',
                          communities=(2, 3), save_path=None):

    assert dual_config in (
        'Dual-Parallel',
        'Dual-Cross-33',
        'Dual-Cross-66',
        'Dual-Cross-100'
    ), (
        "dual_config must be one of: "
        "'Dual-Parallel', 'Dual-Cross-33', "
        "'Dual-Cross-66', 'Dual-Cross-100'"
    )

    clr_com  = COLORS['community']
    clr_clan = COLORS['clan']

    panel_defs = [
        ('Alpha',   'alpha_com',       'alpha_clan'),
        ('Beta',    'beta_com',        'beta_clan'),
        ('Jaccard', 'jaccard_com_0_1', 'jaccard_clan'),
    ]

    ncols = len(panel_defs)
    nrows = len(communities)

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(14, 8),
        sharex=True
    )

    if nrows == 1:
        axes = axes[np.newaxis, :]

    # Column titles
    for c, (title, _, __) in enumerate(panel_defs):
        axes[0, c].set_title(
            title,
            fontsize=18,
            fontweight='medium',
            pad=8
        )

    # Panels
    for r, n in enumerate(communities):

        data = _get(df_final, dual_config, n)

        for c, (title, com_col, clan_col) in enumerate(panel_defs):

            ax = axes[r, c]

            # Community
            if com_col in data.columns and not data[com_col].isna().all():

                grp = data.groupby('time')[com_col]

                mean = grp.mean()
                std  = grp.std()

                ax.plot(
                    mean,
                    color=clr_com,
                    linewidth=1.8,
                    label='Community'
                )

                ax.fill_between(
                    mean.index,
                    mean - std,
                    mean + std,
                    alpha=0.08,
                    color=clr_com
                )

            # Clan
            if clan_col in data.columns and not data[clan_col].isna().all():

                grp = data.groupby('time')[clan_col]

                mean = grp.mean()
                std  = grp.std()

                ax.plot(
                    mean,
                    color=clr_clan,
                    linewidth=1.8,
                    linestyle='--',
                    label='Clan'
                )

                ax.fill_between(
                    mean.index,
                    mean - std,
                    mean + std,
                    alpha=0.08,
                    color=clr_clan
                )

            _style(ax)

            if c == 0:
                ax.set_ylabel(
                    f'n = {n}',
                    fontsize=18,
                    color='gray'
                )

    # Global legend
    handles = [
        plt.Line2D(
            [0], [0],
            color=clr_com,
            linewidth=2,
            label='Community'
        ),
        plt.Line2D(
            [0], [0],
            color=clr_clan,
            linewidth=2,
            linestyle='--',
            label='Clan'
        )
    ]

    fig.legend(
        handles=handles,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.98),
        ncol=2,
        frameon=False,
        fontsize=16
    )

    fig.text(
        0.5,
        0.04,
        'Time',
        ha='center',
        fontsize=18
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])

    if save_path:
        fig.savefig(save_path, **_savekw())

    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
#  Convenience wrapper: both Dual plots side by side (option B)
# ─────────────────────────────────────────────────────────────────────────────

def plot_com_vs_clan_both_dual(df_final, n=2, save_path=None, configs=['Dual-Parallel','Dual-Cross-100']):

    panel_defs = [
        ('Alpha',    ['alpha_com'], ['alpha_clan']),
        ('Beta',     ['beta_com'],  ['beta_clan']),
        ('Jaccard',  None,          ['jaccard_clan']),
    ]

    nrows = len(panel_defs)
    ncols = len(configs)

    valid_jacc = _jaccard_cols_for_n(n)

    clr_com  = COLORS['community']
    clr_clan = COLORS['clan']

    jacc_colors = ['#378ADD', '#5BA3E0', '#84BDE8']

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(7, 9),
        sharex=True
    )

    # Share y-axis across configs for each metric (row)
    for r in range(nrows):
        for ax in axes[r, 1:]:
            ax.sharey(axes[r, 0])

    # Config names as column titles
    for c, cfg in enumerate(configs):
        axes[0, c].set_title(
            cfg,
            fontsize=18,
            fontweight='medium',
            pad=8
        )

    # Metric names as row labels
    for r, (title, _, __) in enumerate(panel_defs):
        axes[r, 0].set_ylabel(
            title,
            fontsize=14,
            color='gray'
        )

    for c, cfg in enumerate(configs):

        data = _get(df_final, cfg, n)

        for r, (title, com_cols, clan_cols) in enumerate(panel_defs):

            ax = axes[r, c]

            if title == 'Jaccard':

                for jc, jcol in enumerate(valid_jacc):

                    if jcol not in data.columns:
                        continue

                    grp = data.groupby('time')[jcol]

                    mean = grp.mean()
                    std  = grp.std()

                    ax.plot(
                        mean,
                        color=jacc_colors[jc],
                        linewidth=1.6,
                        label=f'Community {jcol[-3:].replace("_", "-")}'
                    )

                    ax.fill_between(
                        mean.index,
                        mean - std,
                        mean + std,
                        alpha=0.12,
                        color=jacc_colors[jc]
                    )

            else:

                avail = [
                    col for col in com_cols
                    if col in data.columns and not data[col].isna().all()
                ]

                if avail:

                    com_mean = (
                        data.groupby('time')[avail]
                        .mean()
                        .mean(axis=1)
                    )

                    com_std = (
                        data.groupby('time')[avail]
                        .std()
                        .mean(axis=1)
                    )

                    ax.plot(
                        com_mean,
                        color=clr_com,
                        linewidth=1.8,
                        label='Community'
                    )

                    ax.fill_between(
                        com_mean.index,
                        com_mean - com_std,
                        com_mean + com_std,
                        alpha=0.13,
                        color=clr_com
                    )

            avail_clan = [
                col for col in clan_cols
                if col in data.columns and not data[col].isna().all()
            ]

            if avail_clan:

                clan_mean = (
                    data.groupby('time')[avail_clan]
                    .mean()
                    .mean(axis=1)
                )

                clan_std = (
                    data.groupby('time')[avail_clan]
                    .std()
                    .mean(axis=1)
                )

                ax.plot(
                    clan_mean,
                    color=clr_clan,
                    linewidth=1.8,
                    linestyle='--',
                    label='Clan'
                )

                ax.fill_between(
                    clan_mean.index,
                    clan_mean - clan_std,
                    clan_mean + clan_std,
                    alpha=0.13,
                    color=clr_clan
                )

            _style(ax)

    axes[0, -1].legend(
        frameon=False,
        fontsize=16,
        loc='upper right'
    )

    fig.supxlabel(
    'Generations',
    fontsize=18
)

    fig.tight_layout()  # sobre fig, no plt
    fig.subplots_adjust(bottom=0.08)
    if save_path:
        fig.savefig(save_path, **_savekw())  # bbox_inches='tight', dpi=100


    plt.show()

def plot_com_vs_clan_dual2(df_final, df_extra=None, dual_config='Dual-Parallel', communities=(2, 3), save_path=None):

    assert dual_config in (
        'Dual-Parallel',
        'Dual-Cross-33',
        'Dual-Cross-66',
        'Dual-Cross-100'
    ), (
        "dual_config must be one of: "
        "'Dual-Parallel', 'Dual-Cross-33', "
        "'Dual-Cross-66', 'Dual-Cross-100'"
    )

    clr_com  = COLORS['community']
    clr_clan = COLORS['clan']

    panel_defs = [
        ('Alpha',   'alpha_com',       'alpha_clan'),
        ('Beta',    'beta_com',        'beta_clan'),
        ('Jaccard', 'jaccard_com_0_1', 'jaccard_clan'),
    ]

    ncols = len(panel_defs)
    nrows = len(communities)

    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(14, 8),
        sharex=True
    )

    if nrows == 1:
        axes = axes[np.newaxis, :]

    # Column titles
    for c, (title, _, __) in enumerate(panel_defs):
        axes[0, c].set_title(
            title,
            fontsize=14,
            fontweight='medium',
            pad=8
        )

    # Define init sources
    if df_extra is not None:
        init_sources = [
            (df_final, 'com',  '-'),
            (df_extra, 'clan', '--'),
        ]
    else:
        init_sources = [
            (df_final, 'com', '-'),
        ]

    # Panels
    for r, n in enumerate(communities):
        for c, (title, com_col, clan_col) in enumerate(panel_defs):

            ax = axes[r, c]

            for df_src, init_val, linestyle in init_sources:

                data = _get(df_src, dual_config, n)

                # Community
                if com_col in data.columns and not data[com_col].isna().all():

                    grp  = data.groupby('time')[com_col]
                    mean = grp.mean()
                    std  = grp.std()

                    ax.plot(
                        mean,
                        color=clr_com,
                        linewidth=1.8,
                        linestyle=linestyle,
                        label=f'Community ({init_val}-init)'
                    )

                    ax.fill_between(
                        mean.index,
                        mean - std,
                        mean + std,
                        alpha=0.08,
                        color=clr_com
                    )

                # Clan
                if clan_col in data.columns and not data[clan_col].isna().all():

                    grp  = data.groupby('time')[clan_col]
                    mean = grp.mean()
                    std  = grp.std()

                    ax.plot(
                        mean,
                        color=clr_clan,
                        linewidth=1.8,
                        linestyle=linestyle,
                        label=f'Clan ({init_val}-init)'
                    )

                    ax.fill_between(
                        mean.index,
                        mean - std,
                        mean + std,
                        alpha=0.08,
                        color=clr_clan
                    )

            _style(ax)

            if c == 0:
                ax.set_ylabel(
                    f'n = {n}',
                    fontsize=15,
                    color='gray'
                )

    # Global legend — 2 lines if no df_extra, 4 lines if combined
    if df_extra is not None:
        handles = [
            plt.Line2D([0], [0], color=clr_com,  linewidth=2, linestyle='-',  label='Community (com-init)'),
            plt.Line2D([0], [0], color=clr_com,  linewidth=2, linestyle='--', label='Community (clan-init)'),
            plt.Line2D([0], [0], color=clr_clan, linewidth=2, linestyle='-',  label='Clan (com-init)'),
            plt.Line2D([0], [0], color=clr_clan, linewidth=2, linestyle='--', label='Clan (clan-init)'),
        ]
    else:
        handles = [
            plt.Line2D([0], [0], color=clr_com,  linewidth=2, label='Community'),
            plt.Line2D([0], [0], color=clr_clan, linewidth=2, linestyle='--', label='Clan'),
        ]

    fig.legend(
        handles=handles,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.98),
        ncol=4 if df_extra is not None else 2,
        frameon=False,
        fontsize=12
    )

    fig.text(
        0.5,
        0.04,
        'Time',
        ha='center',
        fontsize=16
    )

    fig.suptitle(
        f'Community vs Clan — {dual_config}',
        fontsize=18,
        y=1.03
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])

    if save_path:
        fig.savefig(save_path, **_savekw())

    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# Matriz and network visualizations
# ─────────────────────────────────────────────────────────────────────────────

####################################################################### Matrix/netwworks

# ── Helpers ───────────────────────────────────────────────────────────────────

def matriz_to_bipartite(matriz):
    B = nx.Graph()
    farms     = [f'farm_{i}'    for i in range(len(matriz))]
    varieties = [f'variety_{j}' for j in range(len(matriz[0]))]
    B.add_nodes_from(farms,     bipartite=0)
    B.add_nodes_from(varieties, bipartite=1)
    for i, farm in enumerate(farms):
        for j, variety in enumerate(varieties):
            weight = matriz[i][j][0]
            if weight >= 1:
                B.add_edge(farm, variety, weight=weight)
    return B

def bipartite_to_projection(B):
    farms = {n for n, d in B.nodes(data=True) if d['bipartite'] == 0}
    return nx.bipartite.weighted_projected_graph(B, farms)

def _get_funcs(com_init):
    if com_init:
        return [('Cross EN', 'simul_cross_100_EN'), ('Parallel EN', 'simul_paralel_EN')]
    else:
        return [('Cross DU', 'simul_cross_100_DU'), ('Parallel DU', 'simul_paralel_DU')]


# ── Refactored functions (receive axes) ───────────────────────────────────────

def plot_heatmap_moments(df_final, n, axes, times=[0, 10, 20], simulation=0, com_init=True):
    funcs = _get_funcs(com_init)

    for row, (func_label, func_name) in enumerate(funcs):
        subset = df_final[
            (df_final['func']       == func_name) &
            (df_final['n']          == n)         &
            (df_final['simulation'] == simulation)
        ]
        for col, t in enumerate(times):
            ax       = axes[row, col]
            row_data = subset[subset['time'] == t]

            if row_data.empty:
                ax.text(0.5, 0.5, 'N/A', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12, color='gray')
                ax.axis('off')
                continue

            matriz = row_data.iloc[0]['matriz']
            matrix = np.array([[cell[0] for cell in r] for r in matriz])

            sns.heatmap(matrix, annot=False, fmt="d", cmap="YlOrRd",
                        linewidths=0.5, linecolor="gray",
                        cbar=False, vmin=0, vmax=9, ax=ax)

            if row == 0:
                ax.set_title(f't = {t}', fontsize=22, pad=8)
            if col == len(times) - 1:
                ax.annotate(func_label, xy=(1.02, 0.5), xycoords='axes fraction',
                            fontsize=22, color='gray', va='center', ha='left', rotation=270)

            ax.set_xlabel('')
            ax.set_ylabel('')
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)


def plot_bipartite_moments(df_final, n, axes, times=[0, 10, 20], simulation=0, com_init=True):
    funcs = _get_funcs(com_init)

    for row, (func_label, func_name) in enumerate(funcs):
        subset = df_final[
            (df_final['func']       == func_name) &
            (df_final['n']          == n)         &
            (df_final['simulation'] == simulation)
        ]
        first = subset[subset['time'] == times[0]]
        if not first.empty:
            B0        = matriz_to_bipartite(first.iloc[0]['matriz'])
            farms     = [node for node, d in B0.nodes(data=True) if d['bipartite'] == 0]
            varieties = [node for node, d in B0.nodes(data=True) if d['bipartite'] == 1]
            pos = {}
            for i, node in enumerate(farms):
                pos[node] = (0, -i)
            for j, node in enumerate(varieties):
                pos[node] = (1, -j * (len(farms) / max(len(varieties), 1)))
        else:
            pos = {}

        for col, t in enumerate(times):
            ax       = axes[row, col]
            row_data = subset[subset['time'] == t]

            if row_data.empty:
                ax.text(0.5, 0.5, 'N/A', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12, color='gray')
                ax.axis('off')
                continue

            matriz        = row_data.iloc[0]['matriz']
            B             = matriz_to_bipartite(matriz)
            farms_now     = [node for node, d in B.nodes(data=True) if d['bipartite'] == 0]
            varieties_now = [node for node, d in B.nodes(data=True) if d['bipartite'] == 1]

            nx.draw_networkx_nodes(B, pos, nodelist=farms_now,
                                   node_color='#378ADD', node_size=30, ax=ax)
            nx.draw_networkx_nodes(B, pos, nodelist=varieties_now,
                                   node_color='#1D9E75', node_size=30, ax=ax)
            nx.draw_networkx_edges(B, pos, alpha=0.3, edge_color='gray', ax=ax)

            if row == 0:
                ax.set_title(f't = {t}', fontsize=22, pad=8)
            if col == len(times) - 1:
                ax.annotate(func_label, xy=(1.02, 0.5), xycoords='axes fraction',
                            fontsize=22, color='gray', va='center', ha='left', rotation=270)

            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_linewidth(0.8)
                spine.set_color('lightgray')
            ax.axis('on')
            ax.set_xticks([])
            ax.set_yticks([])


def plot_network_moments(df_final, n, axes, times=[0, 10, 20], simulation=0, com_init=True):
    funcs = _get_funcs(com_init)

    for row, (func_label, func_name) in enumerate(funcs):
        subset = df_final[
            (df_final['func']       == func_name) &
            (df_final['n']          == n)         &
            (df_final['simulation'] == simulation)
        ]
        first = subset[subset['time'] == times[0]]
        if not first.empty:
            B0  = matriz_to_bipartite(first.iloc[0]['matriz'])
            G0  = bipartite_to_projection(B0)
            pos = nx.spring_layout(G0, seed=42)
        else:
            pos = {}

        for col, t in enumerate(times):
            ax       = axes[row, col]
            row_data = subset[subset['time'] == t]

            if row_data.empty:
                ax.text(0.5, 0.5, 'N/A', transform=ax.transAxes,
                        ha='center', va='center', fontsize=12, color='gray')
                ax.axis('off')
                continue

            matriz  = row_data.iloc[0]['matriz']
            B       = matriz_to_bipartite(matriz)
            G       = bipartite_to_projection(B)
            weights = [G[u][v]['weight'] for u, v in G.edges()]

            nx.draw_networkx_nodes(G, pos, node_color='#378ADD', node_size=30, ax=ax)
            nx.draw_networkx_edges(G, pos, width=[w * 0.5 for w in weights],
                                   alpha=0.4, edge_color='gray', ax=ax)

            #if row == 0:
            #    ax.set_title(f't = {t}', fontsize=22, pad=8)
            if col == len(times) - 1:
                ax.annotate(func_label, xy=(1.02, 0.5), xycoords='axes fraction',
                            fontsize=22, color='gray', va='center', ha='left', rotation=270)

            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_linewidth(0.8)
                spine.set_color('lightgray')
            ax.axis('on')
            ax.set_xticks([])
            ax.set_yticks([])


# ── Wrapper ───────────────────────────────────────────────────────────────────

def plot_all_moments(df_final, n, times=[0, 10, 20], simulation=0, com_init=True, save_path=None):
    n_funcs = 2
    n_times = len(times)

    fig = plt.figure(figsize=(8 * n_times, 3 * n_funcs * 2))

    gs = fig.add_gridspec(
        n_funcs * 2, n_times + 2,
        width_ratios=[1] * n_times + [0.02, 0.04],
        hspace=0.3, wspace=0.1
    )

    axes_heatmap = np.array([[fig.add_subplot(gs[r, c]) for c in range(n_times)] for r in range(n_funcs)])
    axes_network = np.array([[fig.add_subplot(gs[n_funcs + r, c]) for c in range(n_times)] for r in range(n_funcs)])
    cbar_ax      = fig.add_subplot(gs[:n_funcs, n_times + 1])   # spans heatmap rows only

    plot_heatmap_moments(df_final, n, axes_heatmap, times, simulation, com_init)
    plot_network_moments(df_final, n, axes_network, times, simulation, com_init)

    # Single shared colorbar in the reserved column
    sm = plt.cm.ScalarMappable(cmap="YlOrRd", norm=plt.Normalize(vmin=0, vmax=9))
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Plants of the same variety', fontsize=16, labelpad=16, rotation=270)

    if save_path:
        fig.savefig(save_path, **_savekw())
    plt.show()

# ──────────────────────────────────  To use if you want! ─────────────────────────────────────────────

if __name__ == "__main__":

    df_com = pd.read_pickle('local-kin-transmission-model\output\df_final_com_init.pkl')
    df_clan = pd.read_pickle('local-kin-transmission-model\output\df_final_clan_init.pkl')


    #################### FOR INIT COM
    # ── n = 1 ────────────────────────────────────────────────────────────────────
    plot_n1_community_richness(df_com, save_path="local-kin-transmission-model\output\images\com\com_rich_n1.png")
    plot_clan_measures(df_com, communities=(1, 2, 3), save_path="local-kin-transmission-model\output\images\com\clan_rich.png")
    # ── n > 1 · Plot 1: community measures, four configs ─────────────────────────
    plot_community_measures(df_com, communities=[2, 3], save_path="local-kin-transmission-model\output\images\com\com_rich.png")


    # ── n > 1 · Plot 2: com vs clan, separate figures per Dual config ─────────────
    plot_com_vs_clan_dual(df_com, dual_config='Dual-Parallel', save_path= "local-kin-transmission-model\output\images\com\DU_paral_com_clan2n.png")
    #plot_com_vs_clan_dual(df_com, dual_config='Dual-Cross-33')
    #plot_com_vs_clan_dual(df_com,dual_config='Dual-Cross-66')
    plot_com_vs_clan_dual(df_com, dual_config='Dual-Cross-100', save_path= "local-kin-transmission-model\output\images\com\DU_100_com_clan_ns.png")
    
    #
    # ── n > 1 · Plot 2 alt: both Dual in one figure (single n) ───────────────────
    plot_com_vs_clan_both_dual(df_com, n=2, save_path= "local-kin-transmission-model\output\images\com\DU_all_com_clan2.png")
    plot_com_vs_clan_both_dual(df_com, n=3, save_path= "local-kin-transmission-model\output\images\com\DU_all_com_clan3.png")
    plot_all_moments(df_com, n=1, save_path="local-kin-transmission-model\output\images\com\mat_netn1.png")
    plot_all_moments(df_com, n=2, save_path="local-kin-transmission-model\output\images\com\mat_netn2.png")
    plot_all_moments(df_com, n=3, save_path="local-kin-transmission-model\output\images\com\mat_netn3.png")

    ################ FOR INIT CLAN
    # ── n = 1 ────────────────────────────────────────────────────────────────────
    plot_n1_community_richness(df_clan, configs=['Dual-Parallel', 'Dual-Cross-100',], save_path="local-kin-transmission-model\output\images\clan\com_rich_n1.png")
    plot_clan_measures(df_clan, communities=(1, 2, 3), save_path="local-kin-transmission-model\output\images\clan\clan_rich.png")
    # ── n > 1 · Plot 1: community measures, four configs ─────────────────────────
    plot_community_measures(df_clan, communities=[2, 3], configs=['Dual-Parallel', 'Dual-Cross-100'], save_path="local-kin-transmission-model\output\images\clan\com_rich.png")


    # ── n > 1 · Plot 2: com vs clan, separate figures per Dual config ─────────────
    plot_com_vs_clan_dual(df_clan,dual_config='Dual-Parallel', save_path= "local-kin-transmission-model\output\images\clan\DU_paral_com_clan2n.png")
    #plot_com_vs_clan_dual(df_clan, dual_config='Dual-Cross-33')
    #plot_com_vs_clan_dual(df_clan,dual_config='Dual-Cross-66')
    plot_com_vs_clan_dual(df_clan,dual_config='Dual-Cross-100', save_path= "local-kin-transmission-model\output\images\clan\DU_100_com_clan_ns.png")
    #
    # ── n > 1 · Plot 2 alt: both Dual in one figure (single n) ───────────────────
    plot_com_vs_clan_both_dual(df_clan, n=2, save_path= "local-kin-transmission-model\output\images\clan\DU_all_com_clan2.png")
    plot_com_vs_clan_both_dual(df_clan, n=3, save_path= "local-kin-transmission-model\output\images\clan\DU_all_com_clan3.png")
    ### Net
    plot_all_moments(df_clan, n=1 , com_init= False, save_path="local-kin-transmission-model\output\images\clan\mat_netn1.png")
    plot_all_moments(df_clan, n=2, com_init= False,  save_path="local-kin-transmission-model\output\images\clan\mat_netn2.png")
    plot_all_moments(df_clan, n=3, com_init= False,  save_path="local-kin-transmission-model\output\images\clan\mat_netn3.png")



# import matplotlib.pyplot as plt
# import matplotlib as mpl

# fig, ax = plt.subplots(figsize=(1.5, 6))
# fig.subplots_adjust(left=0.05, right=0.4)

# norm = mpl.colors.Normalize(vmin=0, vmax=9)
# sm   = plt.cm.ScalarMappable(cmap="YlOrRd", norm=norm)
# sm.set_array([])

# cbar = fig.colorbar(sm, cax=ax)
# cbar.set_label('Plants of the same variety', fontsize=16, labelpad=16, rotation=270, va='bottom')
# cbar.ax.tick_params(labelsize=13)

# plt.savefig("colorbar.pdf", bbox_inches="tight", dpi=300)
# plt.show()