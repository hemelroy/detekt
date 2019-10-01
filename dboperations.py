import sqlite3

def connect():
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Detections (detection_id INTEGER PRIMARY KEY, file_id integer NOT NULL, imageName text, date text, time text, originalImgpath text, detectImgpath text, FOREIGN KEY(file_id) REFERENCES DataFiles(file_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Objects (object_id INTEGER PRIMARY KEY, detection_id integer NOT NULL, objectName text, quantity integer, FOREIGN KEY(detection_id) REFERENCES Detections(detection_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS DataFiles(file_id INTEGER PRIMARY KEY, fileName text)")
    conn.commit()
    conn.close()

def insert(imageName,date,time,originalImgpath,detectImgpath):
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO Detections VALUES (NULL,?,?,?,?,?)",(imageName,date,time,originalImgpath,detectImgpath))
    cur.execute("SELECT detection_id FROM Detections WHERE imageName=? AND originalImgpath=?",(imageName,originalImgpath))
    detectionId = int(cur.fetchall()[0][0])
    
    #loop this for every object
    #cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?,?,?)",(detectionId,objectName,quantity))
    
    #cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(3,'rock',3))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(3,'sand',1))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(4,'bird',1))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(1,'bird',2))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(2,'bird',7))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(5,'sand',1))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(5,'rock',1))
#    cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)",(5,'cloud',3))
    conn.commit()
    conn.close()

def insert_captures(db_properties, csv_name):
    #imgname, date, time, imgpath, detectimgpath, quantities dictionary

    csv_name = 'csvs/'+csv_name

    conn=sqlite3.connect("records.db")
    cur=conn.cursor()

    cur.execute("INSERT INTO Datafiles VALUES (NULL, ?)", (csv_name,))
    cur.execute("SELECT file_id FROM Datafiles WHERE fileName=?", (csv_name,))
    fileId = int(cur.fetchall()[0][0])

    for i in range(len(db_properties)):
        print("length")
        print(len(db_properties))
        cur.execute("INSERT INTO Detections VALUES (NULL,?,?,?,?,?,?)", (fileId, db_properties[i][0], db_properties[i][1], db_properties[i][2], db_properties[i][3], db_properties[i][4]))
        cur.execute("SELECT detection_id FROM Detections WHERE imageName=? AND originalImgpath=?",(db_properties[i][0],db_properties[i][3]))
        detectionId = int(cur.fetchall()[0][0])
        if 'cat' in db_properties[i][5]:
            cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)", (detectionId, 'cat', db_properties[i][5]['cat']))
            #print(db_properties[i][5]['cat']) prints the number value of cat from dictionary
        if 'dog' in db_properties[i][5]:
            cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)", (detectionId, 'dog', db_properties[i][5]['dog']))
        if 'person' in db_properties[i][5]:
            cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)", (detectionId, 'person', db_properties[i][5]['person']))
        if 'rabbit' in db_properties[i][5]:
            cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)", (detectionId, 'rabbit', db_properties[i][5]['rabbit']))
        if 'package' in db_properties[i][5]:
            cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)", (detectionId, 'package', db_properties[i][5]['package']))
        if 'squirrel' in db_properties[i][5]:
            cur.execute("INSERT INTO Objects VALUES (NULL,?,?,?)", (detectionId, 'squirrel', db_properties[i][5]['squirrel']))
    conn.commit()
    conn.close()
#Sample output of db_properties:
# [['imcapture_0.png', '2019-09-29', '00:06:48', 'images/imcapture_0.png', 'images/detectimg5.png', 
# {'person': 1}], ['imcapture_0.png', '2019-09-29', '00:06:48', 'images/imcapture_0.png', 'images/detectimg6.png', {'person': 1}], 
# ['testgroup.jpg', '2019-09-28', '00:07:07', 'images/testgroup.jpg', 'images/detectimg7.png', {'cat': 1, 'dog': 1, 'squirrel': 1}]]

def viewList(date):
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("SELECT `detection_id`, `imageName` FROM `Detections` WHERE date=?", (date,))
    rows=cur.fetchall()
    conn.close()
    return rows

def viewPreview(imgid, name):
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("SELECT `originalImgpath`, `detectImgpath`, `time` FROM `Detections` WHERE detection_id=? AND imageName=?",(imgid, name))
    rows=cur.fetchall()
    conn.close()
    return rows

def getObjectDetails(detectionId):
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("SELECT `objectName`, `quantity` FROM `Objects` WHERE detection_id=?",(detectionId,))
    rows=cur.fetchall()
    conn.close()
    return rows

def get_csv(imgpath):
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("SELECT `file_id` FROM `Detections` WHERE originalImgpath=?", (imgpath,))
    fileId=int(cur.fetchall()[0][0])

    cur.execute("SELECT fileName FROM Datafiles WHERE file_id=?", (fileId,))
    filepath = cur.fetchall()[0][0]

    conn.close()
    return filepath

#def search(title="",author="",year="",isbn=""):
#    conn=sqlite3.connect("books.db")
#    cur=conn.cursor()
#    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title,author,year,isbn))
#    rows=cur.fetchall()
#    conn.close()
#    return rows
#
#def delete(id):
#    conn=sqlite3.connect("books.db")
#    cur=conn.cursor()
#    cur.execute("DELETE FROM book WHERE id=?",(id,))
#    conn.commit()
#    conn.close()
#
#def update(id,title,author,year,isbn):
#    conn=sqlite3.connect("books.db")
#    cur=conn.cursor()
#    cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title,author,year,isbn,id))
#    conn.commit()
#    conn.close()

connect()

#database's time format: '08:40:22' 