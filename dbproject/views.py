from flask import render_template, redirect, request, url_for, session
import dbOps
from settings import TERM_OPTIONS, REGISTER_OPTIONS, RESPOND_TEXT



def signup_page():
    if "user_id" in session:
        return redirect(url_for("home_page"))

    else: 
        if request.method=="GET":
            return render_template("signup.html", cat_terms=REGISTER_OPTIONS)
        else:
            user_email = str(request.form["email_form"])
            user_password = str(request.form["password_form"])
            user_name = str(request.form["stu_name_form"])
            user_cat_term = str(request.form["stu_cat_term_form"])
            user_cat_term = user_cat_term.replace("_"," ")
            message = dbOps.sign_up(user_name, user_email, user_password, user_cat_term)
            return render_template("login.html", message=message)
        



def login_page():
    if "user_id" in session:
        return redirect(url_for("home_page"))
    else:    
        message = ""
        if request.method=="GET":
            return render_template("login.html")
        else:
            user_email = str(request.form["email_form"])
            user_password = str(request.form["password_form"])
            
            if dbOps.login_checker(user_email, user_password)!=None:
                USER_ID, USER_NAME, USER_MAIL, USER_TERM = dbOps.login_checker(user_email, user_password)
                session["user_id"] = USER_ID
                session["user_name"] = USER_NAME
                session["user_mail"] = USER_MAIL
                session["user_term"] = USER_TERM

                message = RESPOND_TEXT["SUCCESS_LOGIN_MESSAGE"]
                return render_template("home.html",  profileInfo=dbOps.profileInfo(), message=message)

            else:
                message = RESPOND_TEXT["FAIL_LOGIN_MESSAGE"]
                return render_template("login.html", message=message)


    

def logout():
    if "user_id" in session:
        session.pop("user_id", None)
        session.pop("user_name", None)
        session.pop("user_mail", None)
        session.pop("user_term", None)

        message = RESPOND_TEXT["SUCCESS_LOGOUT_MESSAGE"]
        return render_template("home.html", message=message)
    else:
        return redirect(url_for("home_page"))


def home_page():
    if "user_id" in session:
        return render_template("home.html", profileInfo=dbOps.profileInfo())
    else:
        return render_template("home.html")



def transcript_page():
    if "user_id" in session:
        return render_template("transcript.html", results=dbOps.getTranscript() )
    else:
        return render_template("home.html")

def catalogterm_page():
    if "user_id" in session:
        return render_template("catalogterm.html", results=dbOps.summary() )
    else:
        return render_template("home.html")

def editing_page():
    if "user_id" in session:
        message = ""
        if request.method=="POST":
            
            try:
                if request.form["would_be_deleted"]:
                    transcript_id = int(request.form["would_be_deleted"])
                    message = dbOps.delete_on_transcript(transcript_id)
                    return render_template("mapout.html", transcript=dbOps.getTranscript(), GPA = dbOps.calculate_GPA(),eGPA = dbOps.calculate_GPA("e_grade"), catalog_courses=dbOps.getCatalogTerm(), terms=TERM_OPTIONS, message=message)
            except:
                message = "Something goes wrong (1)\t"


            try:
                if request.form["edit"]:
                    message = "You are editing course number " + str(int(request.form["edit"]))
                    transcript_id = int(request.form["edit"])
                    return render_template("editing.html", transcript_id=transcript_id, transcript=dbOps.getTranscript(),  past_selection=dbOps.getTranscript( "*", transcript_id), GPA=dbOps.calculate_GPA(), eGPA = dbOps.calculate_GPA("e_grade"),  catalog_courses=dbOps.getCatalogTerm(), terms=TERM_OPTIONS, message=message)
                    
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
                return render_template("mapout.html", transcript=dbOps.getTranscript(), GPA = dbOps.calculate_GPA(), eGPA = dbOps.calculate_GPA("e_grade"), catalog_courses=dbOps.getCatalogTerm(), terms=TERM_OPTIONS, message=message)
            except:
                message = "Something goes wrong (3)"

            return render_template("mapout.html", transcript=dbOps.getTranscript(), GPA = dbOps.calculate_GPA(), eGPA = dbOps.calculate_GPA("e_grade"), catalog_courses=dbOps.getCatalogTerm(), terms=TERM_OPTIONS,  message=message)
    else:
        return render_template("home.html")



def mapout_page():
    if "user_id" in session:
        if request.method=="GET":
            return render_template("mapout.html", transcript=dbOps.getTranscript(), GPA=dbOps.calculate_GPA(),  eGPA = dbOps.calculate_GPA("e_grade"), catalog_courses=dbOps.getCatalogTerm(), terms=TERM_OPTIONS)
        else:
            course_term = str(request.form["course_term_form"])
            course_id = str(request.form["course_code_form"]).replace("_", " ")
            course_insname = str(request.form["course_insname_form"])
            course_grade = str(request.form["course_grade_form"])
            course_e_grade = str(request.form["course_e_grade_form"])
            addingResult = dbOps.add_course_to_transcript(course_term, course_id, course_grade, course_insname, course_e_grade)
            

            new_course = {"course_id":course_id, 
                        "course_term":course_term, 
                        "course_insname":course_insname,
                        "course_grade": course_grade,
                        "course_e_grade": course_e_grade
                        }
            
            return render_template("mapout.html", transcript=dbOps.getTranscript(), GPA = dbOps.calculate_GPA(), eGPA = dbOps.calculate_GPA("e_grade"), new_course= new_course, addingResult=addingResult, catalog_courses=dbOps.getCatalogTerm(), terms=TERM_OPTIONS)
    else:
        return render_template("home.html")

