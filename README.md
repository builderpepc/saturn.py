# :warning: This project is no longer maintained as I am currently working on more important projects. Please contact me if you'd like to continue it.
(I still have a ton of unpushed changes lying around)

# saturn.py
> ### **:warning: Please make sure you have read and understood the [disclaimer](#disclaimer) before installing or using this library.**
An async Python API wrapper for [Saturn](https://www.joinsaturn.com/)'s unofficial API, featuring a simple Pythonic syntax and more. Influenced in part by the great [discord.py](https://github.com/Rapptz/discord.py/).

This project is currently still a work in progress and is **not yet installable**.

```py
from saturn import Client

bot = Client("my_access_token", "my_refresh_token")

@bot.on("start")
async def on_start():
    print("Saturn bot started")

@bot.on("ready")
async def on_ready():
    print("Connected successfully")
    print("Account name: " + bot.user.name)
    print("Account created at: " + str(bot.user.created_at))

bot.run()
```

## What is Saturn?
[Saturn](https://www.joinsaturn.com/) is a mobile app that allows high school students to submit their class schedules and automatically be placed in group chats for their classes, among other related features. 

## A Note on Stability
Given that saturn.py does not use an official API, the library may at times break due to changes with Saturn's backend. If you notice a bug, please create an issue.

# Disclaimer
Use of this library may violate Saturn's [Terms of Use](https://www.joinsaturn.com/terms-of-use) and other Saturn guidelines.

This library is solely intended as a proof of concept. Its developers are not affiliated in any way with Saturn and this project has not been authorized by said company.

The developers of this library will not be held responsible for your actions or any resulting consequences if you use this library.

The developers of this library by no means encourage you to use it. You do so at your own risk.

If you decide to use this library, please do so ethically and responsibly. Regardless of how you use it, you may face consequences at Saturn's discretion.
