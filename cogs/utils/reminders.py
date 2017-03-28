#!/usr/bin/env python3

import re
import time
import asyncio

class Reminder:
  def __init__(self, channel_id, user_id, message):
    self.channel_id = channel_id
    self.user_id    = user_id
    self.message    = message
    self.end_time   = -1
    self.parse_time()

  def is_ready(self):
    return self.end_time <= time.time()

  async def send(self, bot):
    c = await bot.get_channel(self.channel_id)
    await bot.send_message(c, self.get_message())

  def get_message(self):
    return '@{}: {}'.format(self.user_id, self.message)

  def parse_time(self):
    offset = time.time()
    times = {
             '(\\d+)\s+s(econds?)?'    : 1,
             '(\\d+)\s+m(in(ute)?s?)?' : 60,
             '(\\d+)\s+h(ours?)?'      : 360,
             '(\\d+)\s+d(ays?)?'       : 8640,
             '(\\d+)\s+w(eeks?)?'      : 60480,
             '(\\d+)\s+months?'        : 254016
    }
    for t in times:
      match = re.search(t, timestring)
      self.message = re.sub(t, '', self.message).strip()
      if match:
        offset += times[t]*match.group(1)
    self.end_time = offset

  def insertInto(self, into):
    if not into or self.end_time > into[-1].end_time:
      into.append(self)
      return
    lo = 0
    hi = len(into)
    while lo < hi:
      mid = (lo+hi)//2
      if self.end_time > into[mid].end_time:
        hi = mid
      else:
        lo = mid+1
    into.insert(lo, self)
