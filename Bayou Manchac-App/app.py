import dash
import pandas as pd
import dash_bootstrap_components as dbc
import pickle
import os
import pandas as pd
import glob
import json
from flask_caching import Cache
from Callbacks import *
from Components import *

# load data files:
    
filenames=glob.glob('Data/*.pckl')

f = open(filenames[0],'rb')
Boring_data_dataset1 = pickle.load(f)[0]
f.close()

for i in range(1, len(filenames)):    
    f = open(filenames[i],'rb')
    temp = pickle.load(f)[0]
    f.close()
    for key in temp.keys():
        if key in Boring_data_dataset1.keys():
            Boring_data_dataset1[key] += temp[key]
        else:
            Boring_data_dataset1[key] = temp[key]

external_stylesheets = [dbc.themes.BOOTSTRAP]

#token = 'pk.eyJ1IjoiaGFwcHliZWFyeHAiLCJhIjoiY2tkOWhreWdyMGt1ejJ4cG1yNmt0OGFieSJ9.4V-xjVlLHjj-ewLywkCwOw' # you will need your own token
token = 'pk.eyJ1IjoieWVsbG9uNzMiLCJhIjoiY2wzeDN3Z2trMWFlMzNicDR0OXZheWRyciJ9.g24GXoAQPgpzQ2t3wdr4OQ' # new public token for AAI database

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379')
}
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)


app.layout = layout(app, token, Boring_data_dataset1)

app.title = 'DOTD I10-CMAR Geotechnical Data Explorer'

login_callbacks(app, cache, token, Boring_data_dataset1)
notice4users_callbacks(app, cache)
export_security_layout_callbacks(app, cache)
load_security_layout_callbacks(app, cache)
map_view_layout_collapse_callbacks(app, cache)
map_callbacks(app, cache)
map_point_selection_callbacks(app, cache, Boring_data_dataset1)
loaded_data_datatables_update_signal_callbacks(app, cache)

W2E_fence_plot_callbacks(app, cache)
S2N_fence_plot_callbacks(app, cache)

data_profile_callbacks(app, cache)
composite_soil_profile_callbacks(app, cache)

design_layer_datatable_callbacks(app, cache)
design_profile_callbacks(app, cache)

soil_design_parameter_datatable_callbacks(app, cache)
download_soil_design_parameter_datatable_callbacks(app, cache)
   
if __name__ == '__main__':
    app.run_server(debug=False)
