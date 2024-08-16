import discord
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def blacklist(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Processed {file_path} successfully!")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_member_join(member):
    blacklist('blacklist.json')  

    with open('blacklist.json', 'r') as f:
        blacklist = json.load(f)

    blacklisted_ids = [entry['id'] for entry in blacklist]

    if str(member.id) in blacklisted_ids:
        await member.ban(reason='Blacklisted')
        print(f'Banned {member} because they are blacklisted')

client.run('UrToken')
