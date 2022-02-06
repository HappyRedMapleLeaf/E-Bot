import datetime
from discord.utils import get #for getting roles, may be used in other places too
from discord.ext import commands
from keep_alive import keep_alive #keeping bot online
import os, discord, sys, traceback, csv, u #import secrets, stop program, error logs, read csv's

intents = discord.Intents.none() #telling the bot what it has access to knowing
intents.guilds = intents.members = intents.messages = True
ebot = commands.Bot(command_prefix='[e]', intents=intents, help_command=None)

@ebot.event
async def on_ready():
  #==================
  #INITIALIZING STUFF
  #==================
  #number of 2000 e's already done
  ebot.num2k = 5
  ebot.num2k2 = 0

  #ch for channel
  ebot.ch_contrib_top = ebot.get_channel(888589114235035658)
  ebot.ch_talking = ebot.get_channel(847636238902231093)
  ebot.ch_milestone = ebot.get_channel(848930857142321192)
  ebot.ch_announcement = ebot.get_channel(867487237171314729)
  ebot.ch_logs = ebot.get_channel(850143273871343637)
  ebot.ch_e = ebot.get_channel(917576837524234260)
  ebot.ch_e2 = ebot.get_channel(851162992552050728)
  ebot.ch_mistakes = ebot.get_channel(926679603072892938)
  ebot.ch_commands = ebot.get_channel(926678541347749948)

  #switching
  ebot.suspended = False
  ebot.ch_e_next = ebot.get_channel(919332753093308446)
  ebot.ch_e2_next = ebot.get_channel(897215858642939954)

  #m for message
  ebot.m_contrib_top = await ebot.ch_contrib_top.fetch_message(889251193258385459)
  ebot.m_e_latest_logged = await ebot.ch_e.fetch_message(u.get_latest(2))
  ebot.m_e_latest_contrib = await ebot.ch_e.fetch_message(u.get_latest(3))
  ebot.m_e2_latest_logged = await ebot.ch_e2.fetch_message(u.get_latest(4))

  #p for previous logged message in the e chain
  ebot.p_id = ebot.m_e_latest_logged.id
  ebot.p_length = len(ebot.m_e_latest_logged.content)
  ebot.p_author = ebot.m_e_latest_logged.author
  ebot.p_date = u.adj_date(ebot.m_e_latest_contrib.created_at)

  #2 for second chain
  ebot.p_id2 = ebot.m_e2_latest_logged.id
  ebot.p_length2 = len(ebot.m_e2_latest_logged.content)
  ebot.p_author2 = ebot.m_e2_latest_logged.author

  ebot.guild = ebot.get_guild(int(os.environ['GUILD_ID']))
  #r for role
  ebot.r_slaves = get(ebot.guild.roles, id=847648262294863892)

  ebot.processing = False
  
  #sets status
  await ebot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ᴛʜᴇ ᴇ ʟᴏʀᴅ’s ᴄᴏᴍᴍᴀɴᴅs"))

  #checking missed contributions
  unrecorded_messages_1 = await ebot.ch_e.history(limit=None,after=ebot.m_e_latest_logged).flatten()
  still_correct = True
  for m in unrecorded_messages_1:
    if still_correct:
      if await check_correct(m) == 0:
        #log and milestone
        await ebot.ch_logs.send(f"**_Primary Chain_** --- Good message with {ebot.p_length + 1 + ebot.num2k * 2000} E's by {m.author.name}")
        print(f"**_Primary Chain_** --- Good message with {ebot.p_length + 1 + ebot.num2k * 2000} E's by {m.author.name}")
        ebot.m_e_latest_logged = m
        u.set_latest(2, m.id)

        await record_contribution(m)

        if ebot.p_length + 1 == 1000 or ebot.p_length + 1 == 2000:
          await ebot.ch_milestone.send(f'**{ebot.num2k * 2000 + ebot.p_length + 1}ᴛʜ ᴇ** - <@{m.author.id}> ({m.jump_url})')
        if ebot.p_length + 1 == 1420 and ebot.num2k == 34:
          await ebot.ch_milestone.send(f'**69420ᴛʜ ᴇ** - <@{m.author.id}> ({m.jump_url})')
        
        #change previous info
        ebot.p_id = m.id
        ebot.p_length = len(m.content)
        ebot.p_author = m.author
      else:
        still_correct = False
        await m.delete()
    else:
      await m.delete()
      await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Bot startup chain fix")
      await ebot.ch_mistakes.send(f"<@{m.author.id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ᴡʜɪʟᴇ ᴛʜᴇ ʙᴏᴛ ᴡᴀs ᴅᴏᴡɴ, sᴏᴍᴇʙᴏᴅʏ ʙᴇғᴏʀᴇ ʏᴏᴜ ᴍᴇssᴇᴅ ᴜᴘ ᴛʜᴇ ᴄʜᴀɪɴ. ᴀʟʟ ᴛʜᴇ sᴜʙsᴇᴏ̨ᴜᴇɴᴛ ᴍᴇssᴀɢᴇs ʜᴀᴅ ᴛᴏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ.")
    
  if ebot.p_length == 2000:
    await switch_channel(1)

  #same thing for secondary chain
  unrecorded_messages_2 = await ebot.ch_e2.history(limit=None,after=ebot.m_e2_latest_logged).flatten()
  still_correct2 = True
  for m in unrecorded_messages_2:
    if still_correct2:
      if await check_correct2(m) == 0:
        #log
        await ebot.ch_logs.send(f"**_Secondary Chain_** --- Good message with {ebot.p_length2 + 1 + ebot.num2k2 * 2000} E's by {m.author.name}")
        print(f"**_Secondary Chain_** --- Good message with {ebot.p_length2 + 1 + ebot.num2k2 * 2000} E's by {m.author.name}")
        ebot.m_e2_latest_logged = m
        u.set_latest(4, m.id)
        
        #change previous info
        ebot.p_id2 = m.id
        ebot.p_length2 = len(m.content)
        ebot.p_author2 = m.author
      else:
        still_correct2 = False
        await m.delete()
    else:
      await m.delete()
      await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Bot startup chain fix")
      await ebot.ch_mistakes.send(f"<@{m.author.id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ᴡʜɪʟᴇ ᴛʜᴇ ʙᴏᴛ ᴡᴀs ᴅᴏᴡɴ, sᴏᴍᴇʙᴏᴅʏ ʙᴇғᴏʀᴇ ʏᴏᴜ ᴍᴇssᴇᴅ ᴜᴘ ᴛʜᴇ ᴄʜᴀɪɴ. ᴀʟʟ ᴛʜᴇ sᴜʙsᴇᴏ̨ᴜᴇɴᴛ ᴍᴇssᴀɢᴇs ʜᴀᴅ ᴛᴏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ.")
    
  if ebot.p_length2 == 2000:
    await switch_channel(2)

  print(u.adj_datetime(datetime.datetime.now()))
  print('Logged in as {0.user}'.format(ebot))
  u.log("started")

@ebot.command()
async def mycontribs(ctx):
  await ctx.send(f"<@{ctx.author.id}> ʜᴀs {int(u.get_members(ctx.author.id, 2))} ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴs sɪɴᴄᴇ ʟᴀsᴛ ᴜᴘᴅᴀᴛᴇᴅ.")
@mycontribs.error
async def mycontribs_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]mycontribs")

@ebot.command()
async def help(ctx):
  with open('help.txt') as f:
    await ctx.send(''.join(f.readlines()))
@help.error
async def help_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]help")

@ebot.command()
async def total(ctx):
  await ctx.send(f"{ebot.p_length + ebot.num2k * 2000} ᴛᴏᴛᴀʟ ᴇ's ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴏɴᴇ sᴏ ғᴀʀ.")
@total.error
async def total_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]total")

@ebot.command()
async def total2(ctx):
  await ctx.send(f"{ebot.p_length2 + ebot.num2k2 * 2000} ᴛᴏᴛᴀʟ ᴇ²'s ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴏɴᴇ sᴏ ғᴀʀ.")
@total2.error
async def total2_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]total2")

@ebot.command()
async def contribs(ctx, name, discriminator):
  userid = get(ebot.get_all_members(), name=name, discriminator=discriminator).id
  await ctx.send(f"ᴜsᴇʀ {ebot.get_user(userid)} ʜᴀs {int(u.get_members(userid, 2))} ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴs sɪɴᴄᴇ ʟᴀsᴛ ᴜᴘᴅᴀᴛᴇᴅ.")
@contribs.error
async def contribs_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]contribs <username> <discriminator (4 digits without #)>")

@ebot.command()
async def idcontribs(ctx, *, arg):
  await ctx.send(f"ᴜsᴇʀ {ebot.get_user(int(arg))} ʜᴀs {int(u.get_members(int(arg), 2))} ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴs sɪɴᴄᴇ ʟᴀsᴛ ᴜᴘᴅᴀᴛᴇᴅ.")
@idcontribs.error
async def idcontribs_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]idcontribs <userid>")

@ebot.command()
async def today(ctx):
  if ebot.p_date < u.adj_date(datetime.datetime.now()):
    await ctx.send("0 ᴇ's ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴏɴᴇ ᴛᴏᴅᴀʏ sᴏ ғᴀʀ!")
  else:
    await ctx.send(f"{int(u.get_latest(5))} ᴇ's ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴏɴᴇ ᴛᴏᴅᴀʏ sᴏ ғᴀʀ!")
@today.error
async def today_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]today")

@ebot.command()
async def pastdaily(ctx, year, month, day):
  if datetime.date(int(year), int(month), int(day)) == u.adj_date(datetime.datetime.now()):
    await ctx.send("ᴜsᴇ [e]today ғᴏʀ ᴛᴏᴅᴀʏ's ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴs.")
    return
  yeartext = year + "-" + month.rjust(2, "0") + "-" + day.rjust(2, "0")
  with open('daily.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      if row[0] == yeartext:
        await ctx.send(f"{row[1]} ᴇ's ᴡᴇʀᴇ ᴅᴏɴᴇ ᴏɴ {yeartext}.")
        return
  await ctx.send(f"0 ᴇ's ᴡᴇʀᴇ ᴅᴏɴᴇ ᴏɴ {yeartext}.")
@pastdaily.error
async def pastdaily_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]pastdaily <YYYY> <MM> <DD>")

@ebot.command()
async def allcontribs(ctx):
  all = ""
  with open('members.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      try:
        all += ebot.get_user(int(row[0])).name + '#' + ebot.get_user(int(row[0])).discriminator + ", " + row[1] + "\n"
      except:
        all += "Unknown User " + row[0] + ", " + row[1] + "\n"
  with open('list.txt', 'w') as f:
    f.write(all)
  await ctx.send(file=discord.File("list.txt"), content="ᴍᴇᴍʙᴇʀ ʟɪsᴛ:")
@allcontribs.error
async def allcontribs_error(ctx, error):
  await ctx.send("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ. [e]allcontribs")

@ebot.event
async def on_message(m):
  if m.channel == ebot.ch_commands:
    await ebot.process_commands(m)

  if m.channel == ebot.ch_e_next and ebot.suspended == True and m.content == "E":
    #record singular contribution
    u.add_contrib(m.author.id)
    #change latest logged and contributed e to new e
    #no need to change m_e_latest or whatever because the program is about to exit
    u.set_latest(2, m.id)
    u.set_latest(3, m.id)
    #add a daily
    u.set_latest(5, int(u.get_latest(5)) + 1)
    #stop the program
    sys.exit("waiting for manual next primary channel work")

    #me: change ebot.num2k, ch_e, ch_e_next
    #run the program
    #unlock new channel, message announcements
  
  if m.channel == ebot.ch_e2_next and ebot.suspended == True and m.content == "ᴇ":
    #change latest logged e to new e
    u.set_latest(4, m.id)
    #stop the program
    sys.exit("waiting for manual next secondary channel work")

    #me: change ebot.num2k2, ch_e2, ch_e2_next
    #run the program
    #unlock new channel, message announcements

  if m.channel == ebot.ch_e and ebot.suspended == False:
    if await check_correct(m) == 0:
      ebot.processing = True
      #log and milestone
      await ebot.ch_logs.send(f"**_Primary Chain_** --- Good message with {ebot.p_length + 1 + ebot.num2k * 2000} E's by {m.author.name}")
      print(f"**_Primary Chain_** --- Good message with {ebot.p_length + 1 + ebot.num2k * 2000} E's by {m.author.name}")
      ebot.m_e_latest_logged = m
      u.set_latest(2, m.id)

      if ebot.p_length + 1 == 1000 or ebot.p_length + 1 == 2000:
        await ebot.ch_milestone.send(f'**{ebot.num2k * 2000 + ebot.p_length + 1}ᴛʜ ᴇ** - <@{m.author.id}> ({m.jump_url})')
      if ebot.p_length + 1 == 1420 and ebot.num2k == 34:
        await ebot.ch_milestone.send(f'**69420ᴛʜ ᴇ** - <@{m.author.id}> ({m.jump_url})')
      
      #change previous info
      ebot.p_id = m.id
      ebot.p_length = len(m.content)
      ebot.p_author = m.author

      await record_contribution(m)

      if ebot.p_length == 2000:
        await switch_channel(1)
    else:
      await m.delete()

  
  if m.channel == ebot.ch_e2 and ebot.suspended == False:
    if await check_correct2(m) == 0:
      ebot.processing = True
      #log and milestone
      await ebot.ch_logs.send(f"**_Secondary Chain_** --- Good message with {ebot.p_length2 + 1 + ebot.num2k2 * 2000} E's by {m.author.name}")
      print(f"**_Secondary Chain_** --- Good message with {ebot.p_length2 + 1 + ebot.num2k2 * 2000} E's by {m.author.name}")
      ebot.m_e2_latest_logged = m
      u.set_latest(4, m.id)

      #change previous info
      ebot.p_id2 = m.id
      ebot.p_length2 = len(m.content)
      ebot.p_author2 = m.author

      if ebot.p_length2 == 2000:
        await switch_channel(2)
    else:
      await m.delete()

  ebot.processing = False


async def lock_chains(lock): #if lock is false then unlocks chains
  perms = ebot.ch_e.overwrites_for(ebot.r_slaves)
  perms2 = ebot.ch_e2.overwrites_for(ebot.r_slaves)

  if lock:
    perms.send_messages = False
    perms2.send_messages = False
  else:
    perms.send_messages = True
    perms2.send_messages = True

  await ebot.ch_e.set_permissions(ebot.r_slaves, overwrite=perms)
  await ebot.ch_e2.set_permissions(ebot.r_slaves, overwrite=perms2)

async def switch_channel(chain):
  if chain == 1:
    await ebot.ch_announcement.send("Cᴏɴɢʀᴀᴛs! Aɴᴏᴛʜᴇʀ 2000 E's ʜᴀᴠᴇ ʙᴇᴇɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴛʜᴇ ɴᴇxᴛ E ᴄʜᴀɴɴᴇʟ ɪs sᴇᴛ ᴜᴘ (ᴍᴀx 1 ᴡᴇᴇᴋ, ᴘʀᴏʙᴀʙʟʏ ᴡɪᴛʜɪɴ 1 ᴅᴀʏ).")
    await ebot.get_user(int(os.environ['HRML_ID'])).send("Another 2000 E's completed. Do da things!!")
  elif chain == 2:
    await ebot.ch_announcement.send("Cᴏɴɢʀᴀᴛs! Aɴᴏᴛʜᴇʀ 2000 E²'s ʜᴀᴠᴇ ʙᴇᴇɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴛʜᴇ ɴᴇxᴛ E² ᴄʜᴀɴɴᴇʟ ɪs sᴇᴛ ᴜᴘ (ᴍᴀx 1 ᴡᴇᴇᴋ, ᴘʀᴏʙᴀʙʟʏ ᴡɪᴛʜɪɴ 1 ᴅᴀʏ).")
    await ebot.get_user(int(os.environ['HRML_ID'])).send("Another 2000 E²'s completed. Do da things!!")

  await lock_chains(True)
  ebot.suspended = True

async def record_contribution(m):
  if u.get_members(m.author.id, 2) == -1:
    u.add_member(m.author.id)
    oldContribs = 0
  else:
    oldContribs = int(u.get_members(m.author.id, 2))

  if ebot.p_date < u.adj_date(m.created_at):
    u.add_daily(ebot.p_date, u.get_latest(5))
    u.log('daily added')
    u.set_latest(5, 1)
  else:
    u.set_latest(5, int(u.get_latest(5)) + 1)
  ebot.p_date = u.adj_date(m.created_at)

  ebot.m_e_latest_contrib = m
  u.set_latest(3, m.id)
  
  if oldContribs == 0:
    await m.author.add_roles(get(ebot.guild.roles, id=887095372126773249))
    await m.author.remove_roles(get(ebot.guild.roles, id=912096772392890388))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 1 ᴇ! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ɴᴏᴏʙ (𝟷)**")
  if oldContribs == 9:
    await m.author.add_roles(get(ebot.guild.roles, id=887100199498055751))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 10 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ʙᴇɢɪɴɴᴇʀ**")
  if oldContribs == 49:
    await m.author.add_roles(get(ebot.guild.roles, id=887102637797945384))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 50 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ɪɴᴛᴇʀᴍᴇᴅɪᴀᴛᴇ**")
  if oldContribs == 99:
    await m.author.add_roles(get(ebot.guild.roles, id=887103974413582388))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 100 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ᴇxᴘᴇʀᴛ**")
  if oldContribs == 249:
    await m.author.add_roles(get(ebot.guild.roles, id=888250472731934730))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 250 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ᴍᴀsᴛᴇʀ**")
  if oldContribs == 499:
    await m.author.add_roles(get(ebot.guild.roles, id=887106132668194836))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id} ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 500 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ʟᴇɢᴇɴᴅ**")
    
    #debugging
    all = ""
    with open('members.csv') as f:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
        try:
          all += ebot.get_user(int(row[0])).name + '#' + ebot.get_user(int(row[0])).discriminator + ", " + row[1] + "\n"
        except:
          all += "Unknown User " + row[0] + ", " + row[1] + "\n"
    await ebot.get_user(int(os.environ['HRML_ID'])).send(file=discord.File("list.txt"), content="ᴍᴇᴍʙᴇʀ ʟɪsᴛ:")

  if oldContribs == 999:
    await m.author.add_roles(get(ebot.guild.roles, id=887109559712354304))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 1000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ᴍʏᴛʜ**")
  if oldContribs == 1999:
    await m.author.add_roles(get(ebot.guild.roles, id=887109783902113853))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 2000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ɢᴏᴅ**")
  if oldContribs == 4999:
    await m.author.add_roles(get(ebot.guild.roles, id=887110270164557884))
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{m.author.id}> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 5000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **ᴇ ᴍᴀᴅʟᴀᴅ!**")

  #change csv file
  u.add_contrib(m.author.id)

  #sort contributions
  topids, topcontribs = ([] for i in range(2))
  with open('members.csv') as f:
    reader = csv.reader(f, delimiter=',')

    for row in reader:
      topids.append(row[0])
      topcontribs.append(row[1])
  
  #https://www.geeksforgeeks.org/insertion-sort/
  #sort one array and another one in the same order
  for i in range(1, len(topcontribs)):
    key1 = topcontribs[i]
    key2 = topids[i]
    j = i-1
    while j >= 0 and key1 > topcontribs[j] :
      topcontribs[j + 1] = topcontribs[j]
      topids[j + 1] = topids[j]
      j -= 1
    topcontribs[j + 1] = key1
    topids[j + 1] = key2
  
  newtop = "ᴛʜᴇ ᴛᴏᴘ ᴛᴇɴ ᴇ ᴄᴏɴᴛʀɪʙᴜᴛᴏʀs ᴀʀᴇ:\n"
  for i in range(10): #some creative variable names here!
    newtop = newtop + f'{i + 1}) <@{topids[i]}> - {str(topcontribs[i]).rjust(4, "0")}\n'

  await ebot.m_contrib_top.edit(content=newtop)

  #deal with superior E
  superior_role = get(ebot.guild.roles, id=893616839962284042)
  superior = ebot.guild.get_member(int(topids[0]))
  if not superior_role in superior.roles:
    await ebot.ch_talking.send(f"ᴄᴏɴɢʀᴀᴛs <@{topids[0]}> ғᴏʀ ʙᴇᴄᴏᴍɪɴɢ ᴛʜᴇ #1 ᴇ ᴄᴏɴᴛʀɪʙᴜᴛᴏʀ!")
    await superior_role.members[0].remove_roles(superior_role)
    await superior.add_roles(superior_role)



async def check_correct(m):
  author_id = m.author.id
  if m.type != discord.MessageType.default:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Not a normal message type")
    return 1
  elif author_id == ebot.p_author.id:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Same author as previous message")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ sᴇɴᴛ ᴀ ᴍᴇssᴀɢᴇ ᴡʜᴇɴ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ᴡᴀs ᴀʟsᴏ ʏᴏᴜʀs. (ᴅᴏ ɴᴏᴛ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴏᴡɴ E's.)")
    return 2
  elif m.reference == None:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Not replying to a message")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ. ʏᴏᴜ ᴍᴜsᴛ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴄʜᴀɪɴ.")
    return 3
  elif m.reference != None and m.reference.message_id != ebot.p_id:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Replying to the wrong message")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ (ᴘʀᴇᴠɪᴏᴜs) ᴍᴇssᴀɢᴇ.")
    return 4
  elif len(m.content) - m.content.count('E') > 0:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Not all characters are E's")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: sᴏᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡᴇʀᴇ ɴᴏᴛ E's. Bᴇ sᴜʀᴇ ᴛᴏ ᴇʟɪᴍɪɴᴀᴛᴇ ᴀɴʏ ᴡʜɪᴛᴇ sᴘᴀᴄᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴀɴᴅ/ᴏʀ ᴛʏᴘᴏs.")
    return 5
  elif len(m.content) != ebot.p_length + 1:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Wrong number of E's, should be 1 more than " + str(ebot.p_length))
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴡʀᴏɴɢ ɴᴜᴍʙᴇʀ ᴏғ E's. ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ E's sʜᴏᴜʟᴅ ʙᴇ " + str(ebot.p_length + 1) + ".")
    return 6
  elif ebot.processing == True:
    await ebot.ch_logs.send("**_Primary Chain_** --- Deletion: Bot overflow")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ sᴏ ɢᴏᴏᴅ ᴀᴛ ᴇ'ɪɴɢ ᴛʜᴀᴛ ʏᴏᴜ ᴏᴠᴇʀғʟᴏᴡᴇᴅ ᴛʜᴇ ʙᴏᴛ. ɢᴏᴏᴅ ᴊᴏʙ, ʙᴜᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ʜᴀᴅ ᴛᴏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ. sᴏʀʀʏ!")
    return 7
  else:
    return 0

async def check_correct2(m):
  author_id = m.author.id
  if m.type != discord.MessageType.default:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Not a normal message type")
    return 1
  elif author_id == ebot.p_author2.id:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Same author as previous message")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ sᴇɴᴛ ᴀ ᴍᴇssᴀɢᴇ ᴡʜᴇɴ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ᴡᴀs ᴀʟsᴏ ʏᴏᴜʀs. (ᴅᴏ ɴᴏᴛ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴏᴡɴ E's.)")
    return 2
  elif m.reference == None:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Not replying to a message")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ_Secondary ᴛʜᴇ sᴇᴄᴏɴᴅᴀ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ. ʏᴏᴜ ᴍᴜsᴛ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴄʜᴀɪɴ.")
    return 3
  elif m.reference != None and m.reference.message_id != ebot.p_id2:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Replying to the wrong message")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ (ᴘʀᴇᴠɪᴏᴜs) ᴍᴇssᴀɢᴇ.")
    return 4
  elif len(m.content) - (m.content.count('ᴇ') + m.content.count('É') + m.content.count('È') + m.content.count('Ê') + m.content.count('Ë') + m.content.count('Ě') + m.content.count('ɛ') + m.content.count('Ė') + m.content.count('Ĕ') + m.content.count('Ē') + m.content.count('Ę') + m.content.count('Σ')) > 0:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Not all characters are E's")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: sᴏᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡᴇʀᴇ ɴᴏᴛ E's. Bᴇ sᴜʀᴇ ᴛᴏ ᴇʟɪᴍɪɴᴀᴛᴇ ᴀɴʏ ᴡʜɪᴛᴇ sᴘᴀᴄᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴀɴᴅ/ᴏʀ ᴛʏᴘᴏs.")
    return 5
  elif len(m.content) != ebot.p_length2 + 1:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Wrong number of E's, should be 1 more than " + str(ebot.p_length2))
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴡʀᴏɴɢ ɴᴜᴍʙᴇʀ ᴏғ E's. ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ E's sʜᴏᴜʟᴅ ʙᴇ " + str(ebot.p_length2 + 1) + ".")
    return 6
  elif ebot.processing == True:
    await ebot.ch_logs.send("**_Secondary Chain_** --- Deletion: Bot overflow")
    await ebot.ch_mistakes.send(f"<@{author_id}> Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ sᴏ ɢᴏᴏᴅ ᴀᴛ ᴇ'ɪɴɢ ᴛʜᴀᴛ ʏᴏᴜ ᴏᴠᴇʀғʟᴏᴡᴇᴅ ᴛʜᴇ ʙᴏᴛ. ɢᴏᴏᴅ ᴊᴏʙ, ʙᴜᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ʜᴀᴅ ᴛᴏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ. sᴏʀʀʏ!")
    return 7
  else:
    return 0

#error logging
@ebot.event
async def on_error(event, *args, **kwargs): #catches errors but not warnings. be careful of forgetting to await
  u.log(traceback.format_exc())
  raise

keep_alive()
ebot.run(os.getenv('NAHTITOKEN'))