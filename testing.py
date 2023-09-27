# Creates a list from either csv file with only the necessary information
def loadCSVData(filename):
    finalList = []
    with open(filename, encoding='utf8') as file:
        # lines = file.readLines()[1:]
        for line in file:
            line = line.rstrip()
            lineList = line.split(",")
            # Removes the unnecessary information from TopUni.csv
            if filename == "TopUni.csv":
                del lineList[4:8]
            # Removes the unnecessary information from capitals.csv
            elif filename == "capitals.csv":
                del lineList[2:5]
            finalList.append(lineList)
        del finalList[0]
        return finalList


# Writes to the output file the number of universities (1)
def numofUni():
    output = "Total number of universities => 100"
    return output


# Creates a list with all the countries from TopUni.csv (2)
def uniCountryList(uniList):
    countryList = []
    # Goes through the list of universities and checks if the country is in the list yet
    for i in range(0, 100):
        inList = countryList.count(uniList[i][2])
        # If the country's already in the list, it goes to the next iteration of the for loop
        if inList > 0:
            continue
        # If it's not in the list, it adds the country to the list
        else:
            newCountry = uniList[i][2]
            countryList.append(newCountry)
    countryList = upperCaseList(countryList)
    return countryList


# Writes to the text file the available continents (3)
def continentList():
    output = "Available continents => NORTH AMERICA, EUROPE, ASIA, AUSTRALIA"
    return output


# Finds the university with the highest international rank in the country (4)
def highestInternational(selectedCountry, uniList):
    i = 0
    # Goes through the list of universities until the first one with the selected country shows up
    while uniList[i][2].upper() != selectedCountry.upper():
        i += 1
    # Since the list is ordered by international rank, the first university that shows up is the highest ranked in the world
    rankOfUni = uniList[i][0]
    uniName = uniList[i][1]
    outputText = "At international rank => " + rankOfUni + " the university name is => " + uniName.upper()
    return outputText


# Finds the university with the highest national rank in the country (5)
def highestNational(country, uniList):
    # Creates a list of all the universities in the country, ordered by their national rank
    rankedList = uniFromCountry(country, uniList)
    # The first element in the list will contain the name and rank of the highest nationally ranked university
    nationalRank = rankedList[0][0]
    uniName = rankedList[0][1]
    outputText = "At national rank => " + nationalRank + " the university name is => " + uniName.upper()
    return outputText


# Makes all elements in any list uppercase
def upperCaseList(anyList):
    anyListUpper = [item.upper() for item in anyList]
    return anyListUpper


# Creates a list of all the universities and their info in a specified country
def uniFromCountry(country, uniList):
    uniCountryInfoList = []
    for i in range(0, 100):
        # Checks if the university is in the specified country
        if uniList[i][2].upper() == country.upper():
            # If it is, creates a list of the universities national rank, name and score
            uniAndInfo = [uniList[i][3], uniList[i][1], uniList[i][-1]]
            # Appends this information to the greater list
            uniCountryInfoList.append(uniAndInfo)
        else:
            continue
    # Sorts the list by the national rank (highest to lowest)
    uniCountryInfoList.sort(key=lambda row:
    row[0])
    return uniCountryInfoList


# Gets the average score of all the universities in the country (6)
def averageCountryScore(country, uniList):
    countryList = uniFromCountry(country, uniList)
    totalScore = 0
    # Goes through the list of universities in the country, and adds up all of their scores
    for i in range(0, len(countryList)):
        totalScore += float(countryList[i][2])
    # Calculates the average score
    averageScore = round(totalScore / len(countryList), 2)
    return averageScore


# Gets all the countries in the selected continent
def countriesInContinent(continent, capitalList):
    countryContinentList = []
    # Goes through the list of capitals, and adds all the countries from the specified continent to a list
    for i in range(0, len(capitalList)):
        if capitalList[i][-1] == continent:
            countryContinentList.append(capitalList[i][0])
        else:
            continue
    return countryContinentList


# Gets the ratio between the average score of a country, and the highest score in its continent (7)
def continentRelativeScore(country, uniList, capitalList):
    i = 0
    average = averageCountryScore(country, uniList)
    # Gets the continent of the specified country
    while capitalList[i][0].upper() != country.upper():
        i += 1
    continent = capitalList[i][-1]
    countryList = countriesInContinent(continent, capitalList)
    highestScore = 0
    # Goes through uni list, checks if the uni is in the continent and gets the uni with the highest score
    for i in range(0, len(uniList)):
        # Checks if the country is in the list of countries that are in the continent
        if uniList[i][2] in countryList:
            # Checks if the countries score is higher than the current score
            if float(uniList[i][-1]) > highestScore:
                # Sets the score to the highest score
                highestScore = float(uniList[i][-1])
        else:
            continue
    relativeScore = round((average / highestScore) * 100, 2)
    output = "The relative score to the top university in {} is => ({}/{}) * 100% = {}%".format(continent.upper(),
                                                                                                average, highestScore,
                                                                                                relativeScore)
    return output


# Returns the capital city of the country (8)
def capitalCity(capitalList, country):
    i = 0
    # Goes through the capital list, looking for the specified country
    while capitalList[i][0].upper() != country.upper():
        i += 1
    # Sets capital to the capital found with the country in capitals.csv
    capital = capitalList[i][1]
    return capital


# Creates a list of all the universities with the capital name of the selected country (9)
def uniWithCapitalName(uniList, capitalList, country):
    capital = capitalCity(capitalList, country)
    uniInCountry = uniFromCountry(country, uniList)
    uniWithCapital = []
    # Goes through the list of universities in the selected country
    for i in range(0, len(uniInCountry)):
        # If the capital string is in the name of the university, adds it to the list of universities with capital names
        if capital in uniInCountry[i][1]:
            uniWithCapital.append(uniInCountry[i][1])
        else:
            continue
    return uniWithCapital




def getInformation(selectedCountry, rankingFileName, capitalsFileName):
    # Prints file not found to output.txt if either of the required files don't exist
    try:
        uniList = loadCSVData(rankingFileName)
        capitalList = loadCSVData(capitalsFileName)
    except:
        with open("output.txt", "w") as outputFile:
            outputFile.write("file not found")
            quit()
    firstOutput = numofUni()
    listOfCountries = uniCountryList(uniList)
    thirdOutput = continentList()
    fourthOutput = highestInternational(selectedCountry, uniList)
    fifthOutput = highestNational(selectedCountry, uniList)
    averageScore = averageCountryScore(selectedCountry, uniList)
    sixthOutput = "The average score => " + str(averageScore) + "%"
    seventhOutput = continentRelativeScore(selectedCountry, uniList, capitalList)
    capital = capitalCity(capitalList, selectedCountry)
    eighthOutput = "The capital is => " + capital.upper()
    uniCapitalList = uniWithCapitalName(uniList, capitalList, selectedCountry)
    with open("output.txt", "w") as outputFile:
        outputFile.write(firstOutput)
        outputFile.write('\n')
        outputFile.write("Available countries => ")
        for i in range(0, len(listOfCountries)):
            outputFile.write(listOfCountries[i])
            outputFile.write(", ")
        outputFile.write('\n')
        outputFile.write(thirdOutput)
        outputFile.write('\n')
        outputFile.write(fourthOutput)
        outputFile.write('\n')
        outputFile.write(fifthOutput)
        outputFile.write('\n')
        outputFile.write(sixthOutput)
        outputFile.write('\n')
        outputFile.write(seventhOutput)
        outputFile.write('\n')
        outputFile.write(eighthOutput)
        outputFile.write('\n')
        outputFile.write("The universities that contain the capital name =>")
        outputFile.write('\n')
        for i in range(0, len(uniCapitalList)):
            outputFile.write("#" + str(i + 1) + " ")
            outputFile.write(uniCapitalList[i])
            outputFile.write('\n')



