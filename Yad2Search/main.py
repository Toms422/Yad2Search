import requests
import json
import time
from urllib.parse import urlencode
from telegram import Bot, InputMediaPhoto
from io import BytesIO


async def send_message_async(bot, chat_id, message_text):
    await bot.send_message(chat_id=chat_id, text=message_text,parse_mode='Markdown')
    print("Message sent successfully!")


async def main(params,neighborhood,bot,chat_id_Tom,chat_id_Lee):
    TotalCheck=False
    json_file_path = r'.\unique_date_added.json'
    try:
        with open(json_file_path, 'r') as json_file:
            unique_date_added = set(json.load(json_file))
    except FileNotFoundError:
        unique_date_added = set()

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': '__ssds=3; __ssuzjsr3=a9be0cd8e; __uzmaj3=2482bab2-e643-4981-b19f-ca5d3afc7132; __uzmbj3=1687852959; __uzmlj3=PyqZE7dcY4wB1d0cwdis7E=; y2018-2-cohort=87; leadSaleRentFree=82; __uzmb=1687852961; __uzma=1489c434-41b7-4cb2-ba68-54014c40ede2; __uzme=7900; guest_token=eyJhbGciOiJIUz3ZS04ZWQ0LTQ4NDItOTE3YS0zjoxNjg3ODUyOTYxLCJleHAiOjE3MjEwNzY4MTQ4MDN9.15-hRYa5G_B7ASy6lrVllacDfAG8zz08c_riM57i1vs; abTestKey=79; use_elastic_search=1; canary=never; __uzmcj3=105419468535; __uzmdj3=1690528114; __uzmfj3=7; server_env=production; y2_cohort_2020=8; favorites_userid=edd1063272547; __uzmd=; __uzmc=763',
        'Origin': 'https://www.yad2.co.il',
        'Pragma': 'no-cache',
        'Referer': 'https://www.yad2.co.il/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'mainsite_version_commit': '7c9a9c5c1fe45ec28c16bc473d25aad7141f53bd',
        'mobile-app': 'false',
        'sec-ch-ua': 'Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
    }
    # How many new apartment
    count = 0
    for i in range(1):
        base_url = "https://gw.yad2.co.il/feed-search-legacy/realestate/rent"
        params['page'] = i
        # Encode the parameters
        encoded_params = urlencode(params)
        # Construct the final URL
        final_url = f"{base_url}?{encoded_params}"
        time.sleep(1)
        response = requests.get(final_url, headers=headers)


        if response.status_code == 200:
            data = response.json()
            # How many new apartment
            for d in data['data']['feed']['feed_items']:
                try:
                    date_added = d['date_added']
                    if date_added not in unique_date_added:
                        if d['feed_source'] == "private":
                            count = count + 1
                            TotalCheck = True
                except (KeyError, ValueError):
                    pass
    if count>0:
        await send_message_async(bot, chat_id_Tom, f' דירות חדשות בשכונת *{neighborhood}*: {count}')
        await send_message_async(bot, chat_id_Lee, f' דירות חדשות בשכונת *{neighborhood}*: {count}')


    for i in range(3):
        base_url = "https://gw.yad2.co.il/feed-search-legacy/realestate/rent"
        params['page'] = i
        # Encode the parameters
        encoded_params = urlencode(params)
        # Construct the final URL
        final_url = f"{base_url}?{encoded_params}"

        #url = f'https://gw.yad2.co.il/feed-search-legacy/realestate/rent?topArea=2&area=3&city=8600&neighborhood=1647&rooms=2-4&price=0-7000&balcony=1&squaremeter=65--1&page={i}&forceLdLoad=true'
        time.sleep(1)
        response = requests.get(final_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Process the JSON data as needed
            for d in data['data']['feed']['feed_items']:
                try:
                    neighborhood =d['neighborhood']
                except KeyError:
                    neighborhood = None
                try:
                    if d['feed_source']=="private": # דירות לא מתיווך
                        Address = d['title_1']
                        price=d['price']
                        details=d['row_3'][0]+", "+d['row_3'][1]+", "+d['row_3'][2]
                        date_added = d['date_added']
                        if date_added not in unique_date_added:
                            unique_date_added.add(date_added)
                            #apartment=d['date_added'], d['date'], d['price'], d['title_1'], d['line_2'], d['line_1'], d['line_3'],neighborhood
                            await send_message_async(bot, chat_id_Tom, f' *כתובת*: {Address}, *מחיר*: {price}, *פרטים נוספים*:  {details}')
                            await send_message_async(bot, chat_id_Lee,f' *כתובת*: {Address}, *מחיר*: {price}, *פרטים נוספים*:  {details}')
                            await bot.send_location(chat_id=chat_id_Tom, latitude=d['coordinates']['latitude'], longitude=d['coordinates']['longitude'])
                            await bot.send_location(chat_id=chat_id_Lee, latitude=d['coordinates']['latitude'], longitude=d['coordinates']['longitude'])


                            media_items = []
                            check = False
                            for image in d['images']:
                                image_url=d['images'][image]['src']
                                responseImage = requests.get(image_url)
                                image_bytes = BytesIO(responseImage.content)
                                #await bot.send_photo(chat_id=chat_id, photo=image_bytes)
                                media_items.append(InputMediaPhoto(media=image_bytes))
                                check=True
                            if check==True:
                                await bot.send_media_group(chat_id=chat_id_Tom, media=media_items)
                                await bot.send_media_group(chat_id=chat_id_Lee, media=media_items)
                except (KeyError,ValueError):
                    pass
        else:
            print(f"Request failed with status code: {response.status_code}")

        # Save the updated unique_date_added to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(list(unique_date_added), json_file)

    return TotalCheck
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()

    bot_token = '6582907880:AAEgdSSbRRYzsaoMHNxyl5Jsvl8MQYJq53A'
    bot = Bot(token=bot_token)

    # Replace 'YOUR_CHAT_ID' with the actual chat ID
    chat_id_Tom = 660144693
    chat_id_Lee = 5786521242

    # Define the parameters
    #שכונת הראשונים, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params1 = {
        'topArea': 2,
        'area': 3,
        'city': 8600,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 1647,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }

    # גבעתיים שכונת בורכוב, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params2 = {
        'topArea': 2,
        'area': 3,
        'city': 6300,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 355,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # גבעתיים שכונת הל"ה, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params3 = {
        'topArea': 2,
        'area': 3,
        'city': 6300,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 991510,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # שכונת החשמונאים, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params4 = {
        'topArea': 2,
        'area': 3,
        'city': 8600,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 1477,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # גבעתיים שכונת ארלוזורוב, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params5 = {
        'topArea': 2,
        'area': 3,
        'city': 6300,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 1642,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # גבעתיים שכונת גבעת רמבם, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params6 = {
        'topArea': 2,
        'area': 3,
        'city': 6300,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 1643,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # תל אביב נחלת יצחק, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params7 = {
        'topArea': 2,
        'area': 1,
        'city': 5000,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 317,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # תל אביב מונטיפיורי, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params8 = {
        'topArea': 2,
        'area': 1,
        'city': 5000,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 485,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }
    # גבעתיים שכונת קריית יוסף, 2.5-4 חדרים, עד 7000 שקל, כולל מרפסת, לא מתיווך
    params9 = {
        'topArea': 2,
        'area': 3,
        'city': 6300,
        'rooms': '2.5-4',
        'price': '0-7000',
        'balcony': 1,
        'neighborhood': 1644,
        'squaremeter': '65--1',
        'forceLdLoad': True,
    }

    checkNew1=loop.run_until_complete(main(params1,"הראשונים-רג" ,bot,chat_id_Tom,chat_id_Lee))
    checkNew4=loop.run_until_complete(main(params4, "החשמונאים-רג",bot,chat_id_Tom,chat_id_Lee))
    checkNew2=loop.run_until_complete(main(params2,"בורכוב-גבעתיים",bot,chat_id_Tom,chat_id_Lee))
    checkNew3=loop.run_until_complete(main(params3, "הלה-גבעתיים",bot,chat_id_Tom,chat_id_Lee))
    checkNew9=loop.run_until_complete(main(params9, "קריית יוסף-גבעתיים",bot,chat_id_Tom,chat_id_Lee))
    checkNew5=loop.run_until_complete(main(params5, "ארלוזורוב-גבעתיים",bot,chat_id_Tom,chat_id_Lee))
    checkNew6=loop.run_until_complete(main(params6, "גבעת רמבם-גבעתיים",bot,chat_id_Tom,chat_id_Lee))
    checkNew7=loop.run_until_complete(main(params7, "נחלת יצחק-תל אביב",bot,chat_id_Tom,chat_id_Lee))
    checkNew8=loop.run_until_complete(main(params8, "מונטיפיורי-תל אביב",bot,chat_id_Tom,chat_id_Lee))

    if checkNew1==False and checkNew2==False and checkNew3==False and checkNew4==False and checkNew5==False and checkNew6==False and checkNew7==False and checkNew8==False and checkNew9==False:
        loop.run_until_complete(send_message_async(bot, chat_id_Tom, "*אין דירות חדשות*"))
        loop.run_until_complete(send_message_async(bot, chat_id_Lee, "*אין דירות חדשות*"))
