def get_catalog(link):
    import requests

    URL = link
    page = requests.get(URL)

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(page.content, 'html.parser')
    results = list(soup.find_all("tr"))

    #print(results[1].find_all("td")[1])
    #print(results[1].find_all("span")[0])
    #print(results[1].find_all("b")[0])

    catalog_term_program_name = (results[1].find_all("span")[0]).get_text()
    catalog_term_name = (results[1].find_all("b")[0]).get_text()
    catalog_term_identifier = catalog_term_program_name + " - " + catalog_term_name

    print(catalog_term_identifier, len(catalog_term_identifier))
    print("\n",catalog_term_program_name,"\n",catalog_term_name)
    
    

    category = ["Course Code", "Course Title", "Credit", "Theoretical",
                 "Tutorial", "Lab.", "ECTS", "Type", "Compulsory/Elective", "Semester"]


    cat_courses = list()

    for i in range(2,len(results)-1):
        elements = list(results[i].find_all("td"))
        course = {}

        if elements[0].get_text() == '\xa0':
            continue

        course["course_code"] = elements[0].get_text()
        course["course_title"] = elements[1].get_text()
        course["credit"] = elements[2].get_text()
        course["theoretical"] = elements[3].get_text()
        course["tutorial"] = elements[4].get_text()
        course["lab"] = elements[5].get_text()
        course["etcs"] = elements[6].get_text()
        course["type"] = elements[7].get_text()
        course["c/e"] = elements[8].get_text()
        course["semester"] = elements[9].get_text()

        if elements[0].get_text() == category[0]:
            continue
        else:
            cat_courses.append(course)

            import MySQLdb
            from settings import MYSQLPASSWORD, DATABASE

            database = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
            cursor = database.cursor()
            try:
                cursor.execute("""INSERT INTO COURSE(course_id, course_name, credit) VALUES ('{0}', '{1}', {2}) """.format(course["course_code"], course["course_title"], float(course["credit"]) ) )
            except:
                print(course["course_code"], "exists")
            
            cursor.execute("""INSERT INTO CATALOG_TERM(cat_term_id, course_id) VALUES ("{0}", "{1}") """.format(catalog_term_identifier, course["course_code"]))

            database.commit()
            cursor.close()
            database.close()
    return cat_courses



def set_catalogs():

    Fall1112_Fall1718= 'http://www.sis.itu.edu.tr/eng/curriculums/plan/BLGE/201210.html'
    get_catalog(Fall1112_Fall1718)[0]


    CE100_2017_2018 = 'http://www.sis.itu.edu.tr/eng/curriculums/plan/BLGE/201810.html'
    get_catalog(CE100_2017_2018)[0]


    print("already exists")



