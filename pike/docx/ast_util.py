from markdown_it.token import Token


def check_has_next(ast: list[Token], next_idx: int) -> bool:
    try:
        ast[next_idx]
    except IndexError:
        return False
    else:
        return True


def get_up_to_token(
    ast: list[Token],
    *,
    end_token_type: str,
    current_idx: int = 0,
) -> list[Token]:
    """Given an AST with a starting position, walk the AST and return up to a given tag.

    Parameters
    ----------
    ast: list[Token]
        The AST
    current_idx: int
        Where to start looking, defaults to 0
    end_token_type: str
        The token type to match on and return to inclusive.

        Will return on the first found instance.

    Returns
    -------
    list[Token]
        The new smaller list.
    """
    data: list[Token] = []
    current_token_index = current_idx
    while check_has_next(ast, current_token_index):
        current_token: Token = ast[current_token_index]
        data.append(current_token)
        current_token_index += 1

        if current_token.type == end_token_type:
            break

    return data
