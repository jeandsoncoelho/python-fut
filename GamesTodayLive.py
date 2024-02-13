# %%
import requests
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from telegram import Bot
import asyncio
import time

headers = {
    "authority": "api.sofascore.com",
    "Accept": "*/*",
    "Accept-Language": "en-Us,en,q=0.9",
    "Cache-Control": "max-age=0",
    "dnt": "1",
    "If-None-Match": 'W/"0e064b6941"',
    "Origin": "https://www.sofascore.com",
    "Referer": "https://www.sofascore.com/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
}


async def send_msg(msg):
    bot = Bot(token="6966520329:AAGT11KrihGCNr9gNSFjtBCLYEZ18qRaUZw")
    await bot.send_message(chat_id=-597732178, text=msg)


# %%
sendMessage = []

while True:

    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    # url = "https://api.sofascore.com/api/v1/event/11450125/graph"

    responseIds = requests.get(url, headers=headers)
    dataJsonIds = responseIds.json()
    ids = []
    home = []
    away = []
    homeScore = []
    awayScore = []
    timeGame = []

    for objeto in dataJsonIds["events"]:
        id = objeto["id"]
        homeTeam = objeto["homeTeam"]
        awayTeam = objeto["awayTeam"]
        home.append(homeTeam["name"])
        away.append(awayTeam["name"])
        ids.append(id)
        homeScore.append(objeto["homeScore"]["display"])
        awayScore.append(objeto["awayScore"]["display"])
        startTime = datetime.datetime.fromtimestamp(objeto["startTimestamp"])
        end_time = datetime.datetime.fromtimestamp(objeto["changes"]["changeTimestamp"])
        difference_in_minutes = (end_time - startTime).total_seconds() / 60
        timeGame.append(difference_in_minutes)

    dtLive = pd.DataFrame()
    dtLive["id"] = ids
    dtLive["home"] = home
    dtLive["away"] = away
    dtLive["homeScore"] = homeScore
    dtLive["awayScore"] = awayScore
    dtLive["timeGame"] = timeGame

    for indice, id in enumerate(dtLive["id"]):
        urlEvent = f"https://api.sofascore.com/api/v1/event/{id}/graph"
        responseEvent = requests.get(urlEvent, headers=headers)
        dataJsonEvent = responseEvent.json()

        urlProbability = f"https://api.sofascore.com/api/v1/event/{id}/win-probability"
        responseEventProbability = requests.get(urlProbability, headers=headers)
        dataJsonEventProbability = responseEventProbability.json()

        urlStatistic = f"https://api.sofascore.com/api/v1/event/{id}/statistics"
        responseEventStatistic = requests.get(urlStatistic, headers=headers)
        dataJsonEventStatistic = responseEventStatistic.json()

        minute = []
        value = []
        homeAttack = []
        awayAttack = []
        probalityHome = 0
        probalityAway = 0
        cornersHome = 0
        cornersAway = 0
        gameTime = 0

        if responseEventStatistic.status_code == 200:
            statistics_all = next(
                (
                    s
                    for s in dataJsonEventStatistic["statistics"]
                    if s["period"] == "ALL"
                ),
                None,
            )
            if statistics_all:
                group_tvdata = next(
                    (g for g in statistics_all["groups"] if g["groupName"] == "TVData"),
                    None,
                )
                if group_tvdata:
                    item_corner_kicks = next(
                        (
                            i
                            for i in group_tvdata["statisticsItems"]
                            if i["name"] == "Corner kicks"
                        ),
                        None,
                    )
                    if item_corner_kicks:
                        cornersHome = item_corner_kicks["home"]
                        cornersAway = item_corner_kicks["away"]

        totalCorners = float(cornersHome) + float(cornersAway)

        if responseEventProbability.status_code == 200:
            probalityHome = dataJsonEventProbability["winProbability"]["homeWin"]
            probalityAway = dataJsonEventProbability["winProbability"]["awayWin"]

        if responseEvent.status_code == 200:
            for event in dataJsonEvent["graphPoints"]:
                event_minute = float(event["minute"])
                event_value = float(event["value"])
                minute.append(event_minute)
                value.append(float(event_value))
                gameTime = event_minute
                if event_value > 15:
                    homeAttack.append(event_value)
                if event_value < -15:
                    awayAttack.append(event_value)
            entryMsg = False
            favorityHome = False
            favorityAway = False
            diffAttackPress = 0

            if (len(homeAttack) - len(awayAttack)) < 0:
                diffAttackPress = (len(homeAttack) - len(awayAttack)) * -1
            else:
                diffAttackPress = len(homeAttack) - len(awayAttack)

            if probalityHome > probalityAway:
                favorityHome = True
            else:
                favorityAway = True

            if (
                favorityHome
                and (dtLive["homeScore"][indice] - dtLive["awayScore"][indice]) <= 0
                and diffAttackPress > 10
                and totalCorners > 1
            ):
                entryMsg = True
            if (
                favorityAway
                and (dtLive["awayScore"][indice] - dtLive["homeScore"][indice]) <= 0
                and diffAttackPress > 10
                and totalCorners > 1
            ):
                entryMsg = True

            lastMessage = False    

            for obj in sendMessage:
                if obj.player == dtLive['home'][indice] and obj.time >= 0:
                    obj.time = obj.time - 1
                    lastMessage = True
                elif obj.player == dtLive['home'][indice]:
                    lastMessage = False
                    sendMessage.remove(obj)



            if entryMsg and (gameTime > 30 and gameTime < 45) and lastMessage == False:
                sendMessage.append({"player": dtLive["home"][indice], "time": 3})
                msg = f"Jogo => {dtLive['home'][indice]} {dtLive['homeScore'][indice]} X {dtLive['awayScore'][indice]} {dtLive['away'][indice]}"
                msg += f"\nProbabilidade => {probalityHome}% X {probalityAway}%"
                msg += f"\nPressão => {len(homeAttack)} X {len(awayAttack)}"
                msg += f"\nEscanteios => {totalCorners}"
                msg += f"\nTempo => {round(gameTime)} minutos"
                msg += (
                    f"\n\nhttps://www.bet365.com/?nr=1#/AX/K^{dtLive['home'][indice]}"
                )

                # msg += f"\n===================================================================================================================="
                # Substitua 'CHAT_ID' pelo ID do chat para o qual você deseja enviar a mensagem
                await send_msg(msg)
                print(msg)
            if entryMsg and gameTime > 80 and lastMessage == False:
                sendMessage.append({"player": dtLive["home"][indice], "time": 3})
                msg = f"Jogo => {dtLive['home'][indice]} {dtLive['homeScore'][indice]} X {dtLive['awayScore'][indice]} {dtLive['away'][indice]}"
                msg += f"\nProbabilidade => {probalityHome}% X {probalityAway}%"
                msg += f"\nPressão => {len(homeAttack)} X {len(awayAttack)}"
                msg += f"\nEscanteios => {totalCorners}"
                msg += f"\nTempo => {round(gameTime)} minutos"
                msg += (
                    f"\n\nhttps://www.bet365.com/?nr=1#/AX/K^{dtLive['home'][indice]}"
                )
                # msg += f"\n===================================================================================================================="
                # Substitua 'CHAT_ID' pelo ID do chat para o qual você deseja enviar a mensagem
                await send_msg(msg)
                print(msg)
    time.sleep(60)

# %%
