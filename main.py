#123456789012345678901234567890123456789012345678901234567890123456789012345678

import sys
import re
from stdlib import *

filename = sys.argv[1]
text = open(filename)
traduccion = list()
indent_level = 0
indent = "    "


def appendline(list, line): #es esto necesario?(\n) quizas deba sacarlo luego de ver lo de las RE.
    newline = line + "\n"
    list.append(newline)

def traducirlinea(line):
    #if (line calza con RE de proc,asignacion,ifelse,etc):
    #    traductedline = traduccion de lo que calce.
    #    newline = indent_level*indent + traductedline
    #    modificar indent_level segun corresponda.
    if (re.search(r'VAR\((\w+)\) <= (\d+)', line) != None):
        match = re.search(r'VAR\((\w+)\) <= (\d+)', line)
        linea_traducida =  indent_level*indent + match.group(1) + " = " + match.group(2)
        return linea_traducida

    elif (re.search(r'(\d+) => VAR\((\w+\))') != None):
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

    elif (re.search(r'FALSE => VAR\((\w+\))', line) != None):                           #AGREGAR ASIGNACIONES DE PROCEDIMIENTOS Y DE OTRAS VARIABLES!!!!!
        match = re.search(r'FALSE => VAR\((\w+\))', line)
        linea_traducida = indent_level*indent + match.group(1) + " = False"
        return linea_traducida

    elif (re.search(r'\([\w\d ]*\)', line) != None):
        split = line.split()
        match = list()

        if (len(split) == 1):
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

    elif (re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line) != None): #CORRER ESTE MAS ABAJO DE LAS ASIGNACIONES DE IFELESE!!!!!!

        match = re.search(r'IFELSE \(([\w\d ]*)\) \(([\w\d ]*)\) \(([\w\d ]*)\)', line)
        statement = ""
        cond = match.group(2)
        splits = cond.split()

        if (cond == "TRUE"):
            cond = "True"
        elif (cond == "FALSE"):
            cond = "False"
        elif (len(splits) != 1):
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

        if (len(proc1) == 1):
            linea_traducida += indent_level*indent + "pass\n"
        else:
            for i in range(len(proc1)):
                if (i == 0):
                    continue
                elif (i == len(args1)-1):
                    proc1 += args1[i]+")"
                else:
                    proc1 += args1[i]+", "
            linea_traducida += indent_level*indent + proc1 + "\n"

        indent_level -= 1
        linea_traducida += indent_level*indent + "else:\n"
        indent_level += 1
        args2 = match.group(2).split()
        proc2 = args2[0] + "("

        if (len(proc2) == 1):
            linea_traducida += indent_level*indent + "pass\n"
        else:
            for i in range(len(proc2)):
                if (i == 0):
                    continue
                elif (i == len(args2)-1):
                    proc2 += args2[i]+")"
                else:
                    proc1 += args2[i]+", "
            linea_traducida += indent_level*indent + proc2 + "\n"

        indent_level -= 1

        return linea_traducida





for line in text:#recorriendo lineas del archivo de codigo raro
    traduc = traducirlinea(line)
    appendline(traduccion, traduc)

text.close()

newfile = open(filename+".py")

traduccion.append("from stdlib import *")
for line in traduccion:
    newfile.write(line)

newfile.close()

#asignaciones de enteros: re.search(r'VAR\(\w+\) <= \d+', string) re.search(r'\d+ => VAR\(\w+\)', string)
#asignaciones de booleanos: re.search(r'TRUE => VAR\(\w+\)|FALSE => VAR\(\w+\)', string) re.search(r'VAR\(\w+\) <= TRUE|VAR\(\w+\) <= FALSE', string)


#Procedimientos: alterar indent_level segun la cantidad de espacios que debe tener al comienzo.
#Procedimientos: primera linea: def pname(parama):
#Procedimientos: traducir linea por linea modificando el nivel de indentacion segun corresponda hasta llegar a una liena ^$.


#Procedimientos llamadas: pname(list(var1, var2, var3))

#IFELSE: if (cond): <ifproc>  else: <elseproc>. + otras 2 RE para asignacion.