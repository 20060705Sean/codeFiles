import discord
import sys
from random import randint
client = discord.Client()
bentonOrder = ["大家鐵路1", "大家鐵路2", "大家鐵路3", "太師傅1", "太師傅2", "太師傅3", "正園A", "正園B", "正園羊肉", "吉樂米1", "吉樂米2", "吉樂米3", "吉樂米－素食", "米寶1", "米寶3", "米寶－方便素", "彩鶴"]
price = [65, 70, 75, 70, 65, 60, 55, 55, 55, 60, 70, 80, 60, 60, 75, 60, 50]
orders = {
	"1" : {
		"1" : ("大家鐵路1", 65), 
		"2" : ("大家鐵路2", 70), 
		"3" : ("大家鐵路3", 75)
	}, "2" : {
		"1" : ("太師傅1", 70), 
		"2" : ("太師傅2", 65), 
		"3" : ("太師傅3", 60)
	}, "3" : {
		"1" : ("正園A餐", 55), 
		"2" : ("正園B餐", 55), 
		"3" : ("正園羊肉", 55)
	}, "4" : {
		"1" : ("吉樂米1", 60), 
		"2" : ("吉樂米2", 70), 
		"3" : ("吉樂米3", 80), 
		"4" : ("素食", 60)
	}, "5" : {
		"1" : ("米寶1", 60), 
		"2" : ("米寶3", 75), 
		"3" : ("方便素", 60)
	}, "6" : {
		"1" : ("彩鶴", 50)
	}
}

@client.event
async def on_ready():
	print('目前登入身份：',client.user)
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.startswith('murder'):
		await message.channel.send("無情雙殺")
	if message.content.startswith('stopnow'):
		sys.exit()
	if message.content.startswith('say'):
		tmp = message.content.split(" ")
		for i in range(int(tmp[1]) // 20):
			backslsh = '\n'
			await message.channel.send(f"{tmp[2]}好電{backslsh}" * 20)
	if message.content.startswith('order'):
		name = '{0.author.mention}'.format(message)
		tmp = message.content.split(" ")
		if name == "<@!856551189747204108>":
			if tmp[1] == 'send':
				today = {i : 0 for i in bentonOrder}
				summary_money = 0
				await message.channel.send("now searching lunch orders")
				with open("lunchOwedMoney.txt", 'rb') as file:
					for line in file.readlines():
						info = line.split()
						today[info[1].decode('utf-8')] += 1
						summary_money += int(info[2].decode('utf-8'))
						await message.channel.send(line.decode("utf-8"))
					await message.channel.send(f'today orders:{today}')
					await message.channel.send(f'today summary money:{summary_money}')
		if len(tmp) == 1:
			await message.channel.send("壞份子")
		elif tmp[1] == 'menu':
			await message.channel.send('1 大家鐵路:	\n--> 大家鐵路1號	65\n-->	大家鐵路2號	70\n-->	大家鐵路3號	75\n2 太師傅:\n--> 太師傅1號	70\n--> 太師傅2號	65\n--> 太師傅3號	60\n3 正園:\n--> 正園A餐	55\n--> 正園B餐	55\n--> 正園羊肉	55\n4 吉樂米\n--> 吉樂米1號	60\n--> 吉樂米2號	70\n--> 吉樂米3號	80\n--> 素食	60\n5 米寶:\n--> 米寶1號	60\n--> 米寶3號	75\n--> 方便素	60\n6 彩鶴:\n--> 彩鶴	50')
		elif tmp[1] == 'lunch':
			if tmp[2] in list(orders.keys()):
				temp = orders[tmp[2]]
				if tmp[3] in temp:
					if len(tmp) == 5:
						seat_number = tmp[4]
						if 32 > int(seat_number) > 0:
							msg = f"{name} you have ordered {temp[tmp[3]]}"
							await message.channel.send(msg)
							previous = str()
							with open("lunchOwedMoney.txt", 'ab') as file:
								BACKSLASH = '\n'
								file.write(f"{BACKSLASH}{seat_number} {temp[tmp[3]][0]} {temp[tmp[3]][1]}".encode('utf-8'))
						else:
							await message.channel.send("壞份子")
					else:
						await message.channel.send("壞份子")
				else:
					await message.channel.send("壞份子")
			else:
				await message.channel.send("壞份子")
		elif tmp[1] == 'remove':
			await message.channel.send("Please contact the administrater if you want to cancel your order, our service time: 8am to 9pm")
		elif tmp[1] == 'check':
			previous = str()
			with open("lunchOwedMoney.txt", 'rb') as file:
				p = file.read().decode('utf-8')
			await message.channel.send(p)
		else:
			msg = ["再亂傳呀", "是在哭喔", "不可以瑟瑟", "臭雞雞", "你沒雞雞可剁"][randint(0, 2)]
			await message.channel.send(msg)
	if ("申" in message.content) or ("甲" in message.content):
		await message.channel.send('你才甲甲你全家都甲甲')
	if ("哭" in message.content) or ("電" in message.content):
		await message.channel.send('我有像在哭嗎？')


client.run('OTAwNDAzMTcwNjQyMTAwMjY0.YXAzzA.mIhsXNFEijgmt9azuNOMfh6Lgaw')
