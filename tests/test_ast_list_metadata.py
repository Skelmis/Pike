from pike.docx import Variables, CurrentListNesting, List


def test_lists_add():
    variables: Variables = Variables()
    assert len(variables.current_lists) == 0

    variables.add_list("ordered", CurrentListNesting.LEVEL_1)
    assert len(variables.current_lists) == 1
    assert variables.get_current_list() == List("ordered", CurrentListNesting.LEVEL_1)


# noinspection DuplicatedCode
def test_manual_nesting():
    variables: Variables = Variables()

    """
    We want to mimic the following structure:
    
    1. One
        - Two
        - Three
    2. Four
        - Five
            - Six
    """
    variables.add_list("ordered", CurrentListNesting.LEVEL_1)
    variables.add_list("bullet", CurrentListNesting.LEVEL_2)
    variables.add_list("bullet", CurrentListNesting.LEVEL_2)
    variables.add_list("ordered", CurrentListNesting.LEVEL_1)
    variables.add_list("bullet", CurrentListNesting.LEVEL_2)
    variables.add_list("bullet", CurrentListNesting.LEVEL_3)

    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_3)
    variables.remove_current_list()
    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_2)
    variables.remove_current_list()
    assert variables.get_current_list() == List("ordered", CurrentListNesting.LEVEL_1)
    variables.remove_current_list()
    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_2)
    variables.remove_current_list()
    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_2)
    variables.remove_current_list()
    assert variables.get_current_list() == List("ordered", CurrentListNesting.LEVEL_1)
    variables.remove_current_list()
    assert variables.get_current_list() is None


# noinspection DuplicatedCode
def test_automatic_nesting():
    variables: Variables = Variables()

    """
    We want to mimic the following structure:

    1. One
        - Two
        - Three
    2. Four
        - Five
            - Six
    """
    # This better mimics the expected flow
    variables.add_list("ordered")
    variables.add_nesting()
    variables.add_list("bullet")
    variables.add_list("bullet")
    variables.remove_nesting()
    variables.add_list("ordered")
    variables.add_nesting()
    variables.add_list("bullet")
    variables.add_nesting()
    variables.add_list("bullet")

    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_3)
    variables.remove_current_list()
    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_2)
    variables.remove_current_list()
    assert variables.get_current_list() == List("ordered", CurrentListNesting.LEVEL_1)
    variables.remove_current_list()
    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_2)
    variables.remove_current_list()
    assert variables.get_current_list() == List("bullet", CurrentListNesting.LEVEL_2)
    variables.remove_current_list()
    assert variables.get_current_list() == List("ordered", CurrentListNesting.LEVEL_1)
    variables.remove_current_list()
    assert variables.get_current_list() is None
