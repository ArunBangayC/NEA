primeNumbers = []

def isPrime(n):
    if n<2:
        return False
    elif n == 2 or n == 3 or n == 5:
        primeNumbers.append(n)
    elif n%2 == 0 or n%3 == 0 or n%5 == 0:
        return False
    else:
        possibleFactors = 0
        for i in range(2,(int(n/2)+1)):
            if n%i == 0:
                possibleFactors += 1
        if possibleFactors == 0:
            primeNumbers.append(n)

for i in range(1,128):
    isPrime(i)

for i in range(len(primeNumbers)):
    possibleMultipleOf4 = primeNumbers[i]-9
    possibleMultipleOf9 = primeNumbers[i]-4
    if possibleMultipleOf4%4 == 0 or possibleMultipleOf9%9 == 0:
        print(primeNumbers[i],True)
    else:
        print(primeNumbers[i],False)
