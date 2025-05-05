token="7665078010:AAHiB1jZHwDugXm9FdtdOWbgNPwptfA1mAM"
import telebot
import datetime
import json
bot=telebot.TeleBot(token)
slovar={}
spisoc=[]
slovarocenoc={}

@bot.message_handler(["start"])
def handle_start(message):
    bot.send_message(message.chat.id,"привет")


def proceduricnopci():
    nabor=telebot.types.InlineKeyboardMarkup()
    spisoc=["стрижка","маникюр","массаж"]
    for proced in spisoc:
        cnopca=telebot.types.InlineKeyboardButton(proced,callback_data="proceduri*"+proced)
        nabor.add(cnopca)
    return nabor


def g(message):
    return True

@bot.callback_query_handler(func=g)
def obrabotcacnop(clic):
    print(clic.data)
    a=clic.data.split("*")
    print(a)
    if a[0]=="proceduri":
        print("клик по процедуре")
        bot.send_message(clic.message.chat.id,"вы выбрали "+a[1])
        slovar[clic.message.chat.id].append(a[1])
        bot.send_message(clic.message.chat.id,"выберете дату",reply_markup=dati())
    if a[0]=="dati":
        bot.send_message(clic.message.chat.id,"вы выбрали "+a[1])
        slovar[clic.message.chat.id].append(a[1])
        bot.send_message(clic.message.chat.id,"выберете время",reply_markup=vrema(a[1]))
    if a[0]=="vrema":
        slovar[clic.message.chat.id].append(a[1]) 
        print(slovar)
        spisoc=slovar[clic.message.chat.id]
        bot.send_message(clic.message.chat.id,f"запись на имя {spisoc[0]},на процедуру: {spisoc[1]},на дату: {spisoc[2]},на время: {spisoc[3]} успешно создана")
        fayl=open("file.json","r",encoding="UTF-8")
        slovarjson=json.load(fayl)
        spisoczapisi=slovarjson["zapisi"]
        spisoczapisi.append(spisoc)
        fayl.close()
        fayl=open("file.json","w",encoding="UTF-8")
        json.dump(slovarjson,fayl,ensure_ascii=False,indent=4) 
        fayl.close()
    if a[0]=="ocenca":
        slovarocenoc[str(clic.message.chat.id)].append(a[1])
        spisoc=slovarocenoc[str(clic.message.chat.id)]
        bot.send_message(clic.message.chat.id,f"отзыв на имя {spisoc[0]},с отзывом: {spisoc[1]},с оценкой: {spisoc[2]}, успешно создан")
        fayl=open("file.json","r",encoding="UTF-8")
        slovarjson=json.load(fayl)
        spisoczapisi=slovarjson["otzivi"]
        spisoczapisi.append(spisoc)
        fayl.close()
        fayl=open("file.json","w",encoding="UTF-8")
        json.dump(slovarjson,fayl,ensure_ascii=False,indent=4)
        fayl.close()

def zanatievremena(data):
    file=open("file.json","r",encoding="UTF-8")
    slovarjson=json.load(file)
    spisoczapisi=slovarjson["zapisi"]
    spisoc=[]
    for zapis in spisoczapisi:
        if zapis[2]==data:
            spisoc.append(zapis[3])
    return spisoc


@bot.message_handler(["otziv"])
def otziv(message):
    bot.send_message(message.chat.id,"Введите свое имя")
    bot.register_next_step_handler_by_chat_id(message.chat.id,otzivima)


def otzivima(message):
    slovarocenoc[str(message.chat.id)]=[message.text]
    bot.send_message(message.chat.id,"Введите отзыв")
    bot.register_next_step_handler_by_chat_id(message.chat.id,cnopcaotziv)
    

def ocencacnopci():
    naborocenoc=telebot.types.InlineKeyboardMarkup()
    spisoc=["отлично","хорошо","средне","неплохо","неудовлетворительно"]
    for ocenca in spisoc:
        ocenca=telebot.types.InlineKeyboardButton(ocenca,callback_data="ocenca*"+ocenca)
        naborocenoc.add(ocenca)
    return naborocenoc

def cnopcaotziv(message):
    slovarocenoc[str(message.chat.id)].append(message.text)
    bot.send_message(message.chat.id,"выберете оценку",reply_markup=ocencacnopci())


def ima(message):
    bot.send_message(message.chat.id,"приятно познакомиться, "+message.text)
    slovar[message.chat.id]=[message.text]
    bot.send_message(message.chat.id,"выберете процедуру",reply_markup=proceduricnopci())


@bot.message_handler(["zapis"])
def handle_zapis(message):
    bot.send_message(message.chat.id,"введите свое имя")
    bot.register_next_step_handler_by_chat_id(message.chat.id,ima)


def dati():
    e=7
    s=1
    spisoc=[]
    while e>0:
        dni=datetime.timedelta(days=s)
        data=datetime.date.today()
        r=dni+data
        s=s+1
        e=e-1
        spisoc.append(str(r))
    print(spisoc)
    nabor=telebot.types.InlineKeyboardMarkup()
    for data in spisoc:
        cnopcadat=telebot.types.InlineKeyboardButton(data,callback_data="dati*"+data)
        nabor.add(cnopcadat)
    return nabor


def vrema(data):
    spisoc=[]
    w=8
    while w<18:
        chasi=datetime.time(w,0,0)
        spisoc.append(str(chasi))
        w=w+1
    nabor=telebot.types.InlineKeyboardMarkup()
    spisocvrem=zanatievremena(data)
    for vrema in spisoc:
        if vrema not in spisocvrem:
            cnopcavrema=telebot.types.InlineKeyboardButton(vrema,callback_data="vrema*"+vrema)
            nabor.add(cnopcavrema)
    return nabor

bot.polling()