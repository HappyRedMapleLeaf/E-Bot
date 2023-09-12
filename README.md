# The E-Bot
Possibly the silliest thing I've ever done - keeping it on GitHub for the 2021 nostalgia.

## What It Is
My friends and I started a pointless discord server where someone would type the letter E, the next person would reply to that message with two E's, and so on - eventually, the screen is filled with messages, each one containing one more E character than the next.

Eventually, I noticed that many people were making mistakes and 'breaking the chain', forgetting to reply or typing the wrong number of characters. Also, Discord has a 2000 character limit so we had to restart the chain in a new channel every time 2000 more messages were added to the chain.

Being bored and up for a challenge, I spent a few months creating this utterly ridiculous Discord bot (using discord.py, a Python library that facilitates usage of the Discord API) that:
- Deletes incorrect messages and tells the user what reason the message was deleted for
- Locks channels after 2000 messages, and sets up a new channel to immediately restart the chain in
- Maintains a real-time leaderboard for members in the server who have contributed the most to the chain (sent the most E messages)
- Assigns roles to members with 100, 250, 500, 1000, 2000, or 5000 contributions and congratulates them upon gaining the role
- Hosts commands to access an individual member's contributions, as well as display how many contributions have been made in total in one day
- Seamlessly fixes the chain and resumes normal functionality even if the bot restarts or is somehow down for a period of time
- Prevents messages from being sent too fast

Perhaps it's not very useful, but hey, at least I learned a lot from it and had fun.
