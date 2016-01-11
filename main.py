from stdlib import *
import sys

filename = sys.argv[1]
text = open(filename)

for line in text:
    print line


for i in sys.argv:
    print i

text.close()
