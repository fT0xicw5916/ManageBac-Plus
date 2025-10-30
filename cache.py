from selen import ManagebacDriver
from dbm.credentials import Credentials
from dbm.scores import Scores
from selen import cleanup_chrome_processes
import logging
import threading
import json


def get_grade_data(username):
    g = []
    credentials = Credentials()
    scores = Scores()

    try:
        data = credentials.search(username)[-1]
        id = data[0]
        for class_ in data[4:]:
            if class_ == "None":
                g.append(None)
                continue
            s = [float(i) if i is not None else None for i in scores.search_score(id, class_)[-1][1:]]
            n = [i[0] for i in scores.get_weight_names(class_)[1:]]
            w = []
            for i in n:
                if i == "Overall":
                    w.append(None)
                    continue
                w.append(int(i[i.find('(') + 1:i.find('%')]) / 100)
            g.append({
                "class_name": class_,
                "grades": [list(entry) for entry in zip(n, s, w)]
            })
    except Exception:
        return 1

    return g


class CacheGradeDataThread(threading.Thread):
    def __init__(self, target=None, args=(), daemon=None, R=None):
        super().__init__(target=target, args=args, daemon=daemon)
        self.R = R
        self.args = args

    def run(self):
        super().run()
        GLOB_gpa_data = json.loads(self.R.get("GLOB_gpa_data"))
        GLOB_gpa_data[list(self.args)[0]] = list(self.args)[3]
        self.R.set("GLOB_gpa_data", json.dumps(GLOB_gpa_data))


def cache_grade_data(username, password, microsoft, dest, tick=False, reload=False):
    logger = logging.getLogger("app.cache")
    logger.info(f"Caching GPA data for ({username}, {password}, {"MS" if microsoft else "MB"})...")

    driver = None
    try:
        yield 0.
        driver = ManagebacDriver(username, password, microsoft=microsoft)
        yield 0.1
        for i in driver.get_grades(dest):
            yield i + 0.1
    except Exception as e:
        logger.error(f"Selenium error:\n{e}")
        raise
    finally:
        if driver:
            driver.terminate()
            cleanup_chrome_processes()
        yield 1.

    if len(dest) == 0:
        return None

    credentials = Credentials()
    scores = Scores()

    # New credential entry
    classes = []
    for i in dest:
        if i is None:
            classes.append("None")
            continue
        classes.append(i["class_name"])
        if not scores.check_class(i["class_name"], [cat[0] for cat in i["grades"][1:]]):
            w = []
            for k in i["grades"]:
                if k[0] == "Overall" or k[0] == "整体":
                    continue
                w.append(k[0])
            scores.new_class(i["class_name"], w)
    if (len(credentials.search(username)) == 0 or reload) and not tick:
        credentials.new(username, password, microsoft, classes)

    # New score entry
    id = credentials.search(username)[-1][0]
    for i in dest:
        if i is None:
            continue
        s = []
        for k in i["grades"]:
            s.append(k[1])
        scores.new_score(id, i["class_name"], s)

    logger.info("Cache complete.")
    return None
