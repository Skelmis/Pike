from pike.docx import commands

def test_create_command_str():
    r_1 = commands.create_command_string("test")
    assert r_1 == f"<{commands.MARKER} test>"

    r_2 = commands.create_command_string("test", "arg")
    assert r_2 == f"<{commands.MARKER} test {commands.b64encode('arg'.encode()).hex()}>"

    r_3 = commands.create_command_string("test", 1)
    assert r_3 == f"<{commands.MARKER} test {commands.b64encode('1'.encode()).hex()}>"

def test_parse_command_str():
    r_1_str = f"<{commands.MARKER} test>"
    r_1 = commands.parse_command_string(r_1_str)
    assert r_1 == commands.Command(command="test", arguments=[])