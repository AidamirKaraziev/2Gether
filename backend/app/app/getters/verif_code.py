from app.schemas.verif_code import VerifCode


def get_verif_code(verif_code: VerifCode) -> VerifCode:
    return VerifCode(
        id=verif_code.id,
        value=verif_code.value,
        tel=verif_code.tel,
        created_at=verif_code.created_at,
        actual=verif_code.actual,
    )
