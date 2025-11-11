from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

win = Tk()  # 프로그램 창 만들기(win이라는 Tkinter 객체 생성)
win.title("새싹 스테이 예약 관리 시스템")  # 창 제목 설정
win.geometry("1000x700+300+50")  # 창 크기 설정 + 화면 좌표

# 홈 화면 프레임
home_frame = Frame(win)
home_frame.pack(fill=BOTH, expand=TRUE) # 화면 전체를 꽉 채우고, 창 크기 조절 가능하게

# 홈 화면 라벨_웰컴 새싹 스테이 라벨 넣기
lbl1 = Label(home_frame, bg = 'skyblue', text = 'Welcome to SeSAC STAY', font = ('Arial', 20, 'bold'))
lbl1.pack(fill = X)  # fill=X -> 좌우로 화면 가득 채움

# 홈 화면 배경 이미지_canvas 위에 올릴 이미지 불러오기
bg_image = Image.open("새싹_이시현_251110/image/한옥배경.png") # 해당 경로에서 이미지 불러오기
bg_image = bg_image.resize((1000,400))  # 이미지 크기를 홈 화면에 맞게 조정
bg_photo = ImageTk.PhotoImage(bg_image)

# canvas 위에 이미지 올리기
canvas = Canvas(home_frame, width=1000, height=400)
canvas.pack()
# 이미지를 화면에 붙이기_canvas에 이미지 노출
canvas.create_image(0,0, anchor="nw", image=bg_photo)

# 홈 화면_버튼 프레임 : 한 화면에 여러 버튼을 배치핼때 위치 쉽게 조정하기 위해 별도의 프레임에 버튼을 넣는것임
btn_frame = Frame(home_frame)  # 버튼들을 담을 컨테이너 생성(중앙 정렬용)
btn_frame.pack(pady=20)  # pady=20 : 위아래 여백 20px

# 방 소개 프레임
intro_frame = Frame(win)
# 방 소개 페이지 라벨 넣기
lbl2 = Label(intro_frame, text = '방 소개 페이지', bg = 'skyblue', font = ('Arial', 20, 'bold'))
lbl2.pack(fill = X)

# 뒤로가기 버튼(홈으로) 함수 정의
def back_home():
    intro_frame.pack_forget()
    home_frame.pack(fill=BOTH, expand = YES)

# 뒤로가기 버튼 생성
btn_back_home = Button(intro_frame, text = '< 돌아가기', font = ('Arial', 10, 'bold'), command = back_home)
btn_back_home.pack(anchor = 'w')  # anchor='w'는 왼쪽 정렬

# 방 타입별 이미지 불러오는 함수 정의
def select_room():
    index = lst.curselection()[0]
    if index == 0:
        lbl['image'] = photo1
    elif index == 1:
        lbl['image'] = photo2
    elif index == 2:
        lbl['image'] = photo3

room_type = ['사랑채(2인용)', '안채(4인용)', '별채(4인용)']

# 방 타입 리스트 정의
lst = Listbox(intro_frame, height = 3, selectmode = SINGLE)
for i in room_type:
    lst.insert(END, i)
lst.pack()

# 방 타입 리스트 클릭 버튼 생성
btn_room = Button(intro_frame, text = '선택', command = select_room)
btn_room.pack()

# 이미지 불러오는 경로 설정
photo1 = PhotoImage(file='새싹_이시현_251110/image/방1(2인용).png')
photo2 = PhotoImage(file='새싹_이시현_251110/image/방2(4인용).png')
photo3 = PhotoImage(file='새싹_이시현_251110/image/방3(4인용2).png')
lbl = Label(intro_frame, text= 'room type image')
lbl.pack(fill=BOTH, expand = YES)

# 예약하기 프레임
book_frame = Frame(win)
# 예약하기 페이지 라벨 넣기
lbl_book = Label(book_frame, text = '예약하기 페이지', bg = 'skyblue', font = ('Arial', 20, 'bold'))
lbl_book.pack(fill = X)

# 뒤로가기 버튼(홈으로) 함수 정의
def back_home2():
    book_frame.pack_forget()
    home_frame.pack(fill=BOTH, expand = YES)

# 뒤로가기 버튼 생성
btn_back_home2 = Button(book_frame, text = '< 돌아가기', font = ('Arial', 10, 'bold'), command = back_home2)
btn_back_home2.pack(anchor = 'w')  # anchor='w'는 왼쪽 정렬

# 에약 가능/선택 영역
dates = ["11/10(월)", "11/11(화)", "11/12(수)", "11/13(목)", "11/14(금)", "11/15(토)", "11/16(일)"]
rooms = ["사랑채(2인용)", "안채(4인용)", "별채(4인용)"]

# 각 날짜별 선택 상태 저장(IntVar 생성) -> 한 날짜마다 한 방만 선택 가능
date_vars = {}

for date in dates:            #relief='groove', bd=1 -> 테두리로 날짜 구분 
    frame = Frame(book_frame, relief='groove', bd=1, padx=10, pady=5)  # 날짜별 프레임 생성
    frame.pack(fill=X, pady=5, padx=10)

    lbl_date = Label(frame, text=date, font=('Arial', 12, 'bold'))
    lbl_date.pack(side=LEFT, padx=10)

    var = IntVar(value=-1)  #value=-1 -> 라디오버튼 초기 선택값 없이 노출
    date_vars[date] = var  # 날짜별로 선택한 값을 date_vars 딕셔너리에 저장

    # 라디오 버튼 생성
    for i, room in enumerate(rooms):  
        rb = Radiobutton(frame, text=room, variable=var, value=i)
        rb.pack(side=LEFT, padx=10)


# 예약 완료 버튼 동작 함수 정의
def confirm_book():
    any_selec = False
    for date, var in date_vars.items():
        if var.get() != -1:
            any_selec = True
            break
    
    if any_selec:
        # 팝업창 표시
        messagebox.showinfo("예약 완료", "예약이 완료되었습니다!")
        # 예약 페이지 감추고 홈으로 이동
        book_frame.pack_forget()
        home_frame.pack(fill=BOTH, expand=YES)
        # 선택 초기화
        for var in date_vars.values():
            var.set(-1)

    else:
        # 선택 없으면 경고 팝업
        messagebox.showwarning("선택 없음", "예약할 방을 선택해주세요.")

# 예약 완료 버튼 생성
btn_confirm = Button(book_frame, text = '예약 완료', font=('Arial', 12, 'bold'), command = confirm_book)
btn_confirm.pack(pady=10)


# 방 소개 버튼 동작 함수 정의
def click_intro():
    home_frame.pack_forget()
    intro_frame.pack(fill=BOTH, expand=YES)
    print('방 소개 이동')

# 방 소개 버튼 생성
btn_intro = Button(btn_frame, text = '방 소개', bg = 'white', font = ('Arial', 18, 'bold'), command = click_intro)
btn_intro.pack(side = LEFT, padx = 20)

# 예약하기 버튼 동작 함수 정의
def click_book():
    home_frame.pack_forget()
    book_frame.pack(fill=BOTH, expand=YES)
    print("예약하기 이동")

# 예약하기 버튼 생성
btn_book = Button(btn_frame, text = '예약하기', bg = 'white', font = ('Arial', 18, 'bold'), command = click_book)
btn_book.pack(side = LEFT, padx = 20)   # 버튼 배치(좌우 위치, 간격 = padx)


win.mainloop()