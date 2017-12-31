#!/usr/bin/env python3

import asyncio
import random
import os
from discord.ext import commands
from cogs.utils.config import Config

class Games:
  def __init__(self, bot):
    self.bot  = bot
    self.conf = Config('configs/games.json')

  @commands.command(pass_context=True, aliases=['fa'])
  async def fake_artist(self, ctx, number):
    conf   = self.conf.get('fake_artist', {})
    themes = conf.get('themes', [])
    themes = random.sample(themes, len(themes)-len(themes)%number)
    output = [[]]*number
    fakes  = list(range(number))*(len(themes)//number)
    random.shuffle(fakes)

    # generate
    for theme,fake in zip(themes, fakes):
      for i in range(len(output)):
        output[i].append(theme if i != fake else 'YOU ARE THE FAKE')

    # generate master file
    with open(os.path.join(conf.get('path',''), 'master.html'), 'w') as f:
      for i,theme in enumerate(themes): # add hidden stuff here
        f.write(f'''<input type="button" value="{i}"'''+ \
                f'''onclick="this.value=this.value=='{i}'''+ \
                f'''\'?'{theme}':'{i}';">''')

    # generate player files
    for i in range(len(output)):
      with open(os.path.join(conf.get('path',''), f'{i}.html'), 'w') as f:
        f.write(conf.get('rules'))
        for theme in output[i]:
          f.write(f'<li>{theme}</li>')
        f.write(conf.get('out'))
