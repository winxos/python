#-------------------------------------------------------------------------------
# Name:        using file method to print self.
# Author:      winxos
# Created:     27/03/2011
# Copyright:   (c) winxos 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import os
def main():
	f=open("ptself.py","r")
	print(f.read())
	f.close()
if __name__ == '__main__':
    main()
