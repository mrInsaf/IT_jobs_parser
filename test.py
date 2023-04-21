import difflib
from fuzzywuzzy import process


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()

def similarity_2(list, string):
    best_match, confidence = process.extractOne(string, list)
    return confidence


a = ['требования', 'идеальный кандидат', 'для нас важно что', 'Что нужно, чтобы к нам присоединиться',
     'Для этой работы нам нужен именно такой как ты', 'Что мы ценим', 'что мы ждем', 'Необходимые навыки и умения', 'ожидаем']
flag = False
reqs = 'мы ожидаем'
data = {'company': [1, 4], 'title': [], 'zps': [], 'link': [], 'reqs': []}

print(similarity_2(a, reqs))


# b = []
#
# for word in a:
#     b.append(similarity(word, reqs))
# print(max(b))
# for word in a:
#     if reqs.split() in word.split():
#         flag = True
# print(flag)
