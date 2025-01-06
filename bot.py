# bot.py
import os

import discord
from dotenv import load_dotenv
import json

HEADER = "Recent papers where groups from Munich participated:\n\n"
FOOTER = "\nPlease note that this list may not be exhaustive.\nFor the most up-to-date information, please visit arXiv.\nThanks arXiv for providing the API!"
MAX_LEN = 2000


def json_to_txt(input_json_file, output_txt_file):
    with open(input_json_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    
    with open(output_txt_file, "w", encoding="utf-8") as txt_file:
        list_of_strings = []
        for entry in data:
            s = ""
            s += f"Title: {entry['title']}\n"
            s += f"Authors: {', '.join(entry['authors'])}\n"
            s += f"Publishing_date: {entry['publishing_date']}\n"
            s += f"Link: <{entry['link']}>\n"
            s += "\n"
            list_of_strings.append(s)
        
        txt_file.writelines(list_of_strings)
        return list_of_strings

def up_to_4000(list_of_papers):
    list_of_messages = []
    message = ""
    for paper in list_of_papers:
        if len(paper) + len(message) < MAX_LEN:
            message += paper
        else:
            list_of_messages.append(message)
            if len(paper) < MAX_LEN:
                message = paper
            else:
                message = ""
                print(f"Paper too long to fit in a message: {paper}")
    list_of_messages.append(message)
    return list_of_messages


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID_UPDATE = os.getenv('CHANNEL_ID_UPDATE')
CHANNEL_ID_MUNICH = os.getenv('CHANNEL_ID_MUNICH')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    channel = client.get_channel(CHANNEL_ID_MUNICH)

    if channel:
        input_file = "recent_papers.json"
        output_file = "papers_output.txt"
        l = json_to_txt(input_file, output_file)
        m = up_to_4000(l)
        for i, message in enumerate(m):
            #Just some error handeling for adding header and footer
            if i == 0:
                if len(HEADER) + len(message) <= MAX_LEN:
                    message = HEADER + message
                else:
                    await channel.send(HEADER)
           

            if i == len(m) - 1:
                if len(message) + len(FOOTER) <= MAX_LEN:
                    message = message + FOOTER
                else:
                    if len(FOOTER) <= MAX_LEN:
                        await channel.send(message)
                        await channel.send(FOOTER)
                        continue

            await channel.send(message)
        await client.close()

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
client.run(TOKEN)


