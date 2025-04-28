import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle, PathPatch, Patch
from matplotlib.ticker import FixedLocator

from ._types import AcceptedColors, CurveType
from ._utils import _clean_axis, _generate_cmap
from ._patches import patch_curve3, patch_curve4, patch_line


def sankey(
    data: list[list[tuple[int | str, int | str, float | int]]],
    figsize: tuple[int, int] | None = None,
    frameon: bool = False,
    ax: Axes | None = None,
    spacing: float = 0.00,
    annotate_columns: bool = False,
    rel_column_width: float = 0.15,
    cmap: AcceptedColors = "tab10",
    curve_type: CurveType = "curve4",
    ribbon_alpha: float = 0.2,
    ribbon_color: str = "black",
    title: str | None = None,
    show: bool = True,
    show_legend: bool = False,
    legend_labels: list[str] | None = None,
    column_labels: list[str] | None = None,
) -> Axes:
    """Sankey plot.

    Args:
        data (list[list[tuple[int | str, int | str, float | int]]]): Input data.
        figsize (tuple[int, int] | None): Size of figure. Defaults to `None`.
        frameon (bool, optional): Draw frame. Defaults to `True`.
        ax (matplotlib.Axes | None, optional): Provide matplotlib Axes instance for plotting. Defaults to `None`.
        spacing (float, optional): Spacing between column and ribbon patches. Defaults to `0.0`.
        annotate_columns (bool, optional): Annotate columns of plot. Defaults to `False`.
        rel_column_width (float, optional): Relative width of columns compared to ribbons. Defaults to `0.15`. Value must be between 0 and 1.
        cmap (Sequence[str] | Colormap | str | Sequence[tuple[float, float, float]], optional): Colors or colormap for columns.
        curve_type (Literal["curve3", "curve4", "line"], optional): Curve type ofo ribbon. Defaults to `"curve4"`.
        ribbon_alpha (float, optional): Alpha of ribbons. Defaults to `0.2`.
        ribbon_color (str, optional): Color of ribbons. Defaults to `"black"`.
        title (str | None, optional): Title of figure. Defaults to `None`.
        show (bool, optional): Show figure. Defaults to `True`.
        show_legend (bool, optional): Show legend. Defaults to `False`. If legend should be displayed, also provide `legend_labels`.
        legend_labels (list[str] | None, optional): Labels to display in legend. Defaults to `None`.
        column_labels (list[str] | None, optional): Labels for columns. Defaults to `None`.

    Returns:
        Matplotlib axes instance.

    ReturnType:
        matplitlib.Axes

    """
    assert rel_column_width > 0 and rel_column_width < 1, (
        "Value for parameter 'rel_column_width' must be between 0 and 1."
    )

    if ax is None:
        _, ax = plt.subplots(figsize=figsize, frameon=frameon)

    ncols = len(data) + 1

    ax = _clean_axis(ax, frameon=frameon)

    ax.set_ylim(0.0, 1.0)
    ax.set_xlim(-1 * (rel_column_width / 2), (ncols - 1) + (rel_column_width / 2))

    if column_labels is not None:
        ax.xaxis.set_major_locator(FixedLocator(list(range(ncols))))

    # Prepare data
    column_weights: list[dict[int | str, int | float]] = [{} for _ in range(ncols)]

    cmap = _generate_cmap(cmap, 20)

    for frame_index, frame in enumerate(data):
        for source_index, target_index, weight in frame:
            if column_weights[frame_index] is None:
                column_weights[frame_index] = {
                    source_index: weight,
                }
            else:
                column_weights[frame_index][source_index] = column_weights[frame_index].get(source_index, 0) + weight

            if frame_index == len(data) - 1:
                # Add weights for last column
                if column_weights[frame_index + 1] is None:
                    column_weights[frame_index + 1] = {
                        target_index: weight,
                    }
                else:
                    column_weights[frame_index + 1][target_index] = (
                        column_weights[frame_index + 1].get(target_index, 0) + weight
                    )

    # Plot rectangles
    column_rects: list[dict[int | str, tuple[float, float, float, float]]] = [{} for _ in range(ncols)]
    rect_num = 0

    legend_handles: list[tuple[str, tuple[float, float, float, float]]] = []

    for frame_index in range(ncols):
        column_total_weight = sum(column_weights[frame_index].values())
        column_prev_weight = 0.0

        column_n_spacing = len(column_weights[frame_index].values()) - 1

        spacing_scale_factor = 1 - (spacing * column_n_spacing)

        for column_index, (column_key, weights) in enumerate(column_weights[frame_index].items()):
            rect_x = frame_index - (rel_column_width / 2)
            rect_y = column_prev_weight / column_total_weight + (column_index * spacing)
            rect_height = (weights * spacing_scale_factor) / column_total_weight

            column_prev_weight += weights * spacing_scale_factor

            rect = Rectangle(
                xy=(
                    rect_x,
                    rect_y,
                ),
                width=rel_column_width,
                height=rect_height,
                color=cmap(rect_num),
                zorder=1,
                lw=0,
            )
            ax.add_patch(rect)

            # Save in lookup dict
            if column_rects[frame_index] is None:
                column_rects[frame_index] = {column_key: (rect_x, rect_y, rel_column_width, rect_height)}
            else:
                column_rects[frame_index][column_key] = (rect_x, rect_y, rel_column_width, rect_height)

            if annotate_columns is True:
                ax.text(
                    x=rect_x + (rel_column_width / 2),
                    y=rect_y + (rect_height / 2),
                    s=str(column_key),
                    ha="center",
                    va="center",
                )

            legend_handles.append((str(column_key), cmap(rect_num)))

            rect_num += 1

    # Plot ribbons

    for frame_index in range(ncols - 1):
        target_ribbon_offset: dict[int | str, int | float] = {}

        for column_key in column_weights[frame_index].keys():
            # print(column_key)
            # Source rect dimensions
            rect_x, rect_y, _, rect_height = column_rects[frame_index][column_key]

            # Get all connection targets
            column_targets: dict[int | str, float | int] = {}
            for source, target, connection_weights in data[frame_index]:
                if source == column_key:
                    column_targets[target] = connection_weights

            ribbon_offset: float = 0.0

            for target_index, ribbon_weight in column_targets.items():
                # Start coords
                y1_start = rect_y + +(rect_height * (ribbon_offset / sum(column_targets.values())))
                y2_end = rect_y + (rect_height * ((ribbon_offset + ribbon_weight) / sum(column_targets.values())))

                ribbon_offset += ribbon_weight

                _, target_rect_y, _, target_rect_height = column_rects[frame_index + 1][target_index]

                # End coords
                y1_end = target_rect_y + (
                    target_rect_height
                    * (target_ribbon_offset.get(target_index, 0) / column_weights[frame_index + 1][target_index])
                )
                y2_start = target_rect_y + (
                    target_rect_height
                    * (
                        (ribbon_weight + target_ribbon_offset.get(target_index, 0))
                        / column_weights[frame_index + 1][target_index]
                    )
                )

                target_ribbon_offset[target_index] = target_ribbon_offset.get(target_index, 0) + ribbon_weight

                poly: PathPatch

                if curve_type == "curve4":
                    poly = patch_curve4(
                        x_start=frame_index + (rel_column_width / 2),
                        x_end=frame_index + 1 - (rel_column_width / 2),
                        y1_start=y1_start,
                        y1_end=y1_end,
                        y2_start=y2_start,
                        y2_end=y2_end,
                        row_index=0,
                        alpha=ribbon_alpha,
                        color=ribbon_color,
                        spacing=0,
                    )
                elif curve_type == "curve3":
                    poly = patch_curve3(
                        x_start=frame_index + (rel_column_width / 2),
                        x_end=frame_index + 1 - (rel_column_width / 2),
                        y1_start=y1_start,
                        y1_end=y1_end,
                        y2_start=y2_start,
                        y2_end=y2_end,
                        row_index=0,
                        alpha=ribbon_alpha,
                        color=ribbon_color,
                        spacing=0,
                    )
                elif curve_type == "line":
                    poly = patch_line(
                        x_start=frame_index + (rel_column_width / 2),
                        x_end=frame_index + 1 - (rel_column_width / 2),
                        y1_start=y1_start,
                        y1_end=y1_end,
                        y2_start=y2_start,
                        y2_end=y2_end,
                        row_index=0,
                        alpha=ribbon_alpha,
                        color=ribbon_color,
                        spacing=0,
                    )
                else:
                    raise ValueError(f"curve_type '{curve_type}' not supported.")

                ax.add_patch(poly)

    if show_legend is True:
        legend_patches = []
        for handle_index, (label, color) in enumerate(legend_handles):
            if legend_labels is None:
                legend_patches.append(Patch(facecolor=color, label=label))
            else:
                legend_patches.append(Patch(facecolor=color, label=legend_labels[handle_index]))

        ax.legend(
            handles=legend_patches,
            frameon=False,
            bbox_to_anchor=(1, 1),
            loc="upper left",
        )

    if title is not None:
        ax.set_title(title)

    if show is False:
        plt.close()
    # else:
    #     plt.show()

    if column_labels is not None:
        assert len(column_labels) == ncols
        ax.set_xticklabels(column_labels)
    # else:
    #     ax.set_xticklabels(None)
    #     ax.set_xticks([])

    return ax
