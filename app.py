from flask import Flask, render_template, request, make_response, redirect, send_from_directory, url_for
from selen import ManagebacDriver
from cache import cache_grade_data, get_grade_data
from dbm.credentials import Credentials
from dbm.scores import Scores
from dbm.mochi import Mochi
from dbm.notebooks import Notebooks
from functionals.grades import new_task_predict, radar_ranks, perc2rank, radar_percs, radar_ranks_edge, radar_percs_edge
from functionals.files import allowed_file
from werkzeug.utils import secure_filename
import os
import sys
import logging
import time
import threading
import json

app = Flask("app")

app.config["MAX_CONTENT_LENGTH"] = 128 * 1000 * 1000
app.config["UPLOAD_FOLDER"] = os.path.abspath("files")

stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(name)s - %(message)s")
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("logs.log")
file_handler.setFormatter(formatter)

app.logger.handlers.clear()
app.logger.addHandler(stream_handler)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)


@app.route("/radar")
def radar():
    # Since /radar is from /grades, safe to assume that grades data is cached
    g = get_grade_data(request.cookies.get("username"))
    subjects = [i["class_name"] for i in g]
    ranks = [perc2rank(i["grades"][0][1]) for i in g]
    percs = [i["grades"][0][1] for i in g]
    src = radar_ranks(subjects, ranks)
    src2 = radar_percs(subjects, percs)
    src3 = radar_ranks_edge(subjects, ranks)
    src4 = radar_percs_edge(subjects, percs)
    app.logger.info(f"Radar graph at {src}, {src2}, {src3}, {src4}")
    return render_template("radar.html", src=src, src2=src2, src3=src3, src4=src4)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/toolbox")
def toolbox():
    return render_template("toolbox.html")


@app.route("/toolbox/<sub>")
def toolbox_sub(sub):
    if sub == "mochi":
        mochi = Mochi()
        decks = mochi.browse()
        return render_template("mochi.html", decks=decks)

    elif sub == "notebooks":
        notebooks = Notebooks()
        l = notebooks.browse()
        return render_template("notebooks.html", notebooks=l)

    # elif sub == "trend":
    #     if request.method == "GET":
    #         username = request.cookies.get("username")
    #         if username is None:
    #             return redirect(url_for("settings"))

            # credentials = Credentials()
            # data = credentials.search(username)
            # if len(data) == 0:  # Data not cached
            #     grades_data = cache_grade_data(username, request.cookies.get("password"), int(request.cookies.get("microsoft")))
            #     return render_template("trend.html", classes=[i["class_name"] for i in grades_data])
            # else:  # Data cached
            #     data = data[-1]
            #     return render_template("trend.html", classes=data[3:])

        # elif request.method == "POST":
        #     subject = request.form.get("class")

            # driver = ManagebacDriver(request.cookies.get("username"), request.cookies.get("password"), int(request.cookies.get("microsoft")))
            # past_tasks = driver.get_past_tasks(subject)
            # driver.terminate()

            # trend = []
            # for name, score in past_tasks.items():
            # return render_template("radar.html", prev_href="/toolbox/trend", prev="Trend Graphs", title="Trend Graph", src=src)

    app.logger.error(f"Subdomain out of range at /toolbox/<sub>; requested /toolbox/{sub}")
    return f"Subdomain out of range at /toolbox/<sub>; requested /toolbox/{sub}"


@app.route("/download/<sub>")
def download(sub):
    app.logger.info(f"Download requested for file {os.path.join(app.config["UPLOAD_FOLDER"], sub)}")
    return send_from_directory(app.config["UPLOAD_FOLDER"], sub)


@app.route("/upload/<sub>", methods=["POST", "GET"])
def upload(sub):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username is None or password is None:
        return redirect(url_for("settings"))

    if sub == "mochi":
        if request.method == "GET":
            return render_template("upload_mochi.html", success=False)

        elif request.method == "POST":
            file = request.files["deck_file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                mochi = Mochi()
                name = request.form.get("name")
                description = request.form.get("description")
                mochi.new(name, description, request.cookies.get("username").split('@')[0][2:], os.path.join(app.config["UPLOAD_FOLDER"], filename))

                app.logger.info(f"Upload requested at /upload/{sub}: {os.path.join(app.config["UPLOAD_FOLDER"], filename)}")
                return render_template("upload_mochi.html", success=True)

            else:
                app.logger.error(f"Illegal upload requested at /upload/{sub}: {file.filename}")
                return f"Illegal upload requested at /upload/{sub}: {file.filename}"

    elif sub == "notebooks":
        if request.method == "GET":
            return render_template("upload_notebooks.html", success=False)

        elif request.method == "POST":
            file = request.files["notebook_file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                notebooks = Notebooks()
                name = request.form.get("name")
                description = request.form.get("description")
                notebooks.new(name, description, request.cookies.get("username").split('@')[0][2:], os.path.join(app.config["UPLOAD_FOLDER"], filename))

                app.logger.info(f"Upload requested at /upload/{sub}: {os.path.join(app.config["UPLOAD_FOLDER"], filename)}")
                return render_template("upload_notebooks.html", success=True)

            else:
                app.logger.error(f"Illegal upload requested at /upload/{sub}: {file.filename}")
                return f"Illegal upload requested at /upload/{sub}: {file.filename}"

    app.logger.error(f"Subdomain out of range at /upload/<sub>; requested /upload/{sub}")
    return f"Subdomain out of range at /upload/<sub>; requested /upload/{sub}"


@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    subject = request.args.get("subject")
    if subject is None:
        app.logger.error("No subject specified at /tasks")
        return "No subject specified at /tasks"

    # Since /tasks is redirected from /grades, we can assume the grades data is cached
    if request.method == "GET":
        scores = Scores()
        categories = [i[0] for i in scores.get_weight_names(subject)]
        return render_template("tasks.html", categories=categories[2:])

    elif request.method == "POST":
        credentials = Credentials()
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        driver = ManagebacDriver(username, password, microsoft=int(request.cookies.get("microsoft")))

        id = credentials.search(username)[-1][0]
        category = request.form.get("category")
        new_raw_score = int(request.form.get("new_raw_score"))
        new_max_score = int(request.form.get("new_max_score"))
        scores = Scores()
        current_overall = scores.search_score(id, subject)[-1][1]
        task_num = driver.get_task_num(subject, category)
        local_avg = scores.get_category_score(id, subject)[category]

        driver.terminate()

        grades_dict = {}

        g = get_grade_data(username)
        for s in g:
            if s["class_name"] == subject:
                for c in s["grades"]:
                    if c[0] == "Overall":
                        continue
                    grades_dict[c[0]] = (c[1] if type(c[1]) is float else None, c[2])

        new_local_avg, new_overall, delta_local, delta_overall = new_task_predict(new_raw_score, new_max_score, current_overall, task_num, local_avg, grades_dict, category)

        return render_template("tasks_calc.html", origin=subject, category=category, new_raw_score=new_raw_score, new_max_score=new_max_score, new_overall=new_overall, delta_overall=delta_overall, new_local_avg=new_local_avg, delta_local=delta_local)

    app.logger.error("Unknown request method at /tasks")
    return "Unknown request method at /tasks"


@app.route("/settings", methods=["POST", "GET"])
def settings():
    if request.method == "GET":
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        if username is not None and password is not None:  # Already logged in
            microsoft = bool(int(request.cookies.get("microsoft")))
            return render_template("settings.html", success=False, logged_in=True, username=username, password='*'*len(password), microsoft=microsoft)
        return render_template("settings.html", success=False, logged_in=False)

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        n = request.args.get("next")

        if n is None:
            res = make_response(render_template("settings.html", success=True, logged_in=True, username=username, password='*'*len(password), microsoft=True if request.form.get("microsoft") == "microsoft" else False))
            res.set_cookie("username", username)
            res.set_cookie("password", password)
            res.set_cookie("microsoft", "1" if request.form.get("microsoft") == "microsoft" else "0")
            return res
        else:
            res = make_response(redirect(url_for(n)))
            res.set_cookie("username", username)
            res.set_cookie("password", password)
            res.set_cookie("microsoft", "1" if request.form.get("microsoft") == "microsoft" else "0")
            return res

    app.logger.error("Unknown request method at /settings")
    return "Unknown request method at /settings"


@app.route("/get_cache_grade_data_progress")
def get_cache_grade_data_progress():
    progress = {"progress": GLOB_cache_gpa_progress[request.cookies.get("username")]}
    return json.dumps(progress)


def cache_grade_data_wrapper(username, password, microsoft, dest):
    global GLOB_cache_gpa_progress

    for i in cache_grade_data(username, password, microsoft, dest):
        GLOB_cache_gpa_progress[username] = i


@app.route("/load_grades")
def load_grades():
    global GLOB_gpa_data
    global GLOB_cache_gpa_progress

    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username is None or password is None:
        return redirect(url_for("settings", next="load_grades"))

    GLOB_gpa_data[username] = None
    credentials = Credentials()

    if len(credentials.search(username)) > 0 and int(request.args.get("reload", 0)) == 0:  # Data cached
        GLOB_cache_gpa_progress[username] = 0.
        GLOB_gpa_data[username] = get_grade_data(username)
        GLOB_cache_gpa_progress[username] = 1.
    elif len(credentials.search(username)) == 0 or int(request.args.get("reload", 0)) == 1:  # Data not cached
        GLOB_gpa_data[username] = []
        GLOB_cache_gpa_progress[username] = 0.
        c = threading.Thread(target=cache_grade_data_wrapper, args=(username, password, int(request.cookies.get("microsoft")), GLOB_gpa_data[username]), daemon=True)
        c.start()

    return render_template("load_grades.html")


@app.route("/grades", methods=["POST", "GET"])
def grades():
    if request.method == "GET":
        return render_template("grades.html", grades=GLOB_gpa_data[request.cookies.get("username")])

    elif request.method == "POST":
        subject = request.form.get("subject")
        term = request.form.get("term")
        target = request.form.get("target")

        result = None
        overall = 0.
        for s in GLOB_gpa_data[request.cookies.get("username")]:
            if s["class_name"] == subject:
                overall = s["grades"][0][1]
                overall = 0. if overall is None else overall
                if term == "mid":
                    result = ((0.7 * float(target)) - (0.5 * overall)) / 0.2
                elif term == "final":
                    result = (float(target) - (0.7 * overall)) / 0.3
                break
        return render_template("grades_calc.html", result=f"{result:0.3f}", target=target, term=term, subject=subject, overall=overall)

    app.logger.error("Unknown request method at /grades")
    return "Unknown request method at /grades"


@app.route('/')
def root():
    username = request.cookies.get("username")
    if username is None:
        return render_template("index.html", name=None)

    l = username.split('@')
    return render_template("index.html", name=l[0][2:])


def tick():
    app.logger.info("Tick")

    os.system(f"rm -rf {os.path.abspath("static/gen")}/*.png")

    credentials = Credentials()
    for i in credentials.browse():
        for _ in cache_grade_data(i[0], i[1], i[2], []):
            pass

    app.logger.info("Tock")
    time.sleep(86400)


if __name__ == "__main__":
    os.system("mkdir -p files; cd static; mkdir -p gen")

    db_reset = bool(int(os.environ.get("db_reset", False)))
    debug = bool(int(os.environ.get("debug", False)))
    logs_reset = bool(int(os.environ.get("logs_reset", True)))

    if logs_reset:
        os.system("rm -rf logs.log")

    if db_reset:
        Credentials.reset()
        Scores.reset()
        Mochi.reset()
        Notebooks.reset()

    GLOB_cache_gpa_progress = {}
    GLOB_gpa_data = {}

    t = threading.Thread(target=tick, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=80, debug=debug)
