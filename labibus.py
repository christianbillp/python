import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Labibus():
    unit = ['kW', '', '', '%rh', 'C', '', 'main_batt_mV', 'charger_mV', 'extra_mV', 'main_batt_mA', '', '', '', '', 'On']
    data = pd.Series({})
    server_devices = [6, 7, 8, 9]
    environment_devices = [3, 4]
    ms = 0
    since = int(datetime.datetime(2017, 12, 6, 00, 00, 00).timestamp())*1000

    def set_ms(self, ms):
        self.ms = ms

    def set_since(self, since):
        self.since = since

    def add_data_since(self, since, devices):
        for device in devices:
            self.data[str(device)] = pd.read_json('https://bus.labitat.dk/labibus_since/{}/{}'.format(device, since))
            self.data[str(device)].columns = ['date', self.unit[device]]
            self.data[str(device)]['date'] = pd.to_datetime(self.data[str(device)]['date'],unit='ms')
            self.data[str(device)].set_index('date', drop=False, inplace=True)

    def add_data_ms(self, ms, devices):
        for device in devices:
            self.data[str(device)] = pd.read_json('https://bus.labitat.dk/labibus_last/{}/{}'.format(device, ms))
            self.data[str(device)].columns = ['date', self.unit[device]]
            self.data[str(device)]['date'] = pd.to_datetime(self.data[str(device)]['date'],unit='ms')
            self.data[str(device)].set_index('date', drop=False, inplace=True)

    def get_server_data(self):
        self.add_data_ms(self.ms, self.server_devices)

        df = pd.merge(self.data['6'], self.data['7'], on='date', how='outer')
        df = pd.merge(df, self.data['8'], on='date', how='outer')
        df = pd.merge(df, self.data['9'], on='date', how='outer')
        df.set_index('date', drop=False, inplace=True)
        df = df.sort_values(['date'], ascending=[1])
        headertofill = list(df.columns.values)
        df[headertofill] = df[headertofill].fillna(method='pad')
        df = df.dropna()
        df['day_of_week'] = df['date'].dt.weekday_name
        df = df[['main_batt_mV','charger_mV', 'extra_mV', 'main_batt_mA']].drop_duplicates()

        return df

    def show_server_graphs(self):
        df = self.get_server_data()
#        sns.distplot(df['main_batt_mA']).set_title("Server rack analysis")
#        df.plot(figsize=(7,7), subplots=True, kind='hist', sharex=False, bins=75)
        df.hist(figsize=(7,7))

#        print(df.describe().round(2))

    def get_environment_data(self, ms):
        #data['0'] = pd.read_json('https://power.labitat.dk/since/{}'.format(since))
        self.data['0'] = pd.read_json('https://power.labitat.dk/last/{}'.format(ms))
        self.data['0'].columns = ['date', self.unit[0]]
        self.data['0']['date'] = pd.to_datetime(self.data['0']['date'],unit='ms')
        self.data['0'].set_index('date', drop=False, inplace=True)
        self.data['0'][self.unit[0]] = self.data['0'][self.unit[0]]/1000

        # Add devices to data dictionary
        for device in self.environment_devices:
        #    data[str(device)] = pd.read_json('https://bus.labitat.dk/labibus_since/{}/{}'.format(device, since))
            self.data[str(device)] = pd.read_json('https://bus.labitat.dk/labibus_last/{}/{}'.format(device, ms))
            self.data[str(device)].columns = ['date', self.unit[device]]
            self.data[str(device)]['date'] = pd.to_datetime(self.data[str(device)]['date'],unit='ms')
            self.data[str(device)].set_index('date', drop=False, inplace=True)

        df = pd.merge(self.data['3'], self.data['4'], on='date', how='outer')
        df = pd.merge(df, self.data['0'], on='date', how='outer')
        df = df.sort_values(['date'], ascending=[1])
        headertofill = list(df.columns.values)
        df[headertofill] = df[headertofill].fillna(method='pad')
        df = df.dropna()
        df = df.reset_index(drop=True)
        df.set_index('date', drop=False, inplace=True)
        df = df.drop_duplicates(['kW','%rh', 'C'])
        df['day_of_week'] = df.index.weekday_name

        return df

if __name__ == '__main__':
    ms = 4 * 7 * 24 * 3600 * 1000
    since = int(datetime.datetime(2017, 12, 6, 00, 00, 00).timestamp())*1000
    devices = [6, 7, 8, 9]

    bus = Labibus()
    bus.set_ms(ms)
#    bus.add_data_since(since, devices)
#    bus.add_data_ms(ms, bus.server_devices)
#    df = bus.get_server_data()
    df = bus.get_environment_data(ms)
    bus.show_server_graphs()
