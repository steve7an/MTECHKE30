def goodbye(name, adjective):
    print('Goodbye, %s, it was %s to meet you.' 
    	% (name, adjective))

import atexit
atexit.register(goodbye, 'Sammy', 'bad')

# or:
atexit.register(goodbye, adjective='nice', name='Donny')

while 1:
	print ("")