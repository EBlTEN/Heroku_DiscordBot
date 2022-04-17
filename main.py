import discord
from discord.ext import tasks

import os
from os.path import join, dirname
import json
import datetime
import requests
import sembed
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

client = discord.Client()


@tasks.loop(seconds=1)
async def EqDetect():

    await client.wait_until_ready()

    d = datetime.datetime.now(datetime.timezone(
        datetime.timedelta(hours=9), "JST")).strftime("%Y%m%d%H%M%S")

    try:
        r = requests.get(
            f"http://www.kmoni.bosai.go.jp/webservice/hypo/eew/{int(d) - 2}.json")
        Eq_data = json.loads(r.text)

        if Eq_data["result"]["message"] == "データがありません":
            print(f"{d} Eq no detected")
            pass
        else:
            e = sembed.SEmbed(title=f"震源地{Eq_data['region_name']}{Eq_data['depth']}", description="Description", color=0x7289da,
                              fields=[sembed.SField("最大震度", Eq_data["calcintensity"], True),
                                      sembed.SField("マグニチュード", Eq_data["magunitude"], True), ],
                              author=sembed.SAuthor(f"地震情報"),
                              footer=sembed.SFooter(f"{Eq_data['report_time']} 更新", "https://cdn.discordapp.com/embed/avatars/2.png"))
            await client.get_channel(os.environ.get("CHANNEL")).send(embed=e)

    except json.decoder.JSONDecodeError as err:
        print(err)

EqDetect.start()


client.run(os.environ.get("TOKEN"))
