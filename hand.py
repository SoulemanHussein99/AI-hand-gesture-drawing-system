import random

import cv2
import numpy as np
import mediapipe as mp

import time


camera = cv2.VideoCapture(0)
clf = mp.solutions.hands
mp_hand = clf.Hands(max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)
draw = mp.solutions.drawing_utils

catch = None
current_color = (255,255,255)
co =0
text_data = []
pr8, pry8 = 0, 0
prev_x4, prev_y4 = 0, 0
prev_x8, prev_y8 = 0, 0
prev_x12, prev_y12 = 0, 0
prev_x16, prev_y16 = 0, 0
alpha = 0.2
points = []
draw_mode =False
cursor_index = 0
start_x , start_y = 0, 0
cursor_x, cursor_y = start_x, start_y


while True:
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    success, frame = camera.read()
    if not success:
        break
    h, w, _ = frame.shape
    frame = cv2.flip(frame, 1)
    frame_black = np.zeros_like(frame)
    frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hand.process(frame_RGB)
    hands = results.multi_hand_landmarks
    if hands:
        for hand in hands:
            draw.draw_landmarks(frame_black, hand, clf.HAND_CONNECTIONS)
            x8, y8 = hand.landmark[8].x, hand.landmark[8].y
            x4, y4 = hand.landmark[4].x, hand.landmark[4].y
            x12, y12 = hand.landmark[12].x, hand.landmark[12].y
            x16, y16 = hand.landmark[16].x, hand.landmark[16].y
            
            cx4, cy4 = int(x4 * w), int(y4 * h)
            cx4 = int(alpha * cx4 + (1 - alpha) * prev_x4)
            cy4 = int(alpha * cy4 + (1 - alpha) * prev_y4)
            prev_x4, prev_y4 = cx4, cy4
            
            cx8, cy8 = int(x8 * w), int(y8 * h)
            cx8 = int(alpha * cx8 + (1 - alpha) * prev_x8)
            cy8 = int(alpha * cy8 + (1 - alpha) * prev_y8)
            prev_x8, prev_y8 = cx8, cy8
            
            cx12, cy12 = int(x12 * w), int(y12 * h)
            cx12 = int(alpha * cx12 + (1 - alpha) * prev_x12)
            cy12 = int(alpha * cy12 + (1 - alpha) * prev_y12)
            prev_x12, prev_y12 = cx12, cy12
            
            cx16, cy16 = int(x16 * w), int(y16 * h)
            cx16 = int(alpha * cx16 + (1 - alpha) * prev_x16)
            prev_x16, prev_y16 = cx16, cy16
            
            fingers = [
                    0 if hand.landmark[8].y > hand.landmark[6].y else 1,
                    0 if hand.landmark[12].y > hand.landmark[10].y else 1,
                    0 if hand.landmark[16].y > hand.landmark[14].y else 1,
                    0 if hand.landmark[20].y > hand.landmark[18].y else 1
                ]
         
                
                        
            
            draw_mode = fingers[0]==1 and fingers[1]==1 and sum(fingers[2:])==0 and abs(cx8 - cx12)<30 and abs(cy8 - cy12)<30
            
            
            if draw_mode and len(points) == 0:
                current_color = (
                    random.randint(0,255),
                    random.randint(0,255),
                    random.randint(0,255)
                )
             
            if draw_mode:
                # glowing
                #-----------------
                cv2.line(frame_black, (prev_x8, prev_y8), (cx8, cy8), (255, 180 + int(3*random.random()), 255), 6)
                # light shine
                cv2.circle(frame_black, (cx8, cy8), 10 + int(3*random.random()), (255, 200 , 255), -1)
                   
                points.append((cx8, cy8))
                for i in range(1, len(points)):
                    cv2.line(frame_black, points[i-1], points[i], current_color, 10)

           
                
            if not draw_mode and len(points)>5:
                
                
                text_data.append((points.copy(), current_color))
                points.clear()
                
                
                
            # control the line
            if sum(fingers)== 3 and not draw_mode and abs(cx4 - cx12)<30 and abs(cy4 - cy12)<30:
                for line, color in text_data:
                    for id, (x,y) in enumerate(line):
                        line[id] = (x,y)
                        if abs(cx12 - x)<25 and abs(cy12 - y)<25:
                            line[id] = (cx12, cy12)
                            
            # moving line
            # ----------------------------
            # selecting line
            for line, color in text_data:
                for (x, y) in line:
                    if abs(cx8 - x) < 30 and abs(cy8 - y) < 30:
                        catch = line
                        break
                if catch:
                    break


            # -----------------------
            # (gesture)
            # -----------------------
            if catch and sum(fingers)==3 and not draw_mode and abs(cx4 - cx8)<30 and abs(cy4 - cy8)<30:

                dx = cx8 - pr8
                dy = cy8 - pry8
                
                # -----------------------
                # moving the line
                # -----------------------
                for i, (x, y) in enumerate(catch):
                    catch[i] = (x + dx, y + dy)

            else:
                catch = None  


            # -----------------------
            # updating the previous location
            # -----------------------
            pr8, pry8 = cx8, cy8
            


        
            # clear the lines                        
            if sum(fingers)== 0 :
                text_data.clear()
                
    
        for line, color in text_data:
           for i in range(1, len(line)):
             cv2.line(frame_black, line[i-1], line[i], color, 10)
                    
    cv2.imshow("Hand Writing AI - Cursor Mode", frame_black)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
            
                