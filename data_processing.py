import matplotlib.pyplot
import numpy
import pandas
import datetime
import calendar

class GymOccupancy:
    name = "name"
    occupancy_per = "%-1"
    occupancy_count = "0/0"
    time = "00:00"
    date = "-2021"
    day = ""

    def printGym(self):
        print(f'{self.name}\t{self.occupancy_per}\t{self.occupancy_count}\t{self.date}\t{self.time}\t{self.day}')

    def to_dict(self):
        return {
            'name': self.name,
            'occupancy_per': self.occupancy_per,
            'occupancy_count': self.occupancy_count,
            'time': self.time,
            'date': self.date,
            'day': self.day
        }



def findDay(date_):
    born = datetime.datetime.strptime(date_, '%b-%d-%Y').weekday()
    return calendar.day_name[born]




with open("GymLog/East Fitness (Strength Equipment).txt", "r") as f:
    gym_list = []
    while True:
        temp = GymOccupancy()
        check_eof = f.readline()
        if check_eof == "":
            break
        temp.name = check_eof[5:]

        occupancy = f.readline()

        temp.occupancy_count = int(occupancy[10:].split()[0].split("/")[0])
        # print(temp.occupancy_count)
        temp.occupancy_per = occupancy[10:].split()[2]

        date_time = f.readline()
        temp.date = date_time[14:].split()[0] + temp.date
        temp.time = date_time[14:].split()[1]
        # print(temp.time)
        temp.day = findDay(temp.date)
        f.readline()
        gym_list.append(temp)
        # print(f'{temp.name}\t{temp.occupancy_per}\t{temp.occupancy_count}\t{temp.date}\t{temp.time}')

    df = pandas.DataFrame.from_records([s.to_dict() for s in gym_list])
    df_monday = df[df["day"] == "Saturday"]
    df_monday["time"] = pandas.to_datetime(df_monday['time'])
    df_monday = df_monday.drop_duplicates(subset=['time', 'date'])
    df_monday.plot(x='time', y='occupancy_count', kind='bar')
    print(df_monday)
    matplotlib.pyplot.show()














    # for entry in gym_list:
    #     percent = entry.occupancy_per.split("%")[0]
    #     percent = int(percent)
    #     if percent <= 15:
    #         print(f'{entry.name}\t{entry.occupancy_per}\t{entry.occupancy_count}\t{entry.date}\t{entry.time}')

