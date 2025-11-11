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

        cookies = {
            "username": i[0],
            "password": i[1],
            "microsoft": '0'
        }
        try:
            requests.get("http://managebac.me/load_grades", cookies=cookies)
            time.sleep(30)
        except Exception:
            pass

        cookies = {
            "username": i[0],
            "password": i[1],
            "microsoft": '1'
        }
        try:
            requests.get("http://managebac.me/load_grades", cookies=cookies)
            time.sleep(30)
        except Exception:
            pass


if __name__ == "__main__":
    main()
