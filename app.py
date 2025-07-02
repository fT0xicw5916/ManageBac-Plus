from flask import Flask, render_template, request, make_response, redirect, url_for
from selen import ManagebacDriver
from dbm.credentials import Credentials
from dbm.scores import Scores
from functionals.grades import new_task_predict

app = Flask(__name__)


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/toolbox/<sub>")
def toolbox_sub(sub):
    return render_template("toolbox.html")


@app.route("/tasks", methods=["POST", "GET"])
def tasks():
    subject = request.args.get("subject")
    if subject is None:
        return None

    # Since /tasks is redirected from /grades, we can assume the grades data is cached
    if request.method == "GET":
        scores = Scores()
        categories = [i[0] for i in scores.get_weight_names(subject)]
        return render_template("tasks.html", categories=categories[2:])

    elif request.method == "POST":
        credentials = Credentials()
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        driver = ManagebacDriver(username, password)

        id = credentials.search(username)[-1][0]
        category = request.form.get("category")
        new_raw_score = int(request.form.get("new_raw_score"))
        new_max_score = int(request.form.get("new_max_score"))
        scores = Scores()
        current_overall = scores.search_score(id, subject)[-1][1]
        task_num = driver.get_task_num(subject, category)
        local_avg = scores.get_category_score(id, subject)[category]

        grades_dict = {}

        g = []
        data = credentials.search(username)[-1]
        for class_ in data[3:]:
            s = [float(i) if i is not None else None for i in scores.search_score(id, class_)[-1][1:]]
            n = [i[0] for i in scores.get_weight_names(class_)[1:]]
            w = []
            for i in n:
                if i == "Overall":
                    w.append(None)
                    continue
                w.append(int(i[i.find('(') + 1:i.find('%')]))
            g.append({
                "class_name": class_,
                "grades": list(zip(n, s, w))
            })

        for s in g:
            if s["class_name"] == subject:
                for c in s["grades"]:
                    if c[0] == "Overall":
                        continue
                    grades_dict[c[0]] = (c[1] if type(c[1]) is float else None, c[2])

        new_local_avg, new_overall, delta_local, delta_overall = new_task_predict(new_raw_score, new_max_score, current_overall, task_num, local_avg, grades_dict, category)

        return render_template("tasks_calc.html", origin=subject, category=category, new_raw_score=new_raw_score, new_max_score=new_max_score, new_overall=new_overall, delta_overall=delta_overall, new_local_avg=new_local_avg, delta_local=delta_local)

    return None


@app.route("/settings", methods=["POST", "GET"])
def settings():
    if request.method == "GET":
        return render_template("settings.html", success=False)

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        n = request.args.get("next")

        if n is None:
            res = make_response(render_template("settings.html", success=True))
            res.set_cookie("username", username)
            res.set_cookie("password", password)
            return res
        else:
            res = make_response(redirect(url_for(n)))
            res.set_cookie("username", username)
            res.set_cookie("password", password)
            return res

    return None


@app.route("/grades", methods=["POST", "GET"])
def grades():
    global g

    if request.method == "GET":
        username = request.cookies.get("username")
        password = request.cookies.get("password")
        if username is None or password is None:
            return redirect(url_for("settings", next="grades"))

        credentials = Credentials()
        scores = Scores()
        g = []

        if len(credentials.search(username)) > 0:  # Data cached
            data = credentials.search(username)[-1]
            id = data[0]
            for class_ in data[3:]:
                s = [float(i) if i is not None else None for i in scores.search_score(id, class_)[-1][1:]]
                n = [i[0] for i in scores.get_weight_names(class_)[1:]]
                w = []
                for i in n:
                    if i == "Overall":
                        w.append(None)
                        continue
                    w.append(int(i[i.find('(')+1:i.find('%')]))
                g.append({
                    "class_name": class_,
                    "grades": list(zip(n, s, w))
                })
        else:  # Data not cached
            driver = ManagebacDriver(username, password)
            g = driver.get_grades()

            # New credential entry
            classes = []
            for i in g:
                classes.append(i["class_name"])
                if not scores.check_class(i["class_name"]):
                    w = []
                    for k in i["grades"]:
                        if k[0] == "Overall":
                            continue
                        w.append(k[0])
                    scores.new_class(i["class_name"], w)
            credentials.new(username, password, classes)

            # New score entry
            id = credentials.search(username)[-1][0]
            for i in g:
                s = []
                for k in i["grades"]:
                    s.append(k[1])
                scores.new_score(id, i["class_name"], s)

        return render_template("grades.html", grades=g)

    elif request.method == "POST":
        subject = request.form.get("subject")
        term = request.form.get("term")
        target = request.form.get("target")

        result = None
        overall = None
        for s in g:
            if s["class_name"] == subject:
                overall = s["grades"][0][1]
                if term == "mid":
                    result = ((0.7 * float(target)) - (0.5 * overall)) / 0.2
                elif term == "final":
                    result = (float(target) - (0.7 * overall)) / 0.3
                break
        return render_template("grades_calc.html", result=f"{result:0.3f}", target=target, term=term, subject=subject, overall=overall)

    return None


@app.route('/')
def root():
    username = request.cookies.get("username")
    if username is None:
        return render_template("index.html", name=None)

    l = username.split('@')
    return render_template("index.html", name=l[0][2:])


if __name__ == "__main__":
    Credentials.reset()
    Scores.reset()
    app.run(host="0.0.0.0", port=8080, debug=True)
