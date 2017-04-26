from spyre import server
import pandas as pd
import matplotlib.pyplot as plt

city = {1: 'Cherkasy', 2: 'Chernihiv', 3: 'Chernivtsi', 4: 'Crimea', 5: 'Dnipropetrovsk', 6: 'Donetsk',
        7: 'Ivano-Frankivsk', 8: 'Kharkiv', 9: 'Kherson', 10: 'Khmelnytskyy', 11: 'Kiev', 12: 'Kiev City',
        13: 'Kirovohrad', 14: 'Luhansk', 15: 'Lviv', 16: 'Mykolayiv', 17: 'Odessa', 18: 'Poltava', 19: 'Rivne',
        20: 'Sevastopol', 21: 'Sumy', 22: 'Ternopil', 23: 'Transcarpathia', 24: 'Vinnytsya', 25: 'Volyn',
        26: 'Zaporizhzhya', 27: 'Zhytomyr'}


class Tables(server.App):
    title = "Tables"
    inputs = [{"type": 'dropdown',
               "label": 'Company',
               "options": [{'label': i, 'value': j} for j, i in city.items()],
               "key": 'city',
               "action_id": "update_data"},
              {"type": 'dropdown',
               'label': 'Value',
               'options': [{'label': 'VHI', 'value': 'VHI'},
                           {'label': 'VCI', 'value': 'VCI'},
                           {'label': 'TCI', 'value': 'TCI'}],
               'key': 'some_value',
               'action_id': 'update_data'},
              { 'type': 'dropdown',
                'label': 'First_Year',
                'options': [{'label': i, 'value': i} for i in range(1982, 2016)],
                'key': 'first_year',
                'action_id': 'update_data'},
              {
                  'type': 'dropdown',
                  'label': 'Second_Year',
                  'options': [{'label': i, 'value': i} for i in range(1982, 2016)],
                  'key': 'second_year',
                  'action_id': 'update_data'
              },

              {"type": 'dropdown', 'label': 'Color',
               'options': [{'label': 'Black', 'value': 'black'},
                           {'label': 'Yellow', 'value': 'yellow'},
                           {'label': 'Brown', 'value': 'brown'},
                           {'label': 'Blue', 'value': 'blue'},
                           {'label': 'Green', 'value': 'green'}],
               'key': 'color',
               'action_id': 'update_data'
               },

              {"type": 'dropdown', 'label': 'Style',
               'options': [{'label': '1Style', 'value': 'line'},
                           {'label': '2Style', 'value': 'bar'},
                           {'label': '3Style', 'value': 'hist'},
                           {'label': '4Style', 'value': 'hexbin'},
                           {'label': '5Style', 'value': 'scatter'}],

               'key': 'style',
               'action_id': 'update_data'
               }

              ]

    controls = [{'type': 'hidden', 'id': 'update_data'}]
    tabs = ['Plot', 'Table']
    outputs = [{"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"},

               {"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True}]

    def getData(self, params):
        city = int(params['city'])
        first_year = int(params['first_year'])
        second_year = int(params['second_year'])

        df = pd.read_csv('vhi_id_{} 2017 04 25.csv'.format(city), index_col=False, header=1, skipfooter=1,
                         engine='python',
                         names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'], delimiter='\,\s+|\s+|\,')

        df = df[df.year >= first_year][df.year <= second_year]

        return df

    def getPlot(self, params):
        data = params['some_value']
        color = params['color']
        style = params['style']
        df_1 = self.getData(params)
        plt_obj_1 = df_1.plot(x='week', y=data, colors=color, kind=style)

        fig = plt_obj_1.get_figure()

        return fig


app = Tables()
app.launch(port=9022)