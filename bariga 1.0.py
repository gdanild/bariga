# -*- coding: utf-8 -*-
import btcelib
import time

BTC_api_key = "SI0R2WWI-5BAPA1QQ-8ZN65649-LSWPMEB2-TM9YCG80"
BTC_api_secret = "3939cd59dbb21b7d39cd6e77347e7fd55b0ea60de4c56f2d28ada559ce6b0bc8"


papi = btcelib.PublicAPIv3()
data = papi.call('ticker', limit=5)
keys = data.keys() # all pairs
i = 0
# вывод всех пар
while i!=len(keys):
    print keys[i]
    i += 1

mare = raw_input("Пара валют: ") # ввод пары валют
lave = raw_input("На сколько бабла: ") # ввод на сколько бабла будем барыжить
risk = input("На сколько процентов должен упасть курс: ")
tme = input("За сколько секунд он должен упасть ?: ")
income = input("сколько нужно процентов прибыли, чтобы продать: ")
pare = "'"+mare+"'" # делаю из btc_usd в 'btc_usd'
a = time.time()  # получаю время в секундах начиная от нашей эры

data = papi.call('ticker/' + pare, limit=5)
pare = data.keys()[0]
buy = (data[pare][u'buy'])

lave = str(round(int(lave) / buy, 3))
print lave

# получаю цену покупки по определенной паре

data = papi.call('ticker/' + pare, limit=5) 
pare = data.keys()[0]
old_buy = (data[pare][u'buy'])
while True: # главный цикл которые по очереди задействет цикл то на покупку то на продажу
    while True: # пошел цикл(бесконечный)на покупку
        # получаю цену покупки продажи для пары
        data = papi.call('ticker/' + pare, limit=5)
        pare = data.keys()[0]
        sell = (data[pare][u'sell'])
        buy = (data[pare][u'buy'])
        print "== этап первый ждет падения =="
        print 'buy: ' + str(buy) # вывожу цену покупки
        print 'sell: ' + str(sell) # вывожу цену продажи     
        if int(time.time() - a) > tme and (old_buy/buy -1)*100 >= risk: # если прошло 10 секунд и цена за это время упала на risk процентов
            tapi = btcelib.TradeAPIv1({'Key': BTC_api_key, 'Secret': BTC_api_secret})
            tapi.call('Trade',
                        pair=mare,
                        type = 'buy',
                        rate = buy-5,
                        amount = lave,
                        count=100)
            old_buy = buy
            print("КУПЛЕНО! за " + lave)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            break;
        else:
            if (old_buy/buy -1)*100 > 0:
                print "Упала на " + str((old_buy/buy -1)*100) + " %" # вывожу на сколько процентов изменилась цена
            else:
                print "Поднялась на " + str((old_buy/buy -1)*100*-1) + " %" # вывожу на сколько процентов изменилась цена
            if int(time.time() - a) > tme:
                old_buy = buy # запоминаю цену чтобы потом узнать на сколько изменилась
                a = time.time() # запоминаю время
                print "прошло " + str(tme) + "секунд"
                
        print("@@@@@@@@@@@@@@@")
        time.sleep(3) # пауза цикла на 3 секунды
        #на этот моменте цикл пойдет по новой если еще ничего не куплено
    print "@@@@@@@@@@@@@@@@@@@@"
    while True: # пошел цикл на продажу
        # получаю цену покупки продажи для пары        
        data = papi.call('ticker/' + pare, limit=5)
        pare = data.keys()[0]
        sell = (data[pare][u'sell'])
        buy = (data[pare][u'buy'])
        print "== этап второй продажа =="
        print("покупал за: "+str(old_buy)) # пишу почем покупал
        print 'buy: ' + str(buy) # вывожу цену покупки
        print 'sell: ' + str(sell) # вывожу цену продажи
        print "если продать " + str((float(sell/old_buy) *0.998*0.998 - 1) * 100) + " %"  # сколько процентов заработаю или потеряю если продам
        print("@@@@@@@@@@@@@@@@@")
        if (float(sell/old_buy) *0.998*0.998 - 1) * 100 >= income: # если сейчас продать и прибыль будет больше или равна income то
            # отправляю запрос на продажу
            tapi = btcelib.TradeAPIv1({'Key': BTC_api_key, 'Secret': BTC_api_secret})
            tapi.call('Trade',
                      pair=mare,
                      type = 'sell',
                      rate = sell,
                      amount = str(int(lave)*0.998),
                      count=100)
            print ("Sales good: " + str(float((sell/old_buy -1)) *0.998*0.998 * 100)) # пишу что успешно продал и сколько заработал
            break; # выход из цикла продажт
        time.sleep(2) # остановка на 2 секнды
    raw_input("Repeat?") # если нажать интер то все пойдет по новой, купит, потом продаст
            
            
    
