import sys

def main():
    if len(sys.argv) >2:
        sys.argv.pop(0)
        kb_file = sys.argv.pop(0)
        state = sys.argv.pop(0)

        knowledge = parsing_kb_file(kb_file)
        agenda = state.split(' ')

        inferred = []

        inferred = forward_chaining(agenda, knowledge, inferred)
        if len(inferred) >0:
            print_suggested_move(inferred)
    else:
        print("ERror Bego: Instruksi Kurang py -3 fc.py knowledge.kb 'x11 x12'")

def forward_chaining(agenda, knowledge, inferred):

    while agenda:
        item = agenda.pop(0)      
        for rule in knowledge:
            for j, premise in enumerate(rule[0]):
                if premise == item:
                    rule[0][j] = True
                    
            if check_hipotesis(rule[0]):
                conclusion = rule[1]
                inferred.append(conclusion)
                agenda.append(conclusion)
                rule[0]=['sudah di proses']


    return inferred

def check_hipotesis(hipotesis):
    
    for entry in hipotesis:
        if entry!=True:
            return False
    return True

def print_suggested_move(inferred):
    for i, entry in enumerate(inferred):
        if 'move' in entry and 'can_win'in entry:
            print (inferred.pop(i))
            return
    for i, entry in enumerate(inferred):
        if 'move' in entry and 'force'in entry:
            print (inferred.pop(i))
            return
    for i, entry in enumerate(inferred):
        if 'move' in entry and 'setup'in entry:
            print (inferred.pop(i))
            return

def parsing_kb_file(filename):

    kb_file = open(filename)
    kb_rules = []

    for line in kb_file:
        if not line.startswith('#') and line != '\n':
            kb_rules.append(split_and_build_literals(line.strip()))
    kb_file.close()
    return kb_rules

def split_and_build_literals(line):
    rules =[]
    literals = line.split(' ')
    hipotesis = []

    while len(literals) >1:
        hipotesis.append(literals.pop(0))
    rules.append(hipotesis)
    rules.append(literals.pop(0))

    return rules

if __name__ == '__main__':
    main()