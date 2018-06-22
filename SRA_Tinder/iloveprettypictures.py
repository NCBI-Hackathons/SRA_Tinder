import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
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


if __name__=="__main__":
	tablefile=sys.argv[1]
	profilepic(tablefile)





