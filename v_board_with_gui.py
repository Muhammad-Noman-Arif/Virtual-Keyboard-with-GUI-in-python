from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from HandTrackingModule import HandDetector
#import sys

class button:
    def __init__(self, pos, text, size=[85,85]):#need to add double underscores
        self.pos = pos
        self.size = size
        self.text = text
    def recOfKey(self):
        x ,y = self.pos
        w, h = self.size
        return [self.pos,[x+w,(y+h)]]


global newtext 
global capslock  
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img,button.pos, (x + w,(y + h)), (255, 255, 0),2)
        cv2.putText(img, button.text, (x + 20,(y + 65)),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 4)
    return img
def isInRectangle(rec,point):
    if (rec[1][0]>point[0]>rec[0][0] and rec[1][1]>point[1]>rec[0][1]):
        return True
    else:
        return False
def isPressed(b,lmList1):
    if isInRectangle(b.recOfKey(),lmList1[8][:2]) and isInRectangle(b.recOfKey(),lmList1[4][:2]):
        return True
    else:
        return False
def unpressed(b,lmList1):
    if isInRectangle(b.recOfKey(),lmList1[8][:2]) and isInRectangle(b.recOfKey(),lmList1[4][:2]):
        return False
    else:
      return True
def drawSpecial(img,splbtn):
    for button in splbtn:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img,button.pos, (x + w,(y + h)), (255, 255, 0),2)
        cv2.putText(img, button.text, (x + 20,(y + 65)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 4)
    return img           
def openFile():
    global newtext
    newtext = ""
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Open file okay?",
                                          filetypes= (("text files","*.txt"),
                                          ("all files","*.*")))
    file = open(filepath,'r')
    newtext=file.read()
    clip.delete("1.0","end")
    clip.insert(END,newtext)
    file.close()
def save(newtext):
    try:
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Open file okay?",
                                          filetypes= (("text files","*.txt"),
                                          ("all files","*.*")))
        file = open(filepath,'a')
        file.write('\n text added')
        file.write(newtext)
        file.close()
    except Exception:
        print("Could not write to file")
        newtext=''
    clip.delete("1.0","end")

#welcome.destroy()
#global dumy
#dumy=0

win=Tk()
win.title("VIRTUAL KEYBOARD")
win.geometry("1370x750+10+10")
win.state('zoomed')
win.config(bg="#3a3b3c")
#win['bg']='blue'
newtext=''
capslock= True
video_path=0
# For Browsing Videos
def browse():
    global video_path,cap
    video_path = filedialog.askopenfilename()
    cap = cv2.VideoCapture(video_path)
def live():
    global video_path,cap
    video_path = 0
    cap = cv2.VideoCapture(video_path)
# __________________________________________Live Button ________________________________________________________________
live_btn = Button(win, height = 50, width=130, text="Live",bg='#e7e6d1', fg='magenta', font=("Calibri", 14, "bold"), command=lambda:live())
live_btn.place(x = 500, y = 10, width=150, height=25)
# __________________________________________Browse Button_______________________________________________________________
browse_btn = Button(win, height = 50, width=130,text="Browse",bg='#e7e6d1', fg='magenta', font=("Calibri", 14, "bold"), command=lambda:browse())
browse_btn.place(x = 650, y = 10, width=150, height=25)
# =================================================================================================================================
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
detector = HandDetector(detectionCon=0.2, maxHands=2)
keys = [['1','2','3','4','5','6','7','8','9','0'],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/",' ']]
x=10
y=0

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(button([100*j+50 , 100*i +50],key))
            
cplck=button([1050,50],'CAPSLOCK',size=[185,85])
enter=button([1050,150],'ENTER',size=[185,85])
backspace=button([1050,250],'BkSpace',size=[185,85])
splbtn=[cplck,enter,backspace]

label1 = Label(win, width=1350, height=500)
label1.place(x=10, y=200)

clip=Text(win,height=5,width=20,yscrollcommand=True)
clip.place(x=10,y=40, width=1350, height= 150)
newfilebutton=Button(win,text='File',padx=20,pady=20,bg='#e7e6d1', fg='magenta', font=(
    "Calibri", 14, "bold"),command=lambda:openFile())  
newfilebutton.place(x = 10, y = 10, width=100, height=25)

savebutton=Button(win,text='Save',padx=20,pady=20,bg='#e7e6d1', fg='magenta', font=("Calibri", 14, "bold"),command=lambda : save(newtext))
savebutton.place(x = 1260, y = 10, width=100, height=25)

quit_=Button(win,text='Exit',padx=20,pady=20,bg='#e7e6d1', fg='magenta', font=("Calibri", 14, "bold"),command=lambda : win.destroy())
quit_.place(x = 1150, y = 10, width=100, height=25)

checkagain=True
pressed=button([0,0],None,size=[0,0])
while True:
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (1350, 500))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img=cv2.flip(img, 1)
        hands, img = detector.findHands(img,flipType=False)
        drawSpecial(img,splbtn)
        drawAll(img,buttonList)
        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            if isPressed(cplck,lmList1) and checkagain:
                if capslock:
                    capslock=False
                else:
                    capslock=True
                checkagain=False
                pressed=cplck
            elif isPressed(enter,lmList1) and checkagain:
                newtext+='\n'
                clip.insert(END,'\n')
                checkagain=False
                pressed=enter
            elif isPressed(backspace,lmList1) and checkagain:
                newtext=newtext[:-1]
                clip.delete('1.0',"end")
                clip.insert(END,newtext)
                checkagain=False
                pressed=backspace
            else:
                for i in buttonList:
                    if isPressed(i,lmList1) and checkagain:
                        if  capslock:
                            newtext+=i.text
                            clip.insert(END,i.text)
                        else:
                            newtext+=i.text.lower()
                            clip.insert(END,i.text.lower())
                        checkagain=False
                        pressed=i
            for i in splbtn:
                if unpressed(pressed,lmList1):
                    checkagain=True
                    pressed=button([0,0],None,size=[0,0])
            for i in buttonList:
                if unpressed(pressed,lmList1):
                    checkagain=True
                    pressed=button([0,0],None,size=[0,0])
        image = Image.fromarray(img)
        finalImage =ImageTk.PhotoImage(image)
        label1.configure(image=finalImage)
        label1.image = finalImage
    #cv2.waitKey(20)
    else:    
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    win.update()
