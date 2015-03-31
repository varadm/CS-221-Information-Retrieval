import redis
pr_client = redis.StrictRedis(host='localhost', port=6379, db=15)

f = open('Page_Rank.txt', 'r')
for line in f:
    val = line[1:len(line)-2].split(',')
    v1 = int(val[0])
    v2 = float(val[1])
    pr_client.set(v1, v2)
    print 'Done for' + str(v1)
    
    

