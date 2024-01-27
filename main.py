from bs4 import BeautifulSoup
from selenium import webdriver
import time
import keyboard as keypress
import tkinter
from threading import Thread
import os

TIME = 5

class Vars:

    root = None

    Canvas = None

    StartBt = None

    startCounter=0

    driver = None

    Wordlabel = None

def loadDriver():
    try:
        Vars.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        #driver.get('https://monkeytype.com/')
        Vars.driver.get('https://monkey-type.firebaseapp.com/')
    except Exception as e:
        e = str(e)
        ec = ''
        k=0
        for i in e:
            if k<=55:
                ec+=i
                k+=1
            else:
                ec+='\n'+i
                k=1

        Vars.root.minsize(400,400)
        Vars.Wordlabel.place(x=0, y=190, width=400, height=209)
        Vars.Wordlabel.config(text=ec)
        Vars.StartBt.config(fg='#ffa600')
        Vars.startCounter = 0
        

def main():

    time.sleep(TIME)

    #print("Starting")

    timeRem = 1

    s=['garbageValue']

    Vars.root.minsize(400,400)
    Vars.Wordlabel.place(x=0, y=190, width=400, height=209)

    while(timeRem!=0 and len(s)!=0):
        s=[]

        htmlcode=(Vars.driver.page_source).encode('utf-8')
        soup = BeautifulSoup(htmlcode,features="html.parser")

        #x=soup.findAll('div', class_ = ['word active', 'word'])
        x=soup.findAll('div', { 'class' : ['word active', 'word']})
        for i in range(0, len(x)):
            if(str(x[i]).count("correct")==0 and str(x[i]).count("incorrect")==0):
                s.append(x[i].get_text())

        #print(s)
        #print(len(s))

        wrdstr = ''

        k=0
        for i in s:
            if k<=9:
                wrdstr += i+' '
                k+=1
            else:
                wrdstr += '\n'+i+' '
                k=1

            for j in i:
                keypress.send(j)
            keypress.send(' ')

        if len(wrdstr)!=0:
            Vars.Wordlabel.config(text=wrdstr)

        x=soup.findAll(id = 'premidSecondsLeft')
        #print(x)
        temp = str(x[0]).split('>')
        timeRem = int(temp[1].split("<")[0])
            
        #print(timeRem)
    
    s=[]
    x=soup.findAll('div', { 'class' : ['bottom']})
    for i in x:
        s.append(i.get_text())

def timer():
    TimerLabel = tkinter.Label(Vars.Canvas, text=TIME, bg='white', fg='red', font=("Times New Roman", 20))
    TimerLabel.place(height=20, width=50, x=310, y=145)  
    for i in range(TIME):
        time.sleep(1)
        TimerLabel.config(text=str(TIME-i-1))

def startmain():
    if Vars.startCounter==0:
        Thread(target=lambda:loadDriver()).start()
        Vars.Wordlabel.config(text='')
        Vars.startCounter+=1
        Vars.StartBt.config(fg='#ff2e74')
    else:
        Thread(target=lambda:main()).start()
        Thread(target=lambda:timer()).start()
        Vars.StartBt.config(fg='#ffa600')

def close():
    Vars.root.destroy()
    os._exit(0)

def start():

    Vars.root = tkinter.Tk()

    Vars.root.minsize(400, 200)
    Vars.root.resizable(0, 0)
    Vars.root.title('WebScrapping')

    Vars.Canvas = tkinter.Canvas(Vars.root, bg="white")
    Vars.Canvas.place(x=0, y=0, relheight=1, relwidth=1)  

    Disclaimer_Label = tkinter.Label(Vars.Canvas, text="After clicking Start, \
a webpage will open\nautomatically. Let it load completetely\nand then press the Start button again. A\n\
timer will begin, before it finishes,\nclick on the typing area of the webpage.", bg='white', fg='red',
                font=("Times New Roman", 13)) 
    Disclaimer_Label.place(height=100, width=320, x=40, y=20)

    Vars.StartBt = tkinter.Button(Vars.Canvas, text="Start Scraping", padx=10, bg='white', fg='#ffa600', activebackground='white',
                font=("Times New Roman", 20), relief=tkinter.FLAT, bd=0, command= lambda: startmain())
    Vars.StartBt.place(height=50, width=200, x=100, y=130)

    Vars.Wordlabel = tkinter.Label(Vars.Canvas, bg='#ffa8c5', font=("Times New Roman", 12))
    
    Vars.root.protocol("WM_DELETE_WINDOW", lambda : close())
    Vars.root.mainloop() 

start()