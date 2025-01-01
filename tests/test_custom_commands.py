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

    r_3_str = (
        f"<{commands.MARKER} test ARGS KWARGS test|{commands._b64_encode('test')}>"
    )
    r_3 = commands.parse_command_string(r_3_str)
    assert r_3 == commands.Command(
        command="test", arguments=[], keyword_arguments={"test": "test"}
    )
