# tests/test_imports.py

def test_core_and_tasks_imports():
    import skvai
    import skvai.core
    import skvai.data_loader
    import skvai.tasks.classification
    import skvai.tasks.regression
    import skvai.tasks.clustering

    assert True

