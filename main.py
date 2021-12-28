from datetime import datetime, timedelta #used for printing time
import os, discord, sys #os for importing secrets, discord for obvious reasons, sys for terminating program
from discord.utils import get #for getting roles, may be used in other places too
from keep_alive import keep_alive #for keeping the repl alive

intents = discord.Intents.default() #for getting the guild object from id, idk why its necessary but it is
intents.members = True

ebot = discord.Client(intents=intents)

#number of 2000 e's already done
ebot.num2k = 4
ebot.num2k2 = 0

#https://www.geeksforgeeks.org/insertion-sort/
#for sorting the contributions
def doubleSort(arr1, arr2):
  for i in range(1, len(arr1)):
    key1 = arr1[i]
    key2 = arr2[i]
    j = i-1
    while j >= 0 and key1 > arr1[j] :
      arr1[j + 1] = arr1[j]
      arr2[j + 1] = arr2[j]
      j -= 1
    arr1[j + 1] = key1
    arr2[j + 1] = key2

@ebot.event
async def on_ready():
  ebot.contributions_channel = ebot.get_channel(888589114235035658)
  ebot.contributions_channel2 = ebot.get_channel(888953541778087977)
  ebot.talk_channel = ebot.get_channel(847636238902231093)
  ebot.latest_channel = ebot.get_channel(888591945096658944)

  ebot.e_channel = ebot.get_channel(912101267621441536)
  ebot.next_e_channel = ebot.get_channel(917576837524234260)
  ebot.suspended = False

  ebot.milestone_channel = ebot.get_channel(848930857142321192)
  ebot.announcement_channel = ebot.get_channel(867487237171314729)
  ebot.log_channel = ebot.get_channel(850143273871343637)
  ebot.e2_channel = ebot.get_channel(851162992552050728)
  async for message in ebot.e_channel.history(limit=1):
    ebot.prev_e_id = message.id
  ebot.prev_e_message = await ebot.e_channel.fetch_message(ebot.prev_e_id)
  ebot.prev_e_number = len(ebot.prev_e_message.content)
  ebot.prev_e_author = ebot.prev_e_message.author
  async for message in ebot.e2_channel.history(limit=1):
    ebot.prev_e_id2 = message.id
  ebot.prev_e_message2 = await ebot.e2_channel.fetch_message(ebot.prev_e_id2)
  ebot.prev_e_number2 = len(ebot.prev_e_message2.content)
  ebot.prev_e_author2 = ebot.prev_e_message2.author
  ebot.guild = ebot.get_guild(int(os.environ['GUILD_ID']))
  ebot.unsorted_message = await ebot.contributions_channel2.fetch_message(888954482141048842)
  ebot.sorted_message = await ebot.contributions_channel.fetch_message(889251193258385459)
  ebot.processing = False

  ebot.e_slaves = get(ebot.guild.roles, id=847648262294863892)
  
  await ebot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ᴛʜᴇ ᴇ ʟᴏʀᴅ’s ᴄᴏᴍᴍᴀɴᴅs"))

  #get latest logged message
  ebot.latest_message_message = await ebot.latest_channel.fetch_message(ebot.latest_channel.last_message_id)
  latest_message = await ebot.e_channel.fetch_message(ebot.latest_message_message.content)
  print(latest_message)

  #recording contributions for all messages since latest logged message
  unrecorded_messages = await ebot.e_channel.history(limit=None,after=latest_message).flatten()

  for m in unrecorded_messages:
    numcontributions = 0

    #adding contribution
    new_unsorted = ebot.unsorted_message.content
    numberstart = new_unsorted.find(str(m.author.id)) + 22
    print(m.author.name + " " + str(len(m.content)))
    if numberstart == 21:
      new_unsorted = new_unsorted + "\n<@" + str(m.author.id) + "> - 0001"
      numcontributions = 1
    else:
      number = str(int(new_unsorted[numberstart:numberstart + 4]) + 1)
      new_unsorted = new_unsorted[:numberstart] + number.rjust(4, "0") + new_unsorted[numberstart + 4:]
      numcontributions = int(number)

    #adding roles
    if numcontributions == 1:
      await m.author.add_roles(get(ebot.guild.roles, id=887095372126773249))
      await m.author.remove_roles(get(ebot.guild.roles, id=912096772392890388))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 1 ᴇ! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887095372126773249).name + "**")
    elif numcontributions == 10:
      await m.author.add_roles(get(ebot.guild.roles, id=887100199498055751))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 10 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887100199498055751).name + "**")
    elif numcontributions == 50:
      await m.author.add_roles(get(ebot.guild.roles, id=887102637797945384))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 50 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887102637797945384).name + "**")
    elif numcontributions == 100:
      await m.author.add_roles(get(ebot.guild.roles, id=887103974413582388))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 100 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887103974413582388).name + "**")
    elif numcontributions == 250:
      await m.author.add_roles(get(ebot.guild.roles, id=888250472731934730))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 250 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=888250472731934730).name + "**")
    elif numcontributions == 500:
      await m.author.add_roles(get(ebot.guild.roles, id=887106132668194836))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 500 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887106132668194836).name + "**")
    elif numcontributions == 1000:
      await m.author.add_roles(get(ebot.guild.roles, id=887109559712354304))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 1000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887109559712354304).name + "**")
    elif numcontributions == 2000:
      await m.author.add_roles(get(ebot.guild.roles, id=887109783902113853))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 2000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887109783902113853).name + "**")
    elif numcontributions == 5000:
      await m.author.add_roles(get(ebot.guild.roles, id=887110270164557884))
      await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 5000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887110270164557884).name + "**")
    #strings are 0-indexed

    await ebot.unsorted_message.edit(content=new_unsorted)
    
  #change latest logged message to the latest e
  l = await ebot.e_channel.history(limit=1).flatten()
  await ebot.latest_message_message.edit(content=l[0].id)

  #sort contributions
  c = ebot.unsorted_message.content
  arrECOUNT = [0] * int((len(c) + 1) / 29)
  arrREST = [0] * int((len(c) + 1) / 29)
  new_sorted = ""
  users_in_sorted = 0
  users_in_unsorted = 0
  for i in range(0, len(c), 29):
    arrECOUNT[users_in_unsorted] = int(c[i + 24:i + 28])
    arrREST[users_in_unsorted] = c[i:i + 24]
    users_in_unsorted += 1

  doubleSort(arrECOUNT, arrREST)

  for j in range(0, len(arrECOUNT)):
    if users_in_sorted == 10:
      break
    new_sorted = new_sorted + str(users_in_sorted + 1) + ") " + arrREST[j] + str(arrECOUNT[j]).rjust(4, "0") + "\n"
    users_in_sorted += 1

  await ebot.sorted_message.edit(content=new_sorted)

  print(datetime.now() + timedelta(hours=20))

  print('Logged in as {0.user}'.format(ebot))

@ebot.event
async def on_message(m):
  if m.channel.id == ebot.next_e_channel.id and ebot.suspended == True and m.content == "E":
    #The bot will:
    #record singular contribution
    new_unsorted = ebot.unsorted_message.content
    numberstart = new_unsorted.find(str(m.author.id)) + 22
    print(m.author.name + " " + str(len(m.content)))
    number = str(int(new_unsorted[numberstart:numberstart + 4]) + 1)
    new_unsorted = new_unsorted[:numberstart] + number.rjust(4, "0") + new_unsorted[numberstart + 4:]
    numcontributions = int(number)
    await ebot.unsorted_message.edit(content=new_unsorted)

    #change latest recorded e to new e
    await ebot.latest_message_message.edit(content=m.id)

    #stop the program
    sys.exit("waiting for manual next channel work")

    #I must:
    #change ebot.num2k (numbers of 2000 E's completed)
    #change E_CHANNEL_ID
    #change NEXT_E_CHANNEL_ID
    #run the program
    #unlock new channel
    #message announcements: E channel is back up and running.

  if m.channel.id == ebot.e_channel.id and ebot.suspended == False:
    if m.type != discord.MessageType.default:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Not a normal message type")
      await m.delete()
    elif m.author == ebot.prev_e_author:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Same author as previous message")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ sᴇɴᴛ ᴀ ᴍᴇssᴀɢᴇ ᴡʜᴇɴ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ᴡᴀs ᴀʟsᴏ ʏᴏᴜʀs. (ᴅᴏ ɴᴏᴛ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴏᴡɴ E's.)")
    elif m.reference == None:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Not replying to a message")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ. ʏᴏᴜ ᴍᴜsᴛ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴄʜᴀɪɴ.")
    elif m.reference != None and m.reference.message_id != ebot.prev_e_id:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Replying to the wrong message")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ (ᴘʀᴇᴠɪᴏᴜs) ᴍᴇssᴀɢᴇ.")
    elif len(m.content) - m.content.count('E') > 0:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Not all characters are E's")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: sᴏᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡᴇʀᴇ ɴᴏᴛ E's. Bᴇ sᴜʀᴇ ᴛᴏ ᴇʟɪᴍɪɴᴀᴛᴇ ᴀɴʏ ᴡʜɪᴛᴇ sᴘᴀᴄᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴀɴᴅ/ᴏʀ ᴛʏᴘᴏs.")
    elif len(m.content) != ebot.prev_e_number + 1:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Wrong number of E's, should be 1 more than " + str(ebot.prev_e_number))
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴡʀᴏɴɢ ɴᴜᴍʙᴇʀ ᴏғ E's. ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ E's sʜᴏᴜʟᴅ ʙᴇ " + str(ebot.prev_e_number + 1) + ".")
    elif ebot.processing == True:
      await ebot.log_channel.send("**_Primary Chain_** --- Deletion: Bot overflow")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴍᴀɪɴ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ sᴏ ɢᴏᴏᴅ ᴀᴛ ᴇ'ɪɴɢ ᴛʜᴀᴛ ʏᴏᴜ ᴏᴠᴇʀғʟᴏᴡᴇᴅ ᴛʜᴇ ʙᴏᴛ. ɢᴏᴏᴅ ᴊᴏʙ, ʙᴜᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ʜᴀᴅ ᴛᴏ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ. sᴏʀʀʏ!")
    else:
      ebot.processing = True
      
      numcontributions = 0

      #adding contribution
      new_unsorted = ebot.unsorted_message.content
      numberstart = new_unsorted.find(str(m.author.id)) + 22
      print(m.author.name + " " + str(len(m.content)))
      if numberstart == 21:
        new_unsorted = new_unsorted + "\n<@" + str(m.author.id) + "> - 0001"
        numcontributions = 1
      else:
        number = str(int(new_unsorted[numberstart:numberstart + 4]) + 1)
        new_unsorted = new_unsorted[:numberstart] + number.rjust(4, "0") + new_unsorted[numberstart + 4:]
        numcontributions = int(number)

      await ebot.unsorted_message.edit(content=new_unsorted)
      
      #adding roles
      if numcontributions == 1:
        await m.author.add_roles(get(ebot.guild.roles, id=887095372126773249))
        await m.author.remove_roles(get(ebot.guild.roles, id=912096772392890388))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 1 ᴇ! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887095372126773249).name + "**")
      elif numcontributions == 10:
        await m.author.add_roles(get(ebot.guild.roles, id=887100199498055751))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 10 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887100199498055751).name + "**")
      elif numcontributions == 50:
        await m.author.add_roles(get(ebot.guild.roles, id=887102637797945384))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 50 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887102637797945384).name + "**")
      elif numcontributions == 100:
        await m.author.add_roles(get(ebot.guild.roles, id=887103974413582388))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 100 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887103974413582388).name + "**")
      elif numcontributions == 250:
        await m.author.add_roles(get(ebot.guild.roles, id=888250472731934730))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 250 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=888250472731934730).name + "**")
      elif numcontributions == 500:
        await m.author.add_roles(get(ebot.guild.roles, id=887106132668194836))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 500 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887106132668194836).name + "**")
      elif numcontributions == 1000:
        await m.author.add_roles(get(ebot.guild.roles, id=887109559712354304))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 1000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887109559712354304).name + "**")
      elif numcontributions == 2000:
        await m.author.add_roles(get(ebot.guild.roles, id=887109783902113853))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 2000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887109783902113853).name + "**")
      elif numcontributions == 5000:
        await m.author.add_roles(get(ebot.guild.roles, id=887110270164557884))
        await ebot.talk_channel.send("ᴄᴏɴɢʀᴀᴛs <@" + str(m.author.id) + "> ғᴏʀ ʀᴇᴀᴄʜɪɴɢ 5000 ᴇ's! ʏᴏᴜ ʜᴀᴠᴇ ɢᴀɪɴᴇᴅ ᴛʜᴇ ʀᴏʟᴇ **" + get(ebot.guild.roles, id=887110270164557884).name + "**")
      
      #change latest logged message to the latest e
      l = await ebot.e_channel.history(limit=1).flatten()
      await ebot.latest_message_message.edit(content=l[0].id)

      #sort contributions
      c = ebot.unsorted_message.content
      arrECOUNT = [0] * int((len(c) + 1) / 29)
      arrREST = [0] * int((len(c) + 1) / 29)
      new_sorted = ""
      users_in_sorted = 0
      users_in_unsorted = 0
      for i in range(0, len(c), 29):
        arrECOUNT[users_in_unsorted] = int(c[i + 24:i + 28])
        arrREST[users_in_unsorted] = c[i:i + 24]
        users_in_unsorted += 1

      doubleSort(arrECOUNT, arrREST)

      for j in range(0, len(arrECOUNT)):
        if users_in_sorted == 10:
          break
        new_sorted = new_sorted + str(users_in_sorted + 1) + ") " + arrREST[j] + str(arrECOUNT[j]).rjust(4, "0") + "\n"
        users_in_sorted += 1

      await ebot.sorted_message.edit(content=new_sorted)

      await ebot.log_channel.send("**_Primary Chain_** --- Good message with " + str(ebot.prev_e_number + 1 + ebot.num2k * 2000) + " E's by " + m.author.name)
      
      if ebot.prev_e_number + 1 == 1000 or ebot.prev_e_number + 1 == 2000:
        await ebot.milestone_channel.send('**' + str(ebot.num2k * 2000 + ebot.prev_e_number + 1) + 'ᴛʜ ᴇ** - <@' + str(m.author.id) + '> (' + m.jump_url + ')')
      if ebot.prev_e_number + 1 == 420 and ebot.num2k == 0:
        await ebot.milestone_channel.send('**420ᴛʜ ᴇ** - <@' + str(m.author.id) + '> (' + m.jump_url + ')')
      if ebot.prev_e_number + 1 == 704 and ebot.num2k == 0:
        await ebot.milestone_channel.send("**704ᴛʜ ᴇ**, ʙʀᴇᴀᴋɪɴɢ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ᴇ ᴄʜᴀɪɴ's ʀᴇᴄᴏʀᴅ! - <@" + str(m.author.id) + '> (' + m.jump_url + ')')
      if ebot.prev_e_number + 1 == 1420 and ebot.num2k == 34:
        await ebot.milestone_channel.send('**69420ᴛʜ ᴇ** - <@' + str(m.author.id) + '> (' + m.jump_url + ')')

      if ebot.prev_e_number >= 1999:

        print(os.environ['HRML_ID'])
        print(ebot.get_user(os.environ['HRML_ID']))

        await ebot.announcement_channel.send("@everyone Cᴏɴɢʀᴀᴛs! Aɴᴏᴛʜᴇʀ 2000 E's ʜᴀᴠᴇ ʙᴇᴇɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴛʜᴇ ɴᴇxᴛ E ᴄʜᴀɴɴᴇʟ ɪs sᴇᴛ ᴜᴘ (ᴍᴀx 1 ᴡᴇᴇᴋ, ᴘʀᴏʙᴀʙʟʏ 1 ᴅᴀʏ).")
        await ebot.get_user(int(os.environ['HRML_ID'])).send("Another 2000 E's completed. Do da things!!")

        #lock both chains
        perms = ebot.e_channel.overwrites_for(ebot.e_slaves)
        perms2 = ebot.e2_channel.overwrites_for(ebot.e_slaves)

        perms.send_messages = False
        perms2.send_messages = False

        await ebot.e_channel.set_permissions(ebot.e_slaves, overwrite=perms)
        await ebot.e2_channel.set_permissions(ebot.e_slaves, overwrite=perms2)

        #suspend program
        ebot.suspended = True

      else:
        ebot.prev_e_id = m.id
        ebot.prev_e_message = m
        ebot.prev_e_number = len(m.content)
        ebot.prev_e_author = m.author
      ebot.processing = False

  if m.channel.id == ebot.e2_channel.id and ebot.suspended == False:
    if m.type != discord.MessageType.default:
      await ebot.log_channel.send("**_Secondary Chain_** --- Deletion: Not a normal message type")
      await m.delete()
    elif m.author == ebot.prev_e_author2:
      await ebot.log_channel.send("**_Secondary Chain_** --- Deletion: Same author as previous message")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ sᴇɴᴛ ᴀ ᴍᴇssᴀɢᴇ ᴡʜᴇɴ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ᴡᴀs ᴀʟsᴏ ʏᴏᴜʀs. (ᴅᴏ ɴᴏᴛ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴏᴡɴ E's.)")
    elif m.reference == None:
      await ebot.log_channel.send("**_Secondary Chain_** --- Deletion: Not replying to a message")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ. ʏᴏᴜ ᴍᴜsᴛ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜs ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ ᴄʜᴀɪɴ.")
    elif m.reference != None and m.reference.message_id != ebot.prev_e_id2:
      await ebot.log_channel.send("**_Secondary Chain_** --- Deletion: Replying to the wrong message")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ (ᴘʀᴇᴠɪᴏᴜs) ᴍᴇssᴀɢᴇ.")
    elif len(m.content) - (m.content.count('ᴇ') + m.content.count('É') + m.content.count('È') + m.content.count('Ê') + m.content.count('Ë') + m.content.count('Ě') + m.content.count('ɛ') + m.content.count('Ė') + m.content.count('Ĕ') + m.content.count('Ē') + m.content.count('Ę') + m.content.count('Σ')) > 0:
      await ebot.log_channel.send("**_Secondary Chain_** --- Deletion: Not all characters are E's")
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: sᴏᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡᴇʀᴇ ɴᴏᴛ ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ E ᴄʜᴀʀᴀᴄᴛᴇʀs. Sᴇᴇ #ɪɴsᴛʀᴜᴄᴛɪᴏɴs ғᴏʀ ᴀ ʟɪsᴛ ᴏғ ᴀʟʟᴏᴡᴇᴅ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴄʜᴀɴɴᴇʟ. (ɴᴏʀᴍᴀʟ E's ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴄʜᴀɴɴᴇʟ!). Bᴇ sᴜʀᴇ ᴛᴏ ᴇʟɪᴍɪɴᴀᴛᴇ ᴀɴʏ ᴡʜɪᴛᴇ sᴘᴀᴄᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs ᴀɴᴅ/ᴏʀ ᴛʏᴘᴏs.")
    elif len(m.content) != ebot.prev_e_number2 + 1:
      await ebot.log_channel.send("**_Secondary Chain_** --- Deletion: Wrong number of E's, should be 1 more than " + str(ebot.prev_e_number2))
      await m.delete()
      await m.author.send("Yᴏᴜʀ ᴍᴇssᴀɢᴇ ɪɴ ᴛʜᴇ sᴇᴄᴏɴᴅᴀʀʏ ᴇ ᴄʜᴀɪɴ ɪɴ ᴛʜᴇ sᴇʀᴠᴇʀ 'sʜʀɪɴᴇ ᴏғ ᴛʜᴇ ᴇ' ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ғᴏʀ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʀᴇᴀsᴏɴ: ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴡʀᴏɴɢ ɴᴜᴍʙᴇʀ ᴏғ E's. ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ E's sʜᴏᴜʟᴅ ʙᴇ " + str(ebot.prev_e_number2 + 1) + ".")
    else:
      await ebot.log_channel.send("**_Secondary Chain_** --- Good message with " + str(ebot.prev_e_number2 + 1 + ebot.num2k2 * 2000) + " E's by " + m.author.name)

      if ebot.prev_e_number2 >= 1999:

        print(os.environ['HRML_ID'])
        print(ebot.get_user(os.environ['HRML_ID']))

        await ebot.announcement_channel.send("@everyone Cᴏɴɢʀᴀᴛs! Aɴᴏᴛʜᴇʀ 2000 sᴇᴄᴏɴᴅᴀʀʏ E's ʜᴀᴠᴇ ʙᴇᴇɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. Pʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴛʜᴇ ɴᴇxᴛ sᴇᴄᴏɴᴅᴀʀʏ E ᴄʜᴀɴɴᴇʟ ɪs sᴇᴛ ᴜᴘ (ᴍᴀx 1 ᴡᴇᴇᴋ, ᴘʀᴏʙᴀʙʟʏ 1 ᴅᴀʏ).")
        await ebot.get_user(int(os.environ['HRML_ID'])).send("Another 2000 secondary E's completed. Do da things!!")

        #lock chains, stop program
        perms = ebot.e_channel.overwrites_for(ebot.e_slaves)
        perms2 = ebot.e2_channel.overwrites_for(ebot.e_slaves)

        perms.send_messages = False
        perms2.send_messages = False

        await ebot.e_channel.set_permissions(ebot.e_slaves, overwrite=perms)
        await ebot.e2_channel.set_permissions(ebot.e_slaves, overwrite=perms2)

        sys.exit("waiting for manual next channel work")

      else:
        ebot.prev_e_id2 = m.id
        ebot.prev_e_message2 = m
        ebot.prev_e_number2 = len(m.content)
        ebot.prev_e_author2 = m.author

keep_alive()
ebot.run(os.getenv('NAHTITOKEN'))