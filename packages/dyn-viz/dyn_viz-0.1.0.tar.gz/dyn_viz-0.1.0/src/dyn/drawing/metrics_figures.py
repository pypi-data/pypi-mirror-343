import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator


def draw_hist(data, variable, label, col=None, num_bin=None, integer=True):
    """Plot histogram

    :param data: data to plot
    :type data: list
    :param integer: display only integers ticks
    :type integer: boolean
    """
    fig = plt.figure(figsize=(6, 5))
    plt.title(f"{label} (distribution)", fontsize=15, loc="left")

    if integer:
        fig.get_axes()[0].xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.hist(list(data[variable]), bins=num_bin, color="#8ec3f1")

    plt.xlabel(label, fontsize=12)
    plt.ylabel("Count", fontsize=12)
    sns.despine(left=True)
    plt.show()

    if col:
        g = sns.FacetGrid(data, col=col, col_wrap=4)
        g.map_dataframe(plt.hist, x=variable, color="#1E88E5", alpha=0.5)
        g.set_axis_labels(label, "Count")
        g.fig.suptitle(f"{label} distribution for each snapshot", fontsize=20)
        plt.subplots_adjust(top=0.9)

        sns.despine(left=True)
        plt.show()


def draw_snapshot_hist(data, variable, label, ground_truth=None):
    plt.figure(figsize=(6, 5))
    plt.title(
        f"{label} for each snapshot\n(generated vs groundtruth)",
        fontsize=15,
        loc="left",
    )

    plt.bar(
        x=data["snapshot"],
        height=data[variable],
        label="generated",
        color="#8ec3f1",
    )

    plt.xlabel("Snapshot", fontsize=12)
    plt.ylabel("Count", fontsize=12)

    if ground_truth is not None:
        plt.bar(
            x=ground_truth["snapshot"],
            height=ground_truth[variable],
            label="ground truth",
            color=(0, 0, 0, 0),
            ec="#D81B60",
        )
        plt.legend(loc="upper right")
        plt.title(
            f"{label} for each snapshot\n(generated vs groundtruth)",
            fontsize=15,
            loc="left",
        )
    else:
        plt.title(f"{label} for each snapshot", fontsize=15, loc="left")

    sns.despine(left=True)
    plt.show()


def draw_members(
    data, cmap=sns.cubehelix_palette(as_cmap=True), title="", center=None
):
    x = data["snapshots_online"].unique()
    x = [*range(max(x) + 1)]
    y = data["communities_visited"].unique()
    y = [*range(max(y), -1, -1)]  # seaborn heatmaps start top-left
    res = pd.DataFrame(
        0,
        index=y,
        columns=x,
    )
    for _, row in data.iterrows():
        res.loc[row["communities_visited"], row["snapshots_online"]] += 1

    sns.heatmap(res, cmap=cmap, center=center)

    plt.title(title, fontsize=15, loc="left")
    plt.xlabel("Count of active snapshots")
    plt.ylabel("Count of visited communities")

    sns.despine(left=True)
    plt.show()


def draw_members_comparison(data, ground_truth):
    fig, (ax1, ax2) = plt.subplots(figsize=(12, 5), ncols=2, sharey=True)
    cbar_ax = fig.add_axes([0.91, 0.11, 0.015, 0.77])

    # Generated data
    x1 = data["snapshots_online"].unique()
    x1 = [*range(max(x1) + 1)]
    y1 = data["communities_visited"].unique()
    y1 = [*range(max(y1), -1, -1)]  # seaborn heatmaps start top-left
    res1 = pd.DataFrame(
        0,
        index=y1,
        columns=x1,
    )
    for _, row in data.iterrows():
        res1.loc[row["communities_visited"], row["snapshots_online"]] += 1

    # Ground truth data
    x2 = ground_truth["snapshots_online"].unique()
    x2 = [*range(max(x2) + 1)]
    y2 = ground_truth["communities_visited"].unique()
    y2 = [*range(max(y2), -1, -1)]  # seaborn heatmaps start top-left
    res2 = pd.DataFrame(
        0,
        index=y2,
        columns=x2,
    )
    for _, row in ground_truth.iterrows():
        res2.loc[row["communities_visited"], row["snapshots_online"]] += 1

    # Min / Max values
    vmin = min(res1.values.min(), res2.values.min())
    vmax = max(res1.values.max(), res2.values.max())

    # Reshaping
    shapey_max = max(res1.shape[0], res2.shape[0])
    shapex_max = max(res1.shape[1], res2.shape[1])

    res1 = np.pad(
        res1,
        ((shapey_max - res1.shape[0], 0), (0, shapex_max - res1.shape[1])),
    )
    res1 = pd.DataFrame(res1, index=pd.RangeIndex(shapey_max - 1, -1, -1))

    res2 = np.pad(
        res2,
        ((shapey_max - res2.shape[0], 0), (0, shapex_max - res2.shape[1])),
    )
    res2 = pd.DataFrame(res2, index=pd.RangeIndex(shapey_max - 1, -1, -1))

    # Draw heatmap
    sns.heatmap(
        res1,
        cmap=sns.cubehelix_palette(as_cmap=True),
        ax=ax1,
        cbar=False,
        cbar_ax=cbar_ax,
        vmin=vmin,
        vmax=vmax,
    )
    sns.heatmap(
        res2,
        cmap=sns.cubehelix_palette(as_cmap=True),
        ax=ax2,
        cbar=True,
        cbar_ax=cbar_ax,
        vmin=vmin,
        vmax=vmax,
    )

    # Configure visuals
    # ax2.yaxis.tick_right()

    ax1.set_title("Generated data", fontsize=15, loc="left")
    ax2.set_title("Ground truth", fontsize=15, loc="left")

    ax1.set_xlabel("Count of active snapshots")
    ax2.set_xlabel("Count of active snapshots")
    ax1.set_ylabel("Count of visited communities")

    fig.subplots_adjust(wspace=0.1)
    fig.suptitle("Count of members", fontsize=15, x=0.5)

    sns.despine(left=True)
    plt.show()

    # Draw difference heatmap

    diverging_colorblind_palette = sns.color_palette(
        [
            "#053061",
            "#2166ac",
            "#4393c3",
            "#92c5de",
            "#d1e5f0",
            "#f7f7f7",
            "#fddbc7",
            "#f4a582",
            "#d6604d",
            "#b2182b",
            "#67001f",
        ]
    )

    df = (res1 - res2).sort_index(axis=0, ascending=False)
    sns.heatmap(df, cmap=diverging_colorblind_palette, center=0)

    plt.title(
        "Difference of count of members\n(generated - ground_truth)",
        fontsize=15,
        loc="left",
    )
    plt.xlabel("Count of active snapshots", fontsize=12)
    plt.ylabel("Count of visited communities", fontsize=12)

    sns.despine(left=True)
    plt.show()


def draw_emigrants(data, label_comparison="compared to"):
    plt.title(
        "Distribution of relative size of outgoing flows",
        fontsize=15,
        loc="left",
    )
    plt.ylabel("Relative size outgoing flow", fontsize=12)

    if len(data) == 0:
        pass
    elif "experiment" in data:
        sns.violinplot(
            data=data,
            x="experiment",
            y="relative_emigrants_flow",
            hue="experiment",
            split=False,
            inner="quart",
            linewidth=1,
            palette={"generated": "#8ec3f1", label_comparison: "#D81B60"},
        )
        plt.legend(loc="center")
    else:
        sns.violinplot(
            data=data,
            y="relative_emigrants_flow",
            color="#8ec3f1",
            split=False,
            inner="quart",
            linewidth=1,
        )

    sns.despine(left=True)
    plt.show()


def draw_comparison_expected(
    data, config, function, label, precision=50000, num_bin=10, integer=True
):
    """Plot histogram for given data and another according estimation
    from config file.

    Data and function should be coherent (same attribute).

    :param data: data to plot
    :type data: list
    :param function:
        function name in api (calling function defined in
        config file with constraint checks)
    :type function: string
    :param precision:
        number of function calls to average the results.
        Greater give better approximation
    :type precision: integer
    """
    # Distributions
    dist_generated = data
    dist_expected = np.array(
        [getattr(config, function)() for _ in range(precision)]
    )

    # Computing the bin properties (same for both distributions)
    min_v = min(min(dist_generated), min(dist_expected))
    max_v = max(max(dist_generated), max(dist_expected))
    bin_lims = np.linspace(min_v, max_v, num_bin + 1)
    bin_centers = 0.5 * (bin_lims[:-1] + bin_lims[1:])
    bin_widths = bin_lims[1:] - bin_lims[:-1]

    # Computing the histograms
    hist_generated, _ = np.histogram(dist_generated, bins=bin_lims)
    hist_expected, _ = np.histogram(dist_expected, bins=bin_lims)

    # Normalizing
    if np.max(hist_generated) != 0:
        hist_generated_norm = hist_generated / np.max(hist_generated)
    else:
        hist_generated_norm = hist_generated

    if np.max(hist_expected) != 0:
        hist_expected_norm = hist_expected / np.max(hist_expected)
    else:
        hist_expected_norm = hist_expected

    # Figure drawing
    fig = plt.figure(figsize=(6, 5))
    plt.title(f"{label} (generated vs expected)", fontsize=15, loc="left")

    if integer:
        fig.get_axes()[0].xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.bar(
        bin_centers,
        hist_generated_norm,
        width=bin_widths,
        align="center",
        label="generated",
        color="#8ec3f1",
    )
    plt.bar(
        bin_centers,
        hist_expected_norm,
        width=bin_widths,
        align="center",
        label="expected",
        color=(0, 0, 0, 0),
        ec="#D81B60",
    )

    plt.xlabel(label, fontsize=12)
    plt.ylabel("Normalized Count", fontsize=12)
    plt.legend(loc="upper right")

    sns.despine(left=True)
    plt.show()


def draw_comparison_groundtruth(
    data, gt_data, label, precision=50000, num_bin=10, integer=True
):
    """Plot histogram for given data and another according
    estimation from config file.

    Data and function should be coherent (same attribute).

    :param data: data to plot
    :type data: list
    :param function:
        function name in api (calling function
        defined in config file with constraint checks)
    :type function: string
    :param precision:
        number of function calls to average the results.
        Greater give better approximation
    :type precision: integer
    """
    # Distributions
    dist_generated = data
    dist_expected = gt_data

    # Computing the bin properties (same for both distributions)
    min_v = min(min(dist_generated), min(dist_expected))
    max_v = max(max(dist_generated), max(dist_expected))
    bin_lims = np.linspace(min_v, max_v, num_bin + 1)
    bin_centers = 0.5 * (bin_lims[:-1] + bin_lims[1:])
    bin_widths = bin_lims[1:] - bin_lims[:-1]

    # Computing the histograms
    hist_generated, _ = np.histogram(dist_generated, bins=bin_lims)
    hist_expected, _ = np.histogram(dist_expected, bins=bin_lims)

    # Figure drawing
    fig = plt.figure(figsize=(6, 5))
    plt.title(f"{label} (generated vs groundtruth)", fontsize=15, loc="left")

    if integer:
        fig.get_axes()[0].xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.bar(
        bin_centers,
        hist_generated,
        width=bin_widths,
        align="center",
        label="generated",
        color="#8ec3f1",
    )
    plt.bar(
        bin_centers,
        hist_expected,
        width=bin_widths,
        align="center",
        label="ground truth",
        color=(0, 0, 0, 0),
        ec="#D81B60",
    )

    plt.xlabel(label, fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.legend(loc="upper right")

    sns.despine(left=True)
    plt.show()


def csv_to_heatmap(data, events_list):
    # Initialize dataframe of events
    temp_list = []
    for event in events_list:
        temp_list.append([0, event, 0])

    catalog_df = pd.DataFrame(
        temp_list, columns=["time windows", "label", "count"]
    )

    df = data.copy()
    # Count number of events by time and label
    df["count"] = 0
    df = (
        df[["snapshot", "label", "count"]]
        .groupby(["snapshot", "label"])
        .count()
        .reset_index()
    )
    # Add catalog to normalize table if some events don't appear
    df = pd.concat([df, catalog_df])
    # Return heatmap table data
    return pd.pivot_table(
        df, values="count", index=["label"], columns="snapshot"
    ).fillna(0)


def draw_heatmap(
    data,
    diff=None,
    cmap=None,
    title="",
    x=16,
    y=3,
    ylabel=None,
    annot=False,
    vmin=None,
    vmax=None,
):
    # Check if we have to display and heatmap or the difference
    # between two heatmaps
    if diff is not None:
        data = data - diff
        center = 0
        # Diverging color palette
        if cmap is None:
            cmap = sns.color_palette(
                [
                    "#053061",
                    "#2166ac",
                    "#4393c3",
                    "#92c5de",
                    "#d1e5f0",
                    "#f7f7f7",
                    "#fddbc7",
                    "#f4a582",
                    "#d6604d",
                    "#b2182b",
                    "#67001f",
                ]
            )
    else:
        center = None
        if cmap is None:
            cmap = sns.cubehelix_palette(as_cmap=True)

    plt.figure(figsize=(x, y))
    g = sns.heatmap(
        data, cmap=cmap, annot=annot, center=center, vmin=vmin, vmax=vmax
    )
    g.set(ylabel=ylabel)
    g.set_title(title, fontsize=15, loc="left")
    g.xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x) + 1))
