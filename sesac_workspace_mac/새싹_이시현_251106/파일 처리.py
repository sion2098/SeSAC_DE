'''
f = open("새싹_이시현_251106/text.txt")

print(f.read(5))
print(f.read(3))'''

'''print(f.readline())
print(f.readline())'''


'''print(f.readlines())'''

'''f = open("새싹_이시현_251106/text.txt", "w")

f.write("we going up like NASA\n")
f.write("3, 2, 1 Let's go\n")
f.write("pop pop pop pop")

f.write('''
#hello
#my name is sh
#nice to meet you
#see you soon
''')
#f.close()  

f = open("새싹_이시현_251106/text.txt")
print(f.read())
f.close()  #마지막에 close() 해도 되는건지'''


'''f = open("새싹_이시현_251106/text_creat.txt", "w")

f.writelines(["Month\n", "Python\n", "go home"])

f.close()'''

'''f = open("새싹_이시현_251106/file.txt", 'w')

f.write("Monty Python's Flying Circus\n")
f.write("color\n")


f.close()

f = open("새싹_이시현_251106/file.txt")
print(f.read(5))  #Monty
print(f.read(2))  # P
print(f.tell())
'''
f = open("새싹_이시현_251106/text.txt", encoding = 'utf = 8')
#Hi 안녕하세요
print(f.tell())  # 0
print(f.seek(3)) #공백 / 현재위치: 0에서 3이동 -> Hi(공백) 
print(f.tell())  # 3 
print(f.seek(f.tell() + 3))  # f.seek(6) / 현재위치: 안
print(f.read(1))  # 그 다음 한 글자 : 녕
f.close() 



