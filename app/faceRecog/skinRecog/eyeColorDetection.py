import cv2
import imutils
from imutils import face_utils
import dlib
import numpy as np
import webcolors


flag=0
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

img= cv2.imread('frame2.jpg')
img_rgb= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)   #convert to RGB


#cap = cv2.VideoCapture(0)             #turns on the webcam

(left_Start, left_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]            
#points for left eye and right eye
(right_Start, right_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]




def find_color(requested_colour):             #finds the color name from RGB values
 
        min_colours = {}
        for name, key in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(name)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = key
            closest_name = min_colours[min(min_colours.keys())]
        return closest_name





#ret, frame=cap.read()
#frame = cv2.flip(frame, 1)

#cv2.imshow(winname='face',mat=frame)

gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# detect dlib face rectangles in the grayscale frame
dlib_faces = detector(gray, 0)


for face in dlib_faces:
    eyes = []                          # store 2 eyes

    # convert dlib rect to a bounding box
    (x,y,w,h) = face_utils.rect_to_bb(face)
    cv2.rectangle(img_rgb,(x,y),(x+w,y+h),(255,0,0),1)       #draws blue box over face 
 
    
    
    shape = predictor(gray, face)
    shape = face_utils.shape_to_np(shape)
    
    leftEye = shape[left_Start:left_End]               
    # indexes for left eye key points

    rightEye = shape[right_Start:right_End]
    
    eyes.append(leftEye)  # wrap in a list
    eyes.append(rightEye)
    
    for index, eye in enumerate(eyes):
        flag+=1
        left_side_eye = eye[0]  # left edge of eye
        right_side_eye = eye[3]  # right edge of eye
        top_side_eye = eye[1]  # top side of eye
        bottom_side_eye = eye[4]  # bottom side of eye

        # calculate height and width of dlib eye keypoints
        eye_width = right_side_eye[0] - left_side_eye[0]
        eye_height = bottom_side_eye[1] - top_side_eye[1]

        # create bounding box with buffer around keypoints
        eye_x1 = int(left_side_eye[0] - 0 * eye_width)  
        eye_x2 = int(right_side_eye[0] + 0 * eye_width)  

        eye_y1 = int(top_side_eye[1] - 1 * eye_height)
        eye_y2 = int(bottom_side_eye[1] + 0.75 * eye_height)

        # draw bounding box around eye roi
        
        #cv2.rectangle(img_rgb,(eye_x1, eye_y1), (eye_x2, eye_y2),(0,255,0),2) 
        
        
        roi_eye = img_rgb[eye_y1:eye_y2 ,eye_x1:eye_x2]     #  desired EYE Region(RGB)
        if flag==1:
            break
        
x=roi_eye.shape                                                        
row=x[0] 
col=x[1]
# this is the main part,                             
# where you pick RGB values from the area just below pupil
array1=roi_eye[row//2:(row//2)+1,int((col//3)+3):int((col//3))+6]         

array1=array1[0][2]
array1=tuple(array1)   #store it in tuple and pass this tuple to "find_color" Funtion
                                                        


print(find_color(array1))
        
        
        
        

        


cv2.imshow("frame",roi_eye)
cv2.waitKey(0)
cv2.destroyAllWindows()

    