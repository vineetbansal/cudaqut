from pathlib import Path
import numpy as np
import cupy as cp


def get_module():
    # This operation is expensive - call it as few times as possible.
    # We declare a global variable `cp_module` to store the compiled module.
    with open(Path(__file__).parent / "simple.cu") as f:
        code = f.read()
    return cp.RawModule(code=code)


cp_module = get_module()


def matrix_add(a: np.array, b: np.array):
    assert a.shape == b.shape
    rows, cols = a.shape

    matrix_add = cp_module.get_function("matrixAdd")
    threads_per_block = 16, 16
    blocks_per_grid = (
        (rows + (threads_per_block[0] - 1)) // threads_per_block[0],
        (cols + (threads_per_block[1] - 1)) // threads_per_block[1],
    )

    result = cp.zeros((rows, cols)).astype(a.dtype)
    matrix_add(
        blocks_per_grid,
        threads_per_block,
        (
            cp.asarray(a),
            cp.asarray(b),
            cp.asarray(result),
            np.int32(rows),
            np.int32(cols),
        ),
    )
    return cp.asnumpy(result)


def matrix_subtract(a: np.array, b: np.array):
    assert a.shape == b.shape
    rows, cols = a.shape

    matrix_add = cp_module.get_function("matrixSubtract")
    threads_per_block = 16, 16
    blocks_per_grid = (
        (rows + (threads_per_block[0] - 1)) // threads_per_block[0],
        (cols + (threads_per_block[1] - 1)) // threads_per_block[1],
    )

    result = cp.zeros((rows, cols)).astype(a.dtype)
    matrix_add(
        blocks_per_grid,
        threads_per_block,
        (
            cp.asarray(a),
            cp.asarray(b),
            cp.asarray(result),
            np.int32(rows),
            np.int32(cols),
        ),
    )
    return cp.asnumpy(result)
