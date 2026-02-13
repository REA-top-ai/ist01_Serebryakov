poem_title = input()
poem_author = input()
poem_title_fixed1 = poem_title[0].upper() + poem_title[1:]
print(poem_title_fixed1)
#НО так правильнее
l = poem_title.split(" ")
poem_title_fixed = ""
for i in l:
    poem_title_fixed +=(i[0].upper() + i[1:].lower() + " ")
print(poem_title_fixed)