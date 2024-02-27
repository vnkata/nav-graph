import json
file_name = "test2.txt"
path = "/home/thanh/Documents/GitHub/ISE-Implementation/GroovyParser/Assignment/Output/assignment-v2_" + file_name
f = open(path,"r")
lines = f.read().split("\n")
f.close()
tabs = 0 ; prev_tabs = 0
source_code = ""
row = -1
switchcase_count = 0
defaultCase = False
for line in lines:
    row += 1
    tabs = 0; i = 0;
    while len(line) > 0 and line[i] == '\t':
        tabs += 1; i += 1
    #load json
    try:
        tmp = json.loads(line)
    except:
        continue

    #line indent
    for j in range(tabs):
        source_code += '\t'

    #end-block indent
    copy_tabs = prev_tabs
    while copy_tabs > tabs:
        for j in range(copy_tabs - tabs - 1):
            source_code += '\t'
        if switchcase_count > 0:
            switchcase_count -= 1
        else:
            if defaultCase:
                source_code += '\n'
                defaultCase = False
            source_code += '}\n'
        copy_tabs -= 1
    prev_tabs = tabs
    #normal command
    if tmp['Receiver']:
        code = ""
        #-----------------------------
        # ATTENTION: Custom Keywords
        #-----------------------------
        if tmp['Receiver'] == "CustomKeywords":
            code += tmp['Receiver'] + ".'" + tmp['Action'] + "'("
        else:
            code += tmp['Receiver'] + '.' + tmp['Action'] + '('
        input = tmp['Input']
        for j in range(len(input)):
            in_type = input[j]['type']
            if in_type == 'Constant':
                #const is string -> add quotes
                if input[j]['datatype'] == 'java.lang.String':
                    code += "'" + input[j]['value'] + "'"
                else:
                    code += input[j]['value']
            elif in_type == 'Statement':
                code += input[j]['code']
            elif in_type == 'Variable':
                #var is string -> add quotes
                if input[j]['datatype'] == 'java.lang.String':
                    code += "'" + input[j]['name'] + "'"
                else:
                    code += input[j]['name']    
            
            if j + 1 != len(input):
                code += ', '
        code += ')\n'
        if tmp['Output']:
            lhs = ""
            if tmp['Output'][0]['type'] == "Variable":
                lhs += tmp['Output'][0]['name'] + " = " + code            
            elif tmp['Output'][0]['type'] == "Statement":
                lhs += tmp['Output'][0]['code'] + " = " + code
        source_code += code
    
    else:
        code = ''
        if tmp['Action'] == "Assignment":
            #define new variable
            if tmp['Output'][0]['type'] == 'Variable':
                code += 'def ' + tmp['Output'][0]['name'] + ' = ' + tmp['Input'][0]['code'] + ' ;\n'
            #assign value
            elif tmp['Output'][0]['type'] == 'Statement':
                if tmp['Input'][0]['type'] == 'Constant':
                    if tmp['Input'][0]['datatype'] == 'class java.lang.String':
                        code += tmp['Output'][0]['code'] + " = '" + tmp['Input'][0]['value'] + "'\n"
                    else:
                        code += tmp['Output'][0]['code'] + ' = ' + tmp['Input'][0]['value'] + "\n"
                elif tmp['Input'][0]['type'] == 'Statement':
                    code += tmp['Output'][0]['code'] + ' = ' + tmp['Input'][0]['code'] + "\n"


        elif tmp['Action'] == 'If':
            code += 'if ('
            code += tmp['Input'][0]['code']
            code += ') {\n'

        elif tmp['Action'] == 'Else':    
            copy_row = row + 1
            check_tabs = 0; indx = 0
            while len(lines[copy_row]) > 0 and  lines[copy_row][indx] == '\t':
                check_tabs += 1; indx += 1
            if check_tabs > tabs:
                for count in range(tabs):
                    code += '\t'           
                code += 'else {\n'

        elif tmp['Action'] == 'While':
            code += 'while '
            code += tmp['Input'][0]['code']
            code += ' {\n'

        elif tmp['Action'] == 'For loop':
            code += 'for '
            code += tmp['Input'][0]['code']
            code += ' {\n'

        elif tmp['Action'] == 'Try':
            code += 'try {\n'

        elif tmp['Action'] == 'Catch':
            code = 'catch ('
            if tmp['Input'][0]['datatype'] == 'java.lang.Exception -> java.lang.Exception':
                code += "Exception "
            code += tmp['Input'][0]['name']
            code += " ) {\n"

        elif tmp['Action'] == 'Finally':
            code += 'finally {\n'
        
        elif tmp['Action'] == 'Switch':
            if tmp['Input'][0]['type'] == 'Statement':
                code += 'switch(' + tmp['Input'][0]['code'] + ') {\n'
            elif tmp['Input'][0]['type'] == 'Variable':
                code += 'switch(' + tmp['Input'][0]['name'] + ') {\n'
        
        elif tmp['Action'] == 'Case':
            switchcase_count += 1
            code += 'case '
            if tmp['Input'][0]['type'] == 'Constant':
                if tmp['Input'][0]['datatype'] == 'java.lang.String':
                    code += "'" + tmp['Input'][0]['value'] + "'" + ':\n'
                else:
                    code += tmp['Input'][0]['value'] + ':\n'
            elif tmp['Input'][0]['type'] == 'Variable':
                code += tmp['Input'][0]['name'] + ':\n'
        
        elif tmp['Action'] == 'Default':
            code += 'default: \n'
            defaultCase = True
            switchcase_count += 1

        elif tmp['Action'] == 'Break':
            code += 'break\n'
        
        source_code += code

prefix = "GroovyParser/ConvertParser/Output/convert_"
f = open(prefix + file_name + ".groovy","w")
f.write(source_code)
f.close()