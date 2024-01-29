import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def send_to_discord(username, message_text, channel):
    await channel.send(f'{username}: {message_text}')

async def scrape_chat_room(url, keywords, excluded_users, channel):
    # Create a new instance of the Chrome driver (you need to have Chrome installed)
    driver = webdriver.Chrome()

    try:
        # Open the chat room URL
        driver.get(url)

        while scraping_enabled:
            # Wait for new chat messages to load (adjust the timeout if needed)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'kiwi-messagelist-message')))

            # Extract and print new chat messages with usernames and messages
            chat_entries = driver.find_elements(By.CLASS_NAME, 'kiwi-messagelist-message')
            for entry in chat_entries:
                username_element = entry.find_element(By.CLASS_NAME, 'kiwi-messagelist-nick')
                message_text_element = entry.find_element(By.CLASS_NAME, 'message-text')

                username = username_element.text.strip()
                message_text = message_text_element.text.strip()

                if any(keyword.lower() in message_text.lower() for keyword in keywords):
                    if username.lower() not in map(str.lower, excluded_users):
                        await send_to_discord(username, message_text, channel)

            await asyncio.sleep(30)

    finally:
        driver.quit()

scraping_enabled = False

if __name__ == "__main__":
    chat_room_url = 'https://chat.isexychat.com/?x-utm_source=male&x-utm_term=women&x-utm_content=sex+chat+with+wet+and+ready+women&x-utm_medium=&x-utm_campaign=&server=irc.freechat.zone&nick=JustARandomWhiteDude&channel=&auto=connect#ifap'
    keywords = ['🇱🇰', 'LK', 'SL', 'Sri Lanka', 'Sri Lankan', 'Lankan', 'lanka', 'sinhala', 'kollo', 'kello',]
    excluded_users = ['sahan', 'pradeep', 'lucifer', 'kevinsl', 'hans']

    

    # Add your Discord bot token and channel ID
    BOT_TOKEN = "MTIwMTUwNzA0OTcyMTMxNTM4OA.GeEzpF.Bk1vffdSXK7f4tpSZQH52y-X3wFStNhKXvDJW4"
    CHANNEL_ID = 1201509661963190312  # Replace with your channel ID

    # Import discord module and create a client instance
    import discord
    from discord.ext import commands

    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    @bot.command(name='scrape_start', help='Start scraping the chat room')
    async def scrape_start(ctx):
        global scraping_enabled
        if not scraping_enabled:
            scraping_enabled = True
            await ctx.send('Scraping started...')
            await scrape_chat_room(chat_room_url, keywords, excluded_users, ctx.channel)
        else:
            await ctx.send('Scraping is already in progress.')


    @bot.command(name='scrape_stop', help='Stop the scraping process')
    async def scrape_stop(ctx):
        global scraping_enabled
        scraping_enabled = False
        await ctx.send('Scraping stopped.')

    @bot.event
    async def on_ready():
        print('Bot is ready!')

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello there!')

    @bot.command(name='change_url', help='Change the chat room URL')
    async def change_url(ctx, new_url: str):
        global chat_room_url
        chat_room_url = new_url
        await ctx.send(f'Chat room URL changed to: {new_url}')

    @bot.command(name='exclude_add', help='Add a user to the excluded list')
    async def exclude_add(ctx, user: str):
        user_lower = user.lower()
        if user_lower not in map(str.lower, excluded_users):
            excluded_users.append(user_lower)
            await ctx.send(f'User {user} added to the excluded list.')
        else:
            await ctx.send(f'User {user} is already in the excluded list.')

    @bot.command(name='exclude_remove', help='Remove a user from the excluded list')
    async def exclude_remove(ctx, user: str):
        user_lower = user.lower()
        if user_lower in map(str.lower, excluded_users):
            excluded_users.remove(user_lower)
            await ctx.send(f'User {user} removed from the excluded list.')
        else:
            await ctx.send(f'User {user} is not in the excluded list.')

    @bot.command(name='keyword_add', help='Add a keyword to the keyword list')
    async def keyword_add(ctx, keyword: str):
        keyword_lower = keyword.lower()
        if keyword_lower not in map(str.lower, keywords):
            keywords.append(keyword_lower)
            await ctx.send(f'Keyword {keyword} added to the keyword list.')
        else:
            await ctx.send(f'Keyword {keyword} is already in the keyword list.')

    @bot.command(name='keyword_remove', help='Remove a keyword from the keyword list')
    async def keyword_remove(ctx, keyword: str):
        keyword_lower = keyword.lower()
        if keyword_lower in map(str.lower, keywords):
            keywords.remove(keyword_lower)
            await ctx.send(f'Keyword {keyword} removed from the keyword list.')
        else:
            await ctx.send(f'Keyword {keyword} is not in the keyword list.')

    # Run the bot with the specified token
    bot.run(BOT_TOKEN)
