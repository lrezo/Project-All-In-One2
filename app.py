import os
import shutil
import sqlite3
from datetime import timedelta
from flask import Flask, render_template, flash, redirect, url_for, request, session, send_from_directory
from flask_ckeditor import CKEditor, upload_success, upload_fail
from flask_login import LoginManager
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_googletrans import translator


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hexabyte'
app.permanent_session_lifetime = timedelta(hours=1)
login = LoginManager(app)
login.login_view = "login"
db = sqlite3
ckeditor = CKEditor(app)
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
ts = translator(app)


@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/the/uploaded/directory'
    return send_from_directory(path, filename)



@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('/the/uploaded/directory', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url)  # return upload_success call


def create_app():
    app = Flask(__name__)
    ...
    ckeditor.init_app(app)
    ...
    return app


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def set_password(password):
    password_hash = generate_password_hash(password)
    return password_hash


def check_password(user, password):
    return check_password_hash(user, password)



def insertUser(username, password):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO login (username,password_hash) VALUES (?,?)", (username, password))
    con.commit()
    con.close()


def retrieveUsers():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT email, password_hash FROM login")
    users = cur.fetchall()
    con.close()
    return users


def get_user_data(email):
    free = ''
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT user.id, user.name, user.lastname,login.email, login.password,roles.name , user.student, user.class, user.schoolname  FROM login INNER JOIN user ON login.email = user.email INNER JOIN roles on user.role_id = roles.id")
    users = cur.fetchall()
    con.close()
    for i in users:
        if email in i:
            free = i
    return free


def get_user_email():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT login.email FROM login ")
    email = cur.fetchall()
    email = list(email)
    email_without_comma = []
    for i in email:
        email_without_comma.append(', '.join(i))
    con.close()
    return email_without_comma

def get_projects_id():
    cur = get_db_connection()
    cur = cur.cursor()
    cur.execute(
        "SELECT  projects.id FROM projects ")
    list_id = cur.fetchall()
    list_id = list(list_id)
    list_id_all = []
    for i in list_id:
        list_id_all.append(i[0])
    cur.close()
    return list_id_all


@login.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    curs = conn.cursor()
    curs.execute("SELECT * from login where id = (?)", [user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return int(lu[0])

@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = get_db_connection()
    classrooms = conn.execute('SELECT classroms.Class FROM classroms').fetchall()
    conn.close()
    if 'user' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        email = request.form['email']
        if email == "":
            flash('Email is required!')
        elif email not in get_user_email():
            flash('Email or password are wrong.')
        else:
            email = request.form['email']

            password = request.form['password']
            remember = bool(request.form.get('remember', True))
            conn = sqlite3.connect('database.db')
            curs = conn.cursor()
            curs.execute('UPDATE login SET  remember = ? WHERE email = ?',
                         (remember, email))
            conn.commit()
            conn.close()
            conn = sqlite3.connect('database.db')
            curs = conn.cursor()
            curs.execute("SELECT * FROM login where email = (?)", [email])
            user = list(curs.fetchone())
            user_remember = user[3]
            id_user = user[0]
            pss = user[2]
            user = user[1]

            if email == user and check_password_hash(pss, password):
                if user_remember == '1':
                    session.permanent = None
                else:
                    session.permanent = True
                session['user'] = get_user_data(email)
                readBlobData(session['user'][0])
                img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
                conn = get_db_connection()
                projects = conn.execute('SELECT * FROM projects').fetchall()
                conn.close()
                # flash(f"You have been successfully logged in {session['user'][1]} {session['user'][2]}")
                return render_template('index.html', user=f"{session['user'][1]} {session['user'][2]}",
                                       profile_pic=img_pic, projects=projects)

            else:
                flash('Email or password are wrong.')

    return render_template('login.html', classrooms=classrooms)

@app.route("/login/signup", methods=['GET', 'POST'])
def signup():
    conn = get_db_connection()
    classrooms = conn.execute('SELECT classroms.Class FROM classroms').fetchall()
    conn.close()
    if 'user' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email2 = request.form['email2']
        password2 = request.form['password2']

        if email2 == "" or name == "" or lastname == "" or password2  == "":
            flash('There are some information missing!')

        elif email2 in get_user_data(email2):
            flash('Email already Registered')
        else:
            def upload_profile_pic():
                profile_pic = request.files['img']
                return profile_pic.read()
            name = request.form['name']
            lastname = request.form['lastname']
            email2 = request.form['email2']
            password2 = request.form['password2']
            password2 = set_password(password2)
            classroom = request.form['class']
            role = request.form['role']
            role_id = 2
            school = 'Don Bosco Sint-Denijs-Westrem'
            conn = sqlite3.connect('database.db')
            curs = conn.cursor()
            curs.execute(
                'INSERT INTO user (name, lastname, email,profile_pic,role_id,student,class,schoolname) VALUES (?, ?, ?, ?,?,?,?,?)',
                (name, lastname, email2,upload_profile_pic(), role_id, role, classroom, school))
            conn.commit()
            curs.execute('INSERT INTO login (email,password) VALUES (?,?)', (email2, password2))
            conn.commit()
            conn.close()
            flash('Registered successfully')

    return render_template('login.html',classrooms=classrooms)



def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBlobData(empId):
    sqliteConnection = sqlite3.connect('database.db')

    cursor = sqliteConnection.cursor()

    sql_fetch_blob_query = """SELECT * from user where id = ?"""
    cursor.execute(sql_fetch_blob_query, (empId,))
    record = cursor.fetchall()
    for row in record:
        name = row[1]
        photo = row[4]
        photoPath = f"static/img/profile-pics/{str(empId)}"
        try:
            os.makedirs(photoPath)
            photoPath = f"static/img/profile-pics/{str(empId)}/\\" + name + ".jpg"
            writeTofile(photo, photoPath)
            cursor.close()
        except:
            photoPath = f"static/img/profile-pics/{str(empId)}/\\" + name + ".jpg"
            writeTofile(photo, photoPath)
            cursor.close()




@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user']
        flash(f"You have been logged out {user[1]} {user[2]}")
    session.pop('user', None)

    return redirect(url_for('login'))


@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    if 'user' in session:
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        return render_template('index.html', user=user, profile_pic=img_pic, projects=projects, users = users)
    return render_template('index.html', projects=projects, users =users)
# @app.route('/<string:page_name>')
# def html_page(page_name):
# return render_template(page_name)


@app.route('/profile')
def profile():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    count = 0
    for project in projects:
        if 'user' in session and project['user_id'] == session['user'][0]:
            count += 1
    if 'user' in session:
        user = f"{session['user'][1]} {session['user'][2]}"
        student = session['user'][6]
        school_class = session['user'][7]
        school_name = session['user'][8]
        email = session['user'][3]
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        return render_template('profile.html', user=user, profile_pic=img_pic, student=student,
                               school_class=school_class, school_name=school_name, email=email, projects=projects,
                               counter_p=count)
    else:
        return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    if 'user' in session:
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        return render_template('404.html', user=user, profile_pic=img_pic), 404
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500


@app.route('/<string:page>.html')
def page(page):
    try:
        return redirect(url_for(page)) or render_template(page)
    except:
        if 'user' in session:
            user = f"{session['user'][1]} {session['user'][2]}"
            img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
            return render_template('404.html', user=user, profile_pic=img_pic)
        return render_template('404.html')


@app.route('/project')
def template():
    conn = get_db_connection()
    users_name = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    if 'user' in session:
        for i in users_name:
            print(i)
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        return render_template('projects/project.html', user=user, profile_pic=img_pic, users_name = users_name)
    return render_template('projects/project.html',users_name=users_name)


@app.route('/create', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    if 'user' in session:
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        if request.method == 'POST':
            title = request.form['title']
            content = request.form.get('ckeditor')
            user_id = session['user'][0]
            user_fullname = f"{session['user'][1]} {session['user'][2]}"
            user_name = session['user'][1]
            photos_of_the_project = request.files.getlist('photo_slider')
            photos_of_the_project_list = []
            mate2 = request.form['mate2']
            numbers_lett = list('123456789')
            mate2_id = ''
            if mate2 == 'Choose your team mate':
                mate2 = ''
            for i in mate2:
                if i in numbers_lett:
                    mate2_id +=i
                break
            mate2 = mate2[2:]
            mate2_name = mate2.split(' ')
            if not title:
                flash('Title is required!')


            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO projects (title, content, user_id, user_name_1, user_1_name, user_id_2, user_name_2, user_2_name) VALUES (?, ?, ?, ?,?,?,?,?)',
                             (title, content, user_id, user_fullname, user_name,mate2_id,mate2, mate2_name[0]))
                conn.commit()
                conn.close()
                UPLOAD_FOLDER = f'static/img/project/{str(get_projects_id()[-1])}/{title}'
                try:
                    os.makedirs(UPLOAD_FOLDER)
                    for photo in photos_of_the_project:
                        filename = secure_filename(photo.filename)
                        photos_of_the_project_list.append(filename)
                        photo.save(os.path.join(UPLOAD_FOLDER, filename))
                except:
                    for photo in photos_of_the_project:
                        filename = secure_filename(photo.filename)
                        photos_of_the_project_list.append(filename)
                        photo.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('index'))

        return render_template('create.html', user=user, profile_pic=img_pic, users=users)
    else:
        conn = get_db_connection()
        projects = conn.execute('SELECT * FROM projects').fetchall()
        conn.close()
        return render_template('index.html', projects=projects)


@app.route('/projects/<int:project_id>/edit', methods=('GET', 'POST'))
def edit(project_id):
    UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
    basename = os.listdir(UPLOAD_FOLDER)
    project = get_post(project_id)
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    try:
        if 'user' in session and project['user_id'] == session['user'][0] or project['user_id_2'] == session['user'][0]:
            user = f"{session['user'][1]} {session['user'][2]}"
            img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
            if request.method == 'POST':
                photos_of_the_project = request.files.getlist('photo_slider')
                print(photos_of_the_project)
                photos_of_the_project_list = []
                mate2 = request.form['mate2']
                print(mate2)
                numbers_lett = list('123456789')
                mate2_id = ''
                if mate2 != '':
                    for i in users:
                        if str(i['id']) == project['user_id_2']:
                            break
                if mate2 == 'Choose your team mate':
                    mate2 = ''
                for i in mate2:
                    if i in numbers_lett:
                        mate2_id +=i
                    break
                mate2 = mate2[2:]
                mate2_name = mate2.split(' ')
                content = request.form.get('ckeditor')
                title = request.form['title']
                os.rename(f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}',f'static/img/project/{str(project_id)}/{title}')
                user_id = session['user'][0]
                conn = get_db_connection()
                conn.execute('UPDATE projects SET  content = ?, title = ?,  user_id_2 = ?, user_name_2 = ?, user_2_name = ?' 'WHERE id = ?',
                             (content, title,  mate2_id ,mate2, mate2_name[0],project_id))
                conn.commit()
                conn.close()

                UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
                try:
                    for photo in photos_of_the_project:
                        filename = secure_filename(photo.filename)
                        photos_of_the_project_list.append(filename)
                        photo.save(os.path.join(UPLOAD_FOLDER, filename))
                    flash('The project "{}" was successfully edited!'.format(project['title']))
                    return redirect(url_for('index'))
                except:
                    flash('The project "{}" was successfully edited!'.format(project['title']))
                    return redirect(url_for('index'))
                return redirect(url_for('index'))
            return render_template('edit.html', user=user, profile_pic=img_pic, post=project,photos_slider = basename, path = UPLOAD_FOLDER, users=users)
        elif 'user' in session and project['user_id'] != session['user'][0]:
            user = f"{session['user'][1]} {session['user'][2]}"
            img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
            project = get_post(project_id)
            return render_template('notinproject.html', user=user, profile_pic=img_pic, post=project)
    except:
        conn = get_db_connection()
        projects = conn.execute('SELECT * FROM projects').fetchall()
        conn.close()
        return render_template('index.html', projects=projects)

def get_post(project_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?',
                           [project_id]).fetchone()
    conn.close()
    if project is None:
        abort(404)
    return project



@app.route('/projects/<int:project_id>/delete', methods=('POST', 'GET'))
def delete(project_id):
    project_id = int(project_id)
    project = get_post(project_id)
    try:
        if project['user_id'] == session['user'][0]:
            conn = get_db_connection()
            conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
            conn.commit()
            conn.close()
            UPLOAD_FOLDER = f'static/img/project/{str(project_id)}'

            try:
                shutil.rmtree(UPLOAD_FOLDER)
            except:
                return redirect(url_for('index'))
            flash('The project "{}" was successfully deleted!'.format(project['title']))
        elif 'user' in session and project['user_id'] != session['user'][0]:
            user = f"{session['user'][1]} {session['user'][2]}"
            img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
            project = get_post(project_id)
            return render_template('notinproject.html', user=user, profile_pic=img_pic, post=project)
        if request.path == "/":
            return redirect(url_for('project'))
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))


@app.route('/projects/<int:project_id>/delete/<img>' , methods=('POST','GET'))
def delete_img(project_id, img):
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    conn.close()
    UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
    basename = os.listdir(UPLOAD_FOLDER)
    project = get_post(project_id)
    UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{project[2]}/{img}'
    if 'user' in session and project['user_id'] == session['user'][0] or project['user_id_2'] == session['user'][0] :
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        if request.method == 'GET':
            try:
                os.remove(UPLOAD_FOLDER)
                UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
                basename.remove(img)
            except:
                UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
                return render_template('index.html')
            return render_template('edit.html',  user=user, profile_pic=img_pic, post=project,photos_slider = basename, path = UPLOAD_FOLDER, users = users)
        elif request.method == 'POST':
            photos_of_the_project = request.files.getlist('photo_slider')
            print(photos_of_the_project)
            photos_of_the_project_list = []
            mate2 = request.form['mate2']
            print(mate2)
            numbers_lett = list('123456789')
            mate2_id = ''
            if mate2 != '':
                for i in users:
                    if str(i['id']) == project['user_id_2']:
                        break
            if mate2 == 'Choose your team mate':
                mate2 = ''
            for i in mate2:
                if i in numbers_lett:
                    mate2_id += i
                break
            mate2 = mate2[2:]
            mate2_name = mate2.split(' ')
            content = request.form.get('ckeditor')
            title = request.form['title']
            os.rename(f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}',
                      f'static/img/project/{str(project_id)}/{title}')
            user_id = session['user'][0]
            conn = get_db_connection()
            conn.execute('UPDATE projects SET  content = ?, title = ?,  user_id_2 = ?, user_name_2 = ?, user_2_name = ?' 'WHERE id = ?',
                (content, title, mate2_id, mate2, mate2_name[0], project_id))
            conn.commit()
            conn.close()
            UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
            try:
                for photo in photos_of_the_project:
                    filename = secure_filename(photo.filename)
                    photos_of_the_project_list.append(filename)
                    photo.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('The project "{}" was successfully edited!'.format(project['title']))
                return redirect(url_for('index'))
            except:
                flash('The project "{}" was successfully edited!'.format(project['title']))
                return redirect(url_for('index'))

        return render_template('edit.html', user=user, profile_pic=img_pic, post=project,photos_slider = basename, path = UPLOAD_FOLDER, users = users)

    elif 'user' in session and project['user_id'] != session['user'][0]:
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        project = get_post(project_id)
        return render_template('notinproject.html', user=user, profile_pic=img_pic, post=project)
    if request.path == "/":
        return redirect(url_for('project'))
    else:
        return redirect(url_for('index'))


@app.route('/projects/<int:project_id>')
def project(project_id):
    UPLOAD_FOLDER = f'static/img/project/{str(project_id)}/{get_post(project_id)[2]}'
    basename = os.listdir(UPLOAD_FOLDER)
    len_basename = len(basename)
    project = get_post(project_id)
    if 'user' in session:
        user = f"{session['user'][1]} {session['user'][2]}"
        img_pic = url_for('static', filename=f'img/profile-pics/{session["user"][0]}/' + session['user'][1] + ".jpg")
        return render_template('projects/project.html', post=project, user=user, profile_pic=img_pic, photos_slider = basename, path = UPLOAD_FOLDER, lenpath = len_basename)
    return render_template('projects/project.html', post=project, photos_slider = basename, path = UPLOAD_FOLDER, lenpath = len_basename)

@app.route('/password-recovery')
def recovery_password():
    return render_template('forgot_password.html')


if __name__ == '__main__':
    app.run(debug=True)
