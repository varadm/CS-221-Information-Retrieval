import redis
pr_client = redis.StrictRedis(host='localhost', port=6379, db=12)

f = open('id_title.txt', 'r')
for line in f:
    val = line.split(',')
    v1 = int(val[0])
    v2 = val[1].strip()
    pr_client.set(v1, v2)
    #print 'Done for ' + str(v1) + ' ' + v2

    
    

