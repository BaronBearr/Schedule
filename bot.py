import json
import telebot
import sqlite3
import threading
import time

from autocon import download_convert_schedule



bot = telebot.TeleBot('7099372047:AAHirvtNIWBbg87nqzaStxae1cp53B4Xgog')
schedule_lock = threading.Lock()

def load_schedule_data():
    with schedule_lock:
        with open('rasp1.json', 'r', encoding='utf-8') as file:
            return json.load(file)

def get_schedule(group):
    data = load_schedule_data()
    schedule = f"{group}:\n"

    group_found = False

    for i in range(0, len(data), 13):
        para_num = 1
        para_found = False
        subgroup_schedule = ""

        for key in [
            'key2', 'key3', 'key4', 'key5', 'key6', 'key7', 'key8', 
            'key9', 'key10', 'key11', 'key12', 'key13', 'key14', 'key15',
            'key16', 'key17', 'key18', 'key19', 'key20', 'key21', 'key22',
            'key23', 'key24', 'key25', 'key26', 'key27', 'key28', 'key29']:
            if data[i][key] == group:
                group_found = True
                if not para_found:
                    para_found = True
                    
                for j in range(i+12, len(data), 13):
                    subgroup_schedule += f"Пара {para_num}:\n"
                    
                    schedule_parts1 = data[j][key].split('\n') if data[j][key] else None  
                    schedule_parts2 = data[j+1][key].split('\n') if data[j+1][key] else None
                    
                    if schedule_parts1 and schedule_parts2:
                        if data[j-1][key] == 'Объединённая пара':
                            subgroup_schedule += '\n'.join(schedule_parts1) + '\n\n'
                        else:
                            subgroup_schedule += '\n'.join(schedule_parts1) + '\n\n'
                            subgroup_schedule += '\n'.join(schedule_parts2) + '\n\n'
                        
                    elif schedule_parts1 and not schedule_parts2:
                        if data[j-1][key] != 'Объединённая пара':
                            subgroup_schedule += f'Подгруппа 1:\n'
                        subgroup_schedule += '\n'.join(schedule_parts1) + '\n\n'
                        
                    elif not schedule_parts1 and schedule_parts2:
                        subgroup_schedule += f'Подгруппа 2:\n'  
                        subgroup_schedule += '\n'.join(schedule_parts2) + '\n\n'
                        
                    else:
                        subgroup_schedule += "Пары нет\n\n"
                        
                    para_num += 1

        if para_found:
            schedule += subgroup_schedule
            
    schedule += "\n"
    
    if group_found:
        return schedule.strip()
    else:
        return "Неверная группа"    


@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn = sqlite3.connect('rasp.db')
    cursor = conn.cursor()
    user_id = message.chat.id
    username = message.chat.username if message.chat.username else None
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, active) VALUES (?, ?, ?)", (user_id, username, 1))
    conn.commit()
    conn.close()
    bot.reply_to(message, "Привет! Я бот для вывода расписания группы. ")


@bot.message_handler(func=lambda message: message.chat.id == 784975687 and message.text.startswith('/send'))
def send_to_all(message):
    message_text = message.text.replace('/send', '').strip()
    
    conn = sqlite3.connect('rasp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()
    
    for user_id in users:
        try:
            bot.send_message(user_id[0], message_text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    group = message.text.strip()
    schedule = get_schedule(group)
    if schedule:
        bot.reply_to(message, schedule)
    else:
        bot.reply_to(message, "Расписание для указанной группы не найдено.")

if __name__ == '__main__':
    bot.polling()

