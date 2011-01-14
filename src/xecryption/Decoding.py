'''
Created on Jan 12, 2011

Local Vars:
    encodedData - data passed in the format defined by xecryption
    
    triplets - list of sublists split that consists of encodedData split into
               triplets
    sumsOfTriplets - list of the sums of each triplet
    
    passwordMax - Maximum possible value of the password
    
    possiblePasswords - 

@author: shoe
'''
class Decoder:
    
    badCharThreshold = 30
    
    def __init__(self, encoded):
        #Get rid of whitespace and leading period
        self.encodedData = encoded.strip().lstrip(".")
        self.triplets = self.splitDataIntoTriplets(self.encodedData)
        #if the total number of characters is less than the default threshold,
        #use half the number of characters
        if len(self.triplets) < self.badCharThreshold:
            self.badCharThreshold = len(self.triplets)/2
        self.sums = self.createSumsOfTriplets(self.triplets)
        self.passwordMax = self.findMaxPasswordValue(self.sums)
    
    def splitDataIntoTriplets(self, encoded):
        seq = encoded.split(".")
        #by the xecryption definition, this will always be three
        size = 3 
        return [seq[i:i+size] for i  in range(0, len(seq), size)]
    
    def createSumsOfTriplets(self, triplets):
        sums = []
        for triplet in triplets:
            sum = 0;
            for x in triplet:
                sum = sum + int(x)
            sums.append(sum)
        return sums
    
    def findMaxPasswordValue(self, sums):
        return min(sums)
    
    def decode(self):
        possibleTranslations = []
        for possiblePassVal in range(0, self.passwordMax):
            try:
                x = self.checkPassword(possiblePassVal)
                possibleTranslations.append(x)
            except ValueError:
                print(possiblePassVal, ' is not a valid password value.')
        
        outputFile = open('/Users/shoe/xecrypt.out', 'w')
        for translation in possibleTranslations:
            outputFile.write('\r\n\r\n')
            outputFile.write(''.join(translation[1]))
                
    '''
        Check to see if a given password value is a legit possibility.
        
        To do this, the sums calculated before and the possible password value
        is subtracted from it as described in the Xecryption definition.  The
        remainder is then checked against 32 and 255.  If it is above 255, it
        is not a valid ASCII character (pretty sure this should never happen
        because of the way passwordMax is found).  Anything from 0 to 31 is a
        valid ASCII value but one that a user is very unlikely to enter.  32 is
        the start of commonly typed characters.
        
        Since a password value can never be less than 0, -1 is returned if the
        password is determined to be invalid.
    '''            
    def checkPassword(self, possiblePassVal):
        badChars = 0
        possibleTranslation = []
        for sum in self.sums:
            charVal = sum - possiblePassVal
            possibleTranslation.append(chr(charVal))
            if charVal < 32 or charVal > 127:
                badChars += 1
                if badChars > self.badCharThreshold:
                    raise ValueError
        return [possiblePassVal, possibleTranslation]