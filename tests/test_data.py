from hemlock import Data
from hemlock.app import create_test_app

VARIABLE_NAME = "variable_name"
DATA = 1

app = create_test_app()


def test_repr():
    data = Data(VARIABLE_NAME, DATA)
    assert repr(data) == f"<Data {VARIABLE_NAME} {DATA}>"


def test_basic_packing():
    data = Data(VARIABLE_NAME, DATA)
    assert data.pack_data() == {VARIABLE_NAME: [DATA]}


def test_nrows_packing():
    n_rows = 3
    data = Data(VARIABLE_NAME, DATA, n_rows=n_rows)
    assert data.pack_data() == {VARIABLE_NAME: n_rows * [DATA]}


def test_list_packing():
    data_list = [0, 1, 2]
    data = Data(VARIABLE_NAME, data_list)
    assert data.pack_data() == {VARIABLE_NAME: data_list}


def test_index_packing():
    n_rows = 3
    data = Data(VARIABLE_NAME, DATA, n_rows=n_rows, record_index=True)
    assert data.pack_data() == {
        VARIABLE_NAME: n_rows * [DATA],
        f"{VARIABLE_NAME}_index": n_rows * [None]
    }
