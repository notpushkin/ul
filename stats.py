import json
from datetime import datetime

def stats(messages):
  symbol_len = 0
  word_len = 0
  messages_by_hour = {h: 0 for h in xrange(24)}
  symbols_by_hour = {h: 0 for h in xrange(24)}
  words_by_hour = {h: 0 for h in xrange(24)}
  messages_by_date = {}

  longest_message = None
  longest_message_len = 0

  for m in messages:
    date = datetime.fromtimestamp(m['date'])
    body = unicode(m['body'])
    length = len(body)
    words = body.count(" ") + 1

    symbol_len += length
    word_len += words

    messages_by_hour[date.hour] += 1
    symbols_by_hour[date.hour] += length
    words_by_hour[date.hour] += words

    iso_ = date.date().isoformat()
    if iso_ not in messages_by_date:
      messages_by_date[iso_] = 0
    messages_by_date[iso_] += 1

    if length > longest_message_len:
      longest_message = m
      longest_message_len = length

  return {
    'total': {
      'messages': len(messages),
      'symbols': symbol_len,
      'words': word_len
    },
    'messagesByHour': messages_by_hour,
    'messagesByDate': messages_by_date,
    'symbolsByHour': symbols_by_hour,
    'wordsByHour': words_by_hour,
    'longestMessage': longest_message
  }

def splitMessages(messages):
  incoming, outgoing = [], []
  for m in messages:
    if bool(m['out']):
      outgoing.append(m)
    else:
      incoming.append(m)
  return incoming, outgoing

if __name__ == '__main__':
  with open("messages.json") as f:
    messages = json.loads(f.read())

  incoming, outgoing = splitMessages(messages)

  j = json.dumps({
    'incoming': stats(incoming),
    'outgoing': stats(outgoing),
    'total': stats(messages)
  }, indent=2, ensure_ascii=False).encode("utf-8")

  with open("stats.json", "w") as f:
    f.write(j)
    f.close()

  # with open("stats.js", "w") as f:
  #   f.write("var stats = %s;" % j)
  #   f.close()