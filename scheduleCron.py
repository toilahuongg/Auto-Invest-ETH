from crontab import CronTab
 
my_cron = CronTab(user=True)
for job in my_cron:
    if job.comment == 'priceETH' or "scheduleInvest":
        my_cron.remove(job)
        my_cron.write()
job = my_cron.new(command='/Users/hugon/Documents/Workspace/KHDL/venv/bin/python /Users/hugon/Documents/Workspace/KHDL/getPriceETH.py', comment='priceETH')
job.minute.every(1)
job2 = my_cron.new(command='/Users/hugon/Documents/Workspace/KHDL/venv/bin/python /Users/hugon/Documents/Workspace/KHDL/scheduleInvest.py', comment='scheduleInvest')
job2.minute.every(1)
my_cron.write()