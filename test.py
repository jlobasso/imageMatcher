import sys
print(sys.argv)
if 'docker' in sys.argv: 
  print (sys.argv[1])