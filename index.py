#coding:utf-8
from flask import Flask,render_template,request,url_for,redirect,g,session
from urllib2 import urlopen
import json,time
SECRET_KEY = "hello world"
app = Flask(__name__)
app.config.from_object(__name__)



def getUrl(c, m):
    url = "game.baozouwushuang.com/index.php?c="+c+"&m="+m
    return url



def getUid(username,password):
    url = "http://uc."+getUrl("user", "login")+"&u="+username+"&p="+password
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    print(content['message'])    
    return content['uid']


def getToken(username, password):
    url = "http://s20."+getUrl("login", "user")+"&u="+username+"&p="+password
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    return content['token'] 

def getInfo(token):
    info = {}
    url = "http://s20."+getUrl("member", "index")+"&token="+token
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    info["act"] = content["act"]
    info["gold"] = content["gold"]
    info["silver"] = content["silver"]
    info["levy"] = content["levy"]["times"]
    session["levy"] = info["levy"]
    print(info)
    return info

def levact(times, token):
    url = "http://s20."+getUrl("city", "impose")+"&token="+token
    for i in range(1, times+1):
        request = urlopen(url).read().decode('utf-8')
        content = json.loads(request)
        print("第%d次征收增加了%d银币,同时获得%s" % (i, content["silver"], content['treasuremap']))
        time.sleep(0.5)

def vipWage(token):
    url = "http://s20."+getUrl("vipwage", "get_vip_wage")+"&token="+token
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    print("领取vip每日奖励")


def island(token, counts):
    url = "http://s20."+getUrl("island", "index")+"&token="+token
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    lasturl = ""
    for i in range(len(content['list'])):
        time.sleep(0.4)
        if(content['list'][i]['killed']==0):
            new_url = "http://s20."+getUrl("island", "pk")+"&token="+token+"&id="+content['list'][i]['id']
            lasturl = new_url
            urlopen(new_url)
            print("金银洞征战中")
    lasturl = "http://s20."+getUrl("island", "pk")+"&token="+token+"&id="+content['list'][4]['id']
    for x in range(counts):
        time.sleep(0.4)
        urlopen(lasturl)
        print("金银洞征战中")

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'cnooc1' and request.form['password'] == 'daichenjian':
            session['uid'] = getUid(request.form['username'],request.form['password'])
            session['token'] = getToken(request.form['username'],request.form['password'])
            return redirect('show_info')            
    return render_template('index.html')


def business(token):
    url = "http://s20."+getUrl("business", "index")+"&token="+token
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)   
    times = int(content['times'])
    for i in range(times):
        time.sleep(0.6)
        new_url = "http://s20."+getUrl("business", "go_business")+"&token="+token+"&id="+str(content['trader'][1]['id'])
        request = urlopen(new_url).read().decode('utf-8')
        content = json.loads(request)

def drink(token):
    url = "http://s20."+getUrl("drink", "go_drink")+"&token="+token+"&type=1"
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    
def sanctum(token):
    url = "http://s20."+getUrl("sanctum", "action")+"&token="+token+"&id=50&num=10"
    urlopen(url)


def sanctum_daily(token):
    url = "http://s20."+getUrl("sanctum", "get_reward")+"&token="+token+"&type=1&multiple=0"
    urlopen(url)


def lottery(token):
    url = "http://s20."+getUrl("lottery", "index")+"&token="+token
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    return content['log']['info']['total_num']

def get_lotteries(token):
    url = "http://s20."+getUrl("lottery", "action")+"&token="+token
    for i in range(lottery(token)):
        request = urlopen(url).read().decode('utf-8')
        content = json.loads(request)
  

def hitegg(token):
    url = "http://s20."+getUrl("hitegg", "index")+"&token="+token
    request = urlopen(url).read().decode('utf-8')
    content = json.loads(request)
    for i in range(len(content['list'])):
        if(content['list'][i]['cd']==0):
            egg_url = "http://s20."+getUrl("hitegg", "hit_egg")+"&token="+token+"&id="+str(i+1)
            urlopen(egg_url)
        else:
            print("no egg")








@app.route('/show_info')    
def show_info():
    uid = session['uid']
    token = session['token']
    infolist = getInfo(token)
    return render_template('show.html',uid=uid,token=token,infolist=infolist)
    
@app.route('/update')
def update():
    infolist = getInfo(session['token'])
    return redirect('show_info')

@app.route('/levy')
def levy():
    levact(int(session["levy"]), session['token'])
    return redirect('show_info')

@app.route('/vipwage')
def vipwage():
    vipWage(session['token'])
    return redirect('show_info')

@app.route('/land')
def land():
    island(session['token'], 5)
    return redirect('show_info')
    
@app.route('/get_drink')
def get_drink():
    drink(session['token'])
    return redirect('show_info')  

    
@app.route('/get_business')
def get_business():
    business(session['token'])
    return redirect('show_info')
    
@app.route('/get_lottery')
def get_lottery():
    get_lotteries(session['token'])
    return redirect('show_info')  
    
@app.route('/get_sixiang')
def get_sixiang():
    sanctum_daily(session['token'])
    sanctum(session['token'])
    return redirect('show_info')  
    
    
@app.route('/get_hitegg')
def get_hitegg():
    hitegg(session['token'])
    return redirect('show_info')  
    
    
    


app.run(host='0.0.0.0')
