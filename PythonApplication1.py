from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems
from parsivar import POSTagger
import os
import json
import codecs
import collections
import numpy as np
import matplotlib.pyplot as plt
from scipy import special
import math
from scipy import stats
from sklearn.metrics.pairwise import cosine_similarity
from elasticsearch import Elasticsearch
from elasticsearch import helpers

java_path = r"C:\Program Files\Java\jdk-18\bin\java.exe"
os.environ['JAVAHOME'] = java_path
os.environ.setdefault('JAVA_HOME', java_path)
def loadData():
    f = open("files/IR_data_news_12k.json")
    data = json.load(f)
    f.close()
    return data
stopWords =  codecs.open('files\persian-stopwords-master\persian', encoding='utf-8').read().split('\n')
useStopWords = True

my_normalizer = Normalizer()
my_tokenizer = Tokenizer()
my_tagger = POSTagger(tagging_model="wapiti") 
my_stemmer = FindStems()


#{'علی':{Count:3, docs: {8:[0], 9:[0,3]   }   }
#8: 'علی آمد'
#9: 'علی آمد وبا علی رفت '
#{'علی':{Count:3, docs: {8:[0], 9:[0,3] ,tf:{8:..., 9:...}  }   }

class Value:
    Count = 0
    docs = {}
    tf = {}
    def __init__(self):
        self.Count = 0
        self.docs = {}
        self.tf = {}

def addWord(pos, str, docnu,pos_index):# 2  salam 100 {'salam': {Count:2, docs:{100:[5, 2]  }}    }
    a = my_stemmer.convert_to_stem(str)
    if a in pos_index:
        pos_index[a].Count = pos_index[a].Count + 1
        if docnu in pos_index[a].docs:
            pos_index[a].docs[docnu].append(pos)
        else:
            pos_index[a].docs[docnu]=[pos]
    else:
        pos_index[a] = Value()
        pos_index[a].Count = 1
        pos_index[a].docs = {}
        pos_index[a].docs[docnu] = [pos]

def addSenten(str,docnu,pos_index):
    a = my_normalizer.normalize(str)
    b =  my_tokenizer.tokenize_words(a)
    #c = my_tagger.parse(b)
    #d = list(filter(lambda x: (x[1] == "N" or x[1] =="ADJ" ), c)) 
    #e = [col[0] for col in d]
    for x in range(0,len( b)):
        #if c[x][1]=='N' or c[x][1] =="ADJ" or c[x][1] =="PO" or c[x][1] =="FW" or c[x][1] =="PO":
        if useStopWords ==False or b[x] not in stopWords:
            addWord(x,b[x],docnu,pos_index)

def getQuery(str):
    str = str+" ";
    str = str.replace("!", " !").replace("  ", " ") 
    queries = []
    temp = ""
    isq = False
    for a in str:#   !, ...        ", ...   ,''
        if a == '"' and isq == False:
            if temp!='':
                queries.append( ('!' if  temp[0]=='!' else ''    ,temp[1:] if temp[0]=='!' else  temp))
                temp = ""
            isq = True
        elif a == '"' and isq == True:
            queries.append( ('"'    ,temp))
            temp = ""
            isq = False
        elif a == ' ' and isq == False:
            if temp!="":
                queries.append( ('!' if  temp[0]=='!' else ''    ,temp[1:] if temp[0]=='!' else  temp))
                temp = ""
        else:
            temp  = temp + a
    return queries
def searchHelper(foundeddocs, strs):
    for s in strs:
        if s in foundeddocs:
            foundeddocs[s] =foundeddocs[s] +1
        else:
            foundeddocs[s] = 1
def search(str ,pos_index): 
    #salam !iran   "hi ali"
    #[ ('', 'salam'), ('!', 'iran'), ('"', 'hi ali asghar')   ]
    foundeddocs = {}#{salam:12}
    for a in str:
        if a[0]=='':
            a = my_stemmer.convert_to_stem(a[1])
            if a in pos_index:
                y=[]
                #y =  [x for x in pos_index[a[1]].docs]
                for x in pos_index[a].docs:
                    for x2 in pos_index[a].docs[x]:
                        y.append(x)
                searchHelper(foundeddocs, y)
        if a[0]=='"':
            splited = a[1].split();
            if all(x  in pos_index for x in splited):
                indexes = [pos_index[x].docs for x in splited]
                for doc in indexes[0]:
                    startPos =  indexes[0][doc]
                    for start in startPos:
                        ok = True
                        for i in range(len(splited[1:])):
                            if doc not in indexes[i+1] or start+i+1 not in indexes[i+1][doc] :
                                ok = False
                        if ok == True:
                            searchHelper(foundeddocs, [doc])
    for a in str:
        if a[0]=='!':
            if a[1] in pos_index:
                for doc in pos_index[a[1]].docs:
                    if doc in foundeddocs:
                        foundeddocs.pop(doc)
    foundeddocs = sorted(foundeddocs.items(), key=lambda item: item[1],reverse=True)
    return foundeddocs

count = 0;
 
def doHeapsLaw():
    data = loadData()
    count = 0
    total = []
    distinct = []
    for i in data:
        count = count + 1;
        addSenten(data[i]['content'],i)
        if count % 500 == 0:
            distinct.append( len(pos_index))
            total.append( sum(pos_index[v].Count for v in pos_index) )
        if count >= 2000: 
            break
    fig, ax = plt.subplots()
    ax.scatter(total, distinct, linewidth=2, color='r' )
    for i in range(len(total)):
        ax.annotate("("+ str(total[i]) + ", " + str(distinct[i]) + ")" , (total[i], distinct[i]))
    plt.xlabel("total words")
    plt.ylabel("distinct words")
    l1 = [math.log(x) for x in total]
    l2 = [math.log(x) for x in distinct]
    m, b = np.polyfit(
       np.array([math.log(x,10) for x in total]) ,
      np.array ([math.log(x,10) for x in distinct]) , 1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(l1,l2)
    #log(d)=log(k)+β∗log(N)
    #y=β0+β1∗X => β0=log(k),  β1=β
    k = 10**b
    beta = m
    y = [k*  math.pow( x,beta) for x in   total]
    plt.plot(total, y, linewidth=2, color='b' )
    if useStopWords:
        plt.title("Heaps law with StopWords"  + " k="+str(k) + " beta= " + str(beta))
    else:
        plt.title("Heaps law without StopWords" + " k="+str(k) + " beta= " + str(beta))
    plt.show(block=True)
    print(0)

def doZipfLaw():
    data = loadData()
    m = 1000
    for i in r:
        print(data[i[0]]['title'])
    s = np.array([x[1] for x in r[:m]])
    o = []
    x = np.arange(1., len(s)+1)
    
    for i in x:
        o.append(1/i)
    #plt.plot(x, y/max(y), linewidth=2, color='r')
    plt.plot(x, o/max(o), linewidth=2, color='r', label="zipf")
    plt.plot(x, s/max(s), linewidth=2, color='b', label="result")
    if useStopWords:
        plt.title("zipf law vs result, with StopWords")
    else:
        plt.title("zipf law vs result, without StopWords")
    plt.xlabel("#")
    plt.ylabel("normilized")
    plt.legend(loc="upper right")
    
    #plt.hist(s, density=True)
    #plt.plot(x, y/max(y), linewidth=2, color='r')
    plt.grid()
    plt.show(block=True)



def doNormalWay():
    count = 0
    data = loadData()
    if True:
        pos_index = {};
        for i in data:
            #print(data[i])
            count = count + 1;
            #if i == '10':
            #    break;
            addSenten(data[i]['content'],i,pos_index)
            break;


        #y = json.dumps(pos_index, default=vars)
        #f = open("texts.txt", "w")
        #f.write(y)
        #f.close()
    else:
        f = open("texts.txt", "r", encoding='utf-8')
        x = f.read()
        pos_index = json.loads(x)
        for i in pos_index:
            pos_index[i].Count = pos_index[i]['Count'] 
            pos_index[i].Docs = pos_index[i]['Count'] 
        f.close()

    #pos_index =collections.OrderedDict( sorted(pos_index.items(), key=lambda item: item[1].Count,reverse=True));
    #str = json.dumps(pos_index)
    #f = open("count.txt", "w")
    #f.write(str)
    #f.close()
    #addSenten("سلام، سه جمله دوم است.",7)
    #addSenten("سلام، چرا سه اول و دوم است.",8)
    q = getQuery('آسیا')
    r = search(q, pos_index)

    q = getQuery('تحریم آمریکا !ایران')
    r = search(q, pos_index)


    q = getQuery('"کنگره ضدتروریست"')
    r = search(q, pos_index) 
 
    q = getQuery('"تحریم هسته‌ای" آمریکا !ایران')
    r = search(q, pos_index) 
 
    q = getQuery('اورشلیم !صهیونیست')
    r = search(q, pos_index)
    print (r)


def similar(ws, pos_index):
    q = getQuery(ws)
    count = 0
    pos_index2 = {};
    for i in q:
        addSenten(q[count][1],count,pos_index2)
        count = count + 1
    items = {}
    count = 0;
    for i in q: 
        if q[count][1] in pos_index and q[count][1] in pos_index2:
            for x in pos_index[q[count][1]].docs:
                if x in items:
                    items[x] =items[x] + pos_index[q[count][1]].tf[x]
                else:
                    items[x] = pos_index[q[count][1]].tf[x]
        count = count + 1;
    items = sorted(items.items(), key = lambda i: i[1],reverse= True)[:5]
    print(items)#{5:100, 4:50}
    return items
def tfidf(p, n):
    s = 0;
    for i in p.docs:
        s = s + len(p.docs[i])
    for i in p.docs:
        p.tf[i] =(1+math.log(len(p.docs[i]))) * math.log( n/len(p.docs) ) 
    return;
def tfidf_q2():
    pos_index = {};
    count = 0
    data = loadData()

    #data = {
    #        '0':{'content':'سلام مشهد'}, 
    #        '1':{'content':'سلام سلام ایران'},
    #        '2':{'content':' ایران زیبا'},
    #        '3':{'content':' مشهد زیبا'},
    #        }
    for i in data:
        #print(data[i])
        count = count + 1;
        addSenten(data[i]['content'],i,pos_index)
        if count>1000 :
            break
        #if i == '1':
        #    break;
    for i in pos_index:
        tfidf(pos_index[i], len(data))
    i1 = similar('فوتبال',pos_index)
    i2 = similar('گزارش فوتبال',pos_index)
    i3 = similar('قایقران',pos_index)
    i4 = similar('قایقران ایران',pos_index)
    return;



def connect_elasticsearch():
    #_es = Elasticsearch(['http://localhost:8080'], http_auth=('elastic', '123456'))
    _es = Elasticsearch( hosts="http://elastic:123456@localhost:9200/")
    if _es.ping():
        print('Connected')
    else:
        print('Not connect!')
    return _es

def store_record(es_object, index,id, data):
    try:
        outcome = es_object.index(index=index, id=id, document=data)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')



elasticcounter = 0;

def addtoElastic():
    es = connect_elasticsearch()
    data = loadData();
    bulkdata = [{"_index":"mydata1", "_id":col, "_source":{
        'content': my_normalizer.normalize(data[col]['content'])
        }} for col in data]
    r = helpers.bulk(es, bulkdata)
    print(r);


def getresfromelastic():
    data = loadData();
    es = connect_elasticsearch()
    resp = es.search(index="mydata1", query={"query_string": {
        "query":"(اورشلیم) NOT (صهیونیست)"
        }})
    print(resp)


#addtoElastic();
getresfromelastic();
