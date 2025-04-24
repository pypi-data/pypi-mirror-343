import pandas as pd
import pytest
from skvai.data_loader import DataLoader, load_data

def test_load_csv_valid(tmp_path, capsys):
    # Create a small CSV
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    csv_file = tmp_path / "test.csv"
    df.to_csv(csv_file, index=False)

    loader = DataLoader()
    result = loader.load_csv(str(csv_file))
    assert isinstance(result, pd.DataFrame)
    # DataFrame equality
    pd.testing.assert_frame_equal(result, df)

    # Check the success message
    captured = capsys.readouterr()
    assert "[✔] CSV data loaded successfully." in captured.out

    # Also test the shortcut function
    df2 = load_data(str(csv_file))
    pd.testing.assert_frame_equal(df2, df)

def test_load_csv_invalid(tmp_path, capsys):
    loader = DataLoader()
    result = loader.load_csv(str(tmp_path / "does_not_exist.csv"))
    assert result is None
    captured = capsys.readouterr()
    assert "[✘] Failed to load CSV" in captured.out

def test_preview_and_no_data(capsys):
    loader = DataLoader()
    # No data loaded yet
    assert loader.preview() is None
    captured = capsys.readouterr()
    assert "[!] No data loaded yet." in captured.out

    # After loading
    df = pd.DataFrame({"x": range(10)})
    loader.data = df
    preview = loader.preview(rows=3)
    assert isinstance(preview, pd.DataFrame)
    assert len(preview) == 3
    pd.testing.assert_frame_equal(preview, df.head(3))
