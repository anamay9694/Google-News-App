
from flask import Flask,jsonify
from newsapi import NewsApiClient
import json
import string

app = Flask(__name__)

newsapi = NewsApiClient(api_key='1a11b7ddc4a44b658602017c65832ce9')

stopwords_file=open('stopwords_en.txt','r')
li_temp=stopwords_file.readlines()
stopWords=[z.replace('\n','') for z in li_temp]




@app.route('/getSources/<Category>')
def getSources(Category=None):
    if Category=="all":
        sources= newsapi.get_sources(language='en',country='us')
    else:
        sources = newsapi.get_sources(category=Category,language='en',country='us')
    unique_sources_list_id=[]
    unique_sources_list_name=[]
    
    unique_sources_id=set()
    for ele in sources["sources"]:
        if ele["id"] not in unique_sources_id:
            unique_sources_id.add(ele["id"])
            unique_sources_list_id.append(ele["id"])
            unique_sources_list_name.append(ele["name"])
    sources_dict={}
    
    sources_dict["IDS"]=unique_sources_list_id
    sources_dict["Names"]=unique_sources_list_name
    
    rootDict={}
    rootDict["Sources"]=sources_dict
    return rootDict
    
    
@app.route('/getCards/<qu>/<From>/<To>/<source>')
def getCards(qu,From,To,source): 
    top15_cards={}
    top15_cards["TopCards"]=[]
    try:
        if source=="all":
            response = newsapi.get_everything(q=qu,
                                          from_param=From,
                                          to=To,
                                          language='en',
                                          sort_by='publishedAt',
                                          page_size=30)
        else:
            response = newsapi.get_everything(q=qu,
                                         sources=source,
                                          from_param=From,
                                          to=To,
                                          language='en',
                                          sort_by='publishedAt',
                                          page_size=30)
    except Exception as exception:
        if (type(exception).__name__ )== "NewsAPIException":
            top15_cards["Error"]=exception.args[0]['message']
        else:
            top15_cards["Error"]="Error retriving the results"
        return top15_cards
        
    top15_cards["Error"]="200"
    count=0
    for ele in response["articles"]:
        if ele["author"] != None and ele["author"]!="null" and ele["content"]!=None and ele["content"]!="null" and ele["description"] !=None and ele["description"] !="null" and ele["publishedAt"]!=None and ele["publishedAt"]!="null":
            if ele["title"]!=None and ele["title"]!="null" and ele["url"]!=None and ele["url"]!="null" and ele["urlToImage"]!=None and ele["urlToImage"]!="null" and ele["source"]["id"]!=None and ele["source"]["id"]!="null" and ele["source"]["name"]!=None and ele["source"]["name"]!="null":
                count+=1
                top15_cards["TopCards"].append(ele)
                if count==15:
                    break
    return top15_cards
@app.route('/getTopWords')
def getTopWords():
    top_response=newsapi.get_top_headlines(language='en',
                                          country='us',
                                          page=2)
    
     
    obj_response=top_response
    list_headings=[ e["title"] for e in obj_response["articles"] ]
    
    map_string_int={}
    
    exclude = set(string.punctuation)
    for i in list_headings:
        heading_string=i.split()
        for j in heading_string:
            j=''.join(ch for ch in j if ch not in exclude)
            if j.lower() not in stopWords and len(j)!=0:
                if j.lower() not in map_string_int:
                    map_string_int[j.lower()]=1
                else:
                    map_string_int[j.lower()]+=1
                    
    
     
    sorted(map_string_int.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
     
    
    counter=0
    newdict={}
    newdict["TopWords"]=[]
    for k in sorted(map_string_int.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
        #print(k)
        counter+=1
        if counter==31:
            break
        tempDic={}
        tempDic["text"]=k[0]
        tempDic["size"]=k[1]
        newdict["TopWords"].append(tempDic)
    
    json_str=json.dumps(newdict)
    return json_str

@app.route('/getTopHeadlines')
def getTopHeadlines():
    top_response=newsapi.get_top_headlines(language='en',
                                          country='us',
                                          page_size=50)
    top5_headlines={}
    top5_headlines["TopHeadlines"]=[]
    count=0
    for ele in top_response["articles"]:
        if ele["author"] != None and ele["author"]!="null" and ele["content"]!=None and ele["content"]!="null" and ele["description"] !=None and ele["description"] !="null" and ele["publishedAt"]!=None and ele["publishedAt"]!="null":
            if ele["title"]!=None and ele["title"]!="null" and ele["url"]!=None and ele["url"]!="null" and ele["urlToImage"]!=None and ele["urlToImage"]!="null" and ele["source"]["id"]!=None and ele["source"]["id"]!="null" and ele["source"]["name"]!=None and ele["source"]["name"]!="null":
                count+=1
                top5_headlines["TopHeadlines"].append(ele)
                if count==5:
                    break
    return top5_headlines

@app.route('/getTopHeadlinesCNN')
def getTopHeadlinesCNN():
    top_response = newsapi.get_top_headlines(
                                          sources='cnn',
                                          language='en')
     
    top4_headlines={}
    top4_headlines["TopHeadlines"]=[]
    count=0
    for ele in top_response["articles"]:
        if ele["description"] !=None and ele["description"] !="null":
            if ele["title"]!=None and ele["title"]!="null" and ele["url"]!=None and ele["url"]!="null" and ele["urlToImage"]!=None and ele["urlToImage"]!="null" and ele["source"]["id"]!=None and ele["source"]["id"]!="null" and ele["source"]["name"]!=None and ele["source"]["name"]!="null":
                count+=1
                top4_headlines["TopHeadlines"].append(ele)
                if count==4:
                    break
    return top4_headlines

@app.route('/getTopHeadlinesFox')
def getTopHeadlinesFox():
    top_response = newsapi.get_top_headlines(
                                          sources='fox-news',
                                          language='en')
    top4_headlines={}
    top4_headlines["TopHeadlines"]=[]
    count=0
    for ele in top_response["articles"]:
        if ele["author"] != None and ele["author"]!="null" and ele["content"]!=None and ele["content"]!="null" and ele["description"] !=None and ele["description"] !="null" and ele["publishedAt"]!=None and ele["publishedAt"]!="null":
            if ele["title"]!=None and ele["title"]!="null" and ele["url"]!=None and ele["url"]!="null" and ele["urlToImage"]!=None and ele["urlToImage"]!="null" and ele["source"]["id"]!=None and ele["source"]["id"]!="null" and ele["source"]["name"]!=None and ele["source"]["name"]!="null":
                count+=1
                top4_headlines["TopHeadlines"].append(ele)
                if count==4:
                    break
    return top4_headlines

@app.route('/')
def getNews():
    return app.send_static_file('getNewsApp.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
