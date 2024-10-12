from pike import Engine


def test_find_all_files(set_test_directory_to_example_report, example_report_dir):
    engine = Engine.load_from_directory(example_report_dir)
    assert len(engine.files) == 0
    assert engine._layout_file is None

    engine.locate_all_files()

    assert len(engine.files) == 3
    assert engine._layout_file is not None
