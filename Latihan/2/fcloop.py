import sys

def main():
    if len (sys.argv) > 2:
        sys.argv.pop(0)
        kb_file= sys.argv.pop(0)
        state = sys.argv.pop(0)

        knowledge = parsing_kb_file(kb_file)
        #print(knowledge)
        agenda = state.split(' ')

        inferred=[]
        inferred=forward(agenda, knowledge, inferred)

    else:
        print ('Error Begoooo')

def print_saran(inferred):
    for i, entry in enumerate (inferred):
        if 'move' in entry and 'can_win' in entry:
            print(inferred.pop(i))
            return
    for i, entry in enumerate (inferred):
        if 'move' in entry and 'force' in entry:
            print(inferred.pop(i))
            return
    for i, entry in enumerate (inferred):
        if 'move' in entry and 'setup' in entry:
            print(inferred.pop(i))
            return
    
def forward(agenda, knowledge, inferred):

    while agenda:
        item = agenda.pop(0)
        for rule in knowledge:
            for j, premise in enumerate(rule[0]):
                if premise == item:
                    rule[0][j] = True
            print(rule[0])

            if cek_hipotesis(rule[0]):
                kesimpulan = (rule[1])
                inferred.append(kesimpulan)
                agenda.append(kesimpulan)
                # rule[0]=['sudah di proses']  ini dihapus sehigga loop forever
        
    return inferred

def cek_hipotesis(hipotesis):
    for entry in hipotesis:
        if entry != True:
            return False
    return True

def parsing_kb_file(filename):

    kb_file = open(filename)
    kb_rules = []

    for line in kb_file:
        if not line.startswith('#') and line!= '\n':
            kb_rules.append(split_and_build_literals(line.strip()))

    kb_file.close()
    return kb_rules

def split_and_build_literals(line):
    rules = []
    literals = line.split(' ')
    hipotesis=[]
    while len (literals) >1 :
        hipotesis.append(literals.pop(0))
    rules.append(hipotesis)
    rules.append(literals.pop(0))
    return rules

if __name__ == '__main__':
    main()