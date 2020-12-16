import cv2


MTL = 'LE07_L1TP_199026_20020830_20170214_01_T1_MTL.txt'

B1 = 'LE07_L1TP_199026_20020830_20170214_01_T1_B1.tif'
B3 = 'LE07_L1TP_199026_20020830_20170214_01_T1_B3.tif'
B4 = 'LE07_L1TP_199026_20020830_20170214_01_T1_B4.tif'

P_UL = 1681, 21
P_UR = 7901, 1445
P_LL = 41,5936
P_LR = 6254, 7374

def parse(word):
    inp = open(MTL).readlines()
    for i in iter(inp):
        if word in i:
            original = i[4:]
            return float(original.replace(word + " = ", ""))

def calcPointBetweenTo(p1, p2, k):

    y = p1[1] + (p2[1] - p1[1]) * k
    x = -((p2[0] - p1[0]) * y + (p1[0] * p2[1] - p2[0] * p1[1])) / (p1[1] - p2[1])
    return (int(x), int(y))

def ParallelogramRule(zero, x, y):

    return int(x[0] + y[0] - zero[0]),int( x[1] + y[1] - zero[1])

PARIS = 48.84302835299519,2.3510742187500004

COORD_UL = parse('CORNER_UL_LON_PRODUCT'), parse('CORNER_UL_LAT_PRODUCT')
COORD_UR = parse('CORNER_UR_LON_PRODUCT'), parse('CORNER_UR_LAT_PRODUCT')
COORD_LL = parse('CORNER_LL_LON_PRODUCT'), parse('CORNER_LL_LAT_PRODUCT')
COORD_LR = parse('CORNER_LR_LON_PRODUCT'), parse('CORNER_LR_LAT_PRODUCT')

UPP = (COORD_UL[1] + COORD_UR[1])/2 # UB
LOW = (COORD_LL[1] + COORD_LR[1])/2 # BB
LEF = (COORD_UL[0] + COORD_LL[0])/2 # LB
RIG = (COORD_UR[0] + COORD_LR[0])/2 # RB

cLon = (PARIS[1] - LEF) / (RIG - LEF)
cLat = (PARIS[0] - UPP) / (LOW - UPP)


pOnLon = calcPointBetweenTo(P_UL, P_UR, cLon)
pOnLat = calcPointBetweenTo(P_UL, P_LL, cLat)

town =  ParallelogramRule(P_UL,pOnLon, pOnLat)

B1_IMG = cv2.imread(B1)

cut_list = [(town[0] - 1000, town[1] - 1000), (town[0] + 1000, town[1] - 1000),
                (town[0] + 1000, town[1] + 1000), (town[0] - 1000, town[1] + 1000)]


img = cv2.line(B1_IMG, cut_list[0], cut_list[1], (0,0,255), 15)
img = cv2.line(img, cut_list[1], cut_list[2], (0,0,255), 15)
img = cv2.line(img, cut_list[2], cut_list[3], (0,0,255), 15)
cv2.putText(img,'Paris', (town[0] + 1100, town[1] - 1100),cv2.FONT_HERSHEY_SIMPLEX,8,(0, 0, 255),10)
result = cv2.line(img, cut_list[3], cut_list[0], (0,0,255), 15)

screen_res = 1280, 720

scale_width = screen_res[0] / result.shape[1]
scale_height = screen_res[1] / result.shape[0]
scale = min(scale_width, scale_height)
window_width = int(result.shape[1] * scale)
window_height = int(result.shape[0] * scale)
cv2.namedWindow('1', cv2.WINDOW_NORMAL)
cv2.resizeWindow('1', window_width, window_height)
cv2.imshow('1', result)
cv2.waitKey(0)
cv2.destroyAllWindows()




