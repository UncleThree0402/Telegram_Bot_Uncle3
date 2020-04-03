import telegram
from telegram import  ReplyKeyboardMarkup, ReplyKeyboardRemove
import urllib.request
import json
from time import sleep
from cs50 import SQL
import datetime
import bs4 as bs

db = SQL("sqlite:///Tg_Bot.db")

f = open("token.txt", "r")
BOT_TOKEN = f.readline()
Bot = telegram.Bot(BOT_TOKEN)

a = open("good.txt", "r")
Good = a.read()

lastMessageID = 0



def getText(Update):
    return Update["message"]["text"]

def getID(Update):
    return Update["update_id"]

def getChatId(Update):
    return Update["message"]["chat"]["id"]

def getUserId(Update):
    return Update["message"]["from_user"]["id"]

def pressnull(Update):
    db.execute("UPDATE TG_BOT SET press = :text WHERE Chat_id = :chat_id",text = "NULL", chat_id = getChatId(Update))

def forecast(Update):
    URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    pressnull(Update)
    Update.message.reply_text('天氣概況\n' + Results["generalSituation"] + "\n" + Results["forecastPeriod"]
                              + '\n' + Results["forecastDesc"] +'\n' + '展望:' +'\n' + Results["outlook"])
    Weather(Update)

def nineforecast(Update):
    URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    Results = Results["weatherForecast"]
    pressnull(Update)
    String = ""
    for i in range(len(Results)):
        String += (str(Results[i]["week"]) + "\n" + "吹" + str(Results[i]["forecastWind"])
               + "\n" + "天氣係" + str(Results[i]["forecastWeather"]) + "最高氣溫"
               + str(Results[i]["forecastMaxtemp"]["value"]) + "°C，" + "最低氣溫"
               + str(Results[i]["forecastMintemp"]["value"])+ "°C，"+ "相對濕度"
               + str(Results[i]["forecastMinrh"]["value"]) + "%" + "-"
               + str(Results[i]["forecastMaxrh"]["value"]) + "%" + "。" + "\n"*2)

    Update.message.reply_text(text = String)
    Weather(Update)

def Rain(Update):
    chat_id = getChatId(Update)
    URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    Results = Results["rainfall"]["data"]
    menu = []
    for i in range(len(Results)):
        menu.append([telegram.KeyboardButton(Results[i]["place"])])
    menu.append([telegram.KeyboardButton('返回主頁')])
    reply_markup = ReplyKeyboardMarkup(menu)
    Update.message.reply_text('你想知邊度嘅降雨量?', reply_markup=reply_markup)
    db.execute("UPDATE TG_BOT SET press = :text WHERE Chat_id = :chat_id",text = "Rain", chat_id = chat_id)

def RainAns(Update, lasttext):

    chat_id = getChatId(Update)

    text = db.execute("SELECT text FROM TG_BOT WHERE Chat_id = :chat_id",chat_id = chat_id)
    URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    Results = Results["rainfall"]["data"]
    for i in range(len(Results)):
        if (str(Results[i]["place"]) == lasttext):
            pressnull(Update)
            Bot.sendMessage(chat_id,'依家' + str(Results[i]["place"] + '嘅降雨量係 ' + str(Results[i]["max"]) + ' mm'))
            Weather(Update)
        else:
            pass

def Temperature(Update):
    chat_id = getChatId(Update)
    URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    Results = Results["temperature"]["data"]
    menu = []
    for i in range(len(Results)):
        menu.append([telegram.KeyboardButton(Results[i]["place"])])
    menu.append([telegram.KeyboardButton('返回主頁')])
    reply_markup = ReplyKeyboardMarkup(menu)
    Update.message.reply_text('想知邊度嘅氣溫?', reply_markup=reply_markup)
    db.execute("UPDATE TG_BOT SET press = :text WHERE Chat_id = :chat_id",text = "Temp", chat_id = chat_id)


def TemperatureAns(Update, lasttext):

    chat_id = getChatId(Update)

    text = db.execute("SELECT text FROM TG_BOT WHERE Chat_id = :chat_id",chat_id = chat_id)
    URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    Results = Results["temperature"]["data"]
    for i in range(len(Results)):
        if (str(Results[i]["place"]) == lasttext):
            pressnull(Update)
            Bot.sendMessage(chat_id,'依家' + str(Results[i]["place"] + '嘅氣溫係 ' + str(Results[i]["value"]) + '°C'))
            Weather(Update)
        else:
            pass


def good(Update, Good):
    pressnull(Update)
    Update.message.reply_text(Good)
    Main(Update)
    
    


def Main(Update):
    pressnull(Update)
    menu_main = [[telegram.KeyboardButton('天氣')],
                 [telegram.KeyboardButton('交通')],
                 [telegram.KeyboardButton('良心選項')]]
    reply_markup = ReplyKeyboardMarkup(menu_main)
    Update.message.reply_text('你想睇啲乜嘢呀?', reply_markup=reply_markup)


def Weather(Update):
    pressnull(Update)
    menu_main = [[telegram.KeyboardButton('氣溫')],
                 [telegram.KeyboardButton('降雨量')],
                 [telegram.KeyboardButton('天氣預報')],
                 [telegram.KeyboardButton('九天天氣預報')],
                 [telegram.KeyboardButton('返回主頁')]]
    reply_markup = ReplyKeyboardMarkup(menu_main)
    Update.message.reply_text('想知天氣嘅乜嘢?', reply_markup=reply_markup)


def Transportation(Update):
    pressnull(Update)
    menu_main = [[telegram.KeyboardButton('特別交通消息')],
                 [telegram.KeyboardButton('主要隧道狀況')],
                 [telegram.KeyboardButton('重要路線道路工程')],
                 [telegram.KeyboardButton('返回主頁')]]
    reply_markup = ReplyKeyboardMarkup(menu_main)
    Update.message.reply_text('想知啲交通嘅乜嘢?', reply_markup=reply_markup)

def repair(Update):
    db.execute("UPDATE TG_BOT SET press = :text WHERE Chat_id = :chat_id",text = "repair", chat_id = getChatId(Update))
    menu_main = [[telegram.KeyboardButton('進行中')],
                 [telegram.KeyboardButton('預備中')],
                 [telegram.KeyboardButton('返回主頁')]]
    reply_markup = ReplyKeyboardMarkup(menu_main)
    Update.message.reply_text('想睇邊個種類嘅訊息?', reply_markup=reply_markup)


def repairAns(Update,lasttext):
    chat_id = getChatId(Update)
    URL = "https://resource.data.one.gov.hk/td/roadworks-location/get_all_the_roadworks.json"
    Results = urllib.request.urlopen(URL).read().decode()
    Results = json.loads(Results)
    String = ""
    j = 1
    for i in range(len(Results)):
        if(str(Results[i]["worksstatus_tc"]) == lasttext):
            String += (str(j) + "." + "\n" + "地點: " + str(Results[i]["roadname_tc"])
                       + str(Results[i]["locdesc_tc"]) + str(Results[i]["lane_tc"]) + "\n"
                       + "工程開始時間: " + str(Results[i]["starttime"]) + "\n" + "工程結束時間: "
                       + str(Results[i]["endtime"]) + "\n"*2)
            j += 1
        else:
            pass


    Update.message.reply_text(String)
    Transportation(Update)




def special(Update):
    URL = "https://resource.data.one.gov.hk/td/en/specialtrafficnews.xml"
    Results = urllib.request.urlopen(URL).read()
    xml = bs.BeautifulSoup(Results, 'xml')
    String = ""
    i = 1
    for url in xml.find_all('ChinText'):
        String +=  str(i) + "." + "\n"*2 + url.text + "\n"*2
        i = i + 1
    Update.message.reply_text(String)
    Transportation(Update)


def mainroute(Update):
    db.execute("UPDATE TG_BOT SET press = :text WHERE Chat_id = :chat_id",text = "mainrt", chat_id = getChatId(Update))
    menu_main = [[telegram.KeyboardButton('紅磡海底隧道')],
                 [telegram.KeyboardButton('東區海底隧道')],
                 [telegram.KeyboardButton('西區海底隧道')],
                 [telegram.KeyboardButton('返回主頁')]]
    reply_markup = ReplyKeyboardMarkup(menu_main)
    Update.message.reply_text('邊一條隧道?', reply_markup=reply_markup)


def mainrtAns(Update, lasttext):
    URL = "https://resource.data.one.gov.hk/td/speedmap.xml"
    Results = urllib.request.urlopen(URL).read()
    mainrt = bs.BeautifulSoup(Results, 'xml')
    Full = mainrt.find_all("LINK_ID")
    String = ""
    stat_k = ""
    stat_h = ""
    if(lasttext == "紅磡海底隧道"):
        kmr = mainrt.find("LINK_ID",text = "3363-3369")
        hmr = mainrt.find("LINK_ID",text = "46319-46512")
        kin = Full.index(kmr)
        hin = Full.index(hmr)
        ks = mainrt.find_all("TRAFFIC_SPEED")[kin]
        hs = mainrt.find_all("TRAFFIC_SPEED")[hin]

        if (mainrt.find_all("ROAD_SATURATION_LEVEL")[kin].text == "TRAFFIC GOOD"):
            stat_k = "暢順"
        elif(mainrt.find_all("ROAD_SATURATION_LEVEL")[kin].text == "TRAFFIC AVERAGE"):
            stat_k = "一般"
        else:
            stat_k = "緩慢"

        if (mainrt.find_all("ROAD_SATURATION_LEVEL")[hin].text == "TRAFFIC GOOD"):
            stat_h = "暢順"
        elif(mainrt.find_all("ROAD_SATURATION_LEVEL")[hin].text == "TRAFFIC AVERAGE"):
            stat_h = "一般"
        else:
            stat_h = "緩慢"

        String = ("目前紅磡海底隧道往九龍方向交通" + stat_k + "速度大約有" + ks.text + "km/h"
                  + "，" + "往香港方向交通" + stat_h + "速度大約有" + hs.text + "km/h" + "。")

        Update.message.reply_text(String)
        Transportation(Update)

    elif(lasttext == "東區海底隧道"):
        kmr = mainrt.find("LINK_ID",text = "4650-3651")
        hmr = mainrt.find("LINK_ID",text = "36511-46502")
        kin = Full.index(kmr)
        hin = Full.index(hmr)
        ks = mainrt.find_all("TRAFFIC_SPEED")[kin]
        hs = mainrt.find_all("TRAFFIC_SPEED")[hin]

        if (mainrt.find_all("ROAD_SATURATION_LEVEL")[kin].text == "TRAFFIC GOOD"):
            stat_k = "暢順"
        elif(mainrt.find_all("ROAD_SATURATION_LEVEL")[kin].text == "TRAFFIC AVERAGE"):
            stat_k = "一般"
        else:
            stat_k = "緩慢"

        if (mainrt.find_all("ROAD_SATURATION_LEVEL")[hin].text == "TRAFFIC GOOD"):
            stat_h = "暢順"
        elif(mainrt.find_all("ROAD_SATURATION_LEVEL")[hin].text == "TRAFFIC AVERAGE"):
            stat_h = "一般"
        else:
            stat_h = "緩慢"

        String = ("目前東區海底隧道往九龍方向交通" + stat_k + "速度大約有" + ks.text + "km/h"
                  + "，" + "往香港方向交通" + stat_h + "速度大約有" + hs.text + "km/h" + "。")

        Update.message.reply_text(String)
        Transportation(Update)

    elif(lasttext == "西區海底隧道"):
        kmr = mainrt.find("LINK_ID",text = "4652-4633")
        hmr = mainrt.find("LINK_ID",text = "46332-46522")
        kin = Full.index(kmr)
        hin = Full.index(hmr)
        ks = mainrt.find_all("TRAFFIC_SPEED")[kin]
        hs = mainrt.find_all("TRAFFIC_SPEED")[hin]

        if (mainrt.find_all("ROAD_SATURATION_LEVEL")[kin].text == "TRAFFIC GOOD"):
            stat_k = "暢順"
        elif(mainrt.find_all("ROAD_SATURATION_LEVEL")[kin].text == "TRAFFIC AVERAGE"):
            stat_k = "一般"
        else:
            stat_k = "緩慢"

        if (mainrt.find_all("ROAD_SATURATION_LEVEL")[hin].text == "TRAFFIC GOOD"):
            stat_h = "暢順"
        elif(mainrt.find_all("ROAD_SATURATION_LEVEL")[hin].text == "TRAFFIC AVERAGE"):
            stat_h = "一般"
        else:
            stat_h = "緩慢"

        String = ("目前西區海底隧道往九龍方向交通" + stat_k + "速度大約有" + ks.text + "km/h"
                  + "，" + "往香港方向交通" + stat_h + "速度大約有" + hs.text + "km/h" + "。")

        Update.message.reply_text(String)
        Transportation(Update)






def messagehandler(Update):

    global lastMessageID
    text = getText(Update)
    msg_id = getID(Update)
    user_id = getUserId(Update)
    chat_id = getChatId(Update)


    def textRespone(text):
        chat_id = getChatId(Update)
        try:
            lastpress = db.execute("SELECT press FROM TG_BOT WHERE Chat_id = :chat_id",chat_id = chat_id)[0]["press"]
            lasttext = db.execute("SELECT text FROM TG_BOT WHERE Chat_id = :chat_id",chat_id = chat_id)[0]["text"]
            if(text=="天氣"):
                Weather(Update)

            if(text=="Test"):
                Test(Update)

            if(text=="氣溫"):
                Temperature(Update)

            if(text=="降雨量"):
                Rain(Update)

            if(text=="交通"):
                Transportation(Update)

            if(text=="特別交通消息"):
                special(Update)

            if(text=="主要隧道狀況"):
                mainroute(Update)

            if(text=="重要路線道路工程"):
                repair(Update)

            if(text=="天氣預報"):
                forecast(Update)

            if(text=="九天天氣預報"):
                nineforecast(Update)
                
            if(text=="良心選項"):
                good(Update, Good)

            if(text=="返回主頁"):
                Main(Update)

            if(lastpress == "Temp"):
                TemperatureAns(Update,lasttext)
            elif(lastpress == "Rain"):
                RainAns(Update, lasttext)
            elif(lastpress == "mainrt"):
                mainrtAns(Update, lasttext)
            elif(lastpress == "repair"):
                repairAns(Update,lasttext)

        except:
            pass


        if(text=="/start"):
            user_id = getUserId(Update)
            chat_id = getChatId(Update)
            check_group = db.execute("SELECT Chat_id FROM TG_BOT WHERE Chat_id = :chat_id",chat_id = chat_id)
            if (len(check_group) != 1):
                db.execute("INSERT INTO TG_BOT (Chat_id) VALUES(:chat_id)",chat_id = chat_id)
                Main(Update)
            else:
                Main(Update)



    textRespone(text)
    lastMessageID = msg_id
    print(chat_id, user_id, msg_id, text)




def main():
    global lastMessageID
    Updates = Bot.getUpdates()
    if (len(Updates) > 0):
        lastMessageID = Updates[-1]["update_id"]

    while(True):
        Updates = Bot.getUpdates(offset=lastMessageID)
        Updates = [Update for Update in Updates if Update["update_id"] > lastMessageID]
        for Update in Updates:
            db.execute("UPDATE TG_BOT SET text = :text WHERE Chat_id = :chat_id",text = getText(Update), chat_id = getChatId(Update))
            messagehandler(Update)




if __name__ == "__main__":
    main()