from tkinter import *

win = Tk()
win.title("GUI")
win.geometry("500x300+200+200")

#Label1 생성
lbl1 = Label(win, bg='skyblue', fg='white')  # Label 클래스 객체 생성 / ()에는 Tk객체(=win) 꼭 넣어야 함
lbl1['text'] = "메뉴" 
lbl1.pack(side=LEFT, fill=Y) #pack() 함수로 lbl1객체 화면에 출력

#Label2 생성
lbl2 = Label(win, text = "어서오세요\n이마트입니다", bg = 'pink', font = ('Arial', 16, 'bold'))
lbl2.pack(fill=X)

#버튼1 클릭 동작 함수 정의
def click():
    print('버튼을 클릭했어요~')
    lbl2['text'] = "환영합니다"  #버튼 동작 시 텍스트 변경 기능 추가
    #Label3 생성 > 버튼 클릭 시 노출되는 기능
    lbl3 = Label(win, bg='yellow', text = '메롱'*5)
    lbl3.pack()

#버튼1 생성
btn1 = Button(win, text='버튼', bg = 'violet', fg='white', command=click)
btn1.pack()


#버튼2 동작 함수 정의
def click2(): 
    print(entry.get()) #입력한 문자열 가져오기/ 터미널에 출력됨
    lbl2['text'] = entry.get()

#입력창 생성(입력값 ~로 노출)
entry = Entry(win, show='~')
entry.pack(fill=X)

#버튼2 생성
btn2 = Button(win, text='view', command = click2)
btn2.pack(fill=X)

#체크박스 동작 함수 정의
def check(): #체크박스
    print(var1.get(), var2.get())

#체크박스 변수 
var1 = BooleanVar()
var2 = IntVar()

#체크박스1 생성
chk1 = Checkbutton(win, text='music', variable=var1, command=check)
chk1.select()
chk1.pack(side=LEFT)

#체크박스2 생성
chk2 = Checkbutton(win, text='video', variable=var2, command=check)
chk2.deselect()
chk2.pack(side=LEFT)

#라디오 버튼 동작 함수 정의 
def check2(): #라디오 버튼
    print(g1.get())
#라디오 버튼은 문자로 받을 수 있음
g1 = StringVar()

#라디오 버튼1 생성
rd1 = Radiobutton(win, text='Male', variable=g1, value='M', command=check2)
rd1.pack(side=RIGHT)

#라디오 버튼2 생성
rd2 = Radiobutton(win, text='Female', variable=g1, value='F', command=check2)
rd2.pack(side=RIGHT)

#생성한 라디오 버튼 중 체크상태로 노출될 버튼 선언(선언 안하면 모든 라디오버튼 체크된채로 나옴)
rd1.select()

'''
#리스트 중 한개만 선택
def select():
    index = lst.curselection()[0]
    print(index, lst.get(index))

lst = Listbox(win, height=3, selectmode=SINGLE)
lst.insert(0, 'red')
lst.insert(1, 'green')
lst.insert(2, 'blue')
lst.pack()
'''
# 리스트 중 여러개 선택
def select():
    for index in lst.curselection():
        print(index, lst.get(index))

lst = Listbox(win, height=3, selectmode=MULTIPLE)
color = ['red', 'green', 'blue']
for item in color:
    lst.insert(END, item)
lst.pack()

# 버튼3 생성(리스트 동작 관련)
btn3 = Button(win, text='click', command=select)
btn3.pack()

# exercise : 애완동물 선택
def choice():
    index = lst.curselection()[0]
    if index == 0:
        lbl['image'] = photo1
    elif index == 1:
        lbl['image'] = photo2
    elif index == 2:
        lbl['image'] = photo3

favorite = ['cat', 'dog', 'bear']

lst2 = Listbox(win, height=3, selectmode=SINGLE)
for i in favorite:
    lst2.insert(END, i)
lst2.pack(fill=BOTH)

btn4 = Button(win, text='click', command=choice)
btn4.pack(fill=BOTH)

photo1 = PhotoImage(file='img1.png')
photo2 = PhotoImage(file='img2.png')
photo3 = PhotoImage(file='img3.png')    

lbl = Label(win, text='My favorite')
lbl.pack(fill=BOTH, expand=YES)


# 무한히 반복하는 구조(코드 맨 마지막에 위치)
win.mainloop() 