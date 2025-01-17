import logging
import logging.config

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

import os
from config import Config
from pyrogram import Client
from plugins.database import db 

from plugins.webserver import bot_run
from os import environ
from aiohttp import web as webserver

PORT_CODE = environ.get("PORT", "8080")








class Bot(Client):
   
   def __init__(self):
       super().__init__(
            name="md-rename-bot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={"root": "plugins"},
        )
      
   async def start(self):
      await super().start()
      self.log = logging
      if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
      banned_users = await db.get_banned_users()
      Config.BANNED_USERS = banned_users
      logging.info(f"{self.me.first_name} is Successfully started")
   
      client = webserver.AppRunner(await bot_run())
      await client.setup()
      bind_address = "0.0.0.0"
      await webserver.TCPSite(client, bind_address, PORT_CODE).start()


   async def stop(self):
      await super().stop()
      logging.info(f"{self.me.first_name} is stopped...")

bot = Bot()
bot.run()
