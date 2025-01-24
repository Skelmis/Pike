from pike.docx import commands


def test_create_command_str():
    r_1 = commands.create_command_string("test")
    assert r_1 == f"<{commands.MARKER} test ARGS KWARGS>"

    r_2 = commands.create_command_string("test", "arg")
    assert r_2 == f"<{commands.MARKER} test ARGS {commands._b64_encode('arg')} KWARGS>"

    r_3 = commands.create_command_string("test", 1)
    assert r_3 == f"<{commands.MARKER} test ARGS {commands._b64_encode('1')} KWARGS>"


def test_parse_command_str():
    r_1_str = f"<{commands.MARKER} test ARGS KWARGS>"
    r_1 = commands.parse_command_string(r_1_str)
    assert r_1 == commands.Command(command="test", arguments=[], keyword_arguments={})

    r_2_str = f"<{commands.MARKER} test ARGS {commands._b64_encode('test')} KWARGS>"
    r_2 = commands.parse_command_string(r_2_str)
    assert r_2 == commands.Command(
        command="test", arguments=["test"], keyword_arguments={}
    )

    kw = commands._b64_encode(f"test|{commands._b64_encode('test')}")
    r_3_str = f"<{commands.MARKER} test ARGS KWARGS {kw}>"
    r_3 = commands.parse_command_string(r_3_str)
    assert r_3 == commands.Command(
        command="test", arguments=[], keyword_arguments={"test": "test"}
    )


def test_split_str_into_command_blocks():
    r_1_str = "Hi!"
    r_1 = commands.split_str_into_command_blocks(r_1_str)
    assert r_1 == ["Hi!"]

    r_2_str = commands.create_command_string("test")
    r_2 = commands.split_str_into_command_blocks(r_2_str)
    assert isinstance(r_2, list)
    assert isinstance(r_2[0], commands.Command)
    assert len(r_2) == 1

    r_3_str = (
        "<MARK-807e2383866d289f54e35bb8b2f2918c insert_text "
        "ARGS SGkgSSBhbSA= KWARGS> <MARK-807e2383866d289f54e35bb8b2f2918c "
        "insert_text ARGS aXRhbGljICsgYm9sZA== KWARGS Ym9sZHxWSEoxWlE9PQ== "
        "aXRhbGljfFZISjFaUT09> <MARK-807e2383866d289f54e35bb8b2f2918c insert_text "
        "ARGS YW5k KWARGS> <MARK-807e2383866d289f54e35bb8b2f2918c insert_text ARGS "
        "aW5saW5l KWARGS aW5saW5lfFZISjFaUT09>"
    )
    r_3 = commands.split_str_into_command_blocks(r_3_str)
    assert isinstance(r_3, list)
    assert len(r_3) == 7
    assert isinstance(r_3[0], commands.Command)
    assert isinstance(r_3[1], str)
    assert isinstance(r_3[2], commands.Command)
    assert isinstance(r_3[3], str)
    assert isinstance(r_3[4], commands.Command)
    assert isinstance(r_3[5], str)
    assert isinstance(r_3[6], commands.Command)
