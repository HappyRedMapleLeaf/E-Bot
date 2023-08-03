import csv, datetime

def get_latest(row):
  with open('latest_ids.txt') as f:
    for i in range(row - 1):
      f.readline()
    return f.readline()

def set_latest(row, id):
  with open('latest_ids.txt') as f:
    all = f.readlines()
  all[row - 1] = f'{id}\n'
  with open('latest_ids.txt', 'w') as f:
    f.write(all[0]+all[1]+all[2]+all[3]+all[4])

def add_member(id):
  with open('members.csv', 'a') as f:
    f.write(f'{id},0001\n')

def add_contrib(id):
  members = []
  with open('members.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      temp = row
      if int(temp[0]) == id:
        temp[1] = str(int(temp[1]) + 1).rjust(4, "0")
      members.append(temp)
  with open('members.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    for row in members:
      writer.writerow(row)

def get_members(id, column):
  with open('members.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
      if row[0] == str(id):
        return row[column - 1]
  return -1

def add_daily(day, num):
  spacegap = False
  with open('daily.csv', 'a') as f:
    f.write(f'\n{day},{int(num)}')
  with open('daily.csv') as f:
    all = f.readlines()
    if all[len(all)-2] == '\n':
      spacegap = True
      all.pop(len(all)-2)
  if spacegap == True:
    with open('daily.csv', 'w') as f:
      for row in all:
        f.write(row)

def log(text):
  with open('logs.txt', 'a') as f:
    f.write(f'{adj_datetime(datetime.datetime.now())}:\n{text}\n\n')

def adj_date(datein):
  return (datein - datetime.timedelta(hours=5)).date()

def adj_datetime(datetimein):
  return datetimein - datetime.timedelta(hours=5)
  