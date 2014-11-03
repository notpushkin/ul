import json

def getAllMessages():
  messages = []
  for i in xrange(13, -1, -1):
    with open("dump%i.json" % i) as f:
      j = json.loads(f.read())
      messages.extend(j['response']['items'])

  messages.reverse()

  return messages

if __name__ == '__main__':
  with open("dump_Full.json", "w") as f:
    f.write(json.dumps(getAllMessages(), indent=2, ensure_ascii=False).encode("utf-8"))
    f.close()