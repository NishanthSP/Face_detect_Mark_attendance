from datetime import datetime, date


def markattendence(name):
	with open('Attendence_sheet.csv', 'r+') as f:
		mydatalist = f.readlines()
		namelist = []
		for line in mydatalist:
			entry = line.split(',')
			namelist.append(entry[0])
		if name not in namelist:
			# IST = pytz.timezone('Asia/Kolkata')
			# now = datetime.now(IST)
			now = datetime.now()
			dstring = date.today()
			dtstring = now.strftime('%H:%M:%S')
			f.writelines(f'\n{name},{dstring},{dtstring}')
