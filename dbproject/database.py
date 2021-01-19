import MySQLdb
from settings import MYSQLPASSWORD, DATABASE


def database_init():

    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD);
    cursor = db.cursor()
    cursor.execute("DROP DATABASE IF EXISTS "+DATABASE)
    cursor.execute('CREATE DATABASE IF NOT EXISTS '+DATABASE)
    cursor.close()
    db.close()


    db = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
    cursor = db.cursor()


    cursor.execute("SHOW DATABASES")
    for database in cursor:
        print(database)

    sql_line =  """CREATE TABLE USER(
                    stu_id INT PRIMARY KEY AUTO_INCREMENT,
                    
                    stu_name VARCHAR(40) NOT NULL,
                    email VARCHAR(40) NOT NULL UNIQUE,
                    user_pass VARCHAR(64) NOT NULL,
                    
                    cat_term_id VARCHAR(200) NOT NULL
                    )
                """
    cursor.execute(sql_line)

    sql_line =  """CREATE TABLE CATALOG_TERM(
                    cat_term_id VARCHAR(200) NOT NULL,
                    course_id VARCHAR(10) NOT NULL,
                    PRIMARY KEY(cat_term_id, course_id)
                    )
                """
    cursor.execute(sql_line)

    sql_line =  """CREATE TABLE COURSE(
                    course_id VARCHAR(10) NOT NULL,
                    course_name VARCHAR(200) NOT NULL,
                    credit FLOAT(4) NOT NULL,
                    equ_code VARCHAR(10),
                    PRIMARY KEY(course_id)
                    )
                """
    cursor.execute(sql_line)

    sql_line =  """CREATE TABLE PREREQUISITE(
                    course_id VARCHAR(10) NOT NULL,
                    prereq_id VARCHAR(10) NOT NULL,
                    PRIMARY KEY(course_id, prereq_id)
                    )
                """
    cursor.execute(sql_line)

    sql_line =  """CREATE TABLE TRANSCRIPT(
                    transcript_id INT PRIMARY KEY AUTO_INCREMENT,

                    stu_id INT NOT NULL,
                    term VARCHAR(20) NOT NULL,
                    course_id VARCHAR(10) NOT NULL,

                    grade VARCHAR(2) DEFAULT 'XX',
                    ins_name VARCHAR(40) NOT NULL,
                    crn VARCHAR(10),
                    e_grade VARCHAR(2) DEFAULT 'XX'
                    )
                """
    cursor.execute(sql_line)

    cursor.execute("ALTER TABLE TRANSCRIPT ADD FOREIGN KEY(stu_id) REFERENCES USER(stu_id) ON UPDATE CASCADE")
    #cursor.execute("ALTER TABLE CATALOG_TERM ADD FOREIGN KEY(cat_term_id) REFERENCES USER(cat_term_id)")

    #cursor.execute("ALTER TABLE USER ADD FOREIGN KEY(cat_term_id) REFERENCES CATALOG_TERM(cat_term_id) ON DELETE RESTRICT")
    #cursor.execute("ALTER TABLE COURSE ADD FOREIGN KEY(course_id) REFERENCES CATALOG_TERM(course_id) ON UPDATE CASCADE")

    cursor.execute("ALTER TABLE CATALOG_TERM ADD FOREIGN KEY(course_id) REFERENCES COURSE(course_id) ON UPDATE CASCADE ON DELETE RESTRICT")
    cursor.execute("ALTER TABLE TRANSCRIPT ADD FOREIGN KEY(course_id) REFERENCES COURSE(course_id) ON UPDATE CASCADE ON DELETE RESTRICT")
    cursor.execute("ALTER TABLE PREREQUISITE ADD FOREIGN KEY(course_id) REFERENCES COURSE(course_id) ON UPDATE CASCADE ON DELETE RESTRICT")
    cursor.execute("ALTER TABLE PREREQUISITE ADD FOREIGN KEY(prereq_id) REFERENCES COURSE(course_id) ON UPDATE CASCADE ON DELETE RESTRICT")

    #cursor.execute("ALTER TABLE COURSE ADD FOREIGN KEY(course_id) REFERENCES PREREQUISITE(prereq_id) ON UPDATE CASCADE ON DELETE RESTRICT")

    #cursor.execute("ALTER TABLE USER ADD FOREIGN KEY(stu_id) REFERENCES TRANSCRIPT(stu_id) ON DELETE RESTRICT")
    #cursor.execute("ALTER TABLE COURSE ADD FOREIGN KEY(course_id) REFERENCES TRANSCRIPT(course_id) ON UPDATE RESTRICT")

    cursor.execute("SHOW TABLES")

    cursor.close()
    db.close()

