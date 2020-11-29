# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 22:50:59 2020

@author: Eduardo Vicente
"""
from tkinter import *
from tkinter.font import Font
from PIL import Image,ImageTk
import onto_test
backimg = Image.open(".\\GUI_Materials\\backgrounds.jpg")
global inity

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
    #root.pack()
    
    return root

def create_chat_canvas(root):
    #Create Chat Window(CANVAS)
    canvas = Canvas(root,bd=1,bg='#EAF8F7',width=25, height=5)
    canvas.place(x=304,y=30,height=390,width=330)
    canvas.configure(scrollregion=(0,0,2000,2000))
    #Scrollbar
    vbar = Scrollbar(canvas,orient=VERTICAL)
    vbar.config(command=canvas.yview)
    vbar.pack(side=RIGHT,fill=Y)
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
        final = msg + content
        txt = canvas.create_text(10,inity,font=myFont,justify="left",fill="black",text=final,anchor="nw",width=300)
        bbox = canvas.bbox(txt)
        rect_item = canvas.create_rectangle(bbox,width=2, outline="#CDB720", fill="#F4EDBA")
        canvas.tag_raise(txt,rect_item)

        inity = inity + 45

        
    elif who==2:
        msg = "Utilizador:\n"
        final = msg+content
        txt = canvas.create_text(10,inity,justify="left",font=myFont,fill="black",text=final,anchor="nw",width=300)
        bbox = canvas.bbox(txt)
        rect_item = canvas.create_rectangle(bbox,width=2, outline="#4DB823", fill="#AFF991")
        canvas.tag_raise(txt,rect_item)
        inity = inity + 45
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

    #POST PROCESS -> FALTA COLOCAR AQUI O QUERY PROCESSOR PARA FORMALIZAR A RESPOSTA DO BOT
    response = 
    add_new_msg_chat(canvas, 1, "Recebido")
        

if __name__ == '__main__':
    
    inity=30
    
    root = setGUI()
    img = ImageTk.PhotoImage(backimg)
    labelimg = Label(root,image=img)
    labelimg.place(x=0,y=0,relwidth=1,relheight=1)
    
    #Creates canvas(chatwindow) and Input (inwindow)
    canvas = create_chat_canvas(root)
    #Input window
    inwin = create_input_window(root)

    add_new_msg_chat(canvas,1,"Bem-vindo(a), em que lhe posso ajudar?")
   
    # print(inity)
    #Create Send Button
    print(font.families())
    myFont = font.Font(size=30)
   
    send_btn = Button(root,command=btn_handler,text=">",bg='#6495ED',activebackground='#EAF8F7',width=12,height=5)
    send_btn.place(x=595,y=430,height=42,width=60)
    send_btn['font'] = myFont
    # send_btn.bind("<Button-1>",btn_handler(canvas, inity))
    
    root.mainloop()
    
    root.quit()
    # while 1:
         
    
#     root.update()