import discord
import yt_dlp
import asyncio
 
# Your bot's token
TOKEN = 'token removed for security, add in when run
 
# Create a Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
 
# Initialize yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
 
# Function to download audio from a YouTube link
async def download_youtube_audio(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        audio_url = info['url']
 
        return title, audio_url
 
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
 
@client.event
async def on_message(message):
    # Check if the message is in the desired channel and contains a valid YouTube link
    if message.channel.name == 'general':
        if 'youtube.com' in message.content or 'youtu.be' in message.content:
            await message.channel.send("Processing...")
 
            try:
                # Download the audio
                title, audio_url = await asyncio.to_thread(download_youtube_audio, message.content)
 
                # Send the audio file to the channel
                await message.channel.send(f"Audio from '{title}' is ready:", file=discord.File(audio_url))
            except Exception as e:
                await message.channel.send(f"An error occurred: {e}")
 
# Start the bot
client.run(TOKEN)
 
