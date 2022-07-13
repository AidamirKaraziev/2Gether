from app.schemas.token import TokenBase


def get_token(token: TokenBase) -> TokenBase:
    return TokenBase(
        token=token.token
    )
