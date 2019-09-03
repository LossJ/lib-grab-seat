#-*- coding:utf-8 -*-
import json
import time
import datetime
import random
import math

import requests


class Spider(object):
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.__session=requests.Session()
        headers_list=[
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN',
            'Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/4G Language/zh_CN Process/tools',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_HK',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 wxwork/2.5.1 MicroMessenger/6.3.22 Language/zh',
            'Mozilla/5.0 (Linux; Android 8.0; VKY-AL00 Build/HUAWEIVKY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 wxwork/2.5.8 MicroMessenger/6.3.22 NetType/WIFI Language/zh',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432 MicroMessenger/6.7.2 NetType/WIFI Language/zh_CN',
            'Mozilla/5.0 (Linux; Android 8.1; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044208 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/4G Language/zh_CN',
                      ]
        headers=random.choice(headers_list)
        self.__session.headers.update({'User-Agent': headers})

    def __url_to_str_and_code(self,url):
        spli = url.split('&')
        code = spli[-2].split('=')[-1]
        str = spli[-3].split('=')[-1]
        return str, code

    def __get_code(self, timeout=2, limit_time=5):
        try:
            self.__session.get(r'https://jxnu.huitu.zhishulib.com/', timeout=timeout)
            url = r'https://jxnu.huitu.zhishulib.com/User/Index/login?LAB_JSON=1'
            json_data = self.__session.get(url)
            dict = json.loads(json_data.text)
            url = dict['content']['linkUrl']
            return self.__url_to_str_and_code(url)
        except:
            limi_time = limit_time - 1
            if limi_time <= 0:
                return None
            return self.__get_code(timeout=timeout, limit_time=limi_time)

    def login(self, timeout=4, limit_time=8):
        try:
            url = r'https://jxnu.huitu.zhishulib.com/api/1/login'
            try:
                string, code = self.__get_code()
                time.sleep(1.1)
            except:
                return None
            data = {
                "code": code,
                "login_name": self.username,
                "password": self.password,
                "str": string,
                "org_id": "142",
                "_ApplicationId": "lab4",
                "_JavaScriptKey": "lab4",
                "_ClientVersion": "js_xxx",
                "_InstallationId": "171235db-0ec9-5c88-b2a3-53da2f10d464",
            }
            wb_data = self.__session.post(url=url, data=json.dumps(data))
            if wb_data.status_code == requests.codes.ok:
                print(self.username, '登录成功！')
                return wb_data.json()['id']
            else:
                raise Exception
            # print(wb_data.json())
        except:
            limi_time = limit_time - 1
            if limi_time <= 0:
                return None
            time.sleep(1.1)
            if timeout < 8:
                timeout_new = timeout + 1
            else:
                timeout_new = timeout
            return self.login(timeout=timeout_new,limit_time=limi_time)

    def get_seat_list(self,beginTime, student_count=1, hours=3, room=1, timeout=4, limit_time=5):
        try:
            url = 'https://jxnu.huitu.zhishulib.com/Seat/Index/searchSeats?LAB_JSON=1'
            if room == 1:
                content_id = '35'
            elif room == 2:
                content_id = '36'
            elif room == 3:
                content_id = '31'
            elif room == 4:
                content_id = '37'
            else:
                raise Exception
            seconds = 3600 * hours
            data = {
                'beginTime': beginTime,
                'duration': seconds,
                'num': student_count,
                r'space_category[category_id]': '591',
                r'space_category[content_id]': content_id,
            }
            '''
                beginTime: 1563933600
                duration: 10800 三小时  28800 8小时
                num: 1
                space_category[category_id]: 591 591 591 591
                space_category[content_id]: 35  36  31  37
            '''
            wb_data = self.__session.post(url, data, timeout=timeout)
            if wb_data.status_code == requests.codes.ok:
                json_data = wb_data.json()
                # print(json_data)
                return json_data
            else:
                time.sleep(1.1)
                return self.get_seat_list(beginTime=beginTime, student_count=student_count, hours=hours, room=room,timeout=timeout, limit_time=limit_time)
        except:
            time.sleep(1.1)
            return self.get_seat_list(beginTime=beginTime, student_count=student_count, hours=hours, room=room,timeout=timeout, limit_time=limit_time)

    def grab_seat(self,duration, seats, seatBookers, beginTime, timeout=4, limit_time=5):
        try:
            url = 'https://jxnu.huitu.zhishulib.com/Seat/Index/bookSeats?LAB_JSON=1'
            data = {
                'beginTime': str(beginTime),
                'duration': str(duration),
                r'seats[0]': str(seats),
                r'seatBookers[0]': str(seatBookers),
            }
            # print(data)
            '''
            beginTime: 1563930000
            duration: 10800
            seats[0]: 26746
            seatBookers[0]: 104489
            '''
            wb_data = self.__session.post(url, data, timeout=timeout)
            if wb_data.status_code == requests.codes.ok:
                print(wb_data.json())
                return wb_data.json()
            else:
                if str(wb_data.status_code) == '404':
                    print('404', wb_data)
                    print(wb_data.json())
                    print(data)
                    return None
                else:
                    print('not 404', wb_data)
                    time.sleep(1.1)
                    return self.grab_seat(duration=duration, seats=seats, seatBookers=seatBookers, beginTime=beginTime,timeout=timeout, limit_time=limit_time)
        except:
            limi_time = limit_time - 1
            if limi_time <= 0:
                print('抢座超时，不再重试')
                return None
            time.sleep(1.1)
            if timeout < 9:
                timeout_new = timeout + 1
            else:
                timeout_new = timeout
            return self.grab_seat(duration=duration, seats=seats, seatBookers=seatBookers, beginTime=beginTime,timeout=timeout_new, limit_time=limi_time)

    def grab_best_seat(self,seatBookers, begin_year, begin_month, begin_day,begin_hour=7, room=2, student_count=1, duration_hour=15):
        beginTime = datetime.datetime(begin_year, begin_month, begin_day, begin_hour)
        beginTime = int(time.mktime(beginTime.timetuple()))
        seat_data = self.get_seat_list(beginTime=beginTime, student_count=student_count, room=room, hours=duration_hour)
        best_seat_id = seat_data['data']['bestPairSeats']['seats'][0]['id']
        title = seat_data['data']['bestPairSeats']['seats'][0]['title']
        print('最佳位置id: ', best_seat_id, ',开始抢座......')
        time.sleep(1.1)
        r = self.grab_seat(duration=duration_hour * 3600, seatBookers=seatBookers, beginTime=beginTime, seats=best_seat_id)
        if r:
            print('抢座完毕，座位号：{0}'.format(title))
        else:
            print('抢最佳位置失败！')
        return r


def tomorrow_grab_best_seat(username,password,start_hour,duration_hour,room):
    spider=Spider(username=username,password=password)
    seatBookers=spider.login()

    now = datetime.datetime.now()
    if now.hour>=22:
        start_grab_time = datetime.datetime.strptime("{0}-{1}-{2} 22:00:00".format(now.year, now.month, now.day+1),"%Y-%m-%d %H:%M:%S")
    else:
        start_grab_time = datetime.datetime.strptime("{0}-{1}-{2} 22:00:00".format(now.year, now.month, now.day),"%Y-%m-%d %H:%M:%S")
    clock = math.ceil((start_grab_time - now).total_seconds())
    print('现在是：{0}，{1}秒后开始预约..'.format(now, clock))
    time.sleep(clock)
    print('开始抢座..')

    while True:
        data=spider.grab_best_seat(seatBookers=seatBookers,begin_year=now.year,begin_month=now.month,begin_day=now.day+1,begin_hour=start_hour,room=room,student_count=1,duration_hour=duration_hour)
        try:
            if data['DATA']['result'] == 'success':
                print('抢座成功！')
                break
            elif data['DATA']['result'] == 'fail':
                try:
                    if data['DATA']['msg'] == '超出可预约座位时间范围':
                        print('时间未到！1秒后重试..')
                        time.sleep(1.1)
                    else:
                        print('抢座失败！退出')
                        print(data)
                        break
                except:
                    print('抢座失败！退出')
                    print(data)
                    break
        except:
            print("异常，data['DATA']['result']下标越界")
            print(data)
            print('正在重试..')
            time.sleep(1.1)

    print('抢座结束。')


if __name__ == '__main__':
    tomorrow_grab_best_seat(username='201623333333', password='23333333', start_hour=7, duration_hour=15, room=1)






