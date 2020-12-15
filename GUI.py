# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 22:50:59 2020

@author: Eduardo Vicente and Isabel Carvalho
"""
from NLPreprocessor import *
from SPARQLProcessor import *
from IntentionDetection import *


from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
from threading import Thread
from time import sleep
import random

backimg = Image.open(".\\GUI_Materials\\backgrounds.jpg")
img_fundo = Image.open(".\\GUI_Materials\\logo.gif")

global inity
global fail
global reply

greetings = ['ola', 'oi', 'boas', 'hey', 'viva', 'saudacoes',
                 'cumprimentos', 'bom dia', 'boa tarde',
                 'boa noite']
thanks = ['de nada', 'ora essa', 'o prazer foi todo meu', 'sem problema',
              'estou aqui para ajudar']


def thread_NLP_handler(arg):

    values = preprocess_msg(arg)
    #print(values)
    greeting = values[0]
    th = values[1]
    reply = 0
    global fail

    if greeting:
        txt = random.choice(greetings)
        add_new_msg_chat(canvas,1, txt)
        reply = 1
    if th:
        txt = random.choice(thanks)
        add_new_msg_chat(canvas,1, txt)
        reply = 1
    thread = Thread(target=thread_IR_handler,args=(values[2:],))
    thread.start()
    thread.join(5)

    if fail == 1 and reply == 0:
        add_new_msg_chat(canvas, 1, "Desculpa, nao percebi!! Vamos fazer compras?")
        fail = 0

def thread_IR_handler(arg):
    global fail
    print(arg)
    msg = detect(arg[0],arg[1])
    if(msg != None):
        add_new_msg_chat(canvas,1, msg)
        fail = 0
    else:
        fail = 1

def setGUI():

    root = Tk()

    #Load all Materials needed
    img = ImageTk.PhotoImage(backimg)
    icon = PhotoImage(file=".\\GUI_Materials\\logo.gif")

    root.iconphoto(False,icon)
    #SET Window and MENUS
    root.title("Goldie Bot")

    file_menu = Menu(root,tearoff=False)
    main_menu = Menu(root)

    file_menu.add(label="Save Chat Log",command=lambda: print("Hello"),itemType="command")
    file_menu.add(label="About",command=lambda: print("Hello"),itemType="command")
    file_menu.add(label="Exit",command=lambda: print("Hello"),itemType="command")

    main_menu.add_cascade(label="File",menu=file_menu)
    root.config(menu=main_menu)

    w = img.width()
    h = img.height()

    root.geometry('%dx%d+0+0' % (w,h))

    #Set Background
    labelimg = Label(root,image=img)
    labelimg.place(x=0,y=0,relwidth=1,relheight=1)

    return root

def create_chat_canvas(root):
    #Create Chat Window(CANVAS)
    canvas = Canvas(root,bg='#E5F3F2',bd=1,width=25, height=5)
    canvas.place(x=304,y=30,height=390,width=330)

    #Scrollbar
    vbar = Scrollbar(canvas,orient=VERTICAL)
    vbar.config(command=canvas.yview)
    # vbar.pack(side=RIGHT,fill=Y)

    canvas.config(yscrollcommand=vbar.set)


    return canvas


def create_input_window(root):

    inwin = Text(root,bd=1,bg='#EAF8F7',width=30, height=4)
    inwin.place(x=290,y=430,height=40,width=300)
    inwin.insert(1.0,'Escreva aqui...')

    inwin.bind("<Button-1>",input_entry)

    return inwin

def add_new_msg_chat(canvas,who,content):

    global inity
    content = content
    myFont = font.Font(size=10,family='Ubuntu Condensed')

    if who==1:
        msg = "GoldieBot:\n"
        final = msg + str(content)
        txt = canvas.create_text(10,inity,font=myFont,justify="left",fill="black",text=final,anchor="nw",width=300)
        bbox = canvas.bbox(txt)
        rect_item = canvas.create_rectangle(bbox,width=2, outline="#CDB720", fill="#F4EDBA")
        canvas.tag_raise(txt,rect_item)

        inity = inity + 45


    elif who==2:
        msg = "Utilizador:\n"
        final = msg+ str(content)
        txt = canvas.create_text(300,inity,justify="left",font=myFont,fill="black",text=final,anchor="ne")
        bbox = canvas.bbox(txt)
        rect_item = canvas.create_rectangle(bbox,width=2, outline="#4DB823", fill="#AFF991")
        canvas.tag_raise(txt,rect_item)
        inity = inity + 45

    canvas.update_idletasks()
    canvas.config(scrollregion=bbox)

   # return inity

def input_entry(event):
    aux = event.widget
    txt = aux.get("1.0","end-1c")
    if txt=="Escreva aqui...":
        aux.delete(1.0,"end-1c")
        aux.insert(1.0,"")
    # print(txt)
    # inwin.delete(1.0,"end")

def btn_handler():
    txt = inwin.get("1.0","end-1c")
    add_new_msg_chat(canvas,2, txt)
    inwin.delete(1.0,END)

    #Handle NLP pre-procesing
    thread = Thread(target=thread_NLP_handler,args=(txt,))
    thread.start()


if __name__ == '__main__':

    inity=30

    root = setGUI()


    # c.config(font=("Times New Roman",20))
    # creditos = Text(root,height=2,width=30)
    # creditos.pack()

    # c.pack()

    img = ImageTk.PhotoImage(backimg)
    labelimg = Label(root,image=img)
    labelimg.place(x=0,y=0,relwidth=1,relheight=1)

    img2 = ImageTk.PhotoImage(img_fundo)
    #Creates canvas(chatwindow) and Input (inwindow)
    canvas = create_chat_canvas(root)

    canvas.create_image(160,200,image=img2,)

    # canvas.pack()
    #Input window
    inwin = create_input_window(root)

    add_new_msg_chat(canvas,1,"Bem-vindo(a), em que lhe posso ajudar?")

    #Create Send Button
    myFont = font.Font(size=30)

    send_btn = Button(root,command=btn_handler,text=">",bg='#6495ED',activebackground='#EAF8F7',width=12,height=5)
    send_btn.place(x=595,y=430,height=42,width=60)
    send_btn['font'] = myFont
    # send_btn.bind("<Button-1>",btn_handler(canvas, inity))

    root.mainloop()

    root.quit()
