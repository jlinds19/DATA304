import pandas as pd
import matplotlib.pyplot as plt

# Read csv
df = pd.read_csv('system_of_record_timestamps.csv')

# Cleaning date format and sorting
df['datetime_primary'] = pd.to_datetime(df['Primary_Timestamp'], format='mixed', utc=True)
df['date_only'] = df['datetime_primary'].dt.date
df = df.sort_values(by='date_only')

# Variables for line graph
x = df['date_only']
y = df['Event_Count']

# Plotting line graph
fig, ax = plt.subplots()
ax.plot(x,y)

ax.set(xlabel='Date' ,ylabel='Event Count', title='Event Count over time')
ax.grid()

fig.savefig('ecvtime.png')
plt.show()
