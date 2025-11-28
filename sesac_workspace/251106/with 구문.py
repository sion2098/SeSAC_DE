'''with(
    open("새싹_이시현_251106/text.txt", encoding = 'utf-8') as f1,
    open("새싹_이시현_251106/file.txt", encoding = 'utf-8') as f2
):
    content1 = f1.read()
    content2 = f2.read()

print(content1)
print(content2)'''

f = open("새싹_이시현_251106/text_creat.txt", 'a+', encoding = 'utf-8')

f.write("위시코어")

print(f.read())

f.close()
