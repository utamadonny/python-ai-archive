import sys

temperature_fuzzy_set=['cold','cool','normal','warm','hot']
humidity_fuzzy_set=['dry','moist','wet']
sprinkler_duration_fuzzy_set=['short','medium','long']

def main():
    print('')
    print('Input Of Fuzzzyfication')
    print('')
    print(' Please Input Temperatur Value (celcius): ', end = '',flush=True)
    temperature = int(sys.stdin.readline())

    print(' Please Input Percentage Humidity (%): ', end = '',flush=True)
    humidity = int(sys.stdin.readline())

    #print('temperature Input',temperature)
    #print('humidity Input',humidity)

    rules = parsing_kb_file('rule.kb')

    tmp=temperatureFunction(temperature)
    hum=humidityFunction(humidity)

    print('Output of Fuzzyfication')
    print(tmp)
    print(hum)
    #print('')

    inf = inferred(tmp, hum, rules)
    
    result_rule_min =[]
    for dt in inf:
        #print(dt[0][0][0][1],dt[0][0][0][2],dt[0][0][1][2],dt[1])
        minimum = min(dt[0][0][0][2],dt[0][0][1][2])
        result_rule_min.append([dt[1],minimum])
   # print('')

    #print(result_rule_min)

    result_rule_max ={}
    for data in result_rule_min:
        if data[0] in result_rule_max:
            result_rule_max[data[0]].add(data[1])
        else:
            result_rule_max[data[0]]= set([data[1]])

    output_inference =[]
    for key, value in result_rule_max.items():
        output_inference.append([key,max(value)])

    print('')
    print('Output Inference is', output_inference  )
    print('')

    print('defuzzyfication')
    finalValues =defuzzyfication(output_inference)

    print('Minutes',finalValues)

def defuzzyfication(input):
    result = float(0)
    x1_short = 0
    x2_short = 28
    coefisien_short =float(0)

    x1_medium = 20
    x2_medium = 48
    coefisien_medium =float(0)

    x1_long = 40
    x2_long = 90
    coefisien_long =float(0)

    _short_numerator = float(0)
    _medium_numerator = float(0)
    _long_numerator = float(0)

    _short_denumerator = float(0)
    _medium_denumerator = float(0)
    _long_denumerator = float(0)

    for data in input:
        if data[0]=='short' :
            coefisien_short =data[1]
        if data[0]=='medium' :
            coefisien_medium =data[1]
        if data[0]=='long' :
            coefisien_long =data[1]

    #=========================================================

    if coefisien_short != float(0) and coefisien_medium != float(0) and coefisien_long == float(0):
        x_start_short =x1_short
        x_end_short = x1_medium +1 

        x_start_medium = x2_short
        x_end_medium = x1_long +1 

        for i in range (x_start_short, x_end_short ):
            _short_numerator += i * coefisien_short
            _short_denumerator += coefisien_short
            
        for i in range (x_start_medium, x_end_medium ):
            _medium_numerator += i * coefisien_medium
            _medium_denumerator += coefisien_medium

        result=(_medium_numerator + _short_numerator) / (_medium_denumerator + _short_denumerator)

        # ===========================================

    if coefisien_short == float(0) and coefisien_medium != float(0) and coefisien_long != float(0):
        x_start_medium =x2_short
        x_end_medium = x1_long +1   

        x_start_long = x2_medium
        x_end_long = x2_long +1 

        for i in range (x_start_medium, x_end_medium ):
            _medium_numerator += i * coefisien_medium
            _medium_denumerator += coefisien_medium
            
        for i in range (x_start_long, x_end_long ):
            _long_numerator += i * coefisien_long
            _long_denumerator += coefisien_long

        result=(_long_numerator + _medium_numerator) / (_long_denumerator + _medium_denumerator)


        #==================================
    if coefisien_short != float(0) and coefisien_medium != float(0) and coefisien_long != float(0):
        x_start_short =x1_short
        x_end_short = x1_medium +1 

        x_start_medium =x2_short
        x_end_medium = x1_long +1 

        x_start_long = x2_medium
        x_end_long = x2_long +1 

        for i in range (x_start_short, x_end_short ):
            _short_numerator += i * coefisien_short
            _short_denumerator += coefisien_short

        for i in range (x_start_medium, x_end_medium ):
            _medium_numerator += i * coefisien_medium
            _medium_denumerator += coefisien_medium
            
        for i in range (x_start_long, x_end_long ):
            _long_numerator += i * coefisien_long
            _long_denumerator += coefisien_long

        result=(_short_numerator + _long_numerator+_medium_numerator) / (_short_denumerator + _long_denumerator+_medium_denumerator)

    # =========================================
    if coefisien_short != float(0) and coefisien_medium == float(0) and coefisien_long == float(0):
        x_start_short =x1_short
        x_end_short = x1_medium +1 

        for i in range (x_start_short, x_end_short ):
            _short_numerator += i * coefisien_short
            _short_denumerator += coefisien_short

        result=(_short_numerator) / (_short_denumerator)

        #===============
    if coefisien_short == float(0) and coefisien_medium != float(0) and coefisien_long == float(0):
        x_start_medium =x2_short
        x_end_medium = x1_long +1 

        for i in range (x_start_medium, x_end_medium ):
            _medium_numerator += i * coefisien_medium
            _medium_denumerator += coefisien_medium
            

        result=(_medium_numerator) / (_medium_denumerator)

      #===================
    
    if coefisien_short == float(0) and coefisien_medium == float(0) and coefisien_long != float(0):
        x_start_long = x2_medium
        x_end_long = x2_long +1 
            
        for i in range (x_start_long, x_end_long ):
            _long_numerator += i * coefisien_long
            _long_denumerator += coefisien_long

        result=(_long_numerator)/(_long_denumerator)

    return result

    # for dt in inf:
    #     print(dt)

    # print(inf)
    
def inferred(fuzzification_temp, fuzzification_hum, fuzzification_rule):
    agenda=[]
    possibility=[]

    for dt in fuzzification_temp:
        agenda.append(dt)
    for dt in fuzzification_hum:
        agenda.append(dt)

    while agenda:
        item = agenda.pop(0)
        for rule in fuzzification_rule:
            for j, premise in enumerate(rule[0]):
                if premise == item[0]:
                    rule[0][j]=[True, rule[0][j], item[1]]
                # print(rule[0])   loop forever if not commented
                if check_hipotesis(rule[0]):
                    conclusion = rule[1]
                    possibility.append(rule)
                    agenda.append(conclusion)
                    rule[0] = [rule[0],'processed']  # loop forever bila dihapus

    # print(agenda)

    return possibility

def check_hipotesis(hipotesis):
    
    for entry in hipotesis:
        if entry[0]!=True:
            return False
    return True

def temperatureFunction(input):
    linguistik_temperature= []
    if input >=-10 and input <=3:
        linguistik_temperature.append(temperature_fuzzy_set[0]) #cold
    if input >=0 and input <=15:
        linguistik_temperature.append(temperature_fuzzy_set[1]) #cool
    if input >=12 and input <=27:
        linguistik_temperature.append(temperature_fuzzy_set[2]) #normal
    if input >=24 and input <=39:
        linguistik_temperature.append(temperature_fuzzy_set[3]) #warm
    if input >=36 and input <=50:
        linguistik_temperature.append(temperature_fuzzy_set[4]) #hot

    value_temp=[]

    if len(linguistik_temperature)>1:
        if linguistik_temperature[0] == temperature_fuzzy_set[0] and linguistik_temperature[1] == temperature_fuzzy_set[1]:
            # cold
            cold= -(input-3)/(3-0)
            value_temp.append([linguistik_temperature[0],cold])
            # cool
            cool= (input-0)/(3-0)
            value_temp.append([linguistik_temperature[1],cool])
        elif linguistik_temperature[0] == temperature_fuzzy_set[1] and linguistik_temperature[1] == temperature_fuzzy_set[2]:
            # cool
            cold = -(input-15)/(15-12)
            value_temp.append([linguistik_temperature[0],cool])
            #normal
            normal = (input-12)/(15-12)
            value_temp.append([linguistik_temperature[1],normal])
        elif linguistik_temperature[0] == temperature_fuzzy_set[2] and linguistik_temperature[1] == temperature_fuzzy_set[3]:
            #normal
            normal = -(input-27)/(27-24)
            value_temp.append([linguistik_temperature[0],normal])
            # warm
            warm = (input-24)/(27-24)
            value_temp.append([linguistik_temperature[1],warm])
        elif linguistik_temperature[0] == temperature_fuzzy_set[3] and linguistik_temperature[1] == temperature_fuzzy_set[4]:
            #warm
            warm = -(input-39)/(39-36)
            value_temp.append([linguistik_temperature[0],warm])
            # hot
            hot = (input-36)/(39-36)
            value_temp.append([linguistik_temperature[1],hot])
    else:
        value_temp.append([linguistik_temperature[0],1])

    return value_temp   

def humidityFunction(input):
    linguistik_humidity= []
    if input >=0 and input <=20:
        linguistik_humidity.append(humidity_fuzzy_set[0]) #dry
    if input >=10 and input <=50:
        linguistik_humidity.append(humidity_fuzzy_set[1]) #moist
    if input >=40 and input <=70:
        linguistik_humidity.append(humidity_fuzzy_set[2]) #wet

    value_hum=[]

    if len(linguistik_humidity)>1:
        if linguistik_humidity[0] == humidity_fuzzy_set[0] and linguistik_humidity[1] == humidity_fuzzy_set[1]:
            # dry
            dry= -(input-20)/(20-10)
            value_hum.append([linguistik_humidity[0],dry])
            # moist
            moist= (input-10)/(20-10)
            value_hum.append([linguistik_humidity[1],moist])
        elif linguistik_humidity[0] == humidity_fuzzy_set[1] and linguistik_humidity[1] == humidity_fuzzy_set[2]:
            # moist
            moist = -(input-50)/(50-40)
            value_hum.append([linguistik_humidity[0],moist])
            # wet
            wet = (input-40)/(50-40)
            value_hum.append([linguistik_humidity[1],wet])
    else:
        value_hum.append([linguistik_humidity[0],1])

    return value_hum     

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

