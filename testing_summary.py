import re

def parser_re():
    res = []
    file = "/home/emanuel/José Manuel Miranda Ferrão_12-2017.txt"
    with open(file, "r") as fy:
        source = fy.read()

    pattern = '-|- \n|-|-\n|- |–|•|\no'
    result = re.sub(pattern, ' ', source).split("\n")
    for item in result:
        if item.strip() and len(item.strip()) > 2:
            res.append(item.strip())
    return res

def clean_lines(res):        
    corpus = []
    i = 0
    k = 1
    while True:
        sent = res[i+k]
        if i+k+1 == len(res):
            corpus.append(res[i+k])
            break
        after_sent = res[i+k+1]
        letter = after_sent[0]
        if letter.islower():
            joined = ''.join(sent + ' ' + after_sent)
            while True:
                k += 1
                bacon = res[i+k]
                letter = bacon[0]
                if letter.islower() or bacon.split()[0] == 'Aveiro' or bacon.split()[0] =='After':
                    joined = ''.join(joined + ' ' + bacon)
                else:
                    corpus.append(joined)
                    joined = ''
                    break
        else:
            i += 1
            corpus.append(sent)
            continue
    return corpus

corpus = clean_lines(parser_re())
for elem in corpus:
    print()
    print(elem)
