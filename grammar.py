rule_dict = {
    "Program": [["Declaration-list"]],
    "Declaration-list": [["Declaration", "Declaration-list"], ['epsilon']],
    "Declaration": [["Declaration-initial", "Declaration-prime"]],
    "Declaration-initial": [["#save-in-ss", "Type-specifier", "#save-in-ss", "ID"]],
    "Declaration-prime": [["Fun-declaration-prime"], ["Var-declaration-prime"]],
    "Var-declaration-prime": [[";", "#dec-var"], ["[", "#save-in-ss", "NUM", "]", ";", "#dec-array"]],
    "Fun-declaration-prime": [["#dec-func", "(", "Params", ")", "Compound-stmt", "#end-func"]],
    "Type-specifier": [["int"], ["void"]],
    "Params": [["#save-in-ss", "int", "#save-in-ss", "ID", "Param-prime", "Param-list"], ["void"]],
    "Param-list": [[",", "Param", "Param-list"], ['epsilon']],
    "Param": [["Declaration-initial", "Param-prime"]],
    "Param-prime": [["[", "]"], ['epsilon', "#dec-var"]],
    "Compound-stmt": [[ "{", "Declaration-list", "Statement-list", "}"]],
    "Statement-list": [["Statement", "Statement-list"], ['epsilon']],
    "Statement": [["Expression-stmt"], ["Compound-stmt"], ["Selection-stmt"], ["Iteration-stmt"], ["Return-stmt"]],
    "Expression-stmt": [["Expression", ";"], ["break", ";", "#save-break"], [";"]],
    "Selection-stmt": [["if", "(", "Expression", ")", "#save", "Statement", "else", "#jpf_save", "Statement", "#jp"]],
    "Iteration-stmt": [["repeat", "#label", "#begin", "Statement", "#end", "until", "(", "Expression", ")", "#until"]],
    "Return-stmt": [["return", "Return-stmt-prime"]],
    "Return-stmt-prime": [[";"], ["Expression", ";"]],
    "Expression": [["Simple-expression-zegond"], ["#pid", "ID", "B", "#print"]],
    "B": [["=", "Expression", "#assign"], ["[", "Expression", "]", "#calc-arr-addr", "H"], ["Simple-expression-prime"]],
    "H": [["=", "Expression", "#assign"], ["G", "D", "C"]],
    "Simple-expression-zegond": [["Additive-expression-zegond", "C"]],
    "Simple-expression-prime": [["Additive-expression-prime", "C"]],
    "C": [["Relop", "Additive-expression", "#relation"], ['epsilon']],
    "Relop": [["#save-in-ss", "<"], ["#save-in-ss", "=="]],
    "Additive-expression": [["Term", "D"]],
    "Additive-expression-prime": [["Term-prime", "D"]],
    "Additive-expression-zegond": [["Term-zegond", "D"]],
    "D": [["Addop", "Term", "#add-or-sub", "D"], ['epsilon']],
    "Addop": [["#save-in-ss", "+"], ["#save-in-ss", "-"]],
    "Term": [["Factor", "G"]],
    "Term-prime": [["Factor-prime", "G"]],
    "Term-zegond": [["Factor-zegond", "G"]],
    "G": [["*", "Factor", "#mult", "G"], ['epsilon']],
    "Factor": [["(", "Expression", ")"], ["#pid", "ID", "Var-call-prime"], ["#save-num-in-ss", "NUM"]],
    "Var-call-prime": [["(", "Args", ")"], ["Var-prime"]],
    "Var-prime": [["[", "Expression", "]", "#calc-arr-addr"], ['epsilon']],
    "Factor-prime": [["(", "Args", ")"], ['epsilon']],
    "Factor-zegond": [["(", "Expression", ")"], ["#save-num-in-ss", "NUM"]],
    "Args": [["Arg-list"], ['epsilon']],
    "Arg-list": [["Expression", "Arg-list-prime"]],
    "Arg-list-prime": [[",", "Expression", "Arg-list-prime"], ['epsilon']]
}
rules = [
    {"left": "Program", "right": ["Declaration-list"]},
    {"left": "Declaration-list", "right": ["Declaration", "Declaration-list"]},
    {"left": "Declaration-list", "right": ['epsilon']},
    {"left": "Declaration", "right": ["Declaration-initial", "Declaration-prime"]},
    {"left": "Declaration-initial", "right": ["Type-specifier", "ID"]},
    {"left": "Declaration-prime", "right": ["Fun-declaration-prime"]},
    {"left": "Declaration-prime", "right": ["Var-declaration-prime"]},
    {"left": "Var-declaration-prime", "right": [";"]},
    {"left": "Var-declaration-prime", "right": ["[", "NUM", "]", ";"]},
    {"left": "Fun-declaration-prime", "right": ["(", "Params", ")", "Compound-stmt"]},
    {"left": "Type-specifier", "right": ["int"]},
    {"left": "Type-specifier", "right": ["void"]},
    {"left": "Params", "right": ["int", "ID", "Param-prime", "Param-list"]},
    {"left": "Params", "right": ["void"]},
    {"left": "Param-list", "right": [",", "Param", "Param-list"]},
    {"left": "Param-list", "right": ['epsilon']},
    {"left": "Param", "right": ["Declaration-initial", "Param-prime"]},
    {"left": "Param-prime", "right": ["[", "]"]},
    {"left": "Param-prime", "right": ['epsilon']},
    {"left": "Compound-stmt", "right": ["{", "Declaration-list", "Statement-list", "}"]},
    {"left": "Statement-list", "right": ["Statement", "Statement-list"]},
    {"left": "Statement-list", "right": ['epsilon']},
    {"left": "Statement", "right": ["Expression-stmt"]},
    {"left": "Statement", "right": ["Compound-stmt"]},
    {"left": "Statement", "right": ["Selection-stmt"]},
    {"left": "Statement", "right": ["Iteration-stmt"]},
    {"left": "Statement", "right": ["Return-stmt"]},
    {"left": "Expression-stmt", "right": ["Expression", ";"]},
    {"left": "Expression-stmt", "right": ["break", ";"]},
    {"left": "Expression-stmt", "right": [";"]},
    {"left": "Selection-stmt", "right": ["if", "(", "Expression", ")", "Statement", "else", "Statement"]},
    {"left": "Iteration-stmt", "right": ["repeat", "Statement", "until", "(", "Expression", ")"]},
    {"left": "Return-stmt", "right": ["return", "Return-stmt-prime"]},
    {"left": "Return-stmt-prime", "right": [";"]},
    {"left": "Return-stmt-prime", "right": ["Expression", ";"]},
    {"left": "Expression", "right": ["Simple-expression-zegond"]},
    {"left": "Expression", "right": ["ID", "B"]},
    {"left": "B", "right": ["=", "Expression"]},
    {"left": "B", "right": ["[", "Expression", "]", "H"]},
    {"left": "B", "right": ["Simple-expression-prime"]},
    {"left": "H", "right": ["=", "Expression"]},
    {"left": "H", "right": ["G", "D", "C"]},
    {"left": "Simple-expression-zegond", "right": ["Additive-expression-zegond", "C"]},
    {"left": "Simple-expression-prime", "right": ["Additive-expression-prime", "C"]},
    {"left": "C", "right": ["Relop", "Additive-expression"]},
    {"left": "C", "right": ['epsilon']},
    {"left": "Relop", "right": ["<"]},
    {"left": "Relop", "right": ["=="]},
    {"left": "Additive-expression", "right": ["Term", "D"]},
    {"left": "Additive-expression-prime", "right": ["Term-prime", "D"]},
    {"left": "Additive-expression-zegond", "right": ["Term-zegond", "D"]},
    {"left": "D", "right": ["Addop", "Term", "D"]},
    {"left": "D", "right": ['epsilon']},
    {"left": "Addop", "right": ["+"]},
    {"left": "Addop", "right": ["-"]},
    {"left": "Term", "right": ["Factor", "G"]},
    {"left": "Term-prime", "right": ["Factor-prime", "G"]},
    {"left": "Term-zegond", "right": ["Factor-zegond", "G"]},
    {"left": "G", "right": ["*", "Factor", "G"]},
    {"left": "G", "right": ['epsilon']},
    {"left": "Factor", "right": ["(", "Expression", ")"]},
    {"left": "Factor", "right": ["ID", "Var-call-prime"]},
    {"left": "Factor", "right": ["NUM"]},
    {"left": "Var-call-prime", "right": ["(", "Args", ")"]},
    {"left": "Var-call-prime", "right": ["Var-prime"]},
    {"left": "Var-prime", "right": ["[", "Expression", "]"]},
    {"left": "Var-prime", "right": ['epsilon']},
    {"left": "Factor-prime", "right": ["(", "Args", ")"]},
    {"left": "Factor-prime", "right": ['epsilon']},
    {"left": "Factor-zegond", "right": ["(", "Expression", ")"]},
    {"left": "Factor-zegond", "right": ["NUM"]},
    {"left": "Args", "right": ["Arg-list"]},
    {"left": "Args", "right": ['epsilon']},
    {"left": "Arg-list", "right": ["Expression", "Arg-list-prime"]},
    {"left": "Arg-list-prime", "right": [",", "Expression", "Arg-list-prime"]},
    {"left": "Arg-list-prime", "right": ['epsilon']}
]

first_sets = {
    'Program': ['epsilon', 'int', 'void'],
    'Declaration-list': ['epsilon', 'int', 'void'],
    'Declaration': ['int', 'void'],
    'Declaration-initial': ['int', 'void'],
    'Declaration-prime': ['(', ';', '['],
    'Var-declaration-prime': [';', '['],
    'Fun-declaration-prime': ['('],
    'Type-specifier': ['int', 'void'],
    'Params': ['int', 'void'],
    'Param-list': [',', 'epsilon'],
    'Param': ['int', 'void'],
    'Param-prime': ['[', 'epsilon'],
    'Compound-stmt': ['{'],
    'Statement-list': ['epsilon', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
    'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
    'Expression-stmt': ['break', ';', 'ID', '(', 'NUM'],
    'Selection-stmt': ['if'],
    'Iteration-stmt': ['repeat'],
    'Return-stmt': ['return'],
    'Return-stmt-prime': [';', 'ID', '(', 'NUM'],
    'Expression': ['ID', '(', 'NUM'],
    'B': ['=', '[', '(', '*', '+', '-', '<', '==', 'epsilon'],
    'H': ['=', '*', 'epsilon', '+', '-', '<', '=='],
    'Simple-expression-zegond': ['(', 'NUM'],
    'Simple-expression-prime': ['(', '*', '+', '-', '<', '==', 'epsilon'],
    'C': ['epsilon', '<', '=='],
    'Relop': ['<', '=='],
    'Additive-expression': ['(', 'ID', 'NUM'],
    'Additive-expression-prime': ['(', '*', '+', '-', 'epsilon'],
    'Additive-expression-zegond': ['(', 'NUM'],
    'D': ['epsilon', '+', '-'],
    'Addop': ['+', '-'],
    'Term': ['(', 'ID', 'NUM'],
    'Term-prime': ['(', '*', 'epsilon'],
    'Term-zegond': ['(', 'NUM'],
    'G': ['*', 'epsilon'],
    'Factor': ['(', 'ID', 'NUM'],
    'Var-call-prime': ['(', '[', 'epsilon'],
    'Var-prime': ['[', 'epsilon'],
    'Factor-prime': ['(', 'epsilon'],
    'Factor-zegond': ['(', 'NUM'],
    'Args': ['epsilon', 'ID', '(', 'NUM'],
    'Arg-list': ['ID', '(', 'NUM'],
    'Arg-list-prime': [',', 'epsilon']
}

follow_sets = {
    'Program': ['$'],
    'Declaration-list': ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Declaration': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Declaration-initial': ['(', ';', '[', ',', ')'],
    'Declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Var-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Fun-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Type-specifier': ['ID'],
    'Params': [')'],
    'Param-list': [')'],
    'Param': [',', ')'],
    'Param-prime': [',', ')'],
    'Compound-stmt': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else',
                      'until'],
    'Statement-list': ['}'],
    'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
    'Expression-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
    'Selection-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
    'Iteration-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
    'Return-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
    'Return-stmt-prime': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
    'Expression': [';', ')', ']', ','],
    'B': [';', ')', ']', ','],
    'H': [';', ')', ']', ','],
    'Simple-expression-zegond': [';', ')', ']', ','],
    'Simple-expression-prime': [';', ')', ']', ','],
    'C': [';', ')', ']', ','],
    'Relop': ['(', 'ID', 'NUM'],
    'Additive-expression': [';', ')', ']', ','],
    'Additive-expression-prime': ['<', '==', ';', ')', ']', ','],
    'Additive-expression-zegond': ['<', '==', ';', ')', ']', ','],
    'D': ['<', '==', ';', ')', ']', ','],
    'Addop': ['(', 'ID', 'NUM'],
    'Term': ['+', '-', ';', ')', '<', '==', ']', ','],
    'Term-prime': ['+', '-', '<', '==', ';', ')', ']', ','],
    'Term-zegond': ['+', '-', '<', '==', ';', ')', ']', ','],
    'G': ['+', '-', '<', '==', ';', ')', ']', ','],
    'Factor': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    'Var-call-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    'Var-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    'Factor-prime': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    'Factor-zegond': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    'Args': [')'],
    'Arg-list': [')'],
    'Arg-list-prime': [')']
}

predict_sets = {
    '1': ['int', 'void', '$'],
    '2': ['int', 'void'],
    '3': ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    '4': ['int', 'void'],
    '5': ['int', 'void'],
    '6': ['('],
    '7': [';', '['],
    '8': [';'],
    '9': ['['],
    '10': ['('],
    '11': ['int'],
    '12': ['void'],
    '13': ['int'],
    '14': ['void'],
    '15': [','],
    '16': [')'],
    '17': ['int', 'void'],
    '18': ['['],
    '19': [',', ')'],
    '20': ['{'],
    '21': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
    '22': ['}'],
    '23': ['break', ';', 'ID', '(', 'NUM'],
    '24': ['{'],
    '25': ['if'],
    '26': ['repeat'],
    '27': ['return'],
    '28': ['ID', '(', 'NUM'],
    '29': ['break'],
    '30': [';'],
    '31': ['if'],
    '32': ['repeat'],
    '33': ['return'],
    '34': [';'],
    '35': ['ID', '(', 'NUM'],
    '36': ['(', 'NUM'],
    '37': ['ID'],
    '38': ['='],
    '39': ['['],
    '40': ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','],
    '41': ['='],
    '42': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    '43': ['(', 'NUM'],
    '44': ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','],
    '45': ['<', '=='],
    '46': [';', ')', ']', ','],
    '47': ['<'],
    '48': ['=='],
    '49': ['(', 'ID', 'NUM'],
    '50': ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','],
    '51': ['(', 'NUM'],
    '52': ['+', '-'],
    '53': ['<', '==', ';', ')', ']', ','],
    '54': ['+'],
    '55': ['-'],
    '56': ['(', 'ID', 'NUM'],
    '57': ['(', '*', '+', '-', '<', '==', ';', ')', ']', ','],
    '58': ['(', 'NUM'],
    '59': ['*'],
    '60': ['+', '-', '<', '==', ';', ')', ']', ','],
    '61': ['('],
    '62': ['ID'],
    '63': ['NUM'],
    '64': ['('],
    '65': ['[', '*', '+', '-', ';', ')', '<', '==', ']', ','],
    '66': ['['],
    '67': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    '68': ['('],
    '69': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    '70': ['('],
    '71': ['NUM'],
    '72': ['ID', '(', 'NUM'],
    '73': [')'],
    '74': ['ID', '(', 'NUM'],
    '75': [','],
    '76': [')']
}
