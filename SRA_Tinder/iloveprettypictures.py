import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import sys



def profilepic(tablefile):
    df = pd.read_csv(tablefile)
    qc_data = [go.Bar(x=marks_df.Accession, y=marks_df.mean_quality_score)]
    init_notebook_mode(connected=True)
    py.iplot({ 'data': qc_data,
            'layout': {
               'title': 'Marks Distribution',
               'xaxis': {
                 'title': 'Subjects'},
               'yaxis': {
                'title': 'Marks '}
             }})
def temp():
    init_notebook_mode()
    iplot([{'x': [1, 2, 3], 'y': [5, 2, 7]}])
    # We can also download an image of the plot by setting the image to the
    #format you want. e.g. `image='png'`
    #iplot([{'x': [1, 2, 3], 'y': [5, 2, 7]}], image='png')

temp()



if __name__=="__main__":
	tablefile=sys.argv[1]
	profilepic(tablefile)





