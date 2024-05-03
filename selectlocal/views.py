import json
import random
import time
from urllib.parse import quote

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fake_useragent import UserAgent
import re
from lxml import etree
import xlsxwriter as xw
from selectlocal import models
routerss = None;
def gettraveinfo(requset):
    localname = requset.GET["localname"];
    month = requset.GET.get("month");
    days = requset.GET.get("day");
    avgPrice = requset.GET.get("avgPrice");
    actorType = requset.GET.get("actorType");
    tripType = requset.GET.get("tripType");
    ua = UserAgent();
    url = "https://travel.qunar.com/travelbook/list/"+localname+"/hot_heat/1.htm?";
    if month!='':
        url=url+'&month'+str(month);
    if days!='':
        url=url+'&days'+str(days);
    if avgPrice=='':
        url=url+'&avgPrice'+str(avgPrice);
    if actorType=='':
        url=url+'&actorType'+str(actorType);
    if month=='':
        url=url+'&tripType'+str(tripType);
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    content = response.text;
    places2 = re.findall('<a href="/youji/(.*?)">(.*?)<span class="colOrange">(.*?)</span>(.*?)</a>', content);
    SizePage = re.findall('<a data-beacon="click_result_page" href="(.*?)" rel="nofollow">(.*?)</a>', content)
    datas = [];
    number = 1;
    for i in places2:
        data = [];
        flang = 0;
        title = '';
        for j in i:
            if len(j) < 20:
                datal = j;
            else:
                datal = j.split("<")[0];
            if flang > 0:
                title = title + datal;
            else:
                data.append(j);
                # print(j)
                # image1 = re.findall('<a data-beacon="click_result_pic_'+str(number)+'" target="_blank" href="/youji/'+str(j)+'"><img src="(.*?)" alt="攻略图"></a>', content)
                print('<a data-beacon="click_result_pic_'+str(number)+'" target="_blank" href="/youji/'+str(j)+'"><img src="(.*?)" alt="攻略图"></a>')
                number = number + 1;
            flang = flang + 1;
        data.append(title);
        datas.append(data);

    dicty = {};
    dicty["localdata"] = datas;
    dicty["SizePage"] = SizePage[-1][1]
    dirt = json.dumps(dicty,ensure_ascii=False);
    return HttpResponse(dirt);

def save(data,filename):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook('./txt/'+filename+'.xlsx')  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['大标题', '二号标题', '热度','money','二号标题的介绍','照片','照片内容的介绍']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    h = 2  # 从第二行开始写入数据
    dataty = [];
    for i in data:#i是大标题
        for j in data[i]:#j是二号标题
            datajj = [];
            datajj.append(i);
            y = 0;
            for k in j:
                if y==4:
                    for s in j[k]:
                        if j[k][s]=="null":
                            datajj.append(j[k][s]);
                            print(j[k][s]);
                        else:
                            datajj.append(j[k][s][0]);
                            print(j[k][s][0])
                else:
                    if j[k] == "null":
                        datajj.append(j[k]);
                        print(j[k]);
                    else:
                        datajj.append(j[k][0]);
                        print(j[k][0])
                y=y+1;
            row = "A"+str(h);
            worksheet1.write_row(row, datajj)
            h=h+1;
    workbook.close()  # 关闭表

def getHtml(id,element):#这里是将text的数据的数据改变成html方便使用xpath
    if id[1]=="None":
        return "null";
    else:
        html2 = element.xpath('//*[@id="'+id+'"]/div[@class="period_ct"]');
    return html2[0];
def getTwoTitle(listinfo,id,first,element):#使用xpath爬取数据
    dirt = {};

    setHtml_text = etree.tostring(listinfo,encoding='utf-8').decode('utf-8');
    setHtml = etree.HTML(setHtml_text)

    twotitle= setHtml.xpath('//*[@id="'+id[0]+'"]/div[1]/h5[1]/div[1]/text()');#二级标题
    heat = setHtml.xpath('//*[@id="'+id[0]+'"]/div[1]/h5[1]/a[1]/text()');#热度
    money = setHtml.xpath('//*[@id="'+id[0]+'"]/div[1]/h5[1]/div[2]/div[1]/text()');
    twoInfo = setHtml.xpath('//*[@id="'+id[0]+'"]/div[2]/div[1]/div[1]/div[1]/p/text()');#二号标题的介绍
    if len(twotitle)==0:
        twotitle = element.xpath('//*[@id="'+id[0]+'"]/div[1]/h5[1]/div[1]/a[1]/text()');
    if len(heat)==0:
        heat = "null";
    if len(money)==0:
        money = "null";
    if len(twoInfo)==0:
        twoInfo = "null";
    imgdatas = getiImgInfo(id[0],element);
    # print(imgdatas)
    # print(first,twotitle,heat,money,twoInfo);
    # print("----------------------------------------------------------------------------------------\n\n\n");
    if(len(twotitle)==0 and heat=="null" and money=="null" and twoInfo=="null"):
        return 0
    else:
        dirt["twotitle"] = twotitle;
        dirt["heat"] = heat;
        dirt["money"] = money;
        dirt["twoInfo"] = twoInfo;
        dirt[twotitle[0]]=imgdatas;
    return dirt;

def getiImgInfo(id,element):
    imgInfoDirt = {};
    i=1
    while True :
        imgs=element.xpath('//*[@id="'+id+'"]/div[2]/div[1]/div[1]/dl['+str(i)+']/dt[1]/img[1]/@data-original');#照片
        imginfo = element.xpath('//*[@id="'+id+'"]/div[2]/div[1]/div[1]/dl['+str(i)+']/dd[1]/div[1]/p/text()');#照片内容的介绍
        imgsname = "img"+str(i);
        imginfoname = "imginfo"+str(i);
        if (len(imgs) == 0):
            imgs="null";
        if (len(imginfo) == 0):
            imginfo = "null";
        if( imgs=="null" and imginfo=="null"):

            return imgInfoDirt;
        else:
            imgInfoDirt[imgsname] = imgs;
            imgInfoDirt[imginfoname] = imginfo;
        i=i+1;

def getonetrave(requset):
    localId = requset.GET.get("localId");
    datasDirt = {};
    ua = UserAgent();
    url = "https://travel.qunar.com/travelbook/note/"+str(localId);
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    content = response.text;
    response.encoding = 'utf-8';
    html = response.text;
    element = etree.HTML(html)
    eleids = re.findall(
        '<div class="b_poi_info b_poi_item" id="(.*?)" data-poitype="(.*?)"  poi-id="(.*?)"  data-dist-id="(.*?)" element-type=event>',
        content);
    ids = re.findall('<div id="(.*?)" data-dayidx="(.*?)" class="(.*?)>', content);
    booktitle = element.xpath('//*[@id="booktitle"]/text()')[0];
    setcode = len(ids) - 1;
    lengs = len(eleids) - 1;
    for i in range(len(ids)):
        titleBigs = element.xpath('//*[@id=' + '"' + str(ids[setcode][1]) + '"' + ']/h4[1]/dl[1]/dt[1]/div[2]/text()');
        datas = [];
        htmlh = getHtml(ids[setcode][1],element);
        lengt = 0;
        for eleid in eleids:

            endnum = getTwoTitle(htmlh, eleids[lengs], titleBigs,element);
            if endnum == 0:
                datasDirt[titleBigs[0]] = datas;
                break;
            else:
                lengs = lengs - 1;
                datas.insert(0, endnum);
            if lengs == -1:
                break;
        setcode = setcode - 1;
        if len(datas) > 0:
            datasDirt[titleBigs[0]] = datas;
    # dicty = {};
    # dicty["localdata"] = datasDirt;
    dirt = json.dumps(datasDirt, ensure_ascii=False);
    return HttpResponse(dirt);
    # save(datasDirt, booktitle);
@csrf_exempt
def saveTable_name(requset):
    message =None;
    code = 200;
    dicty = {};
    try:
        username = requset.GET.get('username');
        bornyear = requset.GET.get("bornyear");
        bornmonth = requset.GET.get("bornmonth");
        bornday = requset.GET.get("bornday");
        hobby = requset.GET.get("hobby");
        sex = requset.GET.get("sex");
        image = requset.GET.get("image");
        place = requset.GET.get("place");
        user_info = models.TableName(username=username, bornyear=bornyear, bornmonth=bornmonth, bornday=bornday,
                                     hobby=hobby, sex=sex, image=image, place=place);
        user_info.save();
    except Exception:
        message="输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code =200;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;
def searchTable_name(requset):
    message = None;
    code = 200;
    dicty = {};
    data ={};
    try:
        username = requset.GET.get("username");
        user_obj = models.TableName.objects.filter(username=username).first();
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        data["id"] = user_obj.id;
        data["username"] = user_obj.username;
        data["bornyear"] = user_obj.bornyear;
        data["bornmonth"] = user_obj.bornmonth;
        data["bornday"] = user_obj.bornday;
        data["place"] = user_obj.place;
        data["image"] = user_obj.image;
        data["sex"] = user_obj.sex;
        data["hobby"] = user_obj.hobby;
        dicty["message"] = message;
        dicty["code"] = code;
        dicty["data"] = data;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;
def upDateTable_name(requset):
    message = None;
    code = 200;
    dicty = {};
    data ={};
    try:
        id = requset.GET.get('id');
        username = requset.GET.get('username');
        bornyear = requset.GET.get("bornyear");
        bornmonth = requset.GET.get("bornmonth");
        bornday = requset.GET.get("bornday");
        hobby = requset.GET.get("hobby");
        sex = requset.GET.get("sex");
        image = requset.GET.get("image");
        place = requset.GET.get("place");
        user_obj = models.TableName.objects.filter(id=int(id)).update(username=username, bornyear=bornyear, bornmonth=bornmonth, bornday=bornday,hobby=hobby, sex=sex, image=image, place=place);
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        dicty["message"] = message;
        dicty["code"] = code;
        dicty["data"] = data;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;

def saveAccoutinfo(requset):
    message =None;
    code = 200;
    dicty = {};
    try:
        username = requset.GET.get('username');
        account = requset.GET.get("account");
        password = requset.GET.get("password");
        user_info = models.Accoutinfo(username=username, account=account, password=password);
        user_info.save();
    except Exception:
        message="输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code =200;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;
def searchAccoutinfo(requset):
    message = None;
    code = 200;
    dicty = {};
    data ={};
    try:
        username = requset.GET.get("username");
        user_obj = models.Accoutinfo.objects.filter(username=username).first();

        print(user_obj.id,user_obj.username,user_obj.account,user_obj.password);
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        data["id"] = user_obj.id;
        data["username"] = user_obj.username;
        data["account"] = user_obj.account;
        data["password"] = user_obj.password;
        dicty["code"] = code;
        dicty["data"] = data;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;
def upDateAccoutinfo(requset):
    message = None;
    code = 200;
    dicty = {};
    data ={};
    try:
        id = requset.GET.get('id');
        username = requset.GET.get('username');
        account = requset.GET.get("account");
        password = requset.GET.get("password");
        user_obj = models.TableName.objects.filter(id=int(id)).update(username=username, account=account,password=password);
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        dicty["message"] = message;
        dicty["code"] = code;
        dicty["data"] = data;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;

def searchall(requset):
    all = models.wantGo.objects.all();
    message = "成功";
    code = 200;
    dicty = {};
    datas=[];
    data={};
    dicty["message"] = message;
    dicty["code"] = code;
    j = 1;
    for i in all:
        data["cityId"+str(j)] = i.cityId;
        data["imgUrl"+str(j)] = i.imgUrl;
        data["cityName"+str(j)] = i.cityName;
        data["selectId"+str(j)] = i.selectId;
        j=j+1;
        print(data)
    datas.append(data);
    dicty["datas"] = datas;
    dirt = json.dumps(dicty, ensure_ascii=False);
    return HttpResponse(dirt);

def SaveCityPonitDef(name,url):
    try:
        ua = UserAgent();
        headers = {"User-Agent": ua.random};
        response = requests.get(url=url, headers=headers);
        response.encoding = 'utf-8';
        content = response.text;
        datass = re.findall(
            '<a title="(.*?)" data-beacon="hotline_poi" href="(.*?)" target="_blank" class="link">(.*?)</a>', content);
        datas = [];
        for i in datass:
            if (i[2] in datas):
                pass;
            else:
                datas.append(i[2]);
            # print(i[2]);
        stt = '';
        for i in datas:
            stt = stt + i + ',';
        HotelPoints = stt[0:len(stt) - 1];
        infouser = models.CityTepyFour(HotelPoints = HotelPoints,cityName = name);
        infouser.save();
        print("**************************************************************************************************\n")
    except Exception:
        print(Exception);
    finally:
        pass;


def getImg(url):
    ua = UserAgent();
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    img = re.findall('<img src="(.*?)" alt="(.*?)" style="(.*?)">',content);
    # print(img[0][0])
    return img[0][0];
def getcontrol(url):
    ua = UserAgent();
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    img = re.findall('<img src="(.*?)" alt="(.*?)" style="(.*?)">', content);
    return img[0][0];
def saveCity(requset):
    ua = UserAgent();
    url = "https://travel.qunar.com/place/";
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    placesAll = re.findall('<li class="item "><a href="(.*?)" class="link" target="_blank">(.*?)</a></li>', content);
    message = None;
    code = 200;
    dicty = {};
    dict = {};
    datasw = [];
    datash = [];
    j=1;
    try:
        for i in placesAll:
            if (j%3==0):
                datash.append(datasw);
                datasw.clear();
            imgUrl = getImg(i[0]);
            cityName = i[1];
            dict["cityId"] = j;
            j+=1;
            dict["selectId"] = 0;
            dict["imgUrl"] = imgUrl;
            dict["cityName"] = cityName;
            datasw.append(dict);
            user_info = models.City(imgUrl=imgUrl, cityName=cityName,);
            user_info.save();
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dicty["datash"] = datash;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        dicty["message"] = message;
        dicty["code"] = code;
        dicty["datash"] = datash;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;
def searchCityall(requset):
    currentPage = requset.GET.get("currentPage");
    pageSize = requset.GET.get("pageSize");
    first = (int(currentPage)-1)*int(pageSize);
    endl = int(pageSize)*int(currentPage);
    all = models.City.objects.all()[first:endl];
    message = "成功";
    code = 200;
    dicty = {};
    datas = [];
    datasj = [];
    dicty["message"] = message;
    dicty["code"] = code;
    j = 0;
    for i in all:
        data = {};
        data["cityId"] = i.Id;
        data["imgUrl"] = i.imgUrl;
        data["cityName"] = i.cityName;
        data["selectId"] = i.selectId;
        datas.append(data);
        if (j % 3 == 2):
            datasj.append(datas)
            datas=[];

        j=j+1;
    dicty["data"] = datasj;
    dirt = json.dumps(dicty, ensure_ascii=False);
    return HttpResponse(dirt);


def getco(url,cityName,index):
    try:
        moneys = [250, 455, 488, 999, 200, 1588, 1622, 0];
        ua = UserAgent();
        headers = {"User-Agent": ua.random};
        response = requests.get(url=url, headers=headers);
        response.encoding = 'utf-8';
        content = response.text;
        element = etree.HTML(content)
        for i in range(1,6):
            Hotelfimg = element.xpath('//*[@id="hotel_filter"]/div[2]/ul[1]/li['+str(i)+']/a[1]/img[1]/@src')[0];
            HotelName = element.xpath('//*[@id="hotel_filter"]/div[2]/ul[1]/li['+str(i)+']/div[1]/div[1]/a[1]/text()')[0];
            Hotelfherf = element.xpath('//*[@id="hotel_filter"]/div[2]/ul[1]/li['+str(i)+']/div[1]/div[1]/a[1]/@href')[0];
            Hotelsytype = element.xpath('//*[@id="hotel_filter"]/div[2]/ul[1]/li['+str(i)+']/div[1]/div[2]/text()')[0];
            Hotelslocal = element.xpath('//*[@id="hotel_filter"]/div[2]/ul[1]/li['+str(i)+']/div[1]/div[2]/text()')[1];
            Hotelsscore = 5.0
            Hotelsmoney = moneys[index];
            cityTip = '服务好,性价比高,西站附近住宿推荐清明节去北京,晚上高铁到的比较晚';
            user_info = models.Hotel(Hotelfimg=Hotelfimg, cityName = cityName,HotelName=HotelName, Hotelfherf=Hotelfherf, Hotelsytype=Hotelsytype,
                                             Hotelslocal=Hotelslocal, Hotelsscore=Hotelsscore, Hotelsmoney=Hotelsmoney, cityTip=cityTip);
            user_info.save();

    except Exception:
        print(Exception);
        print("**************************************************************************************************\n")
    else:
        pass
    finally:
        return  None;



def saveHotel(requset):
    ua = UserAgent();
    url = "https://travel.qunar.com/place/";
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    placesAll = re.findall('<li class="item "><a href="(.*?)" class="link" target="_blank">(.*?)</a></li>', content);

    for i in placesAll:
        urls = i[0] + '-jiudian';
        c = random.randint(0, 7)
        getco(urls, i[1], c)

def saveCityPonit(requset):
    ua = UserAgent();
    url = "https://travel.qunar.com/place/";
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    placesAll = re.findall('<li class="item "><a href="(.*?)" class="link" target="_blank">(.*?)</a></li>', content);
    for i in placesAll:
        print(i[1],i[0])
        SaveCityPonitDef(i[1], i[0]);

def searchCityPonit(requset):
    message = None;
    code = 200;
    dicty = {};
    data = [];
    try:
        cityName = requset.GET.get("cityname");
        user_obj = models.CityTepyFour.objects.filter(cityName=cityName).first();
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        data = user_obj.HotelPoints.split(',')
        dicty["code"] = code;
        dicty["data"] = data;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;

router = None;
def getxxruter(url,cityName):
    ua = UserAgent();
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    html = response.text;
    element = etree.HTML(html)
    content = response.text;
    topInfo = re.findall( '"routebox (.*?)" id="(.*?)"><div class="hd_box"><div class="titbox"><span class="tit">(.*?)</span></div><div class="desbox"><div class="des">(.*?)</div><div class="d_note">(.*?)</div></div></div>',content)
    datass = [];
    try:
        for w in topInfo:
            ids = w[1];
            days = int(w[2].split("日")[0][-1]);
            for i in range(1, days + 1):
                localtions = element.xpath(
                    '//*[@id="' + ids + '"]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[1]/span[1]/span[1]/text()')[0];
                timess = \
                element.xpath('//*[@id="' + ids + '"]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[1]/div[1]/text()')[0];
                router = element.xpath(
                    '//*[@id="' + ids + '"]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[1]/span[1]/a/text()');
                for k in router:
                    time.sleep(2);
                    # print(k)
                    getcityinfo(k);
            print("*********************************************************************\n");
    except Exception as e:
        try:
            for k in router:
                time.sleep(2);
                # print(k)
                getcityinfo(k);
        except Exception as e:
            print(e);

def getcityinfo(poinitName):
   try:
       cityName11 = poinitName;
       poinitName = quote(poinitName, encoding='utf-8')
       url = 'https://travel.qunar.com/search/place/'+str(poinitName);
       print(url)
       ua = UserAgent();
       headers = {"User-Agent": ua.random};
       response = requests.get(url=url, headers=headers);
       response.encoding = 'utf-8';
       html = response.text;
       content = response.text;
       reasons = re.findall('<div class="d_brief"><span class="b">简介：</span>(.*?)</div>', content)[0];
       cityimg = re.findall('<a target="_blank" data-beacon="placeResult_1" href="(.*?)" class="d_img"><img src="(.*?)"/></a>', content)[0];
       timers = re.findall('<div class="d_days">(.*?)</div>', content)[0];
       user_obj = models.CityTepyFour.objects.filter(cityName=cityName11).first();
       if(user_obj==None):
           user_info = models.Pointss(cityName=cityName11, reasons=reasons, score='5', timers=timers,
                                      cityimg=cityimg);
           user_info.save();
       else:
           pass;
   except Exception as e:
       print(e)

def savePointss(requset):
    ua = UserAgent();
    url = "https://travel.qunar.com/place/";
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    placesAll = re.findall('<li class="item "><a href="(.*?)" class="link" target="_blank">(.*?)</a></li>', content);
    for i in placesAll:
        urll = i[0] + '-xianlu'
        getxxruter(urll, i[1]);

def getcityserc(url):
    ua = UserAgent();
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    html = response.text;
    element = etree.HTML(html)
    content = response.text;
    topInfo = re.findall( '"routebox (.*?)" id="(.*?)"><div class="hd_box"><div class="titbox"><span class="tit">(.*?)</span></div><div class="desbox"><div class="des">(.*?)</div><div class="d_note">(.*?)</div></div></div>',content)
    try:
        for w in topInfo:
            ids = w[1];
            days = int(w[2].split("日")[0][-1]);
            routerdays = days;
            routerdaysName = w[2];
            for i in range(1, days + 1):
                cityName = element.xpath(
                    '//*[@id="' + ids + '"]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[1]/span[1]/span[1]/text()')[0];
                timess = \
                element.xpath('//*[@id="' + ids + '"]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[1]/div[1]/text()')[0];
                router = element.xpath(
                    '//*[@id="' + ids + '"]/div[2]/div[1]/div[1]/div[' + str(i) + ']/div[1]/span[1]/a/text()');
                routerss = '';
                for w in router:
                    routerss = routerss + '->' + w;
                routerss = routerss[2:len(routerss)];
                user_info = models.Cityserc(cityName=cityName, routerss=routerss, timess=timess,routerdays = routerdays,routerdaysName = routerdaysName);
                user_info.save();
                time.sleep(2)
            print("*********************************************************************\n");
    except Exception as e:
        try:
            print(e)
        except Exception as e:
            print(e);

def savecityserc(requset):
    ua = UserAgent();
    url = "https://travel.qunar.com/place/";
    headers = {"User-Agent": ua.random};
    response = requests.get(url=url, headers=headers);
    response.encoding = 'utf-8';
    content = response.text;
    placesAll = re.findall('<li class="item "><a href="(.*?)" class="link" target="_blank">(.*?)</a></li>', content);
    for i in placesAll:
        urll = i[0] + '-xianlu'
        getcityserc(urll);

def searchCityserc(requset):
    message = None;
    code = 200;
    dicty = {};
    try:
        cityName = requset.GET.get("cityName")+'：';
        routerdays =requset.GET.get("routerdays");
        user_obj = models.Cityserc.objects.filter(cityName=cityName,routerdays=routerdays)[:int(routerdays)];
    except Exception:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    else:
        message = "成功";
        code = 200;
        datash = [];
        if(user_obj!=None):

            for i in user_obj:
                w = 0;
                datayy = [];
                data = {};
                data["id"] = i.Id;
                data["cityName"] = i.cityName;
                data["timess"] = i.timess;
                data["routerss"] = i.routerss;
                data["routerdays"] = i.routerdays;
                data["routerdaysName"] = i.routerdaysName;

                ss = i.routerss.split("->");
                for j in ss:
                    # print(j);
                    datasjday = searchPointss(j,w);
                    datayy.append(datasjday);
                w+=1;
                data["datayy"] = datayy;
                datash.append(data);

        dicty["message"] = message;
        dicty["code"] = code;
        dicty["data"] = datash;
        dirt = json.dumps(dicty, ensure_ascii=False);
        print(dirt)
        return HttpResponse(dirt);
    finally:
        pass;

def searchPointss(cityName,day):
    message = None;
    code = 200;
    dicty = {};
    data = {};
    dayss = ["第一天","第二天","第三天","第四天","第五天","第六天","第七天","第八天","第九天","第十天"];
    try:
        cityName = cityName;
        user_obj = models.Pointss.objects.filter(cityName=cityName).first();
    except Exception:

        return None;
    else:
        if (user_obj != None):
            data["id"] = user_obj.Id;
            data["cityName"] = user_obj.cityName;
            data["reasons"] = user_obj.reasons;
            data["score"] = user_obj.score;
            data["timers"] = user_obj.timers;
            cityimg = user_obj.cityimg.split(",")[1]
            data["cityimg"] = user_obj.cityimg.split(",")[1][0:len(cityimg)-2].split("'")[1];
            data["dayss"] = dayss[day];
        # print(data);
        return data;
    finally:
        pass;

def saveuserhh(requset):
    try:
        message = None;
        code = 200;
        dicty = {};
        data = {};
        username = requset.GET.get("username");
        accout = requset.GET.get("accout");
        passwords = requset.GET.get("passwords");
        phone = requset.GET.get("phone");
        userImg = requset.GET.get("imgdata");
        sex = requset.GET.get("accout");
        rotue = 0;
        frinds = 0;
        coommit = 0;
        love = 0;
        user_info = models.userhh(username=username, accout=accout, passwords=passwords, phone=phone,
                                 userImg=userImg,love=love,
                                 sex=sex, rotue=rotue, frinds=frinds,
                                 coommit=coommit);
        user_info.save();
    except Exception as e:
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
        print(e)
    else:
        message = "成功";
        code = 200;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:
        pass;

def searchuserhh(requset):
    try:
        message = None;
        code = 200;
        dicty = {};
        data = {};
        accout = str(requset.GET.get("accout"));
        passwords = str(requset.GET.get("passwords"));
        user_obj = models.userhh.objects.filter(accout=accout, passwords=passwords).first();
    except Exception as e:
        print(e)
        message = "输入的数据错误";
        code = 500;
        dicty["message"] = message;
        dicty["code"] = code;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);

    else:
        message = "成功";
        code = 200;
        data["id"] = user_obj.Id;
        data["username"] = user_obj.username;
        data["accout"] = user_obj.accout;
        data["passwords"] = user_obj.passwords;
        data["phone"] = user_obj.phone;
        data["userImg"] = user_obj.userImg;
        data["sex"] = user_obj.sex;
        data["personaltypy"] = user_obj.personaltypy;
        data["rotue"] = user_obj.rotue;
        data["frinds"] = user_obj.frinds;
        data["coommit"] = user_obj.coommit;
        data["love"] = user_obj.love
        dicty["message"] = message;
        dicty["code"] = code;
        dicty["data"]=data;
        dirt = json.dumps(dicty, ensure_ascii=False);
        return HttpResponse(dirt);
    finally:pass;



