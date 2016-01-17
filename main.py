#123456789012345678901234567890123456789012345678901234567890123456789012345678

import sys
import re
from stdlib import *

filename = sys.argv[1]
text = open(filename)
traduccion = list()
indent_level = 0
indent = "    "

traduccion.append("from stdlib import *\n\n")

def appendline(list, line):
    newline = line + "\n"
    list.append(newline)

def traducirlinea(line, indentation):

    if (re.search(r'VAR\(\w+\) <= TRUE', line) != None):
        match = re.search(r'VAR\(\w+\) <= TRUE', line)
        linea_traducida =  indentation*indent + match.group(1) + " = True"
        return linea_traducida,indentation

    elif (re.search(r'TRUE => VAR\((\w+\))', line) != None):
        match = re.search(r'TRUE => VAR\((\w+\))', line)
        linea_traducida = indentation*indent + match.group(1) + " = True"
        return linea_traducida,indentation

    elif (re.search(r'VAR\(\w+\) <= FALSE', line) != None):
        match = re.search(r'VAR\(\w+\) <= FALSE', line)
        linea_traducida =  indentation*indent + match.group(1) + " = False"
        return linea_traducida,indentation

    elif (re.search(r'FALSE => VAR\((\w+\))', line) != None):
        match = re.search(r'FALSE => VAR\((\w+\))', line)
        linea_traducida = indentation*indent + match.group(1) + " = False"
        return linea_traducida,indentation

    elif (re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\) => VAR\((\w+)\)', line) != None):

        match = re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\) => VAR\((\w+)\)', line)
        cond = match.group(2)
        splits = cond.split()
        statement = list()

        if (len(splits) == 1):
            splits.append("")

        if (cond == "TRUE"):
            cond = "True"
        elif (cond == "FALSE"):
            cond = "False"
        else:
            cond = splits[0] + "("
            for i in range(len(splits)):
                if (i == len(splits)-1):
                    if (re.search(r'PARAM(\d+)', splits[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', splits[i])
                        cond += "params[" + submatch.group(1) + "])"
                    else:
                        cond += splits[i]+")"
                elif (i == 0):
                    continue
                else:
                    if (re.search(r'PARAM(\d+)', splits[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', splits[i])
                        cond += "params[" + submatch.group(1) + "], "
                    else:
                        cond += splits[i]+", "

        statement.append(indentation*indent + "if (" + cond + "):")
        indentation += 1
        args1 = match.group(1).split()
        proc1 = args1[0] + "("

        if (len(args1) == 1):
            args1.append("")

        for i in range(len(args1)):
            if (i == len(args1)-1):
                if (re.search(r'PARAM(\d+)', args1[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args1[i])
                    proc1 += "params[" + submatch.group(1) + "])"
                else:
                    proc1 += args1[i]+")"
            elif (i == 0):
                continue
            else:
                if (re.search(r'PARAM(\d+)', args1[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args1[i])
                    proc1 += "params[" + submatch.group(1) + "], "
                else:
                    proc1 += args1[i]+", "

        statement.append(indentation*indent + match.group(4) + " = " + proc1)

        indentation -= 1
        statement.append(indentation*indent + "else:")
        indentation += 1
        args2 = match.group(3).split()
        proc2 = args2[0] + "("

        if (len(args2) == 1):
            args2.append("")

        for i in range(len(args2)):
            if (i == len(args2)-1):
                if (re.search(r'PARAM(\d+)', args2[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args2[i])
                    proc2 += "params[" + submatch.group(1) + "])"
                else:
                    proc2 += args2[i]+")"
            elif (i == 0):
                continue
            else:
                if (re.search(r'PARAM(\d+)', args2[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args2[i])
                    proc2 += "params[" + submatch.group(1) + "], "
                else:
                    proc2 += args2[i]+", "

        statement.append(indentation*indent + match.group(4) + " = " + proc2)
        indentation -= 1
        linea_traducida = "\n".join(statement)
        return linea_traducida,indentation

    elif (re.search(r'VAR\((\w+)\) <= IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line) != None):

        match = re.search(r'VAR\((\w+)\) <= IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line)
        cond = match.group(3)
        splits = cond.split()
        statement = list()

        if (len(splits) == 1):
            splits.append("")

        if (cond == "TRUE"):
            cond = "True"
        elif (cond == "FALSE"):
            cond = "False"
        else:
            cond = splits[0] + "("
            for i in range(len(splits)):
                if (i == len(splits)-1):
                    if (re.search(r'PARAM(\d+)', splits[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', splits[i])
                        cond += "params[" + submatch.group(1) + "])"
                    else:
                        cond += splits[i]+")"
                elif (i == 0):
                    continue
                else:
                    if (re.search(r'PARAM(\d+)', splits[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', splits[i])
                        cond += "params[" + submatch.group(1) + "], "
                    else:
                        cond += splits[i]+", "

        statement.append(indentation*indent + "if (" + cond + "):")
        indentation += 1
        args1 = match.group(2).split()
        proc1 = args1[0] + "("

        if (len(args1) == 1):
            args1.append("")

        for i in range(len(args1)):
            if (i == len(args1)-1):
                if (re.search(r'PARAM(\d+)', args1[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args1[i])
                    proc1 += "params[" + submatch.group(1) + "])"
                else:
                    proc1 += args1[i]+")"
            elif (i == 0):
                continue
            else:
                if (re.search(r'PARAM(\d+)', args1[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args1[i])
                    proc1 += "params[" + submatch.group(1) + "], "
                else:
                    proc1 += args1[i]+", "

        statement.append(indentation*indent + match.group(1) + " = " + proc1)

        indentation -= 1
        statement.append(indentation*indent + "else:")
        indentation += 1
        args2 = match.group(4).split()
        proc2 = args2[0] + "("

        if (len(args2) == 1):
            args2.append("")

        for i in range(len(args2)):
            if (i == len(args2)-1):
                if (re.search(r'PARAM(\d+)', args2[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args2[i])
                    proc2 += "params[" + submatch.group(1) + "])"
                else:
                    proc2 += args2[i]+")"
            elif (i == 0):
                continue
            else:
                if (re.search(r'PARAM(\d+)', args2[i]) != None):
                    submatch = re.search(r'PARAM(\d+)', args2[i])
                    proc2 += "params[" + submatch.group(1) + "], "
                else:
                    proc2 += args2[i]+", "

        statement.append(indentation*indent + match.group(1) + " = " + proc2)
        indentation -= 1
        linea_traducida = "\n".join(statement)

        return linea_traducida,indentation

    elif (re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line) != None):

        match = re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line)
        cond = match.group(2)
        splits = cond.split()

        if (len(splits) == 1):
            splits.append("")

        if (cond == "TRUE"):
            cond = "True"
        elif (cond == "FALSE"):
            cond = "False"
        else:
            cond = splits[0] + "("
            for i in range(len(splits)):
                if (i == len(splits)-1):
                    if (re.search(r'PARAM(\d+)', splits[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', splits[i])
                        cond += "params[" + submatch.group(1) + "])"
                    else:
                        cond += splits[i]+")"
                elif (i == 0):
                    continue
                else:
                    if (re.search(r'PARAM(\d+)', splits[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', splits[i])
                        cond += "params[" + submatch.group(1) + "], "
                    else:
                        cond += splits[i]+", "

        linea_traducida = indentation*indent + "if (" + cond + "):\n"
        indentation += 1
        args1 = match.group(1).split()
        proc1 = args1[0] + "("

        if (len(args1) == 1):
            args1.append("")

        if (args1[0] == ""):
            linea_traducida += indentation*indent + "pass\n"
        else:
            for i in range(len(args1)):
                if (i == len(args1)-1):
                    if (re.search(r'PARAM(\d+)', args1[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', args1[i])
                        proc1 += "params[" + submatch.group(1) + "])"
                    else:
                        proc1 += args1[i]+")"
                elif (i == 0):
                    continue
                else:
                    if (re.search(r'PARAM(\d+)', args1[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', args1[i])
                        proc1 += "params[" + submatch.group(1) + "], "
                    else:
                        proc1 += args1[i]+", "
            linea_traducida += indentation*indent + proc1 + "\n"

        indentation -= 1
        linea_traducida += indentation*indent + "else:\n"
        indentation += 1
        args2 = match.group(3).split()
        proc2 = args2[0] + "("

        if (len(args2) == 1):
            args2.append("")

        if (args2[0] == ""):
            linea_traducida += indentation*indent + "pass\n"
        else:
            for i in range(len(args2)):
                if (i == len(args2)-1):
                    if (re.search(r'PARAM(\d+)', args2[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', args2[i])
                        proc2 += "params[" + submatch.group(1) + "])"
                    else:
                        proc2 += args2[i]+")"
                elif (i == 0):
                    continue
                else:
                    if (re.search(r'PARAM(\d+)', args2[i]) != None):
                        submatch = re.search(r'PARAM(\d+)', args2[i])
                        proc2 += "params[" + submatch.group(1) + "], "
                    else:
                        proc2 += args2[i]+", "

            linea_traducida += indentation*indent + proc2

        indentation -= 1

        return linea_traducida,indentation

    elif (re.search(r'VAR\((\w+)\) <= ([\w\d]+)', line) != None):
        match = re.search(r'VAR\((\w+)\) <= ([\w\d]+)', line)
        linea_traducida =  indentation*indent + match.group(1) + " = " + match.group(2)
        return linea_traducida,indentation

    elif (re.search(r'([\w\d]+) => VAR\((\w+\))', line) != None):
        match = re.search(r'([\w\d]+) => VAR\((\w+\))')
        linea_traducida = indentation*indent + match.group(2) + " = " + match.group(1)
        return linea_traducida,indentation

    elif (re.search(r'VAR\((\w+)\) <= \(([\w\d ]*)\)', line) != None):
        match = re.search(r'VAR\((\w+)\) <= \(([\w\d ]*)\)', line)
        args = match.group(2).split()
        proc = args[0] + "("

        if (len(args) == 1):
            args.append("")

        for i in range(len(args)):
            if (i == len(args)-1):
                proc += args[i]+")"
            elif (i == 0):
                continue
            else:
                proc += args[i]+", "

        linea_traducida =  indentation*indent + match.group(1) + " = " + proc
        return linea_traducida,indentation

    elif (re.search(r'\$\^PROC\((\w+)\)', line) != None):
        match = re.search(r'\^PROC\((\w+)\)', line)
        linea_traducida = indentation*indent + "def " + match.group(1) + "(*params):"
        indentation += 1

        return linea_traducida,indentation

    elif (re.search(r'#([\w]+)', line) != None):
        match = re.search(r'#([\w]+)', line)
        linea_traducida = indentation*indent + "return " + match.group(1)

        return linea_traducida,indentation

    elif (re.search(r'#([(\w\d )]+)', line) != None):
        match = re.search(r'#\(([\w\d ]+)\)', line)
        args = match.group(1).split()
        proc = args[0] + "("

        if (len(args) == 1):
            args.append("")

        for i in range(len(args)):
            if (i == len(args)-1):
                proc += args[i]+")"
            elif (i == 0):
                continue
            else:
                proc += args[i]+", "

        linea_traducida =  indentation*indent + "return " + proc

        return linea_traducida,indentation

    elif (re.search(r'\^\$', line)):
        linea_traducida = ""
        indentation -= 1

        return linea_traducida,indentation

    elif (re.search(r'\(([\w\d ]*)\) => VAR\((\w+)\)', line) != None):
        match = re.search(r'\(([\w\d ]*)\) => VAR\((\w+)\)', line)
        args = match.group(1).split()
        proc = args[0] + "("

        if (len(args) == 1):
            args.append("")

        for i in range(len(args)):
            if (i == len(args)-1):
                proc += args[i]+")"
            elif (i == 0):
                continue
            else:
                proc += args[i]+", "
        linea_traducida = indentation*indent + match.group(2) + " = " + proc
        return linea_traducida,indentation

    elif (re.search(r'\([\w\d ]*\)', line) != None):
        split = line.split()
        match = list()

        if (len(split) == 1):
            split.append("")

        if (split[0] == "("):
            linea_traducida = indentation*indent + "pass"
            return linea_traducida,indentation

        for i in range(len(split)):
            if (i == 0):
                strip = split[i].strip("(")
                match.append(strip)
                continue
            elif (i == len(split)-1):
                strip = split[i].strip(")")
                match.append(strip)
                continue
            match.append(split[i])

        proc = match[0]+"("

        for i in range(len(match)):
            if (i == 0):
                continue
            elif (i == len(match)-1):
                proc += match[i]+")"
            else:
                proc += match[i]+", "

        linea_traducida = indentation*indent + proc
        return linea_traducida,indentation

    else:
        linea_traducida = line.strip("\n")
        return linea_traducida,indentation





for line in text:
    traduc,indent_level = traducirlinea(line,indent_level)
    appendline(traduccion, traduc)

text.close()

newfile = open(filename+".py","w")

for line in traduccion:
    newfile.write(line)

newfile.close()