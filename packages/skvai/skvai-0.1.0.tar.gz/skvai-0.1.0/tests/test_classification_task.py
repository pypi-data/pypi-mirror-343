import pandas as pd
import pytest
from skvai.tasks.classification import Task

def make_csv(tmp_path, df, name="data.csv"):
    path = tmp_path / name
    df.to_csv(path, index=False)
    return str(path)

def test_classification_load_and_default_target(tmp_path, capsys):
    # Last column should be picked as target by default
    df = pd.DataFrame({
        "feat1": [0.1, 0.2, 0.3, 0.4],
        "feat2": [1, 0, 1, 0],
        "label": [0, 1, 0, 1],
    })
    csv_path = make_csv(tmp_path, df)
    task = Task()

    task.load_data(csv_path)
    # Data should be loaded
    assert hasattr(task, "data") and isinstance(task.data, pd.DataFrame)
    # Default target is the last column name
    assert task.target == "label"
    # Check no rows were dropped (all labels non-null)
    assert task.data.shape == df.shape

def test_classification_set_target_override(tmp_path):
    # Override user_target before loading
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6],
        "outcome": [1, 0, 1],
    })
    csv_path = make_csv(tmp_path, df)
    task = Task()
    task.set_target("outcome")
    task.load_data(csv_path)
    assert task.target == "outcome"
    # Data still matches
    pd.testing.assert_frame_equal(
        task.data.sort_index(axis=1),
        df.sort_index(axis=1)
    )

def test_classification_bad_target(tmp_path):
    # Setting a non-existent target should raise
    df = pd.DataFrame({"x": [1, 2], "y": [0, 1]})
    csv_path = make_csv(tmp_path, df)
    task = Task()
    task.set_target("no_such_column")
    with pytest.raises(ValueError):
        task.load_data(csv_path)
