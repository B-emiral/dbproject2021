import MySQLdb
from settings import MYSQLPASSWORD, DATABASE

database = MySQLdb.connect(host="localhost", user="root", passwd=MYSQLPASSWORD, db=DATABASE)
cursor = database.cursor()

cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("BLG 101E","BIL 103E"))
cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("BLG 102E","BIL 105E"))

cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("BLG 113E","BLG 111E"))
cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("BLG 223E","BLG 233E"))
cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("BLG 317E","BLG 361E"))
cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("BLG 4902E","BLG 492E"))

cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("MAT 103E","MAT 101E"))
cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("MAT 104E","MAT 102E"))
cursor.execute(""" UPDATE COURSE SET equ_code = '{0}' WHERE course_id = '{1}' """.format("MAT 210E","MAT 201E"))

database.commit()
cursor.close()
database.close()

