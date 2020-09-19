#!/usr/bin/env python3
#find me at t.me/Sakib0194 if you are looking to create a bot
import requests, json, random, string, time, datetime, requests, mysql.connector, sys
import database
from binance.client import Client

class BoilerPlate:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=0, timeout=1):         #FOR GETTING UPDATES
        function = 'getUpdates'
        fieldss = {'timeout' : timeout, 'offset': offset}
        send = requests.get(self.api_url + function, fieldss)
        #print(send.json())
        result_json = send.json()['result']
        return result_json

    def send_message(self, chat_id, text, disable_web_page_preview=False):                  #FOR SENDING NORMAL MESSAGE
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'disable_web_page_preview':disable_web_page_preview}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send
    def send_message_two(self, chat_id, text, reply_markup, one_time_keyboard=False, resize_keyboard=True, disable_web_page_preview=True):         #FOR SENDING MESSAGE WITH KEYBOARD INCLUDED
        reply_markup = json.dumps({'keyboard': reply_markup, 'one_time_keyboard': one_time_keyboard, 'resize_keyboard': resize_keyboard, 'disable_web_page_preview':disable_web_page_preview})
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'reply_markup': reply_markup}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss).json()
        #print(send)
        return send

    def send_message_three(self, chat_id, text, remove_keyboard):               #FOR SENDING MESSAGES AND TO REMOVE KEYBOARD
        reply_markup = json.dumps({'remove_keyboard': remove_keyboard})
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'reply_markup': reply_markup}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss).json()
        return send   

    def send_message_four(self, chat_id, text, reply_markup, disable_web_page_preview=True):               #FOR SENDING MESSAGES WITH INLINE KEYBOARD
        reply_markup = json.dumps({'inline_keyboard': reply_markup})
        fieldss = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2', 'reply_markup': reply_markup, 'disable_web_page_preview':disable_web_page_preview}
        function = 'sendMessage'
        send = requests.post(self.api_url + function, fieldss)
        #print(send)
        #print(send.json)
        return send.json()

    def send_photo(self, chat_id, photo):
        fieldss = {'chat_id':chat_id, 'photo':photo}
        function = 'sendPhoto'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 

    def send_video(self, chat_id, video):
        fieldss = {'chat_id':chat_id, 'video':video}
        function = 'sendVideo'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 
    
    def send_document(self, chat_id, document):
        fieldss = {'chat_id':chat_id, 'document':document}
        function = 'sendDocument'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 

    def send_sticker(self, chat_id, sticker):
        fieldss = {'chat_id':chat_id, 'sticker':sticker}
        function = 'sendSticker'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send 
    
    def InLineAnswer(self, inline_query_id, results):                   #FOR MANAGING INLINE REPLIES
        fieldss = {"inline_query_id": inline_query_id, "results" : results}
        function = 'answerInlineQuery'
        send = requests.post(self.api_url + function, fieldss)
        return send   

    def deleteWebhook(self):                #FOR DELETING WEBHOOK
        function = 'deleteWebhook'
        send = requests.post(self.api_url + function)
        return send

    def delete_message(self, group_id, message_id):         #FOR DELETING MESSAGES FROM GROUP
        fieldss = {'chat_id': group_id, 'message_id': message_id}
        function = 'deleteMessage'
        send = requests.post(self.api_url + function, fieldss)
        return send

    def get_admins(self, chat_id):              #ADMIN LIST IN A GROUP
        function = 'getChatAdministrators'
        fieldss = {'chat_id':chat_id}
        send = requests.get(self.api_url + function, fieldss)
        return send.json()['result']

    def edit_message (self, chat_id, message_id, text):
        fieldss = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode':'MarkdownV2'}
        function = 'editMessageText'
        send = requests.post(self.api_url + function, fieldss)
        return send

    def edit_message_two (self, chat_id, message_id, text, reply_markup, disable_web_page_preview=True, parse_mode='MarkdownV2'):
        reply_markup = json.dumps({'inline_keyboard': reply_markup})
        fieldss = {'chat_id': chat_id, 'message_id': message_id, 'text': text, 'parse_mode':parse_mode, 'reply_markup':reply_markup, 'disable_web_page_preview':disable_web_page_preview}
        function = 'editMessageText'
        send = requests.post(self.api_url + function, fieldss)
        #print(send.json())
        return send

details = sys.argv[1:]
conn = mysql.connector.connect(host=details[0],user=details[1],database=details[2],password=details[3], autocommit=True)
cur = conn.cursor()

token = database.special('api', cur)
bi_pub = database.special('bi pub', cur)
bi_pri = database.special('bi pri', cur)
client = Client(bi_pub, bi_pri, {'timeout':5})
offset = 0
special = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
pairs = database.available_pairs('pairs', cur)
for_price = database.available_pairs('price', cur)
feedback = []
alert = {}

bot = BoilerPlate(token)

def price(coin, client=client):
    try:
        price = client.get_avg_price(symbol=coin)['price']
        return float(price)
    except:
        client = Client(bi_pub, bi_pri, {'timeout':5})
        price = client.get_avg_price(symbol=coin)['price']
        return float(price)

def price_checker():
    alert_up = {}
    alert_down = {}
    all_user = database.all_users(cur)
    for i in pairs:
        alert_up = {}
        alert_down = {}
        for a in all_user:
            up = database.all_up(a, i, cur)
            if up == 'Nothing':
                up = '0'
            else:
                alert_up[a] = up
            down = database.all_down(a, i, cur)
            if down == 'Nothing':
                down = '0'
            else:
                alert_down[a] = down
        for h in alert_up:
            full_text = ''
            cu_price = price(i)
            data = alert_up[h]
            data2 = alert_up[h]
            data = data.split(' ')
            data2 = data2.split(' ')
            for u in data:
                if u == '':
                    data2.remove(str(u))
                else:
                    if cu_price > float(u):
                        data2.remove(str(u))
                        u = u.replace('.', '\\.')
                        bot.send_message(h, f'Current price of {i} has went above {u}')
            if data2 == []:
                pass
            else:
                full_text += f'{data2[0]}'
                for q in range(1, len(data2)):
                    full_text += f' {data2[q]}'
            database.add_up(h, i, full_text, cur)
        for h in alert_down:
            full_text = ''
            data = alert_down[h]
            data2 = alert_down[h]
            data = data.split(' ')
            data2 = data2.split(' ')
            for u in data:
                if u == '':
                    data2.remove(str(u))
                else:
                    if cu_price < float(u):
                        data2.remove(str(u))
                        u = u.replace('.', '\\.')
                        bot.send_message(h, f'Current price of {i} has went below {u}')
            if data2 == []:
                pass
            else:
                full_text += f'{data2[0]}'
                for q in range(1, len(data2)):
                    full_text += f' {data2[q]}'
            database.add_down(h, i, full_text, cur)

def starter():
    global offset, conn, cur
    while True:
        try:
            if conn.is_connected() == True:
                pass
            else:
                conn = mysql.connector.connect(host=details[0],user=details[1],database=details[2],password=details[3], autocommit=True)
                cur = conn.cursor()
            price_checker()
            all_updates = bot.get_updates(offset)
            for current_updates in all_updates:
                #print(current_updates)
                update_id = current_updates['update_id']
                #bot.get_updates(offset = update_id+1)
                try:
                    if 'callback_query' in current_updates:
                        #print('inline keyboard detected')
                        sender_id = current_updates['callback_query']['from']['id']
                        group_id = current_updates['callback_query']['message']['chat']['id']
                        message_id = current_updates['callback_query']['message']['message_id']
                        callback_data = current_updates['callback_query']['data']
                        bot_message_handler(current_updates, update_id, message_id, sender_id, group_id, 0, cur, callback_data=callback_data, callback=True)
                    else:
                        group_id = current_updates['message']['chat']['id']
                        sender_id = current_updates['message']['from']['id']
                        message_id = current_updates['message']['message_id']
                        dict_checker = []
                        for keys in current_updates.get('message'):
                            dict_checker.append(keys)
                        if sender_id == group_id:
                            bot_message_handler(current_updates, update_id, message_id, sender_id, group_id, dict_checker, cur)
                except:
                    bot.get_updates(offset = update_id+1)
        except Exception as e:
            print(e)
            print('got an error')
            pass

def bot_message_handler(current_updates, update_id, message_id, sender_id, group_id, dict_checker, cur, callback_data=0, callback=False):
    try:
        if callback == True:
            print(callback_data)
            
            if callback_data == 'New Alert':
                full_code = []
                if sender_id in alert:
                    del alert[sender_id]
                for i in pairs:
                    full_code.append([{'text':f'{i}', 'callback_data':f'{i}'}])
                full_code.append([{'text':'Back','callback_data':'Back'}])
                bot.edit_message_two(group_id, message_id, 'Select a pair', full_code)
                bot.get_updates(offset = update_id+1)

            elif callback_data in pairs:
                cu_price = price(callback_data)
                cu_price = str(cu_price).replace('.', '\\.')
                bot.edit_message_two(group_id, message_id, f'Current Price of {callback_data}: {cu_price}\\.\nTo create an alert send the price point in one word', [[{'text':'Back', 'callback_data':'New Alert'}]])
                alert[sender_id] = callback_data
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Back':
                if sender_id in alert:
                    del alert[sender_id]
                if sender_id in feedback:
                    feedback.remove(sender_id)
                bot.edit_message_two(group_id, message_id, 'Select one of the options below', [[{'text':'Active Alerts', 'callback_data':'Active Alert'}],
                                                                                    [{'text':'Create New Alert', 'callback_data':'New Alert'}],
                                                                                    [{'text':'Source Code', 'url':'https://github.com/Sakib0194/crypto_price_alert/'}, {'text':'Send Feedback', 'callback_data':'Feedback'}],
                                                                                    [{'text':'Price Checker', 'callback_data':'Price Checker'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Active Alert':
                full_text = ''
                for i in pairs:
                    full_text += f'*{i}*\n'
                    data = database.all_up(sender_id, i, cur).split(' ')
                    for a in data:
                        a = a.replace('.', '\\.')
                        full_text += f'{a}\n'
                    data = database.all_down(sender_id, i, cur).split(' ')
                    for a in data:
                        a = a.replace('.', '\\.')
                        full_text += f'{a}\n'
                bot.edit_message_two(group_id, message_id, full_text, [[{'text':'Back','callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Feedback':
                feedback.append(sender_id)
                bot.edit_message_two(group_id, message_id, 'You can report any bugs, feedback, request features from here\\.\nType your text now, it will be recorded\nTo contact me directly [click here](https://t.me/sakib0194)', [[{'text':'Back','callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if callback_data == 'Price Checker':
                full_text = ''
                for i in for_price:
                    cu_price = price(i)
                    cu_price = str(cu_price).replace('.', '\\.')
                    full_text += f'*{i}*    {cu_price}\n'
                full_text += '\nAll Binance Pairs price can now be checked via the command below\nprice PairNames\nprice BNBBTC\nprice BTCUSDT BNBUSDT etc'
                bot.send_message(sender_id, full_text)
                bot.get_updates(offset = update_id+1)

        else:   
            text = current_updates['message']['text']
            print(text)

            if text == '/start':
                if sender_id in feedback:
                    feedback.remove(sender_id)
                if sender_id in alert:
                    del alert[sender_id]
                users = database.all_users(cur)
                if sender_id not in users:
                    database.add_users(sender_id, cur)
                    database.add_user_alert(sender_id, cur)
                bot.send_message_four(sender_id, 'Select one of the options below', [[{'text':'Active Alerts', 'callback_data':'Active Alert'}],
                                                                                    [{'text':'Create New Alert', 'callback_data':'New Alert'}],
                                                                                    [{'text':'Source Code', 'url':'https://github.com/Sakib0194/crypto_price_alert/'}, {'text':'Send Feedback', 'callback_data':'Feedback'}],
                                                                                    [{'text':'Price Checker', 'callback_data':'Price Checker'}]])
                bot.get_updates(offset = update_id+1)

            if sender_id in alert:
                try:
                    pri_point = float(text)
                    price_point = str(pri_point).replace('.', '\\.')
                    sele_pair = alert[sender_id]
                    bot.send_message_four(sender_id, f'Creating a new alert at {price_point} on pair {sele_pair}', [[{'text':'Done', 'callback_data':'Back'}]])
                    cu_price = price(sele_pair)
                    if pri_point > cu_price:
                        cu_alerts = database.all_up(sender_id, sele_pair, cur)
                        if cu_alerts == 'Nothing':
                            cu_alerts = ''
                            cu_alerts += f'{pri_point}'
                        else:
                            cu_alerts += f' {pri_point}'
                        database.add_up(sender_id, sele_pair, cu_alerts, cur)
                    elif pri_point < cu_price:
                        cu_alerts = database.all_down(sender_id, sele_pair, cur)
                        if cu_alerts == 'Nothing':
                            cu_alerts = ''
                            cu_alerts += f'{pri_point}'
                        else:
                            cu_alerts += f' {pri_point}'
                        database.add_down(sender_id, sele_pair, cu_alerts, cur)
                    elif pri_point == cu_price:
                        bot.send_message_four(sender_id, 'Alert Price cannot be same as the current price\\. Try Again', [[{'text':'Done', 'callback_data':'Back'}]])
                        bot.get_updates(offset = update_id+1)
                    del alert[sender_id]
                    bot.get_updates(offset = update_id+1)
                except:
                    bot.send_message_four(sender_id, 'Text is not a digit\\. Enter a valid numner', [[{'text':'Done', 'callback_data':'Back'}]])
                    bot.get_updates(offset = update_id+1)

            if text.startswith(database.special('mass', cur)):
                message = text.split(' ')[1:]
                full_text = ''
                for i in message:
                    full_text += f'{i} '
                for i in special:
                    full_text = full_text.replace(i, f'\\{i}')
                all_user = database.all_users(cur)
                for i in all_user:
                    bot.send_message(i, full_text)
                bot.get_updates(offset = update_id+1)

            if sender_id in feedback:
                for i in special:
                    text = text.replace(i, f'\\{i}')
                bot.send_message(468930122, text)
                database.add_feedback(sender_id, text, cur)
                bot.send_message_four(sender_id, 'Your feedback has been successfully recorded', [[{'text':'Done', 'callback_data':'Back'}]])
                bot.get_updates(offset = update_id+1)

            if text.startswith('price'):
                try:
                    message = text.split(' ')[1:]
                    full_text = ''
                    for i in message:
                        coin_price = price(i)
                        coin_price = '%.10f'%coin_price
                        coin_price = str(coin_price).replace('.', '\\.')
                        full_text += f'*{i}*     {coin_price}\n'
                    bot.send_message(sender_id, full_text)
                    bot.get_updates(offset = update_id+1)
                except:
                    bot.send_message(sender_id, 'Invalid Pairs')
                    bot.get_updates(offset = update_id+1)
                

    except Exception as e:
        print(e)
        print('got an error')
        pass

starter()
