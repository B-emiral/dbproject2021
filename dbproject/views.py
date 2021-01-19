from flask import render_template, redirect, request, url_for
import dbOps
from settings import TERM_OPTIONS, REGISTER_OPTIONS, RESPOND_TEXT

WAS_LOGGED = False
USER_ID = None
USER_NAME = None
USER_MAIL = None
USER_TERM = None


def signup_page():
    if request.method=="GET":
        return render_template("signup.html", wasLogged=WAS_LOGGED, cat_terms=REGISTER_OPTIONS)
    else:
        user_email = str(request.form["email_form"])
        user_password = str(request.form["password_form"])
        user_name = str(request.form["stu_name_form"])
        user_cat_term = str(request.form["stu_cat_term_form"])
        user_cat_term = user_cat_term.replace("_"," ")
        message = dbOps.sign_up(user_name, user_email, user_password, user_cat_term)
        return render_template("login.html", wasLogged=WAS_LOGGED, user_name=USER_NAME, user_reg_term=USER_TERM, message=message)

def login_page():
    message = ""

    global WAS_LOGGED
    if request.method=="GET":
        return render_template("login.html", wasLogged=WAS_LOGGED)
    else:
        global USER_ID
        global USER_NAME
        global USER_MAIL
        global USER_TERM
        user_email = str(request.form["email_form"])
        user_password = str(request.form["password_form"])
        
        if dbOps.login_checker(user_email, user_password)!=None:
            WAS_LOGGED = True
            USER_ID, USER_NAME, USER_MAIL, USER_TERM = dbOps.login_checker(user_email, user_password)
            message = RESPOND_TEXT["SUCCESS_LOGIN_MESSAGE"]
        else:
            message = RESPOND_TEXT["FAIL_LOGIN_MESSAGE"]

        return render_template("home.html",user_name=USER_NAME, user_reg_term=USER_TERM, profileInfo=dbOps.profileInfo(USER_ID, USER_TERM), message=dbOps.profileInfo(USER_ID, USER_TERM),wasLogged=WAS_LOGGED)

    

def logout():
    global WAS_LOGGED
    WAS_LOGGED = False
    message = RESPOND_TEXT["SUCCESS_LOGOUT_MESSAGE"]
    return render_template("home.html", wasLogged=WAS_LOGGED, message=message)

def home_page():
    return render_template("home.html",user_name=USER_NAME, user_reg_term=USER_TERM, profileInfo=dbOps.profileInfo(USER_ID, USER_TERM), message=dbOps.profileInfo(USER_ID, USER_TERM),wasLogged=WAS_LOGGED)


def transcript_page():
    return render_template("transcript.html", results=dbOps.getTranscript(USER_ID), wasLogged=WAS_LOGGED, user_reg_term=USER_TERM)

def catalogterm_page():
    return render_template("catalogterm.html", results=dbOps.summary(USER_ID, USER_TERM), wasLogged=WAS_LOGGED, user_reg_term=USER_TERM )

def editing_page():
    message = ""
    if request.method=="POST":
        
        try:
            if request.form["would_be_deleted"]:
                transcript_id = int(request.form["would_be_deleted"])
                message = dbOps.delete_on_transcript(transcript_id)
                return render_template("mapout.html", transcript=dbOps.getTranscript(USER_ID), GPA = dbOps.calculate_GPA(USER_ID),eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"), catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, wasLogged=WAS_LOGGED, message=message)
        except:
            message = "Something goes wrong (1)\t"


        try:
            if request.form["edit"]:
                message = "You are editing course number " + str(int(request.form["edit"]))
                transcript_id = int(request.form["edit"])
                return render_template("editing.html",transcript_id=transcript_id, transcript=dbOps.getTranscript(USER_ID),  past_selection=dbOps.getTranscript(USER_ID, "*", transcript_id), GPA=dbOps.calculate_GPA(USER_ID), eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"),  catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, wasLogged=WAS_LOGGED, message=message)
                #return render_template("editing.html", transcript_id=transcript_id, transcript=dbOps.getTranscript(USER_ID), GPA=dbOps.calculate_GPA(USER_ID), eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"), catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, past_selection=dbOps.getTranscript(USER_ID, "*", transcript_id), wasLogged=WAS_LOGGED, message=message)
        except:
            message = "Something goes wrong (2)\t"

        
        try:
            transcript_id = int(request.form["transcript_id_form"])
            new_course_term = str(request.form["course_term_form"])
            new_course_id = str(request.form["course_code_form"])
            new_course_insname = str(request.form["course_insname_form"])
            new_course_grade = str(request.form["course_grade_form"])
            new_course_e_grade = str(request.form["course_e_grade_form"])
            message = dbOps.update_course_on_transcript(transcript_id, new_course_term, new_course_id, new_course_grade, new_course_insname,new_course_e_grade)
            return render_template("mapout.html", transcript=dbOps.getTranscript(USER_ID), GPA = dbOps.calculate_GPA(USER_ID), eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"), catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, wasLogged=WAS_LOGGED, message=message)
        except:
            message = "Something goes wrong (3)"

        return render_template("mapout.html", transcript=dbOps.getTranscript(USER_ID), GPA = dbOps.calculate_GPA(USER_ID), eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"), catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, wasLogged=WAS_LOGGED, message=message)

def mapout_page():
    if request.method=="GET":
        return render_template("mapout.html", transcript=dbOps.getTranscript(USER_ID), GPA=dbOps.calculate_GPA(USER_ID),  eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"), catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, wasLogged=WAS_LOGGED)
    else:
        course_term = str(request.form["course_term_form"])
        course_id = str(request.form["course_code_form"]).replace("_", " ")
        course_insname = str(request.form["course_insname_form"])
        course_grade = str(request.form["course_grade_form"])
        course_e_grade = str(request.form["course_e_grade_form"])
        addingResult = dbOps.add_course_to_transcript(USER_ID, course_term, course_id, course_grade, course_insname, course_e_grade)
        

        new_course = {"course_id":course_id, 
                    "course_term":course_term, 
                    "course_insname":course_insname,
                    "course_grade": course_grade,
                    "course_e_grade": course_e_grade
                    }
        
        return render_template("mapout.html", transcript=dbOps.getTranscript(USER_ID), GPA = dbOps.calculate_GPA(USER_ID), eGPA = dbOps.calculate_GPA(USER_ID,"e_grade"), new_course= new_course, addingResult=addingResult, catalog_courses=dbOps.getCatalogTerm(USER_TERM), terms=TERM_OPTIONS, wasLogged=WAS_LOGGED)


