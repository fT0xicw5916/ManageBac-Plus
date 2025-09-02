from selen import ManagebacDriver
from dbm.credentials import Credentials
from dbm.scores import Scores
import logging


def get_grade_data(username):
    g = []
    credentials = Credentials()
    scores = Scores()

    data = credentials.search(username)[-1]
    id = data[0]
    for class_ in data[4:]:
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
            "grades": [list(entry) for entry in zip(n, s, w)]
        })

    return g


def cache_grade_data(username, password, microsoft, dest):
    logger = logging.getLogger("app.cache")
    logger.info(f"Caching GPA data for ({username}, {password}, {"MS" if microsoft else "MB"})...")

    yield 0.
    driver = ManagebacDriver(username, password, microsoft=microsoft)
    yield 0.1
    for i in driver.get_grades(dest):
        yield i + 0.1
    driver.terminate()
    yield 1.

    credentials = Credentials()
    scores = Scores()

    # New credential entry if credential doesn't exist
    if len(credentials.search(username)) == 0:
        classes = []
        for i in dest:
            classes.append(i["class_name"])
            if not scores.check_class(i["class_name"]):
                w = []
                for k in i["grades"]:
                    if k[0] == "Overall":
                        continue
                    w.append(k[0])
                scores.new_class(i["class_name"], w)
        credentials.new(username, password, microsoft, classes)

    # New score entry
    id = credentials.search(username)[-1][0]
    for i in dest:
        s = []
        for k in i["grades"]:
            s.append(k[1])
        scores.new_score(id, i["class_name"], s)

    logger.info("Cache complete.")
