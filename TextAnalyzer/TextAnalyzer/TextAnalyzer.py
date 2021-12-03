import re
# from nltk.tokenize import sent_tokenize
alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He|She|It|They|Their|Our|We|But|However|That|This|Wherever)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])" 


# Functie pentru maparea unui text, in vederea obtinerii textului sub forma de
# propozitii
def split_into_sentences(text):
    text = re.sub(prefixes, "<prd>", text)
    text = re.sub(websites, "<prd>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub(digits + "[.]", "<prd>", text)
    text = re.sub(suffixes + "[.] " + starters, "<stop>", text)
    text = re.sub(suffixes + "[.]", "<prd>", text)
    text = re.sub(" " + alphabets + "[.]", "<prd>", text)
    text = text.replace(".", "<stop>")
    text = text.replace("?", "<stop>")
    text = text.replace("!", "<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def readData():
    f = open("text.txt", 'r')
    file = f.read()
    f.close()
    file = file.replace("\n", "")
    return file


def analyze():
    text = readData()
    
    statistics = {"words" : 0, "sentences" : 0,
                  "phone numbers" : 0, "CNP" : 0}

    # Calcul pentru numarul de propozitii

    copyText = text[:]
    listSentences = split_into_sentences(copyText)
    statistics["sentences"] = len(listSentences)

    # listSentences = sent_tokenize(text)
    # statistics["sentences"] = len(listSentences)

    # Calcul pentru numarul de cuvinte

    wordRegex = r'\w+'
    listWords = re.findall(wordRegex, text)
    statistics["words"] = len(listWords)

    # Calcul pentru numarul de numere de telefon unice

    phoneRegex = re.compile(r'''(
    (07)
    (\d{8})
    )''', re.VERBOSE)

    listPhones = re.findall(phoneRegex, text)
    listAux = []
    for pair in listPhones:
        listAux.append(pair[0])

    listPhones = listAux[:]
    listAux = []

    for phone in listPhones:
        if phone not in listAux:
            listAux.append(phone)

    listPhones = listAux[:]
    statistics["phone numbers"] = str(len(listPhones)) + " " + str(listPhones)

    # Calcul pentru numarul de CNP-uri unice

    cnpRegex1 = re.compile(r'''(
    ([1-2])
    (\d{12})
    )''', re.VERBOSE)

    cnpRegex2 = re.compile(r'''(
    ([5-6])
    (\d{12})
    )''', re.VERBOSE)

    listCNP1 = re.findall(cnpRegex1, text)
    listCNP2 = re.findall(cnpRegex2, text)
    listCNP = listCNP1[:]
    listCNP.extend(listCNP2)
    listAux = []

    for cnp in listCNP:
        listAux.append(cnp[0])

    listCNP = listAux[:]
    listAux = []

    for cnp in listCNP:
        if cnp not in listAux:
            listAux.append(cnp)

    listCNP = listAux[:]
    statistics["CNP"] = str(len(listCNP)) + " " + str(listCNP)

    # Calcul pentru statistica pe litere, insensitive

    string = "".join(listWords)
    string = string.upper()
    string = "".join([character for character in string if not character.isdigit()])
    numberOfLetters = len(string)

    letters = {}

    for character in string:
        if character not in letters.keys():
            letters[character] = 0
        letters[character] = letters[character] + 1

    letters = sorted(letters.items())

    for pair in letters:
        statistics[pair[0]] = str(pair[1]) + " (" + str("%.3f" % ((100 * pair[1]) / numberOfLetters)) + "%)"

    for key in statistics.keys():
        print(str(key) + " : " + str(statistics[key]))



def main():
    analyze()


main()