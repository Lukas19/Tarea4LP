#123456789012345678901234567890123456789012345678901234567890123456789012345678

import sys
import re
from stdlib import *

filename = sys.argv[1]
text = open(filename)
traduccion = list()
indentation = 0
indent = "    "

traduccion.append("from stdlib import *\n")

def appendline(list, line): #es esto necesario?(\n) quizas deba sacarlo luego de ver lo de las RE.
    newline = line + "\n"
    list.append(newline)

def traducirlinea(line):

    indent_level = indentation

    if (re.search(r'VAR\((\w+)\) <= (\d+)', line) != None):
        match = re.search(r'VAR\((\w+)\) <= (\d+)', line)
        linea_traducida =  indent_level[0]*indent + match.group(1) + " = " + match.group(2)
        return linea_traducida

    elif (re.search(r'(\d+) => VAR\((\w+\))', line) != None):
        match = re.search(r'(\d+) => VAR\((\w+\))')
        linea_traducida = indent_level*indent + match.group(2) + " = " + match.group(1)
        return linea_traducida

    elif (re.search(r'VAR\(\w+\) <= TRUE', line) != None):
        match = re.search(r'VAR\(\w+\) <= TRUE', line)
        linea_traducida =  indent_level*indent + match.group(1) + " = True"
        return linea_traducida

    elif (re.search(r'TRUE => VAR\((\w+\))', line) != None):
        match = re.search(r'TRUE => VAR\((\w+\))', line)
        linea_traducida = indent_level*indent + match.group(1) + " = True"
        return linea_traducida

    elif (re.search(r'VAR\(\w+\) <= FALSE', line) != None):
        match = re.search(r'VAR\(\w+\) <= FALSE', line)
        linea_traducida =  indent_level*indent + match.group(1) + " = False"
        return linea_traducida

    elif (re.search(r'FALSE => VAR\((\w+\))', line) != None):
        match = re.search(r'FALSE => VAR\((\w+\))', line)
        linea_traducida = indent_level*indent + match.group(1) + " = False"
        return linea_traducida

    elif (re.search(r'VAR\((\w+)\) <= ([\w\d]+)', line) != None):
        match = re.search(r'VAR\((\w+)\) <= ([\w\d]+)', line)
        linea_traducida =  indent_level*indent + match.group(1) + " = " + match.group(2)
        return linea_traducida

    elif (re.search(r'([\w\d]+) => VAR\((\w+\))', line) != None):
        match = re.search(r'([\w\d]+) => VAR\((\w+\))')
        linea_traducida = indent_level*indent + match.group(2) + " = " + match.group(1)
        return linea_traducida

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

        linea_traducida =  indent_level*indent + match.group(1) + " = " + proc
        return linea_traducida

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
        linea_traducida = indent_level*indent + match.group(2) + " = " + proc
        return linea_traducida

    elif (re.search(r'\([\w\d ]*\)', line) != None):
        split = line.split()
        match = list()

        if (len(split) == 1):
            split.append("")

        if (split[0] == "("):
            linea_traducida = indent_level*indent + "pass"
            return linea_traducida

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

        linea_traducida = indent_level*indent + proc
        return linea_traducida

    elif (re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\) => VAR\((\w+)\)', line) != None):

        match = re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\) => VAR\((\w+)\)', line)
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
                    cond += splits[i]+")"
                elif (i == 0):
                    continue
                else:
                    cond += splits[i]+", "

        linea_traducida = indent_level*indent + "if (" + cond + "):\n"
        indent_level += 1
        args1 = match.group(1).split()
        proc1 = args1[0] + "("

        if (len(args1) == 1):
            args1.append("")

        for i in range(len(args1)):
            if (i == len(args1)-1):
                proc1 += args1[i]+")"
            elif (i == 0):
                continue
            else:
                proc1 += args1[i]+", "

        linea_traducida += indent_level*indent + match.group(4) + " = " + proc1 + "\n"

        indent_level -= 1
        linea_traducida += indent_level*indent + "else:\n"
        indent_level += 1
        args2 = match.group(3).split()
        proc2 = args2[0] + "("

        if (len(args2) == 1):
            args2.append("")

        for i in range(len(args2)):
            if (i == len(args2)-1):
                proc2 += args2[i]+")"
            elif (i == 0):
                continue
            else:
                proc2 += args2[i]+", "
        linea_traducida += indent_level*indent + match.group(4) + " = " + proc2

        indent_level -= 1

        return linea_traducida

    elif (re.search(r'VAR\((\w+)\) <= IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line) != None):

        match = re.search(r'VAR\((\w+)\) <= IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line)
        cond = match.group(3)
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
                    cond += splits[i]+")"
                elif (i == 0):
                    continue
                else:
                    cond += splits[i]+", "

        linea_traducida = indent_level*indent + "if (" + cond + "):\n"
        indent_level += 1
        args1 = match.group(2).split()
        proc1 = args1[0] + "("

        if (len(args1) == 1):
            args1.append("")

        for i in range(len(args1)):
            if (i == len(args1)-1):
                proc1 += args1[i]+")"
            elif (i == 0):
                continue
            else:
                proc1 += args1[i]+", "

        linea_traducida += indent_level*indent + match.group(1) + " = " + proc1 + "\n"

        indent_level -= 1
        linea_traducida += indent_level*indent + "else:\n"
        indent_level += 1
        args2 = match.group(4).split()
        proc2 = args2[0] + "("

        if (len(args2) == 1):
            args2.append("")

        for i in range(len(args2)):
            if (i == len(args2)-1):
                proc2 += args2[i]+")"
            elif (i == 0):
                continue
            else:
                proc2 += args2[i]+", "
        linea_traducida += indent_level*indent + match.group(1) + " = " + proc2

        indent_level -= 1

        return linea_traducida

    elif (re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line) != None): #CORRER ESTE MAS ABAJO DE LAS ASIGNACIONES DE IFELESE!!!!!!

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
                if (i == 0):
                    continue
                elif (i == len(splits)-1):
                    cond += splits[i]+")"
                else:
                    cond += splits[i]+", "

        linea_traducida = indent_level*indent + "if (" + cond + "):\n"
        indent_level += 1
        args1 = match.group(1).split()
        proc1 = args1[0] + "("

        if (len(args1) == 1):
            args1.append("")

        if (args1[0] == ""):
            linea_traducida += indent_level*indent + "pass\n"
        else:
            for i in range(len(args1)):
                if (i == len(args1)-1):
                    proc1 += args1[i]+")"
                elif (i == 0):
                    continue
                else:
                    proc1 += args1[i]+", "
            linea_traducida += indent_level*indent + proc1 + "\n"

        indent_level -= 1
        linea_traducida += indent_level*indent + "else:\n"
        indent_level += 1
        args2 = match.group(3).split()
        proc2 = args2[0] + "("

        if (len(args2) == 1):
            args2.append("")

        if (args2[0] == ""):
            linea_traducida += indent_level*indent + "pass\n"
        else:
            for i in range(len(args2)):
                if (i == len(args2)-1):
                    proc2 += args2[i]+")"
                elif (i == 0):
                    continue
                else:
                    proc2 += args2[i]+", "
            linea_traducida += indent_level*indent + proc2

        indent_level -= 1

        return linea_traducida

    elif (re.search(r'\$\^PROC\((w+)\)', line) != None):
        match = re.search(r' \^PROC\((w+)\)', line)
        linea_traducida = indent_level*indent+"def "+match.group(1)+"(*params):"

        return linea_traducida

    elif (re.search(r'#(w+)', line) != None):
        match = re.search(r'#(w+)', line)
        linea_traducida = 2*indent_level*indent + "return" + match.group(1)

        return linea_traducida

    else:
        linea_traducida = line.strip("\n")
        return linea_traducida





for line in text:#recorriendo lineas del archivo de codigo raro
    traduc = traducirlinea(line)
    appendline(traduccion, traduc)

text.close()

newfile = open(filename+".py","w")

for line in traduccion:
    newfile.write(line)

newfile.close()


#Procedimientos: alterar indent_level segun la cantidad de espacios que debe tener al comienzo.
#Procedimientos: primera linea: def pname(parama):
#Procedimientos: traducir linea por linea modificando el nivel de indentacion segun corresponda hasta llegar a una liena ^$.