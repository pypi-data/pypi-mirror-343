from collections import defaultdict
from functools import partial
from itertools import count, cycle, product

from ..layout import Layout
from .util import is_valid, invert_shift, _check_distance


def get_data_index(row: int, col: int, col_size: int, start_ind: int = 1) -> int:
    """Converts row and column to data qubit index.

    The data qubits are numbered starting from the bottom-left data qubit,
    and increasing the index by 1 on the horizontal direction.
    Assumes the initial index is 1 (as opposed to 0).

    Parameters
    ----------
    row
        The row of the data qubit.
    col
        The column of the data qubit.
    col_size
        Column size of the code.
    start_ind
        The starting index for the data qubits, by default 1.

    Returns
    -------
    int
        The index of the data qubit.
    """
    row_ind = row // 2
    col_ind = col // 2
    index = start_ind + (row_ind * col_size) + col_ind
    return index


def shift_direction(row_shift: int, col_shift: int) -> str:
    """Translates a row and column shift to a direction.

    Parameters
    ----------
    row_shift
        The row shift.
    col_shift
        The column shift.

    Returns
    -------
    str
        The direction.
    """
    ver_direction = "north" if row_shift > 0 else "south"
    hor_direction = "east" if col_shift > 0 else "west"
    direction = f"{ver_direction}_{hor_direction}"
    return direction


def add_missing_neighbours(neighbor_data: dict) -> None:
    """Adds None for missing neighbours in the neighbor data.
    Note that this modifies the dictionary in place.

    Parameters
    ----------
    neighbor_data
        The neighbor data - a dictionary that contains information
        about the layout connectivity (defined on a square grid,
        connection run diagonally).
    """
    directions = ["north_east", "north_west", "south_east", "south_west"]
    for neighbors in neighbor_data.values():
        for direction in directions:
            if direction not in neighbors:
                neighbors[direction] = None
    return None


def rot_surface_code_rectangle(
    distance_x: int,
    distance_z: int,
    logical_qubit_label: str = "L0",
    init_point: tuple[int | float, int | float] = (1, 1),
    init_data_qubit_id: int = 1,
    init_zanc_qubit_id: int = 1,
    init_xanc_qubit_id: int = 1,
    init_ind: int = 0,
    init_logical_ind: int = 0,
) -> Layout:
    """Generates a rotated surface code layout.

    Parameters
    ----------
    distance_x
        The logical X distance of the code.
    distance_z
        The logical Z distance of the code.
    logical_qubit_label
        Label for the logical qubit, by default ``"L0"``.
    init_point
        Coordinates for the bottom left (i.e. southest west) data qubit.
        By default ``(1, 1)``.
    init_data_qubit_id
        Index for the bottom left (i.e. southest west) data qubit.
        By default ``1``, so the label is ``"D1"``.
    init_zanc_qubit_id
        Index for the bottom left (i.e. southest west) Z-type ancilla qubit.
        By default ``1``, so the label is ``"Z1"``.
    init_xanc_qubit_id
        Index for the bottom left (i.e. southest west) X-type ancilla qubit.
        By default ``1``, so the label is ``"X1"``.
    init_ind
        Minimum index that is going to be associated to a qubit.
    init_logical_ind
        Minimum index that is going to be associated to a logical qubit.

    Returns
    -------
    Layout
        The layout of the code.
    """
    _check_distance(distance_x)
    _check_distance(distance_z)
    if not isinstance(init_point, tuple):
        raise TypeError(
            f"'init_point' must be a tuple, but {type(init_point)} was given."
        )
    if (len(init_point) != 2) or any(
        not isinstance(p, (float, int)) for p in init_point
    ):
        raise TypeError(f"'init_point' must have two elements that are floats or ints.")
    if not isinstance(logical_qubit_label, str):
        raise TypeError(
            "'logical_qubit_label' must be a string, "
            f"but {type(logical_qubit_label)} was given."
        )
    if not isinstance(init_data_qubit_id, int):
        raise TypeError(
            "'init_data_qubit_id' must be an int, "
            f"but {type(init_data_qubit_id)} was given."
        )
    if not isinstance(init_zanc_qubit_id, int):
        raise TypeError(
            "'init_zanc_qubit_id' must be an int, "
            f"but {type(init_zanc_qubit_id)} was given."
        )
    if not isinstance(init_xanc_qubit_id, int):
        raise TypeError(
            "'init_xanc_qubit_id' must be an int, "
            f"but {type(init_xanc_qubit_id)} was given."
        )

    name = f"Rotated dx-{distance_x} dz-{distance_z} surface code layout."
    code = "rotated_surface_code"
    description = None

    freq_order = ["low", "mid", "high"]

    int_order = dict(
        x_type=["north_east", "north_west", "south_east", "south_west"],
        z_type=["north_east", "south_east", "north_west", "south_west"],
    )

    log_z = [f"D{i+init_data_qubit_id}" for i in range(distance_z)]
    log_x = [f"D{i*distance_z+init_data_qubit_id}" for i in range(distance_x)]
    logical_qubits = {
        logical_qubit_label: dict(log_x=log_x, log_z=log_z, ind=init_logical_ind)
    }

    layout_setup = dict(
        name=name,
        code=code,
        logical_qubits=logical_qubits,
        description=description,
        distance_x=distance_x,
        distance_z=distance_z,
        freq_order=freq_order,
        interaction_order=int_order,
    )
    if distance_x == distance_z:
        layout_setup["distance"] = distance_z

    col_size = 2 * distance_z + 1
    row_size = 2 * distance_x + 1
    data_indexer = partial(
        get_data_index, col_size=distance_z, start_ind=init_data_qubit_id
    )
    valid_coord = partial(is_valid, max_size_col=col_size, max_size_row=row_size)

    pos_shifts = (1, -1)
    nbr_shifts = tuple(product(pos_shifts, repeat=2))

    layout_data = []
    neighbor_data = defaultdict(dict)
    freq_seq = cycle(("low", "high"))
    ind = init_ind

    # change initial point because by default the code places the "D1" qubit
    # in the (1,1) point.
    init_point = (init_point[0] - 1, init_point[1] - 1)

    for row in range(1, row_size, 2):
        freq_group = next(freq_seq)
        for col in range(1, col_size, 2):
            index = data_indexer(row, col)

            qubit_info = dict(
                qubit=f"D{index}",
                role="data",
                coords=[row + init_point[0], col + init_point[1]],
                freq_group=freq_group,
                stab_type=None,
                ind=ind,
            )
            layout_data.append(qubit_info)

            ind += 1

    x_index = count(start=init_xanc_qubit_id)
    for row in range(0, row_size, 2):
        for col in range(2 + row % 4, col_size - 1, 4):
            anc_qubit = f"X{next(x_index)}"
            qubit_info = dict(
                qubit=anc_qubit,
                role="anc",
                coords=[row + init_point[0], col + init_point[1]],
                freq_group="mid",
                stab_type="x_type",
                ind=ind,
            )
            layout_data.append(qubit_info)

            ind += 1

            for row_shift, col_shift in nbr_shifts:
                data_row, data_col = row + row_shift, col + col_shift
                if not valid_coord(data_row, data_col):
                    continue
                data_index = data_indexer(data_row, data_col)
                data_qubit = f"D{data_index}"

                direction = shift_direction(row_shift, col_shift)
                neighbor_data[anc_qubit][direction] = data_qubit

                inv_shifts = invert_shift(row_shift, col_shift)
                inv_direction = shift_direction(*inv_shifts)
                neighbor_data[data_qubit][inv_direction] = anc_qubit

    z_index = count(start=init_zanc_qubit_id)
    for row in range(2, row_size - 1, 2):
        for col in range(row % 4, col_size, 4):
            anc_qubit = f"Z{next(z_index)}"
            qubit_info = dict(
                qubit=anc_qubit,
                role="anc",
                coords=[row + init_point[0], col + init_point[1]],
                freq_group="mid",
                stab_type="z_type",
                ind=ind,
            )
            layout_data.append(qubit_info)

            ind += 1

            for row_shift, col_shift in nbr_shifts:
                data_row, data_col = row + row_shift, col + col_shift
                if not valid_coord(data_row, data_col):
                    continue
                data_index = data_indexer(data_row, data_col)
                data_qubit = f"D{data_index}"

                direction = shift_direction(row_shift, col_shift)
                neighbor_data[anc_qubit][direction] = data_qubit

                inv_shifts = invert_shift(row_shift, col_shift)
                inv_direction = shift_direction(*inv_shifts)
                neighbor_data[data_qubit][inv_direction] = anc_qubit

    add_missing_neighbours(neighbor_data)

    for qubit_info in layout_data:
        qubit = qubit_info["qubit"]
        qubit_info["neighbors"] = neighbor_data[qubit]

    layout_setup["layout"] = layout_data
    layout = Layout(layout_setup)
    return layout


def rot_surface_code(
    distance: int,
    logical_qubit_label: str = "L0",
    init_point: tuple[int | float, int | float] = (1, 1),
    init_data_qubit_id: int = 1,
    init_zanc_qubit_id: int = 1,
    init_xanc_qubit_id: int = 1,
    init_ind: int = 0,
    init_logical_ind: int = 0,
) -> Layout:
    """Generates a rotated surface code layout.

    Parameters
    ----------
    distance
        The distance of the code.
    logical_qubit_label
        Label for the logical qubit, by default ``"L0"``.
    init_point
        Coordinates for the bottom left (i.e. southest west) data qubit.
        By default ``1``, so the label is ``"D1"``.
    init_data_qubit_id
        Index for the bottom left (i.e. southest west) data qubit.
        By default ``1``, so the label is ``"D1"``.
    init_zanc_qubit_id
        Index for the bottom left (i.e. southest west) Z-type ancilla qubit.
        By default ``1``, so the label is ``"Z1"``.
    init_xanc_qubit_id
        Index for the bottom left (i.e. southest west) X-type ancilla qubit.
        By default ``1``, so the label is ``"X1"``.
    init_ind
        Minimum index that is going to be associated to a qubit.
    init_logical_ind
        Minimum index that is going to be associated to a logical qubit.

    Returns
    -------
    Layout
        The layout of the code.
    """
    return rot_surface_code_rectangle(
        distance_x=distance,
        distance_z=distance,
        logical_qubit_label=logical_qubit_label,
        init_point=init_point,
        init_data_qubit_id=init_data_qubit_id,
        init_zanc_qubit_id=init_zanc_qubit_id,
        init_xanc_qubit_id=init_xanc_qubit_id,
        init_ind=init_ind,
        init_logical_ind=init_logical_ind,
    )
