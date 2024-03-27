import requests
import openpyxl
import json
import threading

schedule_lock = threading.Lock()

def download_convert_schedule():
    schedule_url = 'https://serp-koll.ru/images/ep/k1/rasp1.xlsx'
    response = requests.get(schedule_url)
    
    if response.status_code == 200:
        with open('rasp1.xlsx', 'wb') as f:
            f.write(response.content)
        
        workbook = openpyxl.load_workbook('rasp1.xlsx')
        sheet = workbook.active

        schedule_data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {
                'key2': row[1],
                'key3': row[2],
                'key4': row[3],
                'key5': row[4],
                'key6': row[5],
                'key7': row[6],
                'key8': row[7],
                'key9': row[8],
                'key10': row[9],
                'key11': row[10],
                'key12': row[11],
                'key13': row[12],
                'key14': row[13],
                'key15': row[14],
                'key16': row[15],
                'key17': row[16],
                'key18': row[17],
                'key19': row[18],
                'key20': row[19],
                'key21': row[20],
                'key22': row[21],
                'key23': row[22],
                'key24': row[23],
                'key25': row[24],
                'key26': row[25],
                'key27': row[26],
                'key28': row[27],
                'key29': row[28],
            }
            schedule_data.append(row_data)

        json_data = json.dumps(schedule_data, indent=4, ensure_ascii=False)

        with schedule_lock:
            with open('rasp1.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json_data)

        print('Конвертация выполнена успешно')
    
    else:
        print('Не удалось загрузить файл расписания')

