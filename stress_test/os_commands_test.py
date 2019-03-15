import commands


status, output = commands.getstatusoutput('ab -n 100 -c 10 -p login.json -T application/json "http://localhost:5000/login"')
print status, output

status, output = commands.getstatusoutput('ab -n 100 -c 10 "http://localhost:5000/Project/List"')
print status, output