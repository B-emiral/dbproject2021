DEBUG = True
PORT = 8080
MYSQLPASSWORD = "password"
DATABASE = "test"



TERM_OPTIONS =[
                "18Fall(17-18)", "18Spring", "18Summer",
                "19Fall(18-19)", "19Spring", "19Summer",
                "20Fall(19-20)", "20Spring", "20Summer",
                "21Fall(20-21)", "21Spring", "21Summer"
            ]

REGISTER_OPTIONS =[
        """Computer Engineering (%100 English) Program Curriculum - Student's Catalog Term: Between 2011-2012 Fall Semester and 2017-2018 Fall Semester""".replace(" ","_"),
        """Computer Engineering (%100 English) Program Curriculum - Student's Catalog Term: After 2017-2018  Fall Semester""".replace(" ","_")
    ]


RESPOND_TEXT = { 
            "SUCCESS_LOGOUT_MESSAGE":"Logout Succesful",
            "SUCCESS_LOGIN_MESSAGE":"Login Succesful",
            "FAIL_LOGIN_MESSAGE":"Login Fail",
            "SUCCESS_SIGNUP_MESSAGE":"Signup Successful",
            "FAIL_SIGNUP_MESSAGE":"Signup Fail"
            }



#from platform import python_version
#print(python_version())

# cd <project_folder>
# python3 -m venv venv
# . venv/bin/activate