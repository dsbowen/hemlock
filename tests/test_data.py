from hemlock import Data

VARIABLE_NAME = "variable_name"
DATA = 1


def test_repr():
    assert repr(Data(VARIABLE_NAME, DATA)) == f"<Data {VARIABLE_NAME} {DATA}>"


def test_basic_packing():
    assert Data(VARIABLE_NAME, DATA).pack_data() == {VARIABLE_NAME: [DATA]}


def test_no_variable():
    assert Data().pack_data() == {}


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
        f"{VARIABLE_NAME}_index": n_rows * [None],
    }
