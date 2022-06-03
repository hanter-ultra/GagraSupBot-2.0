from enum import Enum

Token = '5332316874:AAHNJkx4dGVav73dzDlwS22Th9vU5Px3EIk'
admins = [993699116, 490371324]
#490371324
#993699116

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