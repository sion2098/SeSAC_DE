from tkinter import *

win = Tk()
win.geometry('800x800')

#1. 상단 제목
lbl1 = Label(win, bg='skyblue', text = '좋아하는 동물', font=('Arial', 16, 'bold'))
lbl1.pack(fill=BOTH)

def choice():
    index = lst.curselection()[0]
    if index == 0:
        lbl['image'] = photo1
    elif index == 1:
        lbl['image'] = photo2
    elif index == 2:
        lbl['image'] = photo3

favorite = ['cat', 'dog', 'bear']

lst = Listbox(win, height=3, selectmode=SINGLE)
for i in favorite:
    lst.insert(END, i)
lst.pack(fill=BOTH)

btn = Button(win, text='click', command=choice)
btn.pack(fill=BOTH)

photo1 = PhotoImage(file='새싹_이시현_251110/image/image1.png')
photo2 = PhotoImage(file='새싹_이시현_251110/image/image2.png')
photo3 = PhotoImage(file='새싹_이시현_251110/image/image3.png')    

lbl = Label(win, text='My favorite')
lbl.pack(fill=BOTH, expand=YES)


# 무한히 반복하는 구조(코드 맨 마지막에 위치)
win.mainloop() 