import cv2
import mediapipe as mp
import pyfiglet as pyg  
import time
import json
welcome=pyg.figlet_format("Welcome to the MediaPipe Camera")
print(welcome)
# import threading
# from audio import checkVoice
    
# threading.Thread(target=checkVoice).start()
# checkVoice()

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("testVideo.mp4")

pTime=0

mpDraw=mp.solutions.drawing_utils
mpholistic=mp.solutions.holistic
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh(max_num_faces=3)
holistic=mpholistic.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7)
facelms=None
student1='Abnormal'
student2='Abnormal'
student3='Abnormal'

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results=faceMesh.process(imgRGB)
    
    handResults = holistic.process(imgRGB)
    if results.multi_face_landmarks:
        
    #     # print(dir(results.multi_face_landmarks[0].landmark))
    #     # for i, value in results:
        #     print(i)
        for facelms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, facelms, mpFaceMesh.FACEMESH_TESSELATION, mpDraw.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                    mpDraw.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                    )
    else:
        facelms=None
    mpDraw.draw_landmarks(img, handResults.right_hand_landmarks, mpholistic.HAND_CONNECTIONS, 
                            mpDraw.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                            mpDraw.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                            )
    mpDraw.draw_landmarks(img, handResults.left_hand_landmarks, mpholistic.HAND_CONNECTIONS, 
                            mpDraw.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                            mpDraw.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                            )
    
    
    ctime=time.time()
    fps=1/(ctime-pTime)
    pTime=ctime
    # cv2.putText(img, f"FPS: {int(fps)}", (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
    start_point = (200, 0)
  
    # End coordinate, here (250, 250)
    # represents the bottom right corner of image
    end_point = (200, 1024)
    
    # Green color in BGR
    color = (0, 255, 0)
    
    # Line thickness of 9 px
    thickness = 3
    
    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    cv2.line(img, start_point, end_point, color, thickness)
    start_point = (400, 0)
  
    # End coordinate, here (250, 250)
    # represents the bottom right corner of image
    end_point = (400, 1024)
    
    # Green color in BGR
    color = (0, 255, 0)
    
    # Line thickness of 9 px
    thickness = 3
    
    # Using cv2.line() method
    # Draw a diagonal green line with thickness of 9 px
    cv2.line(img, start_point, end_point, color, thickness)
  
    
    if facelms == None or handResults.right_hand_landmarks != None or handResults.left_hand_landmarks !=None:
                # print(handResults.right_hand_landmarks[0])
                # tempData="Abnormal"
                # file=open("time.txt","w")
                # file.write(str(handResults.right_hand_landmarks[0].landmark[0]))
                # file.close()
                tempData="Normal"
                
                student1=tempData
                student2=tempData
                student3=tempData
                try:
                    RightHandPath=json.dumps(str(handResults.right_hand_landmarks.landmark[0]))[4:14]
                except Exception as e:
                    # print(e)
                    RightHandPath=None
                try:
                    LeftHandPath=json.dumps(str(handResults.left_hand_landmarks.landmark[0]))[4:14]
                except Exception as e:
                    # print(e)
                    LeftHandPath=None
                try:
                    if RightHandPath!=None:
                        
                        if float(RightHandPath) <0.3:
                            student1="Abnormal"
                            student2="Normal"
                            student3="Normal"
                            print("Abnormal student1")
                        elif float(RightHandPath) >0.3 and float(RightHandPath)<0.6:
                            student2="Abnormal"
                            student3="Normal"
                            student1="Normal"
                            print("Abnormal student2")
                        elif float(RightHandPath) >0.6 and float(RightHandPath) <1 :
                            print("Abnormal student3")
                            student3="Abnormal"
                            student1="Normal"
                            student2="Normal"
                    if LeftHandPath!=None:
                        if float(LeftHandPath) <0.3:
                            student1="Abnormal"
                            student2="Normal"
                            student3="Normal"
                            print("Abnormal student1")
                        elif float(LeftHandPath) >0.3 and float(LeftHandPath)<0.6:
                            student2="Abnormal"
                            student3="Normal"
                            student1="Normal"
                            print("Abnormal student2")
                        elif float(LeftHandPath) >0.6 and float(LeftHandPath) <1 :
                            print("Abnormal student3")
                            student3="Abnormal"
                            student1="Normal"
                            student2="Normal"
                except Exception as e:
                    pass  
    else:
            tempData="Normal"
            student1=tempData
            student2=tempData
            student3=tempData
            print(tempData)
            
    cv2.putText(img, f"{student1}", (0,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)

    cv2.putText(img, student2, (220,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
    cv2.putText(img, student3, (420,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
    
    cv2.imshow('Image', img)
#         print(mp_drawing.draw_landmarks)                        
        # cv2.imshow('Raw Webcam Feed', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
