import re, os, datetime, array, requests,  json, aiohttp, asyncio
from datetime import date
class city_wheather:
    def __init__(self, city="", date=date.today(), temp=0, humidity=0, pressure=0):
        self.city=city
        self.date=date
        self.temp=temp
        self.humidity=humidity
        self.pressure=pressure
global c
c=0
global cw_array
cw_array = []

def LoadCityNames (f_name,y):
            file=open(f_name,"r", encoding='utf-8')
            for i in file:
                result=re.findall(r'\b[A-Z]\D\S+', i)
                result1=" ".join(result)
                cw_array.append(city_wheather())
                cw_array[y].city=result1
                if len(result1)>0: y+=1 
                global c
                c=y
def filedir():
      l = os.path.basename(__file__)
      m = os.path.abspath(__file__).replace(l, '')
      return m

start_time = datetime.datetime.now()
try:
    LoadCityNames(f'{filedir()}cities.txt',0)
except:
    print (f'Ошибка загрузки списка городов из {filedir()}cities.txt')
    print ("Программа завершена")
    exit()



async def main():
    global b
    b=0
    while b < c:  
                openweatherAPI = '0fb610dab7456bc44dbdde2ddba9be71'
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={cw_array[b].city}&appid={openweatherAPI}&units=metric') as response:
                        req=await response.text()

                        cw_array[b].temp=json.loads(req)['main']['temp']
                        cw_array[b].date=datetime.date.fromtimestamp(json.loads(req)['dt'])
                        cw_array[b].humidity=json.loads(req)['main']['humidity']
                        cw_array[b].pressure=json.loads(req)['main']['pressure']
                        print(f'В городе {cw_array[b].city} на {cw_array[b].date}: \n'
                                          f'Температура воздуха составит: {cw_array[b].temp} C° \n'
                                          f'Влажность воздуха: {cw_array[b].humidity}%\n'
                                          f'Давление: {cw_array[b].pressure} мм.р.т.\n')                     
                b += 1 


try:   
    global b
    b= 0 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end_time = datetime.datetime.now()
    print(f'Длительность асинхронного выполнения задачи = {end_time-start_time}')              
except:
        print (f'Ошибка доступа к сайту с данными погоды или некорректное наименование города {cw_array[b].city}')
        print ("Программа завершена")
        exit()



