from enum import Enum

Token = ''
admins = []

db_file = "database.vdb"

class States(Enum):
    S_START = '0'
    SendClaim = '1'
    WFMesT = '2'
    NewEventName = '3'
    NewEventText = '4'
    NewEventPrice = '5'

    EditNameEvent = '6'
    EditTextEvent = '7'
    EditPriceEvent = '8'