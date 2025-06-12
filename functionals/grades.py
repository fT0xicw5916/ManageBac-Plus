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
    new_local_avg = round(local_avg * (task_num / (task_num + 1)) + (per_score / (task_num + 1)), 2)
    excluded_overall_score = 0.
    for _, value in grades.items():
        if value[0] is None:
            continue
        excluded_overall_score += value[0] * value[1]
    excluded_overall_score -= grades[category][0] * grades[category][1]
    new_overall = round((excluded_overall_score + (new_local_avg * grades[category][1])) / sum([value[1] for key, value in grades.items() if value[0] is not None]), 2)
    delta_local = "{:+}".format(round(new_local_avg - local_avg), 2)
    delta_overall = "{:+}".format(round(new_overall - current_overall), 2)
    return new_local_avg, new_overall, delta_local, delta_overall
