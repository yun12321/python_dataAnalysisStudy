
import time
import requests
import pymongo

conn=pymongo.MongoClient("mongodb://localhost:27017")
db=conn['yanxuan']
table=db['yanxuan']

def search_keyword(keyword):
    url='https://you.163.com/xhr/search/search.json'
    query={
            "keyword":keyword,
            "page":1
            }
    try:
        res=requests.get(url,params=query).json()
        result=res['data']['directly']['searcherResult']['result']
        product_id=[]
        for r in result:
            product_id.append(r['id'])
        return product_id
    except:
        raise

def details(product_id):
    url='https://you.163.com/xhr/comment/listByItemByTag.json'
    try:
        c_list=[]
        for i in range(1,101):
            query={
                    'itemId':product_id,
                    'page':i
                    }
            res=requests.get(url,params=query).json()
            if not res['data']['commentList']:
                break
            print('爬取第%s页评论'%i)
            commentList=res['data']['commentList']
            c_list.append(commentList)
            time.sleep(1)
            try:
                table.insert_many(commentList)
            except:
                continue
        return c_list
    except:
        raise

if __name__ =="__main__":

    ids=search_keyword('文胸')
    for id in ids:
        details(id)
