import math

#Input received four floats passed as parameters sen 1-4
def normalize_sensor_input(sen1: float, sen2: float, sen3: float, sen4: float) -> float:

    # square input parameters
    sen1sq = sen1 * sen1
    sen2sq = sen2 * sen2
    sen3sq = sen3 * sen3
    sen4sq = sen4 * sen4

    # Totalling the four inputs together stored in senT
    senT = sen1sq + sen2sq + sen3sq + sen4sq

    # normalized sensor input data variable
    normsi: float = math.sqrt(senT)

    #Prints out normalized value
    #print(normsi)

    #Return normal for sensor input
    return normsi
    

#Test Function Run
#normalize_sensor_input(1, 1, 1, 1)
