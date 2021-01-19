import MySQLdb
from settings import MYSQLPASSWORD, DATABASE

database = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
cursor = database.cursor()



import requests
from bs4 import BeautifulSoup

URL = "http://www.sis.itu.edu.tr/eng/prerequisites/onsart_eng.php?subj=BLG"
page = requests.get(URL)



soup = BeautifulSoup(page.content, 'html.parser')


results = list(soup.find_all("tr"))

print(results)

special = []
none = []
single = {}

for i in range(3, len(results)-5):
    row = results[i].find_all("td")
    course_code = row[0].get_text()
    course_name = row[1].get_text()
    course_prereq = row[2].get_text()
    course_class = row[3].get_text()

    
    course_prereq = course_prereq.replace("MIN", "")
    course_prereq = course_prereq.replace("DD", "")
    course_prereq = course_prereq.replace("or", "")
    course_prereq = course_prereq.replace("   ", "*or*")
    course_prereq = course_prereq.replace("and", "*AND*")
    course_prereq = course_prereq.replace("  ", "")

    if course_prereq.find("*AND*") != -1:
        special.append(course_prereq.replace("*or*"," OR ").replace("*AND*"," AND "))
    elif course_prereq=="None":
        none.append(course_prereq)
    else:
        prereqs = course_prereq.split("*or*")
        single[str(course_code)] = prereqs
        print(single[str(course_code)])

        for prereq in single[str(course_code)]:
            try:
                query = """INSERT INTO PREREQUISITE(course_id, prereq_id) VALUES ('{0}','{1}') """.format(course_code, prereq)
                cursor.execute(query)
            except:
                print("ERROR:", course_code, prereq)



cursor.execute( """SELECT * FROM PREREQUISITE """)
print("PREREQS>>>>>", cursor.fetchall())
database.commit()
cursor.close()
database.close()
        

print(special[0])
    
    

print(len(results))

print(single)