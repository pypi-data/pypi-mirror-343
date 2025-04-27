import cv2
import mediapipe as mp

class handDetector():

    def __init__(self, mode=False, no_hand=2, det_con=0.5, trac_con=0.5):

        self.mode = mode
        self.no_hand = no_hand
        self.detCon = det_con
        self.tracCon = trac_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands( static_image_mode=self.mode,
    max_num_hands=self.no_hand,
    min_detection_confidence=self.detCon,
    min_tracking_confidence=self.tracCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img, handNo=0):

        self.lmlist = []

        if self.results.multi_hand_landmarks:

            myHand=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                self.cx, self.cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, self.cx, self.cy])

        return self.lmlist


    def drawCircle(self,img,idNo=0,allPoints=False):

        if allPoints:
            cv2.circle(img, (self.cx, self.cy), 15, (234, 143, 62), cv2.FILLED)

        else:
            val = self.lmlist[idNo]
            cv2.circle(img, (val[1], val[2]), 15, (234, 143, 62), cv2.FILLED)

        return img


