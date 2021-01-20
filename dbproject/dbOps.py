import MySQLdb
from flask import session
from settings import MYSQLPASSWORD, DATABASE, RESPOND_TEXT


def add_course_to_catalogTerm( course_id, course_name, course_credit):
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()

    cursor.execute("INSERT INTO COURSE (course_id, course_name, credit) VALUES (%s, %s, %s)",(course_id, course_name, course_credit))

    db.commit()
    cursor.close()
    db.close()


def add_course_to_transcript( term, course_id, grade='XX', ins_name='NoName', e_grade="XX", crn='00000'):
    course_id = course_id.replace("_", " ")
    stu_id = session["user_id"]
    


    if (e_grade == "XX") | (e_grade == ""):
        e_grade = grade
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    result = "Course added succesfully"

    try:
        cursor.execute( """INSERT INTO TRANSCRIPT (stu_id, term, course_id, grade, ins_name, e_grade ) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}')""".format(stu_id, term, course_id,grade,ins_name,e_grade))
    except:
        print("Course doesn't exist on map-out")
        result = "Course doesn't exist on map-out"

    db.commit()
    cursor.close()
    db.close()
    return result

def update_course_on_transcript(transcript_id, new_term, new_course_id, new_grade="", new_ins_name="", new_e_grade="",new_crn=""):
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    message = "Updated-> "

    
    if new_term:
        cursor.execute( "UPDATE TRANSCRIPT SET term='{0}' WHERE transcript_id={1}".format(str(new_term), int(transcript_id)) )
        message += str(new_term) + " "
    if new_course_id:
        cursor.execute( "UPDATE TRANSCRIPT SET course_id='{0}' WHERE transcript_id={1}".format(str(new_course_id), int(transcript_id)) )
        message += str(new_course_id)+ " "
    if new_grade:
        cursor.execute( "UPDATE TRANSCRIPT SET grade='{0}' WHERE transcript_id={1}".format(str(new_grade), int(transcript_id)) )
        message += str(new_grade)+ " "
    if new_ins_name:
        cursor.execute( "UPDATE TRANSCRIPT SET ins_name='{0}' WHERE transcript_id={1}".format(str(new_ins_name), int(transcript_id)) )
        message += str(new_ins_name)+ " "
    if new_crn:
        cursor.execute( "UPDATE TRANSCRIPT SET crn='{0}' WHERE transcript_id={1}".format(str(new_crn), int(transcript_id)) )
        message += str(new_crn)+ " "
    if new_e_grade:
        cursor.execute( "UPDATE TRANSCRIPT SET e_grade='{0}' WHERE transcript_id={1}".format(str(new_e_grade), int(transcript_id)) )
        message += str(new_e_grade)+ " "
    db.commit()
    cursor.close()
    db.close()
    return message


def delete_on_transcript(transcript_id):
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM TRANSCRIPT WHERE transcript_id={0}".format(int(transcript_id)) )
        db.commit()
        message = "Deleting Success-> "+str(transcript_id)
    except:
        message = "Deleting Failiure"

    cursor.close()
    db.close()
    return message


def getTranscript(attributeName="*", transcript_id = ""):
    stu_id = session["user_id"]

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    if transcript_id=="":
        cursor.execute("SELECT "+attributeName+" FROM TRANSCRIPT WHERE stu_id = "+ str(stu_id)) 
    else:
        cursor.execute("SELECT "+attributeName+" FROM TRANSCRIPT WHERE transcript_id = "+ str(transcript_id)) 
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def getCourse(attributeName="*"):
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT "+attributeName+" FROM COURSE")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def getCatalogTerm(attribute="*"):
    CATALOG_TERM = session["user_term"]

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    cat_term = CATALOG_TERM.replace("_"," ")
    result = None
    try:
        query = """SELECT {0} FROM COURSE WHERE course_id IN (SELECT course_id FROM CATALOG_TERM WHERE cat_term_id = "{1}") """.format(attribute,cat_term)
        cursor.execute(query)
        result = cursor.fetchall()
    except:
        print( "catalog term doesn't exists in database")
    
    
    cursor.close()
    db.close()
    return result


def login_checker(email, password):

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    result = None
    try:
        query = "SELECT stu_id,stu_name,email,cat_term_id FROM USER WHERE email='{0}' AND user_pass='{1}'".format(email, password)
        cursor.execute(query)
        result = cursor.fetchall()[0]
    except:
        print( "login failiure")
        result = None

    cursor.close()
    db.close()
    return result


def sign_up(user_name, email, password, cat_term):
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    message = ""
    try:
        query = """INSERT INTO USER(stu_name, email, user_pass, cat_term_id) VALUES ('{0}', '{1}', '{2}', "{3}")""".format(user_name, email, password, cat_term)
        cursor.execute(query)
        message = RESPOND_TEXT["SUCCESS_SIGNUP_MESSAGE"]
    except:
        #message = RESPOND_TEXT["FAIL_SIGNUP_MESSAGE"]
        message = cat_term
        

    db.commit()
    cursor.close()
    db.close()
    return message


def calculate_GPA(whichGrade="grade"):
    user_id = session["user_id"]

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    message = ""



    # current course grade and credits
    query =(""" SELECT  COURSE.credit, TRANSCRIPT.{0}
                FROM TRANSCRIPT INNER JOIN COURSE ON TRANSCRIPT.course_id = COURSE.course_id
                WHERE (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term) 
                IN(
                    SELECT TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                    FROM TRANSCRIPT
                    INNER JOIN COURSE ON TRANSCRIPT.course_id=COURSE.course_id
                    WHERE stu_id = {1}
                    GROUP BY TRANSCRIPT.course_id
                ) 
            """
            ).format(whichGrade, user_id)
    cursor.execute(query)
    grades = cursor.fetchall()
    
    total = 0
    total_credit = 0
    
    for credit, grade in grades:
        if grade == "AA":
            total_credit += credit
            total += 4.0*credit
        if grade == "BA":
            total_credit += credit
            total += 3.5*credit
        if grade == "BB":
            total_credit += credit
            total += 3.0*credit
        if grade == "CB":
            total_credit += credit
            total += 2.5*credit
        if grade == "CC":
            total_credit += credit
            total += 2.0*credit
        if grade == "DC":
            total_credit += credit
            total += 1.5*credit
        if grade == "DD":
            total_credit += credit
            total += 1.0*credit
        if grade == "FF":
            total_credit += credit
            total += 0.0*credit
        if grade == "VF":
            total_credit += credit
            total += 0.0*credit
        if grade == "XX":
            pass
        if grade == "NG":
            pass
        if grade == "":
            pass
    return (total / total_credit) if total_credit else None


def profileInfo():
    stu_id = session["user_id"]
    user_term = session["user_term"]

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    message = ""
    result = {  
                "user_name" : "",
       
                "completed_course" : 0,
                "completed_credit" : 0,

                "total_mandatory_course" : 0,
                "total_mandatory_credit" : 0,

                "course_ratio" : 0,
                "credit_ratio" : 0
            }

    
    try:
        # number of current completed course
        query =(""" SELECT  COUNT(COURSE.course_id)
                    FROM TRANSCRIPT INNER JOIN COURSE ON TRANSCRIPT.course_id = COURSE.course_id
                    WHERE(
                        (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term) 
                        IN(
                            SELECT TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                            FROM TRANSCRIPT
                            INNER JOIN COURSE ON TRANSCRIPT.course_id=COURSE.course_id
                            WHERE stu_id = {0}
                            GROUP BY TRANSCRIPT.course_id
                        )
                        AND TRANSCRIPT.grade!='' AND TRANSCRIPT.grade!='XX' AND TRANSCRIPT.grade!='FF' AND TRANSCRIPT.grade!='VF'
                    )
                    GROUP BY stu_id
                """
                ).format(stu_id)
                
        cursor.execute(query)
        result["completed_course"] = cursor.fetchall()[0][0]
    except:
        message = "Fail: Completed Course Query" 


    try:
        # current completed credits
        query =(""" SELECT  SUM(COURSE.credit)
                    FROM TRANSCRIPT INNER JOIN COURSE ON TRANSCRIPT.course_id = COURSE.course_id
                    WHERE(
                        (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term) 
                        IN(
                            SELECT TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                            FROM TRANSCRIPT
                            INNER JOIN COURSE ON TRANSCRIPT.course_id=COURSE.course_id
                            WHERE stu_id = {0}
                            GROUP BY TRANSCRIPT.course_id
                        )
                        AND TRANSCRIPT.grade!='' AND TRANSCRIPT.grade!='XX' AND TRANSCRIPT.grade!='FF' AND TRANSCRIPT.grade!='VF'
                    )
                    GROUP BY stu_id
                """
                ).format(stu_id)

        cursor.execute(query)
        result["completed_credit"] = cursor.fetchall()[0][0]
    except:
        message = "Fail: Completed Credit Query" 


    try:
        query = """ SELECT COUNT(course_id) FROM CATALOG_TERM WHERE cat_term_id="{0}"  """.format(user_term.replace("_"," "))
        cursor.execute(query)
        result["total_mandatory_course"] = cursor.fetchall()[0][0]
    except:
        message = "Fail: Completed Total Course Query" 


    try:
        query = """ SELECT SUM(credit) FROM COURSE WHERE course_id IN(SELECT course_id FROM CATALOG_TERM WHERE cat_term_id ="{0}") """.format(user_term.replace("_"," "))
        cursor.execute(query)
        result["total_mandatory_credit"] = cursor.fetchall()[0][0]
    except:
        message = "Fail: Completed Total Credit Query" 


    try:
        result["course_ratio"] = round(result["completed_course"] / result["total_mandatory_course"], 4)
        result["credit_ratio"] = round(result["completed_credit"] / result["total_mandatory_credit"], 4)
    except:
        message = "Last Fail: Ratio"


    return result


def summary():
    stu_id = session["user_id"]
    reg_term = session["user_term"]

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    message = ""
    result_list = []

    try:
        # catalog term course and grades
        query =(""" SELECT CATALOG_TERM.course_id, COURSE.equ_code,COURSE.course_name, COURSE.credit, TRANSCRIPT.grade
                    FROM CATALOG_TERM
                    LEFT JOIN COURSE ON CATALOG_TERM.course_id = COURSE.course_id
                    LEFT JOIN TRANSCRIPT ON CATALOG_TERM.course_id = TRANSCRIPT.course_id
                    WHERE( 
                        (
                            (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term)
                            IN(
                                SELECT  TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term
                                WHERE
                                (
                                    ( TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term ) 
                                    IN(
                                        SELECT  TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                                        FROM TRANSCRIPT
                                        WHERE TRANSCRIPT.stu_id = {0}
                                        GROUP BY TRANSCRIPT.course_id
                                    ) 
                                )
                            )
                            OR
                            TRANSCRIPT.stu_id IS NULL
                        )
                        AND CATALOG_TERM.cat_term_id = "{1}" 
                    )
                """).format(stu_id, reg_term)
        cursor.execute(query)
        for row in cursor.fetchall():
            result = {}
            result["course_id"] = row[0]
            result["equ_code"] = row[1]
            result["course_name"] = row[2]
            result["credit"] = row[3]
            result["grade"] = row[4]
            result_list.append(result)

    except:
        message="Summary Fail"

    return result_list

def delete_user():
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    cursor.execute("DELETE FROM USER WHERE stu_id={0}".format(int(session["user_id"]) ) )
    db.commit()
    cursor.close()
    db.close()


def update_name(new_name):
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()
    cursor.execute( "UPDATE USER SET stu_name='{0}' WHERE stu_id={1}".format(new_name, session["user_id"]) )
    db.commit()
    cursor.close()
    db.close()



def detailed_course(course_code):
    course_code = course_code.replace("_", " ")
    course_code = course_code.upper()

    result = {}
    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()

    query = (""" SELECT PREREQUISITE.prereq_id FROM PREREQUISITE WHERE PREREQUISITE.course_id = '{0}'
            """).format(course_code)
    cursor.execute(query)
    result["prereqs"] = list(cursor.fetchall())


    query = (""" SELECT COURSE.course_name, COURSE.course_id, COURSE.equ_code, COURSE.credit FROM COURSE WHERE COURSE.course_id = '{0}'
            """).format(course_code)
    cursor.execute(query)
    ret = cursor.fetchall()
    result["course_name"] = ret[0][0]
    result["course_id"] = ret[0][1]
    result["equ_code"] = ret[0][2]
    result["credit"] = ret[0][3]


    return result



    




db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
cursor = db.cursor()


query =("""     SELECT SUM(DISTINCT unique_credits), SUM(DISTINCT COURSE.credit) AS "unique_credits"
                FROM TRANSCRIPT INNER JOIN COURSE ON TRANSCRIPT.course_id=COURSE.course_id
                WHERE (stu_id = '{0}' AND grade!='' AND grade!='XX'AND grade!='FF' AND grade!='VF')
                GROUP BY COURSE.course_id, TRANSCRIPT.stu_id
        """    ).format(1)


query = ("""    SELECT CATALOG_TERM.course_id, COURSE.course_name, TRANSCRIPT.grade, TRANSCRIPT.stu_id
                FROM CATALOG_TERM
                LEFT JOIN COURSE ON COURSE.course_id = CATALOG_TERM.course_id
                LEFT JOIN TRANSCRIPT ON TRANSCRIPT.course_id = COURSE.course_id
                
        """).format(1)



# completed course and crades
query =(""" SELECT  TRANSCRIPT.course_id, TRANSCRIPT.transcript_id, COURSE.credit, TRANSCRIPT.grade
            FROM TRANSCRIPT INNER JOIN COURSE ON TRANSCRIPT.course_id = COURSE.course_id
            WHERE(
                (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term) 
                IN(
                    SELECT TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                    FROM TRANSCRIPT
                    INNER JOIN COURSE ON TRANSCRIPT.course_id=COURSE.course_id
                    WHERE stu_id = '{0}'
                    GROUP BY TRANSCRIPT.course_id
                )
                AND TRANSCRIPT.grade!='' AND TRANSCRIPT.grade!='XX' AND TRANSCRIPT.grade!='FF' AND TRANSCRIPT.grade!='VF'
            )
        """
        ).format(1)



# catalog term course and grades
query =(""" SELECT CATALOG_TERM.cat_term_id, CATALOG_TERM.course_id, COURSE.course_name, TRANSCRIPT.grade, TRANSCRIPT.stu_id
            FROM CATALOG_TERM
            LEFT JOIN COURSE ON CATALOG_TERM.course_id = COURSE.course_id
            LEFT JOIN TRANSCRIPT ON CATALOG_TERM.course_id = TRANSCRIPT.course_id
            WHERE( 
                (
                    (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term)
                    IN(
                        SELECT  TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term
                        WHERE
                        (
                            ( TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term ) 
                            IN(
                                SELECT  TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                                FROM TRANSCRIPT
                                WHERE TRANSCRIPT.stu_id = {0}
                                GROUP BY TRANSCRIPT.course_id
                            ) 
                        )
                    )
                    OR
                    TRANSCRIPT.stu_id IS NULL
                )
                AND CATALOG_TERM.cat_term_id = "{1}" 
            )
        """
        ).format(1,"Computer Engineering (%100 English) Program Curriculum - Student's Catalog Term: Between 2011-2012 Fall Semester and 2017-2018 Fall Semester")

cursor.execute(query)
for elm in cursor.fetchall():
    print(elm[1], elm[2], elm[3])

# completed course and crades
query =(""" SELECT  TRANSCRIPT.stu_id, TRANSCRIPT.transcript_id, TRANSCRIPT.course_id, COURSE.credit, TRANSCRIPT.grade
            FROM TRANSCRIPT INNER JOIN COURSE ON TRANSCRIPT.course_id = COURSE.course_id
            WHERE(
                (TRANSCRIPT.stu_id, TRANSCRIPT.course_id, TRANSCRIPT.term) 
                IN(
                    SELECT TRANSCRIPT.stu_id, TRANSCRIPT.course_id,  MAX(TRANSCRIPT.term) AS "selected_term"
                    FROM TRANSCRIPT
                    INNER JOIN COURSE ON TRANSCRIPT.course_id=COURSE.course_id
                    WHERE stu_id = '{0}'
                    GROUP BY TRANSCRIPT.course_id
                )
            )
        """
        ).format(1)

cursor.execute(query)
print(cursor.fetchall())





