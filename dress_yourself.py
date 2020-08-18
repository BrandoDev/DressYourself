import os
import sqlite3
from tkinter import *

#Functions
def make_compositions(connection,cursor):
    sql = '''CREATE TABLE compositions (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        image    TEXT
    );
    '''
    cursor.execute(sql)
    connection.commit()

def select_composition(connection,cursor,category):
    from PIL import Image, ImageTk
    if category == '':
        cursor.execute('''SELECT * FROM compositions ORDER BY RANDOM() LIMIT 1;''')
        rows = cursor.fetchall()
    else:
        inputdata = (category,)
        cursor.execute('''SELECT * FROM compositions WHERE category = ? ORDER BY RANDOM() LIMIT 1;''',inputdata)
        rows = cursor.fetchall()

    for row in rows:
        category = row[1]
        image = row[2]

        class Window(Frame):
            def __init__(self, master=None):
                Frame.__init__(self, master)
                self.master = master
                self.pack(fill=BOTH, expand=1)

                load = Image.open(image)
                height = 700
                wpercent = (height / float(load.size[1]))
                width = int(load.size[0] * float(wpercent))
                listOfGlobals = globals()
                listOfGlobals['width'] = width
                resized = load.resize((width, height), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(resized)
                resized = Label(self, image=render)
                resized.image = render
                resized.place(x=0, y=0)

        root = Tk()
        app = Window(root)
        root.wm_title(category)
        root.geometry(f"{width}x700")
        root.mainloop()

    main()

def add_composition(connection,cursor):
    category = input('\nNow insert a category for the composition\n(Example: Elegant,Casual: ')
    category = category.lower()
    image = input('\nNow insert the file name of the image\n(Example: image.png): ')
    image = image.lower()
    if image == '':
        image = 'image.png'

    onlyfiles = next(os.walk('compositions/'))[2]
    count_files = len(onlyfiles)
    if count_files != 0:
        count_files = count_files-1
    image_ext = image[-4:]
    image_wext = image[:-4]
    image_new = f"compositions/{image_wext}_{count_files}{image_ext}"
    try:
        os.replace(image, image_new)
    except:
        exit('\nImage not found')

    inputdata = (category,image_new)
    cursor.execute('''INSERT INTO compositions(category,image) VALUES(?, ?)''',inputdata)
    connection.commit()

    main()

def remove_composition(connection,cursor):
    cursor.execute('''SELECT * FROM compositions ORDER BY ID ASC''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}    Category: {row[1]}      Image: {row[2]}")

    id = input('Now select composition to remove by inserting ID: ')

    sql = 'DELETE FROM compositions WHERE id=?'
    cursor.execute(sql, (id,))
    connection.commit()

    main()

def main():
    os.system('cls')

    print('________                                         _____.___.                                       .__     _____ ')
    print('\______ \  _______   ____    ______  ______      \__  |   |  ____   __ __ _______   ______  ____  |  |  _/ ____\\')
    print(' |    |  \ \_  __ \_/ __ \  /  ___/ /  ___/       /   |   | /  _ \ |  |  \\_  __ \ /  ___/_/ __ \ |  |  \   __\ ')
    print(' |    `   \ |  | \/\  ___/  \___ \  \___ \       \____   |(  <_> )|  |  / |  | \/ \___ \ \  ___/ |  |__ |  |   ')
    print('/_______  / |__|    \___  >/____  >/____  >      / ______| \____/ |____/  |__|   /____  > \___  >|____/ |__|   ')
    print('        \/              \/      \/      \/       \/                                   \/      \/               ')
    print('\n')

    print('Random composition:      1')
    print('Elegant composition:     2')
    print('Casual composition:      3')
    print('Add composition:         4')
    print('Remove composition:      5')
    print('Quit:                    6')

    x = input('\nSelect option: ')

    if x == '':
        x = main()

    if x == '1':
        result = select_composition(connection, cursor, '')

    if x == '2':
        result = select_composition(connection, cursor, 'elegant')

    if x == '3':
        result = select_composition(connection, cursor, 'casual')

    if x == '4':
        result = add_composition(connection, cursor)

    if x == '5':
        result = remove_composition(connection, cursor)

    if x == '6':
        os.system('cls')
        exit('Thank you for using Dress Yourself')

    if x:
        main()

#Database
try:
    connection = sqlite3.connect('compositions/database.db', timeout=200)
except:
    path = "compositions"
    os.mkdir(path)
finally:
    connection = sqlite3.connect('compositions/database.db', timeout=200)
cursor = connection.cursor()

try:
    sql = """SELECT count(*) from compositions"""
    cursor.execute(sql)
    totalrows = cursor.fetchone()
except:
    make_compositions(connection,cursor)
else:
    if totalrows == 0:
        make_compositions(connection, cursor)

#Main
if __name__ == "__main__":
    main()

if(connection):
    connection.close()