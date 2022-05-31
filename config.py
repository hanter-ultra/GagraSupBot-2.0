from enum import Enum

Token = '5332316874:AAG0dDTY4CMkWXoZs_80Swmc0uuQ_LiFszw'
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