import re
from collections import Counter

# filename = input('Enter file name')
filename = 'book.txt'
with open(filename) as filehandler:
    words = re.findall('\w{3,}', filehandler.read().lower())
c = Counter(words)
print('Частоты: ', c)
