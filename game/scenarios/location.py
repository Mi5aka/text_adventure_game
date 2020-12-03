from states import States


class Location(object):
    OFFICE = 'Офис компании'
    HOME = 'Твоя квартира'
    ENTERANCE = 'Подъезд'


def get_location(state: str) -> str:
    if state in (
        States.BACK_TO_OFFICE,
        States.PULL_REQUEST,
        States.MIMICRY
    ):
        return Location.OFFICE
    elif state == States.FIRST_MEETING:
        return Location.ENTERANCE
    return Location.HOME