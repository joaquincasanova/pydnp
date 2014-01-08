def freqround(number): # this will round us to the .5 MHz
    number /= 1e6
    remainder = number - math.floor(number)
    print "I've determined the remainder to be: ", remainder
    if remainder < .25:
        remainder = 0.0
    elif (remainder >= .25 and remainder <= .75):
        remainder = .50
    elif remainder > .75:
        remainder = 1
    number = round(number,0)    
    print "I just rounded the number to: ", number
    number += remainder    
    number *= 1e6
    print "calculated remainder is ", remainder, "new frequency is: ", number
    return number
	
def yig_set_freq(frequency, resolution)
	frequency = freqround(frequency)
	channel = frequency/resolution
	string[0] = 'C'
	for j in range(0, 4)
		string[4-j] = 0xFF & (channel>>(8*j))
	printf "setting frequency ", frequency, " at resolution ", resolution, " with channel ", channel ," yields string " string
	write_yig(string,5)


def write_yig(string, strlen)
	small_wait = 25e-6 # this isn't right! changed b/c I thought it was the digatt
	long_wait = 150e-3
	GPIO.ouput(yig_e, 1) 
	time.sleep(small_wait)
	GPIO.ouput(yig_e, 0) #select low
	time.sleep(small_wait)
	for j in range(0,strlen)
		for whichbit in range(7,0,-1)
			#the following is copied from python, and should hopefully just work
			GPIO.ouput(yig_d,((1<<whichbit) & string[j])>>whichbit)
			GPIO.ouput(yig_c, 1)
			time.sleep(small_wait)
			GPIO.ouput(yig_c, 0)
			time.sleep(small_wait)
	GPIO.ouput(yig_e, 1) 
	time.sleep(long_wait)
	
def yig_check_lock
	time.sleep(500e-3)
	retval = GPIO.input(yig_l)
	return retval