"""
Sometimes users cannot login due to various weird reasons. Run this script to automatically retry login for every
recorded user from the log file.
"""

import requests
import time


def read_logs(path, start_date, end_date):
    li = None
    with open(path, 'r') as f:
        li = f.readlines()

    for i in range(len(li)):
        if f"2025-{start_date}" in li[i]:
            li = li[i:]
            break
    for i in range(-1, -len(li) - 1, -1):
        if f"2025-{end_date}" in li[i]:
            if i == -1:
                break
            li = li[:i+1]
            break

    r = []
    for line in li:
        if "app.cache - Caching GPA data for" in line:
            info = line[line.find('(')+1:line.find(')')].split(", ")
            try:
                r.append((info[0], info[1]))
            except Exception:
                pass

    return r


def main():
    li = read_logs("../logs.log", "11-03", "11-11")
    print(len(li))
    for i in li:
        print(i)

        session = requests.Session()
        session.cookies.set("username", i[0])
        session.cookies.set("password", i[1])
        session.cookies.set("microsoft", '0')
        try:
            session.get("http://managebac.me/load_grades")
            time.sleep(120)
            session.close()
        except Exception:
            pass

        session = requests.Session()
        session.cookies.set("username", i[0])
        session.cookies.set("password", i[1])
        session.cookies.set("microsoft", '1')
        try:
            session.get("http://managebac.me/load_grades")
            time.sleep(120)
            session.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
