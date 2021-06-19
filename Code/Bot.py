# Imports
# Discord
from discord.ext.commands.core import command
from discord import channel, colour
from aiohttp.client import request
from discord.ext import commands
import requests
import discord

# Github
from github import Github

# Youtube
from youtubesearchpython.internal.constants import VideoDurationFilter
import youtubesearchpython as ytsearch
from pytube import YouTube
from bs4 import BeautifulSoup
from lxml import etree
import urllib
import sys

# Other
from numpy import random as rand
from pprint import pprint
import linecache
import aiohttp
import random
import json
import os


# API Url's
giphyURL = "http://api.giphy.com/v1/gifs/search"

# Command Initialization
bot = commands.Bot(command_prefix=';')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Sandbox -----------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def test(ctx, user: discord.Member, arg2):
    if arg2:
        await ctx.send(user.mention + ' ' + arg2)
    else:
        await ctx.send('You dumbass, this command requires two arguments')


# Random meme responses ---------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:  # skip bot messages
        return

    # write all possible words in lower case. 
    if message.content.lower() in ['wall']:
        await message.channel.send('https://cdn.discordapp.com/attachments/767899814402326559/854588332247744572/1596575456116-1.png')
        
    if message.content.lower() in ['bradley']:
        await message.channel.send('https://cdn.discordapp.com/attachments/630596126344609793/854344671279054908/VID_20200622_191526_839.mp4')
        
    if message.content.lower() in ['rekt']:
        await message.channel.send('https://cdn.discordapp.com/attachments/630596126344609793/854004996801298433/iqlr99et24571.jpg')
        
    if message.content.lower() in ['response to kai']:
        await message.channel.send('https://tenor.com/view/cry-about-it-cat-hoverboard-cat-on-hoverboard-cry-gif-21748938')
        
    if message.content.lower() in ['yes']:
        await message.channel.send('https://tenor.com/view/yes-chad-gif-18386674')
        
    if message.content.lower() in ['rage']:
        await message.channel.send('https://tenor.com/view/rage-dog-smash-keyboard-gaming-gif-21319862')
        
    if message.content.lower() in ['who']:
        await message.channel.send('cares')
        
    if message.content.lower() in ['goodnight', 'gn']:
        await message.channel.send('https://cdn.discordapp.com/attachments/586797838458028034/855737692334850068/Snapchat-1984710211.jpg')
        
    if message.conetnt.lower() in ['weed']:
        await message.channel.send('https://cdn.discordapp.com/attachments/628658329899499563/825228862198644758/eeeTHALLISc4ra1_1275649121454624768480P_1.mp4')

    await bot.process_commands(message)  # to allow other commands
    

# Giphy Implementation ----------------------------------------------------------------------------------------------------------------------------
giphyKey = linecache.getline('Fonzie-Bot\Authentication Keys\Authentication.txt', 17).rstrip()

@bot.command(pass_context=True)
async def giphy(ctx, *, search):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    # If the search is empty return a random gif
    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=' + giphyKey)
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    elif search != '': # If the search is not empty then implement it into the search url
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=' + giphyKey + '&limit=10')
        data = json.loads(await response.text())
        gif_choice = rand.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()
    await ctx.send(embed=embed)


# Detector ----------------------------------------------------------------------------------------------------------------------------------------
detectorAnswers = ['ITS OFF THE SCALE!!!', 'Its getting a bit sus my guy.', 'None Detected.']

@bot.command()
async def detect(ctx, user: discord.Member, arg):
    randNum = rand.randint(3)
    if user:
        random.seed(user.id)
        if randNum == 0:
            # await ctx.send("hello, {}".format(user.mention))
            await ctx.send('{}\'s {}: {}'.format(user.mention, arg, detectorAnswers[0]))
        elif randNum == 1:
            # await ctx.send("goodbye, {}".format(user.mention))
            await ctx.send('{}\'s {}: {}'.format(user.mention, arg, detectorAnswers[1]))
        elif randNum == 2:
            # await ctx.send("goodbye, {}".format(user.mention))
            await ctx.send('{}\'s {}: {}'.format(user.mention, arg, detectorAnswers[2]))
    else:
        await ctx.send('You have to mention someone numnutz')
    

# GitHub API --------------------------------------------------------------------------------------------------------------------------------------
githubAPIToken = linecache.getline('Fonzie-Bot\Authentication Keys\Authentication.txt', 20).rstrip()
github = Github(githubAPIToken)

@bot.command()
async def botstatus(ctx):
    await ctx.send("https://github.com/Shrewkin/Fonzie-Bot/commit/main")

@bot.command()
async def git(ctx, keyword):
    for repo in github.search_repositories(keyword):
        await ctx.send('I found a repo that matches your keyword: https://github.com/{}'.format(repo.full_name))
        break
    
@bot.command()
async def gituser(ctx, keyword):
    url = 'https://api.github.com/users/{}'.format(keyword)
    urlData = requests.get(url).json()
    if ('html_url' not in urlData):
        await ctx.send('Github has no record of the username ' + keyword)
    else:
        await ctx.send('{}'.format(urlData['html_url']))


# Youtube API -------------------------------------------------------------------------------------------------------------------------------------
@bot.command()
async def searchvideo(ctx, keyword):
    videosSearch = ytsearch.VideosSearch('NoCopyrightSounds', limit = 2)
    print(videosSearch.result())
    await ctx.send('https://www.youtube.com/watch?v={}'.format(videosSearch.result['id']))
    
def fetch_titles(url):
    video_titles = []
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html5lib")
    # print(soup.find_all('script'))
    counter = 0
    jsonFile = ''
    for scripts in soup.find_all('script'):
        counter += 1
        if counter == 33:
            print(scripts)
            jsonFile = scripts
            print(jsonFile["responseContext"]["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]["tabRenderer"]["endpoint"]["content"]["sectionListRenderer"]["contents"]["sectionListRenderer"]["contents"]["itemSectionRenderer"]["contents"]["gridRenderer"]["videoId"])
    
    # # What the fuck even is this, trying to parse youtube data I ripped is a nightmare
    # print("beginning")
    # for ytInitialData in soup.find_all("ytInitialData"):
    #     print("pretest")
    #     for responseContext in soup.find_all("responseContext"):
    #         print("test")
    #         for contents in soup.find_all("contents"):
    #             print("test1")
    #             for twoColumnBrowseResultsRenderer in soup.find_all("twoColumnBrowseResultsRenderer"):
    #                 print("test2")
    #                 for tabs in soup.find_all("tabs"):
    #                     print("test3")
    #                     for tabRenderer in soup.find_all("tabRenderer"):
    #                         print("test4")
    #                         for endpoint in soup.find_all("endpoint"):
    #                             print("test5")
    #                             for content in soup.find_all("content"):
    #                                 print("test6")
    #                                 for sectionListRenderer in soup.find_all("sectionListRenderer"):
    #                                     print("test7")
    #                                     for contents in soup.find_all("contents"):
    #                                         print("test8")
    #                                         for itemSectionRenderer in soup.find_all("itemSectionRenderer"):
    #                                             print("test9")
    #                                             for contents in soup.find_all("contents"):
    #                                                 print("test10")
    #                                                 for gridRenderer in soup.find_all("gridRenderer"):
    #                                                     print("test11")
    #                                                     for videoId in soup.find_all("videoId"):
    #                                                         print(videoId)
                                                    
    for entry in soup.find_all("videoId"):
        for link in entry.find_all("videoId"):
            youtube = etree.HTML(urllib.request.urlopen(link["href"]).read()) 
            video_title = youtube.xpath("//span[@id='eow-title']/@title") 
            if len(video_title) > 0:
                video_titles.append({"title":video_title[0], "url":link.attrs["href"]})
    return video_titles
    
@bot.event
async def on_message(message):
    if message.author == bot.user:  # skip bot messages
        return

    if message.content.lower() in ['saturday']:        
        url = 'https://www.youtube.com/channel/UCKAXX-M_naEMD491kiqntBA/videos'
        keyword = 'Saturday'
        videoTitles = fetch_titles(url)
        for video in videoTitles:
            if video['title'].__contains__(keyword):
                await message.channel.send(video['url'])
                break

    await bot.process_commands(message)  # to allow other commands


# Joke Commands -----------------------------------------------------------------------------------------------------------------------------------

#Credit: AustinJacob
@bot.command()
async def penis(ctx, *users: discord.Member):
    dongs = {}
    msg = ""
    state = random.getstate()

    for user in users:
        random.seed(user.id)
        if user.id == 245063782924156929:
            dongs[user] = "8{}D".format("=" * 40)
        else:
            dongs[user] = "8{}D".format("=" * random.randint(0, 30))

    random.setstate(state)
    dongs = sorted(dongs.items(), key=lambda x: x[1])

    for user, dong in dongs:
        msg += "**{}'s size:**\n{}\n".format(user.display_name, dong)
    await ctx.send(msg)

# Code to get token for bot -----------------------------------------------------------------------------------------------------------------------
token = linecache.getline('Fonzie-Bot\Authentication Keys\Authentication.txt', 8).rstrip()

bot.run(token)