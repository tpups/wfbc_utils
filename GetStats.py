from decimal import Decimal


hCats = ['2B','3B','AB','AVG','BB','CS','GP','H','HBP','HR','K','OPS','PA','R','RBI','SB','SF']
pCats = ['BB','BS','ER','ERA','GP','H','HB','HR','IP','K','L','QS','R','SV','W','WHIP','WP']

# Hitting
#############

def getAVG(H, AB):
    AVG = 0
    if AB > 0:
        AVG = Decimal(H / AB)
    # print("AVG: " + str(AVG))
    return AVG

def getOBP(AB, H, BB, HBP, SF):
    OBP = 0
    if (AB + BB + SF + HBP) > 0:
        OBP = Decimal((H + BB + HBP) / (AB + BB + SF + HBP))
    # print("OBP: " + str(OBP))
    return OBP

def getSLG(totalBases, AB):
    SLG = 0
    if AB > 0:
        SLG = Decimal(totalBases / AB)
    # print("SLG: " + str(SLG))
    return SLG

def getOPS(OBP, SLG):
    OPS = Decimal(OBP + SLG)
    # print("OPS: " + str(OPS))
    return OPS

def getTotalBases(H, _2B, _3B, HR):
    _1B = H - _2B - _3B - HR
    if _1B < 0:
        return "bad hits value"
    totalBases = _1B + 2 * _2B + 3 *_3B + 4 * HR
    # print("Total Bases: " + str(totalBases))
    return totalBases

def getAtBats():
    return

# Pitching
#############

def getERA(ER, IP):
    ERA = 0
    if IP > 0:
        ERA = Decimal(9 * (ER / IP))
    elif IP == 0 and ER > 0:
        ERA = 99999
    # print("ERA: " + str(ERA))
    return ERA

def getWHIP(H, BB, IP):
    WHIP = 0
    if IP > 0:
        WHIP = Decimal((BB + H) / IP)
    elif IP == 0 and (BB + IP) > 0:
        WHIP = 99999
    # print("WHIP: " + str(WHIP))
    return WHIP

def getFIPConstant(lgERA, lgHR, lgBB, lgHBP, lgK, lgIP):
    constant = lgERA - ( ( ( 13 * lgHR ) + ( 3 * ( lgBB + lgHBP ) ) - ( 2 * lgK ) ) / lgIP )
    # print("FIP Constant: " + str(constant))
    return constant

def getFIP(IP, HR, BB, HBP, K, FIP_constant):
    FIP = ( 13 * HR + 3 * ( BB + HBP ) - 2 * K ) / IP + FIP_constant
    # print("FIP: " + str(FIP))
    return FIP

def getxFIP(flyBalls, lgHrFbPct, BB, HBP, K, IP, FIP_constant):
    xFIP = ( ( 13 * ( flyBalls * lgHrFbPct ) ) + ( 3 * ( BB + HBP ) ) - ( 2 * K ) ) / IP + FIP_constant
    # print("xFIP: " + str(xFIP))
    return xFIP


# stats as of 9/21
# lgHR = 2050
# lgBB = 5432
# lgHBP = 744
# lgK = 13775
# lgIP = 13719.1
# lgERA = 4.46
# lgHrFbPct = 0.148

# OBP = getOBP(10, 3, 1, 0, 0)
# TB = getTotalBases(10, 2, 0, 0)
# SLG = getSLG(TB, 40)
# OPS = getOPS(OBP, SLG)
# AVG = getAVG(4, 13)
# ERA = getERA(3, 15)
# WHIP = getWHIP(3, 1, 5)

# FIP_constant = getFIPConstant(lgERA, lgHR, lgBB, lgHBP, lgK, lgIP)
# print("Gallen:")
# FIP = getFIP(66, 9, 23, 2, 72, FIP_constant)
# xFIP = getxFIP(59, lgHrFbPct, 23, 2, 72, 66, FIP_constant)