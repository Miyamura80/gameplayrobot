import cv2
from GenerallyUsefulFunctions import createGrid2

"""
Modeled by a 
"""


def webcamVideoFeed(recordOn):
    #Video writing stuffs + Save file parameters
    if recordOn:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    #Change parameter to 1 to use USB connected webcam
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        # Ret -> Bool, checks if any output from camera
        # Frame -> frame object being taken
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Potential mods to the frames
        """
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flipFrame = cv2.flip(frame,0)
        """
        if recordOn:
            out.write(frame)

        detection = detectPianoTiles(frame)
        frame = colourPixels(frame)
        for i in range(4):
            if detection[i]:
                print("Black present at index: ",i)

        # Display frame
        cv2.imshow("Video feed", frame)
        #End while loop if q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    print(frame.shape)
    cap.release()
    if recordOn:
        out.release()
    cv2.destroyAllWindows()

def detectPianoTiles(frame):
    blackConstant = 20
    detectedTiles = [False,False,False,False]
    for i in range(4):
        # print(frame[50,150+i*130])
        if frame[50,150+i*130] < blackConstant:
            detectedTiles[i] = True
    return detectedTiles


def colourPixels(frame):
    frame[50:80,150:180] = 0
    frame[50:80, 280:310] = 0
    frame[50:80, 410:440] = 0
    frame[50:80, 540:570] = 0

    return frame

webcamVideoFeed(False)

