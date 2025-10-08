from matplotlib import pyplot as plt
import numpy as np
import random
import matplotlib
import os
import sys
import re

sys.path.insert(0, "..")

from enums import Colors


def shorter_names(x):
    """
    Shortens the name of the given subject for the sake of displaying them on the legend of GPA graphs.

    :param x: The original, full name of the subject
    :return: The shortened name of the given subject
    """
    dp_year = None
    name = None
    level = None
    grade = re.findall("Grade ..", x)[0]

    if x[:5] == "IB DP":
        x = x[6:]

    if x[:2] == "PE":
        if grade == "Grade 10":
            dp_year = "Pre-DP"
        elif grade == "Grade 11" or grade == "Grade 12":
            dp_year = "DP"
        name = "PE"

    elif x[:2] == "DP":
        dp_year = x[:3]

        if x[4:7] == "CAS":
            level = "IB DP Core Course"
            name = "CAS"

        elif x[4:7] == "TOK":
            level = "IB DP Core Course"
            name = "TOK"

        else:
            name_pattern = r"DP[12]\s+(.*?)\s+(?:SL|HL)"
            name_match = re.search(name_pattern, x)
            if name_match:
                name = name_match.group(1)
                level = re.findall(r"(HL|SL)", x)[0]

    else:
        dp_year = "Pre-DP"
        name_pattern = r"[A-Za-z].*?(?=\s*\()"
        name_match = re.search(name_pattern, x)
        if name_match:
            name = name_match[0]
        if "English" in x:
            if x[0] == 'A':
                level = "Advanced English"
            elif x[0] == 'I':
                level = "Intermediate English"
            elif x[0] == 'S':
                level = "Standard English"
        elif "Calculus" in x:
            if x[13] == 'E':
                level = "Extended Mathematics"
            elif x[13] == 'C':
                level = "Core Mathematics"
            elif x[13] == 'B':
                level = "Basic Mathematics"
        elif "Honor" in x:
            level = "Honor Course"
        else:
            level = "Standard Course"

    return name, level, dp_year, grade


def radar_percs_edge(subjects, percs):
    """
    Graphs the radar graph of given subjects with respect to their percentage grades, using the positions of arcs as the GPA indicator instead of vertices.

    :param subjects: A list of the names of the subjects
    :param percs: A list of the percentage grades of the subjects
    :return: The path where the image file of the radar graph is stored relative to static/
    """
    matplotlib.use("agg")
    subjects = [shorter_names(i)[0] for i in subjects]

    circle = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()
    closed_circle = circle.copy()
    closed_circle.append(0)

    ax = plt.subplot(polar=True)
    plt.xticks(circle, [''] * len(subjects))
    plt.yticks([0, 40, 60, 65, 70, 80, 90], ['0', "40", "60", "65", "70", "80", "90"], fontsize=5)
    plt.ylim(0, 100)

    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, [60] * len(theta), color=Colors.RED, alpha=0.3, linewidth=1.5)

    lax = []
    for i in range(len(subjects)):
        s = np.linspace(0, 2 * np.pi, 100 * len(subjects))
        r = [0] * 100 * len(subjects)
        try:
            bounds = (i * 100, (i + 1) * 100)
            r[bounds[0] : bounds[1]] = [percs[i]] * (bounds[1] - bounds[0])
        except IndexError:  # Wrap around
            bounds = (0, i * 100)
            r[bounds[0] : bounds[1]] = [percs[i]] * (bounds[1] - bounds[0])
        l, = ax.plot(s, r, color=Colors.tolist()[i])
        lax.append(l)
        ax.fill(s, r, alpha=0.3, color=Colors.tolist()[i])

    ax.legend(handles=lax, labels=subjects, loc=3, bbox_to_anchor=(0, 0, 1, 1))

    id = str(random.randint(0, 1000000))
    os.system(f"rm -rf {os.path.abspath("static/gen/" + id + ".png")}")
    plt.savefig(os.path.abspath("static/gen/" + id + ".png"), dpi=300, format="png")
    plt.close()

    return f"gen/{id}.png"


def radar_ranks_edge(subjects, ranks):
    """
    Graphs the radar graph of given subjects with respect to their IB ranks, using the positions of arcs as the GPA indicator instead of vertices.

    :param subjects: A list of the names of the subjects
    :param ranks: A list of the ranks of the subjects
    :return: The path where the image file of the radar graph is stored relative to static/
    """
    matplotlib.use("agg")
    subjects = [shorter_names(i)[0] for i in subjects]

    circle = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()
    closed_circle = circle.copy()
    closed_circle.append(0)

    ax = plt.subplot(polar=True)
    plt.xticks(circle, [''] * len(subjects))
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], ['0', '1', '2', '3', '4', '5', '6', '7'])
    plt.ylim(0, 7)

    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, [3] * len(theta), color=Colors.RED, alpha=0.3, linewidth=1.5)

    lax = []
    for i in range(len(subjects)):
        s = np.linspace(0, 2 * np.pi, 100 * len(subjects))
        r = [0] * 100 * len(subjects)
        try:
            bounds = (i * 100, (i + 1) * 100)
            r[bounds[0]: bounds[1]] = [ranks[i]] * (bounds[1] - bounds[0])
        except IndexError:  # Wrap around
            bounds = (0, i * 100)
            r[bounds[0]: bounds[1]] = [ranks[i]] * (bounds[1] - bounds[0])
        l, = ax.plot(s, r, color=Colors.tolist()[i])
        lax.append(l)
        ax.fill(s, r, alpha=0.3, color=Colors.tolist()[i])

    ax.legend(handles=lax, labels=subjects, loc=3, bbox_to_anchor=(0, 0, 1, 1))

    id = str(random.randint(0, 1000000))
    os.system(f"rm -rf {os.path.abspath("static/gen/" + id + ".png")}")
    plt.savefig(os.path.abspath("static/gen/" + id + ".png"), dpi=300, format="png")
    plt.close()

    return f"gen/{id}.png"


def perc2rank(value, m=100):
    """
    Converts percentage/scalar GPA to IB's 7-based GPA.

    :param value: Percentage/scalar grade of the task, default out of 100
    :param m: Maximum grade of the task, defaulting to 100
    :return: IB's strict 7-based GPA of the task, no rounding, returns 0 if input is out of domain, returns 7 if input is higher than 100%
    """
    p = (float(value) / float(m)) * 100
    return 7 if p >= 90 else 6 if p >= 80 else 5 if p >= 70 else 4 if p >= 65 else 3 if p >= 60 else 2 if p >= 40 else 1 if p >= 0 else 0


def radar_ranks(subjects, ranks, transparent=False, color=Colors.BLUE):
    """
    Graphs the radar graph of given subjects with respect to their IB ranks.

    Credits to Charles Zhang Chuhan.

    :param color: The color of the radar graph. Defaults to "blue"
    :param transparent: Whether the saved PNG file is transparent or not. Defaults to False
    :param subjects: A list of the names of the subjects
    :param ranks: A list of the ranks of the subjects
    :return: The path where the image file of the radar graph is stored relative to static/
    """
    matplotlib.use("agg")
    subjects = [shorter_names(i)[0] for i in subjects]

    circle = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()
    closed_circle = circle.copy()
    closed_circle.append(0)
    ranks.append(ranks[0])

    ax = plt.subplot(polar=True)
    plt.xticks(circle, subjects)
    plt.yticks([0, 1, 2, 3, 4, 5, 6, 7], ['0', '1', '2', '3', '4', '5', '6', '7'])
    plt.ylim(0, 7)

    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, [3] * len(theta), color=Colors.RED, alpha=0.3, linewidth=1.5)
    ax.plot(closed_circle, ranks, color=color)
    ax.fill(closed_circle, ranks, alpha=0.2, color=color)

    id = str(random.randint(0, 1000000))
    os.system(f"rm -rf {os.path.abspath("static/gen/" + id + ".png")}")
    plt.savefig(os.path.abspath("static/gen/" + id + ".png"), dpi=300, format="png", transparent=transparent)
    plt.close()

    return f"gen/{id}.png"


def radar_percs(subjects, percs, transparent=False, color=Colors.BLUE):
    """
    Graphs the radar graph of given subjects with respect to their percentage grades.

    Credits to Charles Zhang Chuhan.

    :param color: The color of the radar graph. Defaults to "blue"
    :param transparent: Whether the saved PNG file is transparent or not. Defaults to False
    :param subjects: A list of the names of the subjects
    :param percs: A list of the percentage grades of the subjects
    :return: The path where the image file of the radar graph is stored relative to static/
    """
    matplotlib.use("agg")
    subjects = [shorter_names(i)[0] for i in subjects]

    circle = np.linspace(0, 2 * np.pi, len(subjects), endpoint=False).tolist()
    closed_circle = circle.copy()
    closed_circle.append(0)
    percs.append(percs[0])

    ax = plt.subplot(polar=True)
    plt.xticks(circle, subjects)
    plt.yticks([0, 40, 60, 65, 70, 80, 90], ['0', "40", "60", "65", "70", "80", "90"], fontsize=5)
    plt.ylim(0, 100)

    theta = np.linspace(0, 2 * np.pi, 100)
    ax.plot(theta, [60] * len(theta), color=Colors.RED, alpha=0.3, linewidth=1.5)
    ax.plot(closed_circle, percs, color=color)
    ax.fill(closed_circle, percs, alpha=0.2, color=color)

    id = str(random.randint(0, 1000000))
    os.system(f"rm -rf {os.path.abspath("static/gen/" + id + ".png")}")
    plt.savefig(os.path.abspath("static/gen/" + id + ".png"), dpi=300, format="png", transparent=transparent)
    plt.close()

    return f"gen/{id}.png"


def new_task_predict(raw_score, max_score, current_overall, task_num, local_avg, grades, category):
    """
    This function simulates the score change in a given category as well as the change in overall score of the subject when a new task is added.

    For example, "How would my overall score and quiz average score vary if I get a 60/100 in the new quiz, given that my current overall score is 90, there are a total of 10 quizzes already logged, the current quiz average score is 90, and the current grade information?" ==> new_task_predict(60, 100, 90, 10, 90, {grades}, "Quiz")

    Credits to Charles Zhang Chuhan.

    :param raw_score: The raw score of the new task to be simulated. For example, to simulate a new task with grades 60/100, raw_score = 60
    :param max_score: The maximum score of the new task to be simulated. For example, to simulate a new task with grades 13/16, max_score = 16
    :param current_overall: The subject's current overall score before the new task is simulated
    :param task_num: The number of tasks already present in the given category in which the new task is simulated. For example, if I want to simulate a new quiz and there's already 10 quizzes on ManageBac, task_num = 10
    :param local_avg: The score of the given category in which the new task is simulated. For example, if I want to simulate a new quiz and the current quiz average score is 90, local_avg = 90
    :param grades: The subject's current grade information in the format of {"category name": (category score, category weight), ...}. Use None type if the category doesn't contain a score
    :param category: The name of the category in which the new task will be simulated. For example, if I want to simulate a new quiz, category = "Quiz"
    :return: new_local_avg, the new category average score after the simulation; new_overall, the new overall score after the simulation; delta_local: the change in the task's category average score after the new task is added; delta_overall: the change of overall score after the new task is added
    """
    per_score = round((raw_score / max_score) * 100, 2)
    if sum([value[1] for _, value in grades.items() if value[0] is not None]) == 0:
        return per_score, per_score, '-', '-'
    current_overall = 0 if current_overall is None else current_overall
    local_avg = 0 if local_avg is None else local_avg
    new_local_avg = round(((local_avg * task_num) + per_score) / (task_num + 1), 2)
    excluded_overall_score = 0.
    for _, value in grades.items():
        if value[0] is None:
            continue
        excluded_overall_score += value[0] * value[1]
    excluded_overall_score -= (0 if grades[category][0] is None else grades[category][0]) * grades[category][1]
    if local_avg == 0:
        new_overall = round((excluded_overall_score + (new_local_avg * grades[category][1])) / (sum([value[1] for _, value in grades.items() if value[0] is not None]) + grades[category][1]), 2)
    else:
        new_overall = round((excluded_overall_score + (new_local_avg * grades[category][1])) / sum([value[1] for _, value in grades.items() if value[0] is not None]), 2)
    delta_local = "{:+}".format(round(new_local_avg - local_avg, 2))
    delta_overall = "{:+}".format(round(new_overall - current_overall, 2))
    return new_local_avg, new_overall, delta_local, delta_overall
