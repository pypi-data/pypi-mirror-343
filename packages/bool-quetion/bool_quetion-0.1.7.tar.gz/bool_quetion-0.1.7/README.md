# bool_quetion
## Python-module for asking yes/no or accept/cancel questions.

### Installing
#### Install on Debian 11 or older from PyP:

`pip install bool_quetion`

#### Install on Debian 12 and later from PyP:

`pip install bool_quetion --break-system-packages`

#### Install from APT repositories:

Add APT repositories:

`echo "deb [signed-by=/usr/share/keyrings/pablinet.gpg] https://pablinet.github.io/repo ./" | sudo tee /etc/apt/sources.list.d/pablinet.list`

Upload APT repositories:

`sudo apt update`

Install bool_quetion:

`sudo apt install python-bool-quetion`

### Using the code in Python 3.x
~~~
from bool_quetion import true_false
names = []
reply = True
while reply:
    element = input ('Enter the full name: ')
    names.append(element)
    for name in names:
        print (name)
        reply = true_false('Do you wish to continue?', ['Yes', 'no'])
else:
    reply = True
~~~

It is also possible to customize the error message and highlight the characters that can be entered:
~~~
reply = true_false('Do you wish to continue?', ['Yes', 'no'], True)
reply = true_false('Continue?', ['Yes', 'no'], 'Error Key', True)
~~~
