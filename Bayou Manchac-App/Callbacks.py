import dash
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math
import time
from dash_extensions.snippets import send_data_frame
import io
from pybase64 import b64decode
from datetime import timedelta
from cryptography.fernet import Fernet
from scipy.signal import find_peaks
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import random
import colorsys
from dash_table.Format import Format, Scheme, Trim
from dash_extensions.snippets import send_data_frame

def determine_zoom_level(latitudes, longitudes):
    if not latitudes or not longitudes:
        return 0, (0, 0)

    if len(latitudes) < 1:
        return 0, (0, 0)

    b_box_height=max(latitudes)-min(latitudes)
    b_box_width=max(longitudes)-min(longitudes)
    b_box_center=((max(longitudes)+min(longitudes))/2, (max(latitudes)+min(latitudes))/2)
    max_width = max(b_box_height, b_box_width)
    zoom = -1.425*np.log(max_width) + 7.8943
# =============================================================================
#     print(area)
#     print(zoom)
#     print(b_box.center)
# =============================================================================
# =============================================================================
#     return zoom, b_box.center
# 
# =============================================================================
    return zoom, b_box_center
# =============================================================================
# Longitude = [-90, -90.5, -91]
# Latitude  = [30, 29.5, 30.5]
# 
# a=determine_zoom_level(Latitude, Longitude)
# =============================================================================
def general_datatable_func(data_table_name):
    general_datatable = dash_table.DataTable(
        id='dataset1-selected-'+data_table_name.replace('_', '-')+'-table',
        columns=[],
        data=[],        
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        # export_columns='visible',
        # row_selectable="multi",
        # row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 50,
        style_table={
            'height': '600', 'overflowY': 'auto', 
            'width': 'auto', 'overflowX': 'auto', 'minWidth': '100%'},    
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
            'whiteSpace': 'normal'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        # fixed_columns={'headers': True, 'data': 1},       
        fixed_rows={'headers': True},
    )
    return general_datatable
def general_datatable_tab_func(datatable, datatable_tab_name, datatable_tab_color, datatable_tab_text_color):
# =============================================================================
# =============================================================================
# # # datatable_tab_content:
# =============================================================================
# =============================================================================
    datatable_tab_content = dbc.Card(
        dbc.CardBody(
            [
                datatable,
                ]
        ),
        className="mt-3",
    )
# =============================================================================
# =============================================================================
# # # datatable_tab:
# =============================================================================
# =============================================================================
    datatable_tab = dbc.Tab(label=datatable_tab_name, 
            tab_id=datatable_tab_name.replace(' ', '-') + '-tab',
            children=[
                datatable_tab_content,
                ],
            tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            active_tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            label_style={
                "color": datatable_tab_text_color,
                'background-color': datatable_tab_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '10px',                  
                },
            active_label_style={
                "color": datatable_tab_color,
                'background-color': datatable_tab_text_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '10px',                  
                },
            )    
    return datatable_tab # -*- coding: utf-8 -*-
def plot_location_point_in_mapbox(map_fig, df, group_name, map_fill_color, map_line_color, map_marker_size, map_text_color, map_text_size):
    if len(df) > 0:
# =============================================================================
# # assgin Point Color Code to point:
# =============================================================================
        Point_Color_Code_list = []    
        for i in range(0, len(df)):
            h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
            r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
            rgbhex = ['#%02x%02x%02x' % (r, g, b)]
            if rgbhex not in Point_Color_Code_list:        
                Point_Color_Code_list += rgbhex
        df.loc[:,"Point Color Code"] = [a for a in Point_Color_Code_list]
# =============================================================================
# # Marker boundary:
# =============================================================================            
        map_fig['data'].append(go.Scattermapbox(
            lat = df["Latitude Decimal"].tolist(),
            lon = df["Longitude Decimal"].tolist(), 
            customdata = df.index,
            mode='markers',
            fillcolor=map_fill_color,
            marker=go.scattermapbox.Marker(
                allowoverlap = True,
                size=map_marker_size/5*6,
                color=df["Point Color Code"], # map_line_color,
                opacity=1.,
            ),
            opacity = 0.3,
            legendgroup=group_name,
            showlegend=False,                    
            hoverinfo = 'none',
            ))
# =============================================================================
# # Marker fill:
# =============================================================================            
        map_fig['data'].append(go.Scattermapbox(
            lat = df["Latitude Decimal"].tolist(),
            lon = df["Longitude Decimal"].tolist(), 
            customdata = df["Point Color Code"], # df.index
            name=group_name,
            mode = 'markers+text',
            text = df["Location ID"].tolist(),
            textfont = dict(color=map_text_color,size=map_text_size),
            textposition = "bottom right", # "top left" | "top center" | "top right" | "middle left" | "middle center" | "middle right" | "bottom left" | "bottom center" | "bottom right"
            fillcolor = map_fill_color,
            marker = go.scattermapbox.Marker(
                allowoverlap = True,
                size = map_marker_size,
                color = map_fill_color,
            ),
            opacity = 0.9,
            legendgroup = group_name,
            showlegend = True,                    
            hoverinfo = 'text',
            hovertext = ['Project Number: '+a+
                        '<br>'+'Location ID: '+b+
                        '<br>'+'Location Type: '+str(c)+
                        '<br>'+'Ground Elevation (ft.): '+str(d)+
                        '<br>'+'Final Depth (ft.): '+str(e) 
                        for a,b,c,d,e in zip(df["Project Number"].tolist(),
                                             df["Location ID"].tolist(),
                                             df["Location Type"].tolist(),
                                             df["Elevation"].tolist(),
                                             df["Final Depth"].tolist()
                                             )
                        ]
            ))

def fence_plot_func(
        ctx,
        fence_graph_fig_text_size, 
        fence_graph_fig_bar_width,
        map_selection_points,
        dataset1_selected_soil_lithology_data_table_data,
        dataset1_selected_soil_boring_data_table_data,
        dataset1_selected_CPT_data_table_data,
        dataset1_selected_test_pile_table_data,
        fence_graph_fig,
        x_axis_key_name4bars,
        x_axis_key_name4ID_and_elevation_line,
        fence_graph_direction,
        selected_CPT_method,
                    ):
    if not ctx.triggered:
        triggered_input_id = []
    else:
        triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        fence_graph_fig_data=fence_graph_fig['data']
    if triggered_input_id=='generate-' + fence_graph_direction + '-fence-plot-button':            
        fence_graph_fig_data=[]
# =============================================================================
# # add Soil Lithology Columns:
# =============================================================================
        if dataset1_selected_soil_lithology_data_table_data:            
            data=pd.DataFrame.from_records(dataset1_selected_soil_lithology_data_table_data)
            data.sort_values(by=[x_axis_key_name4bars], inplace=True)
            lithology_hovertext = ['Project Number: '+str(a)+
                    '<br>'+'Location ID: '+str(b)+
                    '<br>'+'Top Elevation (ft.): '+str(c)+
                    '<br>'+'Bottom Elevation (ft.): '+str(d)+
                    '<br>'+'Symbol: '+str(e)+
                    '<br>'+'Description: '+str(f)
                    for a,b,c,d,e,f in zip(data["Project Number"].tolist(),
                                         data["Location ID"].tolist(),
                                         [round(a,2) for a in data["Elevation Top"]],
                                         [round(a,2) for a in data["Elevation Base"]],
                                         data["Legend Code"].tolist(),
                                         data["Additional Description"].tolist(),
                                           )]   
            soil_lithology_trace ={
                'x': data[x_axis_key_name4bars], 
                'y': data['Depth Base']-data['Depth Top'],
                'mode': 'markers',
                'name': "Soil Lithology Columns",
                'type': 'bar',
                'width': fence_graph_fig_bar_width,
                'base': data['Elevation Base'],
                'marker': {
                    'color': data['Color Code'],
                    'line': {
                        'color':'black',
                        'line': 1,
                        },
                    },
                'text': data['Location ID'],
                'textfont': {
                    'size': 1,
                    'color': 'black',
                    }, 
                'hoverinfo': 'text',
                'hovertext': lithology_hovertext,                     
                }
            fence_graph_fig_data.append(soil_lithology_trace)
# =============================================================================
# # add Soil Lithology Symbol:
# =============================================================================
            soil_lithology_symbol_trace ={
                'x': data[x_axis_key_name4bars], 
                'y': (data["Elevation Top"]+
                   data["Elevation Base"])/2,
                'mode': 'text',
                'name': "Soil Lithology Symbols",
                'type': 'scatter',                
                'text': data['Legend Code'],
                'textfont': {
                    'color':'white',
                    'size': fence_graph_fig_text_size*0.8,
                    },
                'textposition': 'middle center',
                'visible': 'legendonly',
                'showlegend': True,
                'hoverinfo': 'text',
                'hovertext': lithology_hovertext,                     
                }
            fence_graph_fig_data.append(soil_lithology_symbol_trace)
# =============================================================================
# # add Soil Samples:
# =============================================================================
        if dataset1_selected_soil_boring_data_table_data:            
            data=pd.DataFrame.from_records(dataset1_selected_soil_boring_data_table_data)
            data.sort_values(by=[x_axis_key_name4bars], inplace=True)
# define soil_sample_blocks_hovertext:
            display_field_name_list = [
                'Location ID',
                'Elevation Top','Elevation Base',
                'Legend Code',
                'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                'Total Unit Weight','Dry Density',
                'Test Type','Failure Mode','Chamber Pressure','Compressive Strength','Undrained Shear Strength',
                'Percentage Passing at 0_075',
                'SPT N',
                #'USCS Symbol','USCS Group Name',
                #'AASHTO Classification',
                #'Specific Gravity',
                ]
            soil_sample_blocks_hovertext= ["Project Number: "+a for a in data["Project Number"]]
            for i in range(0, len(soil_sample_blocks_hovertext)):
                for j in range(0, len(display_field_name_list)):
# =============================================================================
#                     if pd.isnull(dataset1_selected_soil_boring_data_table_data_df[display_field_name_list[j]][i]) == False:
# =============================================================================
                    if (display_field_name_list[j] in list(data.keys()) and 
                        pd.isnull(data[display_field_name_list[j]][i]) == False):                           
                        soil_sample_blocks_hovertext[i]+='<br>'+ display_field_name_list[j].replace('Percentage Passing at 0_075', '#200 Sieve Percentage Passing').replace("_", " ") + ": " + str(data[display_field_name_list[j]][i])
            soil_sample_trace ={
                'x': data[x_axis_key_name4bars], 
                'y': data['Elevation Top']-data['Elevation Base'],
                'mode': 'markers',
                'name': "Soil Sample Blocks",
                'type': 'bar',
                'width': fence_graph_fig_bar_width*0.8,
                'base': data['Elevation Base'],
                'marker': {
                    'color': data['Color Code'],
                    'line': {
                        'color':'white',
                        'line': 0.1,
                        },
                    },
                'text': data['Legend Code'],
                'textfont': {
                    'size': 1,
                    'color': 'black',
                    }, 
                'visible': 'legendonly',
                'showlegend': True,
                'hoverinfo': 'text',
                'hovertext': soil_sample_blocks_hovertext,                     
                }
            fence_graph_fig_data.append(soil_sample_trace)
# =============================================================================
# # add CPT Columns:
# =============================================================================
        if dataset1_selected_CPT_data_table_data:            
            data=pd.DataFrame.from_records(dataset1_selected_CPT_data_table_data)
            data.sort_values(by=[x_axis_key_name4bars], inplace=True)
            cpt_hovertext=['CPT ID: '+a+
                    '<br>'+'Elevation (ft): '+str(b)+
                    '<br>'+'Total Unit Weight (pcf): '+str(c)+
                    '<br>'+'Su (ksf): '+str(d)+
                    '<br>'+'SBTn, after 1990: '+str(e)+
                    '<br>'+'SBT, 2010: '+str(f)+
                    '<br>'+'Probabilistic Soil Classification (PSC): '+str(g)+
                    '<br>'+'PSC Sand, %: '+str(h)+
                    '<br>'+'PSC Silt, %: '+str(i)+
                    '<br>'+'PSC Clay, %: '+str(j)
                    for a,b,c,d,e,f,g,h,i,j in zip(data["Location ID"].tolist(),
                                       [round(a,2) for a in data["Elevation Base"]],
                                       data['Estimated Total Unit Weight (pcf)'].tolist(),
                                       data['Su (psf), Nkt'].tolist(),
                                       data["SBTn Description"].tolist(),
                                       data["SBT Description"].tolist(),
                                       data["Probabilistic Soil Classification"].tolist(),
                                       data["PSC Sand, %"].tolist(),
                                       data["PSC Silt, %"].tolist(),
                                       data["PSC Clay, %"].tolist(),
                                           )]
            if selected_CPT_method == "SBTn":
                cpt_bar_fill_color = data['SBTn Color Code 1']
                cpt_bar_line_color = data['SBTn Color Code 1']
            if selected_CPT_method == "SBT":
                cpt_bar_fill_color = data['SBT Color Code 1']
                cpt_bar_line_color = data['SBT Color Code 1']
            elif selected_CPT_method == "PSC":
                cpt_bar_fill_color = data['PSC Color Code 1']
                cpt_bar_line_color = data['PSC Color Code 1']
            cpt_trace ={
                'x': data[x_axis_key_name4bars], 
                'y': data['Elevation Base']-data['Elevation Top'],
                'mode': 'markers',
                'name': "CPT Columns",
                'type': 'bar',
                'width': fence_graph_fig_bar_width,
                'base': data['Elevation Base'],
                'marker': {
                    'color': cpt_bar_fill_color,
                    'line': {
                    'color': cpt_bar_line_color,
                    'line': 1,
                    },
                    },
                'text': data['Location ID'],
                'textfont': {
                    'size': 1,
                    'color': 'black',
                    }, 
                'hoverinfo': 'text',
                'hovertext': cpt_hovertext,                     
                }
            trace_name_list = [a['name'] for a in fence_graph_fig_data]
            if 'CPT Columns' not in trace_name_list:
                fence_graph_fig_data.append(cpt_trace)
            else:
                fence_graph_fig_data[trace_name_list.index('CPT Columns')] = cpt_trace    
# Monitor Pile:
        if dataset1_selected_test_pile_table_data:
            test_pile_data=pd.DataFrame.from_records(dataset1_selected_test_pile_table_data)
            data = test_pile_data [test_pile_data['Test Pile Category'] == 'Monitor Pile']
            if len(data) > 0:
                data.sort_values(by=[x_axis_key_name4bars], inplace=True)
                monitor_pile_hovertext = ['Project Number: '+str(a)+
                        '<br>'+'Location ID: '+str(b)+
                        '<br>'+'Test Pile Category: '+str(c)+
                        '<br>'+'Top Elevation (ft.): '+str(d)+
                        '<br>'+'Tip Elevation (ft.): '+str(e)+
                        '<br>'+'Test Pile Type ID: '+str(f)+
                        '<br>'+'Hammer ID: '+str(g)+
                        '<br>'+'Cutoff Elevation (ft.): '+str(h)+
                        '<br>'+'Target Load (tonf): '+str(i)+
                        '<br>'+'Design Load (tonf): '+str(j)+
                        '<br>'+'Blow Count End of Initial Drive: '+str(k)+
                        '<br>'+'Stroke End of Initial Drive (ft.): '+str(l)+
                        '<br>'+'End Of Drive Notes: '+str(m)+
                        '<br>'+'Designer: '+str(n)
                        for a,b,c,d,e,f,g,h,i,j,k,l,m,n in zip(data["Project Number"].tolist(),
                                             data["Location ID"].tolist(),
                                             data["Test Pile Category"].tolist(),
                                             [round(a+b,2) for a,b in zip(data["EOD Tip Elevation, ft"], data["Pile Length, ft"])],
                                             [round(a,2) for a in data["EOD Tip Elevation, ft"]],
                                             data["Test Pile Type ID"].tolist(),
                                             data["Hammer ID"].tolist(),
                                             data["Cutoff Elevation, ft"].tolist(),
                                             data["Target Load, tonf"].tolist(),
                                             data["Design Load, tonf"].tolist(),
                                             data["Blow Count End of Initial Drive"].tolist(),
                                             data["Stroke End of Initial Drive, ft"].tolist(),
                                             data["End Of Drive Notes"].tolist(),
                                             data["Designer"].tolist(),
                                               )]
                monitor_pile_trace ={
                    'x': data[x_axis_key_name4bars], 
                    'y': data['Cutoff Elevation, ft'] - data['EOD Tip Elevation, ft'],
                    'mode': 'markers',
                    'name': 'Monitor Piles',
                    'type': 'bar',
                    'width': fence_graph_fig_bar_width,
                    'base': data['EOD Tip Elevation, ft'],
                    'marker': {
                        'color': 'Aqua',
                        'line': {
                            'color':'black',
                            'line': 1,
                            },
                        },
                    'text': data['Location ID'],
                    'textfont': {
                        'size': 1,
                        'color': 'black',
                        },   
                    'hoverinfo': 'text',
                    'hovertext': monitor_pile_hovertext,                     
                    }
                fence_graph_fig_data.append(monitor_pile_trace)
# Test Pile:
        if dataset1_selected_test_pile_table_data:
            test_pile_data=pd.DataFrame.from_records(dataset1_selected_test_pile_table_data)
            data = test_pile_data[test_pile_data['Test Pile Category'] == 'Test Pile']
            if len(data) > 0:
                data.sort_values(by=[x_axis_key_name4bars], inplace=True)
                test_pile_hovertext = ['Project Number: '+str(a)+
                        '<br>'+'Location ID: '+str(b)+
                        '<br>'+'Test Pile Category: '+str(c)+
                        '<br>'+'Top Elevation (ft.): '+str(d)+
                        '<br>'+'Tip Elevation (ft.): '+str(e)+
                        '<br>'+'Test Pile Type ID: '+str(f)+
                        '<br>'+'Hammer ID: '+str(g)+
                        '<br>'+'Cutoff Elevation (ft.): '+str(h)+
                        '<br>'+'Target Load (tonf): '+str(i)+
                        '<br>'+'Design Load (tonf): '+str(j)+
                        '<br>'+'Blow Count End of Initial Drive: '+str(k)+
                        '<br>'+'Stroke End of Initial Drive (ft.): '+str(l)+
                        '<br>'+'End Of Drive Notes: '+str(m)+
                        '<br>'+'Designer: '+str(n)
                        for a,b,c,d,e,f,g,h,i,j,k,l,m,n in zip(data["Project Number"].tolist(),
                                             data["Location ID"].tolist(),
                                             data["Test Pile Category"].tolist(),
                                             [round(a+b,2) for a,b in zip(data["EOD Tip Elevation, ft"], data["Pile Length, ft"])],
                                             [round(a,2) for a in data["EOD Tip Elevation, ft"]],
                                             data["Test Pile Type ID"].tolist(),
                                             data["Hammer ID"].tolist(),
                                             data["Cutoff Elevation, ft"].tolist(),
                                             data["Target Load, tonf"].tolist(),
                                             data["Design Load, tonf"].tolist(),
                                             data["Blow Count End of Initial Drive"].tolist(),
                                             data["Stroke End of Initial Drive, ft"].tolist(),
                                             data["End Of Drive Notes"].tolist(),
                                             data["Designer"].tolist(),
                                               )]
                test_pile_trace ={
                    'x': data[x_axis_key_name4bars], 
                    'y': data['Cutoff Elevation, ft'] - data['EOD Tip Elevation, ft'],
                    'mode': 'markers',
                    'name': 'Test Piles',
                    'type': 'bar',
                    'width': fence_graph_fig_bar_width,
                    'base': data['EOD Tip Elevation, ft'],
                    'marker': {
                        'color': 'Fuchsia',
                        'line': {
                            'color':'black',
                            'line': 1,
                            },
                        },
                    'text': data['Location ID'],
                    'textfont': {
                        'size': 1,
                        'color': 'black',
                        }, 
                    'hoverinfo': 'text',
                    'hovertext': test_pile_hovertext,                     
                    }
                fence_graph_fig_data.append(test_pile_trace)
# =============================================================================
# # add Location ID text and Ground Elevation Line:
# =============================================================================
        if map_selection_points and map_selection_points['points']:
            data = pd.DataFrame.from_dict(map_selection_points['points']).dropna(subset=['hovertext'])
            data['Elevation'] = [a.split('<br>')[[i for i, s in enumerate(a.split('<br>')) if 'Ground Elevation (ft.): ' in s][0]].replace('Ground Elevation (ft.): ', '') for a in data['hovertext']]
            data['Elevation'] = [float(a) for a in data['Elevation']]
            data = data[['text', 'lon', 'lat', 'Elevation']]
            data.sort_values(by=[x_axis_key_name4ID_and_elevation_line], inplace=True)
# =============================================================================
# # add Location ID text:
# =============================================================================
        if data is not None:                               
            location_ID_hovertext = ['Location ID: '+a+
                    '<br>'+'Longitude (deg.): '+str(b)+ 
                    '<br>'+'Latitude (deg.): '+str(c) 
                    for a,b,c in zip(data["text"].tolist(),
                                     data["lon"].tolist(),
                                     data["lat"].tolist(),
                                           )]
            location_ID_trace ={
                'x': data[x_axis_key_name4ID_and_elevation_line], 
                'y': [j+15 if i % 2 == 1 else j+5 for i,j in zip(range(len(data["Elevation"])), data["Elevation"])],
                'mode': 'text',
                'name': "Location ID",
                'type': 'scatter',                
                'text': data['text'],
                'textposition':"top center",
                'textfont': {
                    'color':'black',
                    'size': fence_graph_fig_text_size,
                    },
                'visible': True,
                'showlegend': True,
                'hoverinfo': 'text',
                'hovertext': location_ID_hovertext,                     
                }
            fence_graph_fig_data.append(location_ID_trace)
# =============================================================================
# # add Ground Elevation Line:
# =============================================================================
            ground_line_hovertext=['Location ID: '+a+
                '<br>'+'Longitude (deg.): '+str(b)+ 
                '<br>'+'Latitude (deg.): '+str(c) 
                for a,b,c in zip(data["text"].tolist(),
                                 data["lon"].tolist(),
                                 data["lat"].tolist(),
                                       )]
            ground_line_trace ={
                'x': data[x_axis_key_name4ID_and_elevation_line], 
                'y': data["Elevation"],
                'mode': 'lines',
                'name': "Top Elevation Line",
                'type': 'scatter', 
                'connectgaps': True, # override default to connect the gaps
                'text': data['text'],
                'line': {
                    'color':'black',
                    'width': 2,
                    'dash': 'dash', # dash options include 'dash', 'dot', and 'dashdot'
                    },
                'visible': True,
                'showlegend': True,
                'hoverinfo': 'none',
                'hovertext': ground_line_hovertext,                     
                }
            fence_graph_fig_data.append(ground_line_trace)
    elif len(fence_graph_fig_data)>0 and triggered_input_id== fence_graph_direction + '-fence-plot-text-size-slider':
        for i in range(0, len(fence_graph_fig_data)):
            if 'textfont' in fence_graph_fig_data[i].keys():
                fence_graph_fig_data[i]['textfont']['size'] = fence_graph_fig_text_size
# =============================================================================
#     elif len(fence_graph_fig_data)>0 and triggered_input_id==fence_graph_direction + '-fence-plot-bar-width-slider':
#         for i in range(0, len(fence_graph_fig_data)):
#             if 'width' in fence_graph_fig_data[i].keys() and fence_graph_fig_data[i]['name']!="Soil Sample Blocks":
#                 fence_graph_fig_data[i]['width'] = fence_graph_fig_bar_width
#             elif 'width' in fence_graph_fig_data[i].keys() and fence_graph_fig_data[i]['name']=="Soil Sample Blocks":
#                 fence_graph_fig_data[i]['width'] = fence_graph_fig_bar_width*0.8
#         
#     elif triggered_input_id=='map-graph' and len(fence_graph_fig_data)>0:
#         fence_graph_fig_data=[]
# =============================================================================
    if fence_graph_fig_data:                           
        return fence_graph_fig_data         
def finalize_composite_soil_boring_func(
        data,
        composite_thickness_resolution,
        data_profile_data_store_1,
        data_profile_data_store_2,
        data_profile_data_store_3,
        data_profile_data_store_4,
        data_profile_data_store_5,
        ):
    composite_soil_boring_data = [a for a in data]
    if len(data) > 0:
        x_axis_parameter_list = ['']*5
        composite_layer_elev_base = data[0]['base']
        composite_layer_elev_top =[a+b for a,b in zip(data[0]['base'], data[0]['y'])]
        composite_layer_soil_classification =data[0]['text']
        composite_layer_soil_type = [a for a in data[0]['text']]
        for i in range(0, len(composite_layer_soil_type)):
            if composite_layer_soil_classification[i] in ["GP-GC","GP","GC"]:
                composite_layer_soil_type[i] = 'Gravel'
            elif composite_layer_soil_classification[i] in ["SP", "SP-SM", "SP-SC", "SM", "SC-SM", "SC"]:
                composite_layer_soil_type[i] = 'Sand'
            elif composite_layer_soil_classification[i] in ["MLS", "ML"]:
                composite_layer_soil_type[i] = 'Silt'
            elif composite_layer_soil_classification[i] in ["CLS", "CH+SC", "CL-ML", "CL", "CH", "OH", "PT"]:
                composite_layer_soil_type[i] = 'Clay'
        for i in range(0,5):
            vars()['data_profile_layer_elev_list_' + str(i+1)] = []
            if len(vars()['data_profile_data_store_' + str(i+1)])>0:
                x_axis_parameter_list[i] = vars()['data_profile_data_store_' + str(i+1)][0]['name']
# get layer elevation list from all data profiles: 
# =============================================================================
#                 if (len(vars()['data_profile_data_store_' + str(i+1)])>5 and 
#                     vars()['data_profile_data_store_' + str(i+1)][5]['name'] == 'Stratification Text'):
#                     vars()['data_profile_layer_elev_list_' + str(i+1)] = vars()['data_profile_data_store_' + str(i+1)][5]['y']
# 
# =============================================================================
                if (len(vars()['data_profile_data_store_' + str(i+1)])>5):
                    trace_name_list = [a['name'] for a in vars()['data_profile_data_store_' + str(i+1)]]
                    if 'Stratification Text' in trace_name_list:
                        idx = trace_name_list.index('Stratification Text')
                        vars()['data_profile_layer_elev_list_' + str(i+1)] = vars()['data_profile_data_store_' + str(i+1)][idx]['y']
        final_soil_type = [a for a in composite_layer_soil_type]
        final_layer_top_elevation = [a for a in composite_layer_elev_top]
        final_layer_base_elevation = [a for a in composite_layer_elev_base]
# =============================================================================
# # finalize layers based on shear/compressive strength in fines layers:
# =============================================================================    
        for i in range(0,5):
            if (x_axis_parameter_list[i] in ['Compressive Strength','Undrained Shear Strength'] and
                len(vars()['data_profile_layer_elev_list_' + str(i+1)])>0):
                for j in range(0, len(final_soil_type)):
                    if final_soil_type[j] in ["Clay", "Silt", "Clay or Silt"]:
                        for k in range(0, len(vars()['data_profile_layer_elev_list_' + str(i+1)])):
                            if (vars()['data_profile_layer_elev_list_' + str(i+1)][k] < final_layer_top_elevation[j]-composite_thickness_resolution and
                                vars()['data_profile_layer_elev_list_' + str(i+1)][k] >= final_layer_base_elevation[j]+composite_thickness_resolution):
                                final_layer_top_elevation.append(vars()['data_profile_layer_elev_list_' + str(i+1)][k])
                                final_layer_base_elevation.append(vars()['data_profile_layer_elev_list_' + str(i+1)][k])
                                final_soil_type.append(final_soil_type[j])
                final_soil_type = [x for _,x in sorted(zip(final_layer_top_elevation,final_soil_type), reverse=True)]  
                final_layer_top_elevation=sorted(final_layer_top_elevation, reverse=True)   
                final_layer_base_elevation=sorted(final_layer_base_elevation, reverse=True)   
# =============================================================================
# # finalize layers based on other parameters:
# =============================================================================
        x_axis_parameter_priority_list = ['Moisture Content', 
                                          'Total Unit Weight', 'Dry Density', 
                                          'Liquid Limit', 'Plastic Limit',
                                          'Plasticity Index', 'Liquidity Index',
                                          '#200 Finer',
                                          'SPT N',
                                          ]
        for m in x_axis_parameter_priority_list:
            if m in x_axis_parameter_list:
                i = x_axis_parameter_list.index(m)
                if (len(vars()['data_profile_layer_elev_list_' + str(i+1)])>0):
                    for j in range(0, len(final_soil_type)):
                        if final_soil_type[j] in ["Clay", "Silt", "Clay or Silt"]:
                            vars()['data_profile_layer_elev_list_' + str(i+1)] = [x for x in vars()['data_profile_layer_elev_list_' + str(i+1)] if x]
# =============================================================================
#                             print(vars()['data_profile_layer_elev_list_' + str(i+1)])
# =============================================================================
                            for k in range(0, len(vars()['data_profile_layer_elev_list_' + str(i+1)])):
                                if (vars()['data_profile_layer_elev_list_' + str(i+1)][k] < final_layer_top_elevation[j]-composite_thickness_resolution and
                                    vars()['data_profile_layer_elev_list_' + str(i+1)][k] >= final_layer_base_elevation[j]+composite_thickness_resolution):
                                    final_layer_top_elevation.append(vars()['data_profile_layer_elev_list_' + str(i+1)][k])
                                    final_layer_base_elevation.append(vars()['data_profile_layer_elev_list_' + str(i+1)][k])
                                    final_soil_type.append(final_soil_type[j])
                    final_soil_type = [x for _,x in sorted(zip(final_layer_top_elevation,final_soil_type), reverse=True)]  
                    final_layer_top_elevation=sorted(final_layer_top_elevation, reverse=True)   
                    final_layer_base_elevation=sorted(final_layer_base_elevation, reverse=True)   
        final_soil_type4plotting = final_soil_type + [None]
        final_layer_elevation = final_layer_top_elevation + [final_layer_base_elevation[-1]]
        final_layer_elevation4plotting = [np.float('NaN')]*(len(final_layer_elevation)*3)
        final_layer_elevation4plotting[::3] = final_layer_elevation
        final_layer_elevation4plotting[1::3] = final_layer_elevation
        x4final_layer_elevation4plotting  = [np.float('NaN')]*(len(final_layer_elevation)*3)
        x4final_layer_elevation4plotting[::3] = [-60] * len(final_layer_elevation)
        x4final_layer_elevation4plotting[1::3] = [140] * len(final_layer_elevation)
        final_layer_elevation_text_list=[str(round(a,1)) + ' ft.' for a in final_layer_elevation]
        x4final_layer_elevation_text_list = [-60] * len(final_layer_elevation)
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_trace               
# =============================================================================
# =============================================================================
# =============================================================================
        stratification_line_trace ={
            'x': x4final_layer_elevation4plotting, 
            'y': final_layer_elevation4plotting,
            'customdata': final_layer_elevation4plotting,
            'mode': 'lines',
            'name': 'Stratification',
            'type': 'scatter',
            'line': {
                'color': 'gray',
                'width': 1,
                'dash': 'dashdot',
                },
            'visible': True, #'legendonly',
            'showlegend': True,
            'legendgroup': 'Stratification',            
            'hoverinfo': 'text',
            #'hovertext': None,                     
            }
        trace_name_list = [a['name'] for a in composite_soil_boring_data]
        if 'Stratification' not in trace_name_list:
            composite_soil_boring_data.append(stratification_line_trace) 
        else:
            composite_soil_boring_data[trace_name_list.index('Stratification')] = stratification_line_trace    
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_text_trace               
# =============================================================================
# =============================================================================
# =============================================================================
        stratification_line_text_trace ={
            'x': x4final_layer_elevation_text_list, 
            'y': final_layer_elevation,
            'customdata': final_soil_type4plotting,
            'mode': 'text',
            'name': 'Stratification Text',
            'type': 'scatter',
            'line': {
                'color': 'gray',
                'width': 1,
                'dash': 'dashdot',
                },
            'text': final_layer_elevation_text_list,
            'textposition': "top right",
            'textfont': {
                'size': 8,                    
                },
            'visible': True, #'legendonly',
            'showlegend': False,
            'legendgroup': 'Stratification',
            'hoverinfo': 'text',
            #'hovertext': None,                     
            }
        trace_name_list = [a['name'] for a in composite_soil_boring_data]
        if 'Stratification Text' not in trace_name_list:
            composite_soil_boring_data.append(stratification_line_text_trace) 
        else:
            composite_soil_boring_data[trace_name_list.index('Stratification Text')] = stratification_line_text_trace    
    return composite_soil_boring_data
def finalize_design_lines_func(
        design_profile_fig_data,
        design_line_elevation,
        design_soil_types,
        soil_design_values,
                    ):
    top_elevation = design_line_elevation[:-1]
    base_elevation = design_line_elevation[1:]
    design_soil_types = design_soil_types[:-1]
    soil_design_values = soil_design_values[:-1]
# =============================================================================
# # design_line_trace:       
# =============================================================================
# define x and y lists:
    y_list = [np.float('NaN')]*(len(top_elevation)*3)
    y_list[::3] = [a for a in top_elevation]
    y_list[1::3] = [a for a in base_elevation]
    x_list = [np.float('NaN')]*(len(soil_design_values)*3)
    x_list[::3] = [a for a in soil_design_values]
    x_list[1::3] = [a for a in soil_design_values]
    design_line_trace ={
        'x': x_list, 
        'y': y_list,
        'customdata': x_list,
        'mode': 'lines',
        'name': 'Design Lines',
        'type': 'scatter',
        'line': {
            'color': 'red',
            'width': 3,
            'dash': 'solid',
            },
        'visible': True, #'legendonly',
        'showlegend': True,
        'legendgroup': 'Design Lines',               
        'hoverinfo': 'text',
        #'hovertext': None,                     
        }
    trace_name_list = [a['name'] for a in design_profile_fig_data]
    if 'Design Lines' not in trace_name_list:
        design_profile_fig_data.append(design_line_trace) 
    else:
        design_profile_fig_data['Design Lines'] = design_line_trace             
# design_line_text_trace               
    design_line_text_trace ={
        'x': soil_design_values, 
        'y': top_elevation,
        'customdata': design_soil_types,
        'mode': 'text',
        'name': 'Design Line Text',
        'type': 'scatter',
        'text': [a if pd.isnull(a) == True else round(a,0) for a in soil_design_values],
        'textposition': "top right",
        'textfont': {
            'size': 12,
            'color': 'red',
            },
        'visible': True, #'legendonly',
        'showlegend': False,
        'legendgroup': 'Design Lines',               
        'hoverinfo': 'text',
        #'hovertext': None,                     
        }
    if 'Design Line Text' not in trace_name_list:
        design_profile_fig_data.append(design_line_text_trace) 
    else:
        design_profile_fig_data['Design Line Text'] = design_line_text_trace             
    return design_profile_fig_data 
def general_data_profile_func(data_profile_name):
    data_profile_plot_fig = go.Figure()
    #data_profile_plot_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
    #data_profile_plot_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
    data_profile_plot_fig.update_yaxes(autorange=False,
                                       showline=True, linewidth=1, linecolor='gray', mirror=True,
                                       showgrid=True, gridwidth=0.2, gridcolor='lightgray',
                                       zeroline=True, zerolinewidth=1, zerolinecolor='darkgray',
                                       #showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across",
                                       )
    data_profile_plot_fig.update_xaxes(autorange=False,
                                       showline=True, linewidth=1, linecolor='gray', mirror=True,
                                       showgrid=True, gridwidth=0.1, gridcolor='lightgray',
                                       zeroline=True, zerolinewidth=1, zerolinecolor='darkgray',
                                       )
    #data_profile_plot_fig.add_trace(go.Bar())
    data_profile_plot_fig.update_layout(        
        plot_bgcolor = '#FEF5E7',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',
        barmode='stack',
        # title='Fence Plot, West to East',
        xaxis=dict(
            title='X Axis Parameter',
            #autorange=True,
        ),
        yaxis=dict(
            title='Elevation (ft.)',
            #autorange=True,
        ),
        font=dict(
            #family='Times New Roman',
            size=8,
            color='black',
            ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="left",
            x=0.01,
            bordercolor = 'darkgray',
            bgcolor = 'white',
            borderwidth = 1,
            tracegroupgap = 5,
            # itemsizing = 'constant',
            font = dict(
                size = 6,                
                ),            
            ),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=500,
        autosize=True,            
        margin=dict(
            l=1,
            r=1,
            b=1,
            t=1,
            pad=1,
        ),
        clickmode='event+select',
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        hoverdistance = 1,
        # This is where to change to hoverlable text font size 07/14/2022, 6-> 10
        hoverlabel=dict(font=dict(size=10), namelength=-1,),
        dragmode="pan",         
        )
    data_profile_graph_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 1200,# None
            'width': 400, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
# =============================================================================
#         'edits': {
#             'legendPosition': True,
#             'legendText': True,
#             
#             },
# =============================================================================
        'doubleClick': 'autosize',
        'modeBarButtonsToAdd':['drawline',
                               #'drawopenpath',
                               #'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':[#'select2d',
                               #'lasso2d',
                               'zoom2d',
                               'zoomIn2d',
                               'zoomOut2d',
                               'hoverCompareCartesian',
                               ],
            }
    data_profile_graph=dcc.Graph(
        id= data_profile_name.replace(" ", "-") + '-data-profile-graph',
        # animate=False,
        figure=data_profile_plot_fig,
        config=data_profile_graph_config,
    )
    return data_profile_graph
def general_data_profile_tab_func(data_profile_graph, 
                                    data_profile_name, 
                                    x_axis_parameter_list, 
                                    x_axis_parameter_selection,
                                    data_profile_tab_color,
                                    data_profile_tab_text_color,                                    
                                    ):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # x_axis_parameter_select_object:
# =============================================================================
# =============================================================================
# =============================================================================
    x_axis_parameter_select_object=dbc.Select(
        id=data_profile_name.replace(" ", "-") + '-x-axis-parameter-select',
        options=[{'label': a.replace('Percentage Passing at 0_075', '#200 Finer').replace("_", " "), 'value': a} for a in x_axis_parameter_list],
        value=x_axis_parameter_selection,
        bs_size = "sm",
        style={
        'width': '100%',
        # 'margin': '5px 5px 5px 5px',
        'borderWidth': '1px',
        'color': data_profile_tab_text_color,
        'background-color': data_profile_tab_color,
        'font-size': 'xx-small',
        },
        )
    x_axis_parameter_select_object_group = dbc.FormGroup(
        [
            dbc.Label(" X-Axis ", 
                      size = 'sm', 
                      # className="mt-0 mb-0 ml-0 mr-0",
                      html_for=data_profile_name.replace(" ", "-") + '-x-axis-parameter-select', 
                      id=data_profile_name.replace(" ", "-") + '-x-axis-parameter-select-label',
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 5px 0px',
                          'padding': '0px 0px 0px 10px', 
                          },                      
                      ),
            x_axis_parameter_select_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'left',
            'margin': '10px 0px 5px 0px',
            'padding': '5px 25px 5px 5px',   
            'background-color': 'white',
            'font-size': 'xx-small',
        },  
    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # window_size_slider_object:
# =============================================================================
# =============================================================================
# =============================================================================
    window_size_slider_object=dcc.Slider(
        id=data_profile_name.replace(" ", "-") + "-window-size-slider", 
        min=1, 
        max=10, 
        step=1, 
        value=4,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a), 'style':{'font-size': 'xx-small'}} for a in range(1,11,2)},
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-4 pl-2 pr-2",
        )
    window_size_slider_object_group = dbc.FormGroup(
        [
            dbc.Label("Window Size", 
                      size = 'sm', 
                      html_for=data_profile_name.replace(" ", "-") + "-window-size-slider", 
                      id=data_profile_name.replace(" ", "-") + "-window-size-slider-label",
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 2px 0px',
                          'padding': '0px 0px 0px 10px', 
                          }, 
                      ),
            window_size_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'left',
            'margin': '5px 0px 10px 0px',
            'padding': '0px 0px 0px 0px', 
            'background-color': 'white',
            'font-size': 'xx-small',
        },    
    )
# =============================================================================
# =============================================================================
# # # data_profile_group_tab_content:
# =============================================================================
    data_profile_group_tab_content = html.Div(
            [
                dbc.Row(
                    [
                        dcc.Store(
                            id=data_profile_name.replace(" ", "-") + '-clientside-figure-data-store',
                            data=[],
                        ), 
                        dcc.Store(
                            id=data_profile_name.replace(" ", "-") + '-clientside-figure-layout-store',
                            data={},
                        ), 
                        dbc.Col(            
                            dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                                id=data_profile_name.replace(" ", "-") + '-clientside-store-loading-hidden-div', children="Loading Status", style={'display': 'none'})),            
                            width='0',
                            ),
                        dbc.Col(
                            x_axis_parameter_select_object_group,
                            width='12',
                            ),
                        dbc.Col(
                            dcc.Loading(window_size_slider_object_group,type="default", fullscreen=False, color="red", ),
                            width='12',
                            ),
                        dcc.Store(
                            id=data_profile_name.replace(" ", "-") + '-window-size-slider-store',
                            data=[1, 1, 1, 1, {1: {'label': '1'}}],
                        ), 
                        ],
                    style={
                        'width': '99%',            
                        'borderWidth': '0px',
                        'borderStyle': 'solid',
                        'borderRadius': '10px',
                        'margin': '10px 0px 5px 0px',
                        'padding': '0px 0px 0px 0px',    
                        'background-color': 'lightgray',
                    },            
                    # className="ml-2 mr-2",
                    ),
                dbc.Row(
                        dbc.Col(data_profile_graph,width='12'),
                    ),
                ],
        className="mt-0 mb-0 ml-0 mr-0",
    )
# =============================================================================
# =============================================================================
# # # data_profile_tab:
# =============================================================================
# =============================================================================
    data_profile_tab = dbc.Tab(label=data_profile_name, 
            tab_id=data_profile_name.replace(' ', '-') + '-tab',
            children=[
                data_profile_group_tab_content,
                ],
            tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            active_tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            label_style={
                "color": data_profile_tab_text_color,
                'background-color': data_profile_tab_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '10px',                  
                },
            active_label_style={
                "color": data_profile_tab_color,
                'background-color': data_profile_tab_text_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '10px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )    
    return data_profile_tab
def general_design_profile_tab_func_A(design_profile_graph, 
                                    design_profile_name, 
                                    x_axis_parameter_list, 
                                    x_axis_parameter_selection,
                                    design_profile_tab_color,
                                    design_profile_tab_text_color,                                    
                                    ):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # x_axis_parameter_select_object:
# =============================================================================
# =============================================================================
# =============================================================================
    x_axis_parameter_select_object=dbc.Select(
        id=design_profile_name.replace(" ", "-") + '-x-axis-parameter-select',
        options=[{'label': a.replace('Percentage Passing at 0_075', '#200 Finer').replace("_", " "), 'value': a} for a in x_axis_parameter_list],
        value=x_axis_parameter_selection,
        bs_size = "sm",
        style={
        'width': '100%',
        # 'margin': '5px 5px 5px 5px',
        'borderWidth': '1px',
        'color': design_profile_tab_text_color,
        'background-color': design_profile_tab_color,
        'font-size': 'xx-small',
        },
        )
    x_axis_parameter_select_object_group = dbc.FormGroup(
        [
            dbc.Label(" X-Axis ", 
                      size = 'sm', 
                      # className="mt-0 mb-0 ml-0 mr-0",
                      html_for=design_profile_name.replace(" ", "-") + '-x-axis-parameter-select', 
                      id=design_profile_name.replace(" ", "-") + '-x-axis-parameter-select-label',
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 5px 0px',
                          'padding': '0px 0px 0px 10px', 
                          },                      
                      ),
            x_axis_parameter_select_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'left',
            'margin': '10px 0px 5px 0px',
            'padding': '5px 25px 5px 5px',   
            'background-color': 'white',
            'font-size': 'xx-small',
        },  
    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # quantile_range_slider_object:
# =============================================================================
# =============================================================================
# =============================================================================
    quantile_range_slider_object=dcc.RangeSlider(
        id=design_profile_name.replace(" ", "-") + "-quantile-range-slider", 
        min=0.05, 
        max=1, 
        step=0.05, 
        value=[0.25, 0.75],
        included=True,
        allowCross=False,
        pushable=0.05,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={x: {'label': str(x), 'style':{'font-size': 'xx-small'}} for x in np.arange(0.25, 0.76, 0.25)},
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-4 pl-2 pr-2",
        )
    quantile_range_slider_object_group = dbc.FormGroup(
        [
            dbc.Label("Quantile Range", 
                      size = 'sm', 
                      html_for=design_profile_name.replace(" ", "-") + "-quantile-range-slider", 
                      id=design_profile_name.replace(" ", "-") + "-quantile-range-slider-label",
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 2px 0px',
                          'padding': '0px 0px 0px 10px', 
                          }, 
                      ),
            quantile_range_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'left',
            'margin': '5px 0px 10px 0px',
            'padding': '0px 0px 0px 0px', 
            'background-color': 'white',
            'font-size': 'xx-small',
        },    
    )
# =============================================================================
# =============================================================================
# # # design_profile_group_tab_content:
# =============================================================================
    design_profile_group_tab_content = html.Div(
            [
                dbc.Row(
                    [
                        dcc.Store(
                            id=design_profile_name.replace(" ", "-") + '-clientside-figure-data-store',
                            data=[],
                        ), 
                        dcc.Store(
                            id=design_profile_name.replace(" ", "-") + '-clientside-figure-layout-store',
                            data={},
                        ), 
                        dbc.Col(            
                            dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                                id=design_profile_name.replace(" ", "-") + '-clientside-store-loading-hidden-div', children="Loading Status", style={'display': 'none'})),            
                            width='0',
                            ),
                        dbc.Col(
                            x_axis_parameter_select_object_group,
                            width='12',
                            ),
                        dbc.Col(
                            dcc.Loading(quantile_range_slider_object_group,type="default", fullscreen=False, color="red", ),
                            width='12',
                            ),                        
                        ],
                    style={
                        'width': '99%',            
                        'borderWidth': '0px',
                        'borderStyle': 'solid',
                        'borderRadius': '10px',
                        'margin': '10px 0px 5px 5px',
                        'padding': '0px 0px 0px 0px',    
                        'background-color': 'lightgray',
                    },            
                    # className="ml-2 mr-2",
                    ),
                dbc.Row(
                        dbc.Col(design_profile_graph,width='12'),
                    ),
                ],
        className="mt-0 mb-0 ml-0 mr-0",
    )
# =============================================================================
# =============================================================================
# # # design_profile_tab:
# =============================================================================
# =============================================================================
    design_profile_tab = dbc.Tab(label=design_profile_name, 
            tab_id=design_profile_name.replace(' ', '-') + '-tab',
            children=[
                design_profile_group_tab_content,
                ],
            tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            active_tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            label_style={
                "color": design_profile_tab_text_color,
                'background-color': design_profile_tab_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '10px',                  
                },
            active_label_style={
                "color": design_profile_tab_color,
                'background-color': design_profile_tab_text_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '10px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )    
    return design_profile_tab
def general_design_profile_tab_func_B(design_profile_graph, 
                                    design_profile_name, 
                                    design_profile_tab_color,
                                    design_profile_tab_text_color,                                    
                                    ):
    # =============================================================================
# =============================================================================
# =============================================================================
# # # # design_line_check_group:
# =============================================================================
# =============================================================================
# =============================================================================
    design_line_check_group = dbc.FormGroup(
        [
            dbc.Checkbox(
                id=design_profile_name.replace(" ", "-") + '-design-line-checkbox', 
                className="form-check-input",
                checked=True,
            ),
            dbc.Label(
                "Design Parameter",
                html_for=design_profile_name.replace(" ", "-") + '-design-line-checkbox',
                id=design_profile_name.replace(" ", "-") + '-design-line-checkbox-label',
                style={
                    'font-size': '8px',
                    'margin': '5px 0px 5px 0px',
                    'padding': '5px 0px 5px 0px', 
                    },                                                          
            ),
        ],
        inline=False,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'left',
            'margin': '5px 0px 5px 0px',
            'padding': '5px 10px 5px 10px',   
            'background-color': '#F2F4F4',
        },                                                                  
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # select_baseline_design_parameters_object_group:
# =============================================================================
# =============================================================================
# =============================================================================
    select_baseline_design_parameters_object=dbc.Select(
        id=design_profile_name.replace(" ", "-") + '-baseline-design-parameters-select',
        options=[
            {'label': 'Mean', 'value': 'Mean'}, 
            {'label': 'Lower Bound', 'value': 'Lower Bound'},
            {'label': 'Upper Bound', 'value': 'Upper Bound'},
            ],
        value='Mean',
        bs_size = "sm",
        style={
        'width': '100%',
        # 'margin': '5px 5px 5px 5px',
        'borderWidth': '1px',
        'color': design_profile_tab_text_color,
        'background-color': design_profile_tab_color,
        'font-size': 'xx-small',
        },
        )
    select_baseline_design_parameters_object_group = dbc.FormGroup(
        [
            dbc.Label(" Baseline Case:", 
                      size = 'sm', 
                      # className="mt-0 mb-0 ml-0 mr-0",
                      html_for=design_profile_name.replace(" ", "-") + '-baseline-design-parameters-select', 
                      id=design_profile_name.replace(" ", "-") + '-baseline-design-parameters-select-label',
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 5px 0px',
                          'padding': '0px 0px 0px 10px', 
                          },                      
                      ),
            select_baseline_design_parameters_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'left',
            'margin': '10px 0px 10px 0px',
            'padding': '5px 5px 5px 5px',   
            'background-color': 'white',
            'font-size': 'xx-small',
        },  
    )
# =============================================================================
# =============================================================================
# # # design_profile_group_tab_content:
# =============================================================================
    design_profile_group_tab_content = html.Div(
            [
                dbc.Row(
                    [
                        dcc.Store(
                            id=design_profile_name.replace(" ", "-") + '-clientside-figure-data-store',
                            data=[],
                        ), 
                        dcc.Store(
                            id=design_profile_name.replace(" ", "-") + '-clientside-figure-layout-store',
                            data={},
                        ), 
                        dbc.Col(            
                            dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                                id=design_profile_name.replace(" ", "-") + '-clientside-store-loading-hidden-div', children="Loading Status", style={'display': 'none'})),            
                            width='0',
                            ),
                        dbc.Col(
                            design_line_check_group,
                          width='4',
                            ),            
                        dbc.Col(
                            select_baseline_design_parameters_object_group,
                            width='8',
                            ),            
                        ],
                    style={
                        'width': '99%',            
                        'borderWidth': '0px',
                        'borderStyle': 'solid',
                        'borderRadius': '10px',
                        'margin': '10px 0px 5px 0px',
                        'padding': '0px 0px 0px 0px',    
                        'background-color': 'lightgray',
                    },            
                    # className="ml-2 mr-2",
                    ),
                dbc.Row(
                        dbc.Col(design_profile_graph,width='12'),
                    ),
                ],
        className="mt-0 mb-0 ml-0 mr-0",
    )
# =============================================================================
# =============================================================================
# # # design_profile_tab:
# =============================================================================
# =============================================================================
    design_profile_tab = dbc.Tab(label=design_profile_name, 
            tab_id=design_profile_name.replace(' ', '-') + '-tab',
            children=[
                design_profile_group_tab_content,
                ],
            tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            active_tab_style={
                'margin': '1px 1px 1px 1px',
                'padding': '1px 1px 1px 1px',                        
                },
            label_style={
                "color": design_profile_tab_text_color,
                'background-color': design_profile_tab_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '10px',                  
                },
            active_label_style={
                "color": design_profile_tab_color,
                'background-color': design_profile_tab_text_color,
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '10px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )    
    return design_profile_tab
def map_point_selection_func(data_dict,
                             selected_point_location_ID,
                             combined_column_names_sort_order,
                             collection_name):
    selected_point_data_table_columns=[]
    selected_point_data_table_data=[]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Project-Based mode:
# =============================================================================
# =============================================================================
# =============================================================================
    if collection_name in list(data_dict.keys()) and data_dict[collection_name] is not None:
# =============================================================================
# =============================================================================
# generate datatable:            
# =============================================================================
# =============================================================================
        data = data_dict[collection_name]
        data = [d for d in data if d['Location ID'] in selected_point_location_ID]
        combined_column_names = list(set(x for l in data for x in l.keys()))                
        combined_column_names = [a for x in combined_column_names_sort_order for a in combined_column_names if a == x]
        #print(combined_column_names)
        selected_point_data_table_columns=[{"name": i.replace('Percentage Passing at 0_075', '#200 Sieve Percentage Passing').replace("_"," "), "id": i}  for i in combined_column_names]
        selected_point_data_table_data=sorted(data, key = lambda i: (i['Location ID'], 
                                                                     i['Longitude Decimal'], 
                                                                     i['Latitude Decimal'], 
                                                                     #i['Depth Top'],
                                                                     ))
    return selected_point_data_table_columns, selected_point_data_table_data
def point_list_legend_func(
        selected_point_list_df,
                    ):
# =============================================================================
# # add Soil Sample data:
# =============================================================================
        point_list_fig_data = []
        if len(selected_point_list_df)>0:
            point_list_rows = int(np.ceil(len(selected_point_list_df)/30))
            x_value_list = list(range(0,30))*(point_list_rows-1)+list(range(0,len(selected_point_list_df)-(point_list_rows-1)*30))
            y_value = [2.5*a for a in list(range(0, point_list_rows))]
            y_value.sort(reverse = True)
            y_value_list =[]
            for i in range(0, point_list_rows-1):
                y_value_list += [y_value[i]]*30   
            y_value_list += [y_value[-1]]*(len(selected_point_list_df)-(point_list_rows-1)*30)     
            point_list_trace ={
                'x': x_value_list, 
                'y': y_value_list,
                'mode': 'markers+text',
                'name': 'Point List',
                'type': 'scatter',
                'marker': {
                    'color': selected_point_list_df['customdata'],
                    'size': 10,
                    'line': {
                        'color':'black',
                        'width': 1,
                        },
                    },
                'text': selected_point_list_df['text'],
                'textposition': "top center",
                'textfont': {
                    'size': 6,
                    'color':'black',
                    },
                'visible': True, #'legendonly',
                'showlegend': False,
                'hoverinfo': 'text',
                'hovertext': selected_point_list_df['hovertext'],                     
                }
            point_list_fig_data.append(point_list_trace)
        return point_list_fig_data 
def stratify_composite_soil_boring_func(data, composite_thickness_resolution):
    boring_top_elevation=max(data['Elevation Top'])
    boring_base_elevation=min(data['Elevation Base'])
    soil_sample_elevation=(data["Elevation Top"]+ data["Elevation Base"])/2
    soil_sample_legend_code=data['Legend Code']
    number_of_soil_layers=int(np.ceil((boring_top_elevation-boring_base_elevation)/composite_thickness_resolution))
    soil_layer_elevation=[boring_top_elevation]*(number_of_soil_layers+1)
    for i in range(1, len(soil_layer_elevation)):
        soil_layer_elevation[i] = round(soil_layer_elevation[i-1]-composite_thickness_resolution,1)
    soil_layer_elevation[-1] = boring_base_elevation
    soil_sample_elevation_layer_groups=[[]]*number_of_soil_layers
    soil_sample_legend_code_layer_groups=[[]]*number_of_soil_layers
    for i in range(0, number_of_soil_layers):
        soil_sample_elevation_layer_groups[i]=[a for a in soil_sample_elevation if a<=soil_layer_elevation[i] and a>soil_layer_elevation[i+1]]
        soil_sample_legend_code_layer_groups[i]=[a for a, b in zip(soil_sample_legend_code, soil_sample_elevation) if b<=soil_layer_elevation[i] and b>soil_layer_elevation[i+1]]    
    legend_code4gravel = ["GP-GC","GP","GC"]
    legend_code4sand = ["SP", "SP-SM", "SP-SC", "SM", "SC-SM", "SC"]
    legend_code4silt = ["MLS", "ML"]
    legend_code4clay = ["CLS", "CH+SC", "CL-ML", "CL", "CH", "OH", "PT"]
    soil_layer_color=['']*len(soil_sample_legend_code_layer_groups)
    soil_type=[""]*len(soil_sample_legend_code_layer_groups)
    layer_clay_ratio=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    layer_silt_ratio=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    layer_fines_ratio=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    layer_sands_ratio=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    layer_gravel_ratio=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    layer_coarse_ratio=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    number_of_soil_sample_in_layer=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups)
    for j in range(0, len(soil_sample_legend_code_layer_groups)):
        if len(soil_sample_legend_code_layer_groups[j])>0:
            clay_ratio=len(list(x for x in soil_sample_legend_code_layer_groups[j] if x in legend_code4clay))/len(soil_sample_legend_code_layer_groups[j])
            silt_ratio=len(list(x for x in soil_sample_legend_code_layer_groups[j] if x in legend_code4silt))/len(soil_sample_legend_code_layer_groups[j])
            fines_ratio=len(list(x for x in soil_sample_legend_code_layer_groups[j] if x in legend_code4clay + legend_code4silt))/len(soil_sample_legend_code_layer_groups[j])
            sand_ratio=len(list(x for x in soil_sample_legend_code_layer_groups[j] if x in legend_code4sand))/len(soil_sample_legend_code_layer_groups[j])
            gravel_ratio=len(list(x for x in soil_sample_legend_code_layer_groups[j] if x in legend_code4gravel))/len(soil_sample_legend_code_layer_groups[j])
            others_ratio=len(list(x for x in soil_sample_legend_code_layer_groups[j] if x not in legend_code4clay + legend_code4silt + legend_code4sand + legend_code4gravel))/len(soil_sample_legend_code_layer_groups[j])
            total_ratio=clay_ratio+fines_ratio+silt_ratio+sand_ratio+gravel_ratio+others_ratio
            if total_ratio <1:
                print("Layer "+ str(j) +": total_ratio < 1")
            layer_clay_ratio[j] = clay_ratio
            layer_silt_ratio[j] = silt_ratio
            layer_fines_ratio[j] = fines_ratio
            layer_sands_ratio[j] = sand_ratio
            layer_gravel_ratio[j] = gravel_ratio
            layer_coarse_ratio[j] = sand_ratio + gravel_ratio
            number_of_soil_sample_in_layer[j] = len(soil_sample_legend_code_layer_groups[j])
            if clay_ratio>=0.5:
                soil_layer_color[j] = '#006400'
                soil_type[j]="Clay"
            elif silt_ratio>=0.5:
                soil_layer_color[j] = '#FF4500'
                soil_type[j]="Silt"
            elif fines_ratio>=0.5:
                soil_layer_color[j] = '#6B8E23'
                soil_type[j]="Clay or Silt"
            elif sand_ratio>0.5:
                soil_layer_color[j] = '#DAA520'
                soil_type[j]="Sand"
            elif gravel_ratio>0.5:
                soil_layer_color[j] = '#708090'
                soil_type[j]="Gravel"
            elif fines_ratio<0.5:
                soil_layer_color[j] = '#BDB76B'
                soil_type[j]="Sand or Gravel"
            elif others_ratio>0.5:
                soil_layer_color[j] = '#FFFFFF'
                soil_type[j]="Others"
            elif j>=1 and total_ratio<1:
                soil_layer_color[j]=soil_layer_color[j-1]
                soil_type[j]=soil_type[j-1]
            elif j<len(soil_sample_legend_code_layer_groups)-1 and total_ratio<1:
                soil_layer_color[j]=soil_layer_color[j+1]
                soil_type[j]=soil_type[j+1]
        elif j > 0:
            layer_clay_ratio[j] = 0
            layer_silt_ratio[j] = 0
            layer_fines_ratio[j] = 0
            layer_sands_ratio[j] = 0
            layer_gravel_ratio[j] = 0
            layer_coarse_ratio[j] = 0
            number_of_soil_sample_in_layer[j] = 0            
    for_loop_repeat_idx=0
    while for_loop_repeat_idx <100:
        for i in range(1, len(soil_layer_color)):
            if soil_layer_color[i] == "":
                soil_layer_color[i] = soil_layer_color[i-1]
                soil_type[i] = soil_type[i-1]
        for_loop_repeat_idx+=1
# =============================================================================
# # combine same soil type:    
# =============================================================================
    soil_layer_color_combined=[soil_layer_color[0]]
    soil_type_combined=[soil_type[0]]
    soil_layer_top_elevation_combined=[soil_layer_elevation[0]]
    soil_layer_base_elevation_combined=[]
    for i in range(1, len(soil_type)):
        if soil_type[i]!=soil_type[i-1]:
            soil_layer_color_combined.append(soil_layer_color[i]) 
            soil_type_combined.append(soil_type[i])
            soil_layer_top_elevation_combined.append(soil_layer_elevation[i])
    soil_layer_base_elevation_combined=soil_layer_top_elevation_combined[1:]
    soil_layer_base_elevation_combined.append(soil_layer_elevation[-1])
    soil_layer_elevation_combined = soil_layer_top_elevation_combined[0:]
    soil_layer_elevation_combined.append(soil_layer_elevation[-1])
    number_of_soil_layers_combined = len(soil_type_combined)
    soil_sample_elevation_layer_groups_combined=[[]]*number_of_soil_layers_combined
    soil_sample_legend_code_layer_groups_combined=[[]]*number_of_soil_layers_combined
    for i in range(0, number_of_soil_layers_combined):
        soil_sample_elevation_layer_groups_combined[i]=[a for a in soil_sample_elevation if a<=soil_layer_elevation_combined[i] and a>soil_layer_elevation_combined[i+1]]
        soil_sample_legend_code_layer_groups_combined[i]=[a for a, b in zip(soil_sample_legend_code, soil_sample_elevation) if b<=soil_layer_elevation_combined[i] and b>soil_layer_elevation_combined[i+1]]    
    soil_layer_color_combined=['']*len(soil_sample_legend_code_layer_groups_combined)
    soil_type_combined=[""]*len(soil_sample_legend_code_layer_groups_combined)
    layer_clay_ratio_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    layer_silt_ratio_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    layer_fines_ratio_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    layer_sands_ratio_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    layer_gravel_ratio_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    layer_coarse_ratio_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    number_of_soil_sample_in_layer_combined=[np.float("NaN")]*len(soil_sample_legend_code_layer_groups_combined)
    for j in range(0, len(soil_sample_legend_code_layer_groups_combined)):
        if len(soil_sample_legend_code_layer_groups_combined[j])>0:
            clay_ratio_combined=len(list(x for x in soil_sample_legend_code_layer_groups_combined[j] if x in legend_code4clay))/len(soil_sample_legend_code_layer_groups_combined[j])
            silt_ratio_combined=len(list(x for x in soil_sample_legend_code_layer_groups_combined[j] if x in legend_code4silt))/len(soil_sample_legend_code_layer_groups_combined[j])
            fines_ratio_combined=len(list(x for x in soil_sample_legend_code_layer_groups_combined[j] if x in legend_code4clay + legend_code4silt))/len(soil_sample_legend_code_layer_groups_combined[j])
            sand_ratio_combined=len(list(x for x in soil_sample_legend_code_layer_groups_combined[j] if x in legend_code4sand))/len(soil_sample_legend_code_layer_groups_combined[j])
            gravel_ratio_combined=len(list(x for x in soil_sample_legend_code_layer_groups_combined[j] if x in legend_code4gravel))/len(soil_sample_legend_code_layer_groups_combined[j])
            others_ratio_combined=len(list(x for x in soil_sample_legend_code_layer_groups_combined[j] if x not in legend_code4clay + legend_code4silt + legend_code4sand + legend_code4gravel))/len(soil_sample_legend_code_layer_groups_combined[j])
            total_ratio_combined=clay_ratio_combined+fines_ratio_combined+silt_ratio_combined+sand_ratio_combined+gravel_ratio_combined+others_ratio_combined
            if total_ratio_combined <1:
                print("Layer "+ str(j) +": total_ratio_combined < 1")
            layer_clay_ratio_combined[j] = np.round(clay_ratio_combined,2)
            layer_silt_ratio_combined[j] = np.round(silt_ratio_combined,2)
            layer_fines_ratio_combined[j] = np.round(fines_ratio_combined,2)
            layer_sands_ratio_combined[j] = np.round(sand_ratio_combined,2)
            layer_gravel_ratio_combined[j] = np.round(gravel_ratio_combined,2)
            layer_coarse_ratio_combined[j] = np.round(sand_ratio_combined + gravel_ratio_combined,2)
            number_of_soil_sample_in_layer_combined[j] = len(soil_sample_legend_code_layer_groups_combined[j])
            if clay_ratio_combined>=0.5:
                soil_layer_color_combined[j] = '#006400'
                soil_type_combined[j]="Clay"
            elif silt_ratio_combined>=0.5:
                soil_layer_color_combined[j] = '#FF4500'
                soil_type_combined[j]="Silt"
            elif fines_ratio_combined>=0.5:
                soil_layer_color_combined[j] = '#6B8E23'
                soil_type_combined[j]="Clay or Silt"
            elif sand_ratio_combined>0.5:
                soil_layer_color_combined[j] = '#DAA520'
                soil_type_combined[j]="Sand"
            elif gravel_ratio_combined>0.5:
                soil_layer_color_combined[j] = '#708090'
                soil_type_combined[j]="Gravel"
            elif fines_ratio_combined<0.5:
                soil_layer_color_combined[j] = '#BDB76B'
                soil_type_combined[j]="Sand or Gravel"
            elif others_ratio_combined>0.5:
                soil_layer_color_combined[j] = '#FFFFFF'
                soil_type_combined[j]=""
            elif j>=1 and total_ratio_combined<1:
                soil_layer_color_combined[j]=soil_layer_color_combined[j-1]
                soil_type_combined[j]=soil_type_combined[j-1]
            elif j<len(soil_sample_legend_code_layer_groups_combined)-1 and total_ratio_combined<1:
                soil_layer_color_combined[j]=soil_layer_color_combined[j+1]
                soil_type_combined[j]=soil_type_combined[j+1]
        elif j > 0:
            layer_clay_ratio_combined[j] = 0
            layer_silt_ratio_combined[j] = 0
            layer_fines_ratio_combined[j] = 0
            layer_sands_ratio_combined[j] = 0
            layer_gravel_ratio_combined[j] = 0
            layer_coarse_ratio_combined[j] = 0
            number_of_soil_sample_in_layer_combined[j] = 0            
    for_loop_repeat_idx=0
    while for_loop_repeat_idx <100:
        for i in range(1, len(soil_layer_color_combined)):
            if soil_layer_color_combined[i] == "":
                soil_layer_color_combined[i] = soil_layer_color_combined[i-1]
                soil_type_combined[i] = soil_type_combined[i-1]
        for_loop_repeat_idx+=1
# =============================================================================
#         print(soil_layer_color_combined)
#         print(soil_type_combined)
#         print(soil_layer_top_elevation_combined)
# =============================================================================
        composite_soil_boring_data = pd.DataFrame()
        composite_soil_boring_data['Color Code']=soil_layer_color_combined
        composite_soil_boring_data['Soil Type']=soil_type_combined
        composite_soil_boring_data['Elevation Top']=soil_layer_top_elevation_combined
        composite_soil_boring_data['Elevation Base']=soil_layer_base_elevation_combined
        composite_soil_boring_data['Layer Thickness']=[np.round(a-b,2) for a,b in zip(composite_soil_boring_data['Elevation Top'], composite_soil_boring_data['Elevation Base'])]
        composite_soil_boring_data['Clay Ratio']=layer_clay_ratio_combined
        composite_soil_boring_data['Silt Ratio']=layer_silt_ratio_combined
        composite_soil_boring_data['Fines Ratio']=layer_fines_ratio_combined
        composite_soil_boring_data['Sand Ratio']=layer_sands_ratio_combined
        composite_soil_boring_data['Gravel Ratio']=layer_gravel_ratio_combined
        composite_soil_boring_data['Coarses Ratio']=layer_coarse_ratio_combined
        composite_soil_boring_data['Quantity of Soil Samples']=number_of_soil_sample_in_layer_combined
    return composite_soil_boring_data
def update_composite_design_column_func(
        data,
        layout,
        water_level_elevation,
        # data_profile_fig_text_size,
                    ):
    composite_design_column_fig_data = []
    if data['Top Elevation'][len(data)-1] == "":
        data = data.iloc[:-1].copy()
        data['Color Code'] = ['#006400' if a == "Clay" else '#FF4500' if a == "Silt" else '#DAA520' if a == "Sand" else '#708090' if a == "Gravel" else '#FFFFFF' for a in data['Soil Type']]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add soil_block_trace:
# =============================================================================
# =============================================================================
# =============================================================================
        soil_block_trace ={
            'x': [0.]* len(data['Top Elevation']), 
            'y': data['Top Elevation']-data['Base Elevation'],
            'mode': 'markers',
            'name': "Soil Layer Blocks",
            'type': 'bar',
            'width': 50,
            'base': data['Base Elevation'],
            'marker': {
                'color': data['Color Code'],
                'line': {
                    'color':'black',
                    'line': 1,
                    },
                },
            'text': data['Soil Type'],
            'textfont': {
                'size': 1,
                'color': 'black',
                },
            'hoverinfo': 'text',
            #'hovertext': None,                     
            }
        composite_design_column_fig_data.append(soil_block_trace)
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add Soil Type Symbol:
# =============================================================================
# =============================================================================
# =============================================================================
        soil_type_symbol_trace ={
            'x': [0.]* len(data['Top Elevation']),  
            'y': (data["Top Elevation"]+
               data["Base Elevation"])/2,
            'mode': 'text',
            'name': "Soil Types",
            'type': 'scatter',                
            'text': data['Soil Type'],
            'textfont': {
                'color':'white',
                'size': 8, # data_profile_fig_text_size*0.8,
                },
            'textposition': 'middle center',
            'visible': True,
            'showlegend': True,
            'hoverinfo': 'text',
            #'hovertext': None,                     
            }
        composite_design_column_fig_data.append(soil_type_symbol_trace)
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add Soil Symbol:
# =============================================================================
# =============================================================================
# =============================================================================
        if "" not in list(data['Soil Symbol']):                
            soil_symbol_trace ={
                'x': [30.]* len(data['Top Elevation']),  
                'y': (data["Top Elevation"]+
                   data["Base Elevation"])/2,
                'mode': 'text',
                'name': "Soil Symbols",
                'type': 'scatter',                
                'text': data['Soil Symbol'],
                'textfont': {
                    'color':'black',
                    'size': 8, # data_profile_fig_text_size*0.8,
                    },
                'textposition': 'middle right',
                'visible': 'legendonly',
                'showlegend': True,
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            composite_design_column_fig_data.append(soil_symbol_trace)            
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_trace               
# =============================================================================
# =============================================================================
# =============================================================================
        final_soil_type4plotting = data["Soil Type"].tolist() + [None]
        final_layer_elevation = data["Top Elevation"].tolist() + [data["Base Elevation"].tolist()[-1]]
        final_layer_elevation4plotting = [np.float('NaN')]*(len(final_layer_elevation)*3)
        final_layer_elevation4plotting[::3] = final_layer_elevation
        final_layer_elevation4plotting[1::3] = final_layer_elevation
        x4final_layer_elevation4plotting  = [np.float('NaN')]*(len(final_layer_elevation)*3)
        x4final_layer_elevation4plotting[::3] = [-60] * len(final_layer_elevation)
        x4final_layer_elevation4plotting[1::3] = [140] * len(final_layer_elevation)
        stratification_line_trace ={
            'x': x4final_layer_elevation4plotting, 
            'y': final_layer_elevation4plotting,
            'customdata': final_layer_elevation4plotting,
            'mode': 'lines',
            'name': 'Stratification',
            'type': 'scatter',
            'line': {
                'color': 'gray',
                'width': 1,
                'dash': 'dashdot',
                },
            'visible': True, #'legendonly',
            'showlegend': True,
            'legendgroup': 'Stratification',            
            'hoverinfo': 'text',
            #'hovertext': None,                     
            }
        trace_name_list = [a['name'] for a in composite_design_column_fig_data]
        if 'Stratification' not in trace_name_list:
            composite_design_column_fig_data.append(stratification_line_trace) 
        else:
            composite_design_column_fig_data[trace_name_list.index('Stratification')] = stratification_line_trace    
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_text_trace               
# =============================================================================
# =============================================================================
# =============================================================================
        final_layer_elevation_text_list=[str(round(a,1)) + ' ft.' for a in final_layer_elevation]
        x4final_layer_elevation_text_list = [-60] * len(final_layer_elevation)
        stratification_line_text_trace ={
            'x': x4final_layer_elevation_text_list, 
            'y': final_layer_elevation,
            'customdata': final_soil_type4plotting,
            'mode': 'text',
            'name': 'Stratification Text',
            'type': 'scatter',
            'line': {
                'color': 'gray',
                'width': 1,
                'dash': 'dashdot',
                },
            'text': final_layer_elevation_text_list,
            'textposition': "top right",
            'textfont': {
                'size': 8,                    
                },
            'visible': True, #'legendonly',
            'showlegend': False,
            'legendgroup': 'Stratification',
            'hoverinfo': 'text',
            #'hovertext': None,                     
            }
        trace_name_list = [a['name'] for a in composite_design_column_fig_data]
        if 'Stratification Text' not in trace_name_list:
            composite_design_column_fig_data.append(stratification_line_text_trace) 
        else:
            composite_design_column_fig_data[trace_name_list.index('Stratification Text')] = stratification_line_text_trace    
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add water table line:    
# =============================================================================
# =============================================================================
# =============================================================================
        if water_level_elevation is not None:
            water_table_line = {
                'type': 'line',
                'xref': 'paper',
                'yref': 'y',
                'x0': 0,
                'y0': water_level_elevation,
                'x1': 1,
                'y1': water_level_elevation,
                'opacity': 0.8,
                'line': {
                    'color': 'lightblue',
                    'width': 3,
                  },                                       
                }
            layout['shapes']= []
            layout['shapes'].append(water_table_line)
        else:
            layout['shapes']= []
# =============================================================================
# # =============================================================================
# # =============================================================================
# # =============================================================================
# # # # # update y axis range:    
# # =============================================================================
# # =============================================================================
# # =============================================================================
#                 
#         y_axis_offset = 0.3* (np.nanmax(data['Top Elevation']) - np.nanmin(data['Base Elevation']))
# 
# 
#         
#         layout['yaxis']['range'] = [
#             np.nanmin(data['Base Elevation']) - y_axis_offset,
#             np.nanmax(data['Top Elevation']) + y_axis_offset*0.5, 
#             ]
# =============================================================================
        return composite_design_column_fig_data, layout 
def update_composite_soil_profile_func(
        # data_profile_fig_text_size,         
        dataset1_selected_soil_boring_data_table_data,
        dataset1_selected_soil_lithology_data_table_data,
        composite_soil_profile_fig_layout, 
        composite_thickness_resolution,
        water_level_elevation,
                    ):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add Soil columns:
# =============================================================================
# =============================================================================
# =============================================================================
        composite_soil_profile_fig_data = []
        composite_soil_profile_fig_layout = composite_soil_profile_fig_layout
        if dataset1_selected_soil_lithology_data_table_data:            
            data=pd.DataFrame.from_records(dataset1_selected_soil_lithology_data_table_data)
            unique_location_ID_list=np.unique(data['Location ID'])
# =============================================================================
# =============================================================================
# # # single soil boring:            
# =============================================================================
# =============================================================================
            if len(unique_location_ID_list) == 1:
# =============================================================================
# # add Soil Lithology Columns:
# =============================================================================
                lithology_hovertext = ['Project Number: '+str(a)+
                        '<br>'+'Location ID: '+str(b)+
                        '<br>'+'Top Elevation (ft.): '+str(c)+
                        '<br>'+'Bottom Elevation (ft.): '+str(d)+
                        '<br>'+'Symbol: '+str(e)+
                        '<br>'+'Description: '+str(f)
                        for a,b,c,d,e,f in zip(data["Project Number"].tolist(),
                                             data["Location ID"].tolist(),
                                             [round(a,2) for a in data["Elevation Top"]],
                                             [round(a,2) for a in data["Elevation Base"]],
                                             data["Legend Code"].tolist(),
                                             data["Additional Description"].tolist(),
                                               )]   
                soil_lithology_trace ={
                    'x': [0.]* len(data['Depth Base']), 
                    'y': data['Depth Base']-data['Depth Top'],
                    'mode': 'markers',
                    'name': "Soil Lithology Columns",
                    'type': 'bar',
                    'width': 50,
                    'base': data['Elevation Base'],
                    'marker': {
                        'color': data['Color Code'],
                        'line': {
                            'color':'black',
                            'line': 1,
                            },
                        },
                    'text': data['Legend Code'],
                    'textfont': {
                        'size': 1,
                        'color': 'black',
                        },
                    'hoverinfo': 'text',
                    'hovertext': lithology_hovertext,                     
                    }
                composite_soil_profile_fig_data.append(soil_lithology_trace)
# =============================================================================
# # add Soil Lithology Symbol:
# =============================================================================
                soil_lithology_symbol_trace ={
                    'x': [0.]* len(data['Depth Base']),  
                    'y': (data["Elevation Top"]+
                       data["Elevation Base"])/2,
                    'mode': 'text',
                    'name': "Soil Lithology Symbols",
                    'type': 'scatter',                
                    'text': data['Legend Code'],
                    'textfont': {
                        'color':'white',
                        'size': 8, #data_profile_fig_text_size*0.8,
                        },
                    'textposition': 'middle center',
                    'visible': 'legendonly',
                    'showlegend': True,
                    'hoverinfo': 'text',
                    'hovertext': lithology_hovertext,                     
                    }
                composite_soil_profile_fig_data.append(soil_lithology_symbol_trace)
# =============================================================================
# # add Soil Samples:
# =============================================================================
                if dataset1_selected_soil_boring_data_table_data:            
                    data=pd.DataFrame.from_records(dataset1_selected_soil_boring_data_table_data)
    # define soil_sample_blocks_hovertext:
                    display_field_name_list = [
                        'Location ID',
                        'Elevation Top','Elevation Base',
                        'Legend Code',
                        'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                        'Total Unit Weight','Dry Density',
                        'Test Type','Failure Mode','Chamber Pressure','Compressive Strength','Undrained Shear Strength',
                        'Percentage Passing at 0_075',
                        'SPT N',
                        #'USCS Symbol','USCS Group Name',
                        #'AASHTO Classification',
                        #'Specific Gravity',
                        ]
                    soil_sample_blocks_hovertext= ["Project Number: "+a for a in data["Project Number"]]
                    for i in range(0, len(soil_sample_blocks_hovertext)):
                        for j in range(0, len(display_field_name_list)):
# =============================================================================
#                     if pd.isnull(dataset1_selected_soil_boring_data_table_data_df[display_field_name_list[j]][i]) == False:
# =============================================================================
                            if (display_field_name_list[j] in list(data.keys()) and 
                                pd.isnull(data[display_field_name_list[j]][i]) == False):                           
                                soil_sample_blocks_hovertext[i]+='<br>'+ display_field_name_list[j].replace('Percentage Passing at 0_075', '#200 Sieve Percentage Passing').replace("_", " ") + ": " + str(data[display_field_name_list[j]][i])
                    soil_sample_trace ={
                        'x': [0.]* len(data['Elevation Base']), 
                        'y': data['Elevation Top']-data['Elevation Base'],
                        'mode': 'markers',
                        'name': "Soil Sample Blocks",
                        'type': 'bar',
                        'width': 50*0.8,
                        'base': data['Elevation Base'],
                        'marker': {
                            'color': data['Color Code'],
                            'line': {
                                'color':'white',
                                'line': 0.1,
                                },
                            },
                        'text': data['Legend Code'],
                        'textfont': {
                            'size': 1,
                            'color': 'black',
                            },     
                        'visible': 'legendonly',
                        'showlegend': True,
                        'hoverinfo': 'text',
                        'hovertext': soil_sample_blocks_hovertext,                     
                        }
                    composite_soil_profile_fig_data.append(soil_sample_trace)
# =============================================================================
# # add Location ID text:
# =============================================================================
                    location_ID_hovertext = ['Location ID: '+data["Location ID"][0]+
                            '<br>'+'Longitude (deg.): '+str(data["Longitude Decimal"][0])+ 
                            '<br>'+'Latitude (deg.): '+str(data["Latitude Decimal"][0])
                            ]
                    location_ID_trace ={
                        'x': [0.], 
                        'y': [data["Elevation"][0]],
                        'mode': 'text',
                        'name': "Location ID",
                        'type': 'scatter',                
                        'text': [data["Location ID"][0]],
                        'textposition':"top center",
                        'textfont': {
                            'color':'black',
                            'size': 10, #data_profile_fig_text_size,
                            },
                        'visible': True,
                        'showlegend': True,
                        'hoverinfo': 'text',
                        'hovertext': location_ID_hovertext,                     
                        }
                    composite_soil_profile_fig_data.append(location_ID_trace)            
# =============================================================================
# =============================================================================
# # # multiple soil borings:            
# =============================================================================
# =============================================================================
            elif len(unique_location_ID_list) > 1:
                if dataset1_selected_soil_boring_data_table_data:            
                    data=pd.DataFrame.from_records(dataset1_selected_soil_boring_data_table_data)
                    data.sort_values(by=['Elevation Top'], inplace=True)
# =============================================================================
# # add Composite Soil Column:
# =============================================================================
                    data = stratify_composite_soil_boring_func(data, composite_thickness_resolution)
                    composite_boring_hovertext = ['Composite Soil Type: '+str(a)+
                            '<br>'+'Top Elevation (ft.): '+str(b)+
                            '<br>'+'Bottom Elevation (ft.): '+str(c)+
                            '<br>'+'Layer Thickness (ft.): '+str(d)+
                            '<br>'+'Soil Sample Quantity within Layer: '+str(e)+
                            '<br>'+'Fines Sample Ratio: '+str(f)+
                            '<br>'+'Coarse Sample Ratio: '+str(g)+
                            '<br>'+'Clay Sample Ratio: '+str(h)+
                            '<br>'+'Silt Sample Ratio: '+str(i)+
                            '<br>'+'Sand Sample Ratio: '+str(j)+
                            '<br>'+'Gravel Sample Ratio: '+str(k)
                            for a,b,c,d,e,f,g,h,i,j,k in zip(data["Soil Type"],
                                                 data["Elevation Top"],
                                                 data["Elevation Base"],
                                                 data["Layer Thickness"],
                                                 data["Quantity of Soil Samples"],
                                                 data["Fines Ratio"],
                                                 data["Coarses Ratio"],
                                                 data["Clay Ratio"],
                                                 data["Silt Ratio"],
                                                 data["Sand Ratio"],
                                                 data["Gravel Ratio"],
                                                   )]   
                    composite_boring_trace ={
                        'x': [0.]* len(data['Elevation Base']), 
                        'y': data['Elevation Top']-data['Elevation Base'],
                        'mode': 'markers+text',
                        'name': "Composite Soil Column",
                        'type': 'bar',
                        'width': 50,
                        'base': data['Elevation Base'],
                        'marker': {
                            'color': data['Color Code'],
                            'line': {
                                'color':'black',
                                'line': 1,
                                },
                            },
                        'text': data['Soil Type'],
                        'textfont': {
                            'size': 1,
                            'color': 'black',
                            },
                        'visible': True, #'legendonly',
                        'showlegend': True,
                        'hoverinfo': 'text',
                        'hovertext': composite_boring_hovertext,                     
                        }
                    composite_soil_profile_fig_data.append(composite_boring_trace)
# =============================================================================
# # add Composite Soil type text:
# =============================================================================
                    composite_boring_soil_type_text_trace ={
                        'x': [0.]* len(data['Elevation Base']), 
                        'y': (data['Elevation Top']+data['Elevation Base'])/2,
                        'mode': 'text',
                        'name': "Composite Soil Type",        
                        'type': 'scatter',
                        'text': data['Soil Type'],
                        'textposition': "middle center",
                        'textfont': {
                            'size': 8, # data_profile_fig_text_size, 
                            'color': 'white',
                            },                        
                        'visible': True, #'legendonly',
                        'showlegend': True,
                        'hoverinfo': 'text',
                        'hovertext': composite_boring_hovertext,                     
                        }
                    composite_soil_profile_fig_data.append(composite_boring_soil_type_text_trace)
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add water table line:    
# =============================================================================
# =============================================================================
# =============================================================================
            if water_level_elevation is not None:
                water_table_line = {
                    'type': 'line',
                    'xref': 'paper',
                    'yref': 'y',
                    'x0': 0,
                    'y0': water_level_elevation,
                    'x1': 1,
                    'y1': water_level_elevation,
                    'opacity': 0.8,
                    'line': {
                        'color': 'lightblue',
                        'width': 3,
                      },                                       
                    }
                composite_soil_profile_fig_layout['shapes']= []
                composite_soil_profile_fig_layout['shapes'].append(water_table_line)
            else:
                composite_soil_profile_fig_layout['shapes']= []
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update y axis range:    
# =============================================================================
# =============================================================================
# =============================================================================
            y_axis_offset = 0.3* (max(data['Elevation Top']) - min(data['Elevation Base']))
            composite_soil_profile_fig_layout['yaxis']['range'] = [
                min(data['Elevation Base']) - y_axis_offset,
                max(data['Elevation Top']) + y_axis_offset*0.5, 
                ]
        return composite_soil_profile_fig_data, composite_soil_profile_fig_layout 
def update_data_profile4_interpretation_mode_func(
        data_profile_fig_data,
        data_window_size,
                    ):

# =============================================================================
# =============================================================================
# =============================================================================
# # # # Visualization Mode:
# =============================================================================
# =============================================================================
# =============================================================================
        if len(data_profile_fig_data) > 0:
            data = pd.DataFrame()
            data['x'] = [a for a in data_profile_fig_data[0]['x']]
            data['y'] = [a for a in data_profile_fig_data[0]['y']]
            data.dropna(subset=['x'], inplace=True)
            data.sort_values(by=['y'], inplace=True, ascending=False)            
            data['Moving Average'] = data['x'].rolling(data_window_size, min_periods=1).mean()
            data['Moving Standard Deviation - Measured'] = data['x'].rolling(data_window_size, min_periods=1).std()
            data['Moving Standard Deviation - Model'] = [a/np.sqrt(data_window_size) for a in data['Moving Standard Deviation - Measured']]
            data['Moving Standard Deviation - Total'] = [np.sqrt(a**2+b**2) for a,b in zip(data['Moving Standard Deviation - Measured'], data['Moving Standard Deviation - Model'])]
            data['COV - Model'] = [a/b for a,b in zip(data['Moving Standard Deviation - Model'], data['Moving Average'])]
            COV_model_peaks_idx, _ = find_peaks(data['COV - Model'].tolist(), distance=data_window_size)
# =============================================================================
# # stratification lines:
# =============================================================================
            layer_elevation_list = [list(data['y'])[i] for i in COV_model_peaks_idx]
            layer_elevation_list4plotting = [np.float('NaN')]*(len(layer_elevation_list)*3)
            layer_elevation_list4plotting[::3] = layer_elevation_list
            layer_elevation_list4plotting[1::3] = layer_elevation_list
            x_axis_offset = 0.2* (np.nanmax(data['x']) - np.nanmin(data['x']))
            x4layer_elevation_list4plotting = [np.float('NaN')]*(len(layer_elevation_list)*3)
            x4layer_elevation_list4plotting[::3] = [np.nanmin(data['x']) - x_axis_offset]*len(layer_elevation_list)
            x4layer_elevation_list4plotting[1::3] = [np.nanmax(data['x']) + x_axis_offset]*len(layer_elevation_list)
            layer_elevation_text_list=[str(round(a,1)) + ' ft.' for a in layer_elevation_list]
            x4layer_elevation_text_list=[np.nanmin(data['x']) - x_axis_offset]*len(layer_elevation_list)
# =============================================================================
# COV in each layer:
# =============================================================================
            data_groups4layers=[[]]*(len(layer_elevation_list)+1)
            COV_model4data_groups=[np.float("NaN")]*(len(layer_elevation_list)+1)
            if len(layer_elevation_list)>0:
                data_groups4layers[0] = [a for a,b in zip(data['x'], data['y']) if b>layer_elevation_list[0]]
                data_groups4layers[-1] = [a for a,b in zip(data['x'], data['y']) if b<=layer_elevation_list[-1]]
                for i in range(1, len(data_groups4layers)-1):
                    data_groups4layers[i]=[a for a,b in zip(data['x'], data['y']) if b<=layer_elevation_list[i-1] and b>layer_elevation_list[i]]
                # On July 07/13/2022, try to use total cov instead of cov_model
                COV_model4data_groups=[np.std(a, ddof=1)*np.sqrt(1+1/len(a))/np.mean(a) if len(a)>1 else np.float("NaN") for a in data_groups4layers]
                text4COV_model = [a if pd.isnull(a) == True else 'COV_t: ' + str(round(a,3)) for a in COV_model4data_groups]
                x4COV_model_text=[np.nanmax(data['x']) + x_axis_offset]*len(COV_model4data_groups)
                y4COV_model_text=[layer_elevation_list[0]+5] + [a-1 for a in layer_elevation_list]
# =============================================================================
#             print(data_profile_fig_data[0]['name'])
# =============================================================================
# trace_name_list
            trace_name_list = [a['name'] for a in data_profile_fig_data]
# =============================================================================
# =============================================================================
# =============================================================================
# # # moving_avg_line_trace               
# =============================================================================
# =============================================================================
# =============================================================================
            moving_avg_line_trace ={
                'x': data['Moving Average'], 
                'y': data['y'],
                'customdata': list(data.index),
                'mode': 'lines',
                'name': 'Moving Avg.',
                'type': 'scatter',
                'line': {
                    'color': 'red',
                    'width': 3,
                    'shape': 'vh',
                    },
                'text': data['Moving Average'],
                'visible': True, #'legendonly',
                'showlegend': True,
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if 'Moving Avg.' not in trace_name_list:
                data_profile_fig_data.append(moving_avg_line_trace) 
            else:
                data_profile_fig_data[trace_name_list.index('Moving Avg.')] = moving_avg_line_trace  
# =============================================================================
#             if len(data_profile_fig_data) == 1:
#                 data_profile_fig_data.append(moving_avg_line_trace) 
#             elif len(data_profile_fig_data) > 1:
#                 data_profile_fig_data[1] = moving_avg_line_trace
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # upper_bound_trace               
# =============================================================================
# =============================================================================
# =============================================================================
            upper_bound_trace ={
                'x': data['Moving Average'] + data['Moving Standard Deviation - Total'], 
                'y': data['y'],
                'customdata': list(data.index),
                'mode': 'lines',
                'name': 'Moving Std. Band  - Upper',
                'type': 'scatter',
                'line': {
                    'color': 'ligtgray',
                    'width': 0,
                    'shape': 'vh',
                    },
                'orientation': 'h',
                'text': data['Moving Average'] + data['Moving Standard Deviation - Total'],
                'visible': True, #'legendonly',
                'showlegend': False,                
                'legendgroup': 'Moving Std. Band',               
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if 'Moving Std. Band  - Upper' not in trace_name_list:
                data_profile_fig_data.append(upper_bound_trace) 
            else:
                data_profile_fig_data[trace_name_list.index('Moving Std. Band  - Upper')] = upper_bound_trace  
# =============================================================================
#             if len(data_profile_fig_data) == 2:
#                 data_profile_fig_data.append(upper_bound_trace) 
#             elif len(data_profile_fig_data) > 2:
#                 data_profile_fig_data[2] = upper_bound_trace                
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # lower_bound_trace               
# =============================================================================
# =============================================================================
# =============================================================================
            lower_bound_trace ={
                'x': data['Moving Average'] - data['Moving Standard Deviation - Total'], 
                'y': data['y'],
                'customdata': list(data.index),
                'mode': 'lines',
                'name': 'Moving Std. Band',
                'type': 'scatter',
                'line': {
                    'color': 'ligtgray',
                    'width': 0,
                    'shape': 'vh',
                    },
                'orientation': 'h',
                'fill': 'tonextx',
                'fillcolor': 'rgba(255, 165, 0, 0.6)',
                'text': data['Moving Average'] - data['Moving Standard Deviation - Total'],
                'visible': True, #'legendonly',
                'showlegend': True,                
                'legendgroup': 'Moving Std. Band',               
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if 'Moving Std. Band' not in trace_name_list:
                data_profile_fig_data.append(lower_bound_trace) 
            else:
                data_profile_fig_data[trace_name_list.index('Moving Std. Band')] = lower_bound_trace  
# =============================================================================
#             if len(data_profile_fig_data) == 3:
#                 data_profile_fig_data.append(lower_bound_trace) 
#             elif len(data_profile_fig_data) > 3:
#                 data_profile_fig_data[3] = lower_bound_trace                
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_trace               
# =============================================================================
# =============================================================================
# =============================================================================
            stratification_line_trace ={
                'x': x4layer_elevation_list4plotting, 
                'y': layer_elevation_list4plotting,
                'customdata': layer_elevation_list4plotting,
                'mode': 'lines',
                'name': 'Stratification',
                'type': 'scatter',
                'line': {
                    'color': 'gray',
                    'width': 1,
                    'dash': 'dashdot',
                    },
                'visible': True, #'legendonly',
                'showlegend': True,
                'legendgroup': 'Stratification',               
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if 'Stratification' not in trace_name_list:
                data_profile_fig_data.append(stratification_line_trace) 
            else:
                data_profile_fig_data[trace_name_list.index('Stratification')] = stratification_line_trace  
# =============================================================================
#             if len(data_profile_fig_data) == 4:
#                 data_profile_fig_data.append(stratification_line_trace) 
#             elif len(data_profile_fig_data) > 4:
#                 data_profile_fig_data[4] = stratification_line_trace    
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_text_trace               
# =============================================================================
# =============================================================================
# =============================================================================
            stratification_line_text_trace ={
                'x': x4layer_elevation_text_list, 
                'y': layer_elevation_list,
                'customdata': layer_elevation_list,
                'mode': 'text',
                'name': 'Stratification Text',
                'type': 'scatter',
                'line': {
                    'color': 'gray',
                    'width': 1,
                    'dash': 'dashdot',
                    },
                'text': layer_elevation_text_list,
                'textposition': "top right",
                'textfont': {
                    'size': 8,                    
                    },
                'visible': True, #'legendonly',
                'showlegend': False,
                'legendgroup': 'Stratification',
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if 'Stratification Text' not in trace_name_list:
                data_profile_fig_data.append(stratification_line_text_trace) 
            else:
                data_profile_fig_data[trace_name_list.index('Stratification Text')] = stratification_line_text_trace  
# =============================================================================
#             if len(data_profile_fig_data) == 5:
#                 data_profile_fig_data.append(stratification_line_text_trace) 
#             elif len(data_profile_fig_data) > 5:
#                 data_profile_fig_data[5] = stratification_line_text_trace
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # COV_model_trace
# =============================================================================
# =============================================================================
# =============================================================================
            if len(layer_elevation_list)>0 and data_window_size>1:
                COV_model_trace ={
                    'x': x4COV_model_text, 
                    'y': y4COV_model_text,
                    'customdata': COV_model4data_groups,
                    'mode': 'text',
                    'name': 'COV, total',
                    'type': 'scatter',
                    'line': {
                        'color': 'gray',
                        'width': 1,
                        'dash': 'dashdot',
                        },
                    'text': text4COV_model,
                    'textposition': "bottom left",
                    'textfont': {
                        'size': 8,
                        'color': ['red' if a >= 0.3 else 'green' for a in COV_model4data_groups],
                        },
                    'visible': True, #'legendonly',
                    'showlegend': True,
                    'hoverinfo': 'text',
                    #'hovertext': None,                     
                    }
                if 'COV, model' not in trace_name_list:
                    data_profile_fig_data.append(COV_model_trace) 
                else:
                    data_profile_fig_data[trace_name_list.index('COV, model')] = COV_model_trace  
# =============================================================================
#                 if len(data_profile_fig_data) == 6:
#                     data_profile_fig_data.append(COV_model_trace) 
#                 elif len(data_profile_fig_data) > 6:
#                     data_profile_fig_data[6] = COV_model_trace
# =============================================================================
            return data_profile_fig_data 
def update_data_profile_func(
        map_selection_points,
        dataset1_selected_soil_boring_data_table_data,
        data_profile_fig_layout,
        x_axis_parameter,
        x_axis_parameter_unit,
        water_level_elevation,
        interpretation_mode_select,
        data_window_size,
                    ):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # change x axis label:    
# =============================================================================
# =============================================================================
# =============================================================================
        if x_axis_parameter_unit != '':
            data_profile_fig_layout['xaxis']['title']['text'] = x_axis_parameter.replace('Percentage Passing at 0_075', '#200 Finer') + ', ' + x_axis_parameter_unit
        else:
            data_profile_fig_layout['xaxis']['title']['text'] = x_axis_parameter
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add water table line:    
# =============================================================================
# =============================================================================
# =============================================================================
        if water_level_elevation is not None:
            water_table_line = {
                'type': 'line',
                'xref': 'paper',
                'yref': 'y',
                'x0': 0,
                'y0': water_level_elevation,
                'x1': 1,
                'y1': water_level_elevation,
                'opacity': 0.8,
                'line': {
                    'color': 'lightblue',
                    'width': 3,
                  },                                       
                }
            data_profile_fig_layout['shapes']= []
            data_profile_fig_layout['shapes'].append(water_table_line)
        else:
            data_profile_fig_layout['shapes']= []
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add Soil Sample data:
# =============================================================================
# =============================================================================
# =============================================================================
        data_profile_fig_data = []
        data_profile_fig_layout = data_profile_fig_layout
        if dataset1_selected_soil_boring_data_table_data:            
            data=pd.DataFrame.from_records(dataset1_selected_soil_boring_data_table_data)
            if x_axis_parameter in data.keys():
# define soil_sample_blocks_hovertext:
                display_field_name_list = [
                    'Location ID',
                    'Elevation Top','Elevation Base',
                    'Legend Code',
                    'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                    'Total Unit Weight','Dry Density',
                    'Test Type','Failure Mode','Chamber Pressure','Compressive Strength','Undrained Shear Strength',
                    'Percentage Passing at 0_075',
                    'SPT N',
                    #'USCS Symbol','USCS Group Name',
                    #'AASHTO Classification',
                    #'Specific Gravity',
                    ]
                soil_sample_blocks_hovertext= ["Project Number: "+a for a in data["Project Number"]]
                for i in range(0, len(soil_sample_blocks_hovertext)):
                    for j in range(0, len(display_field_name_list)):
# =============================================================================
#                     if pd.isnull(dataset1_selected_soil_boring_data_table_data_df[display_field_name_list[j]][i]) == False:
# =============================================================================
                        if (display_field_name_list[j] in list(data.keys()) and 
                            pd.isnull(data[display_field_name_list[j]][i]) == False):                           
                            soil_sample_blocks_hovertext[i]+='<br>'+ display_field_name_list[j].replace('Percentage Passing at 0_075', '#200 Sieve Percentage Passing').replace("_", " ") + ": " + str(data[display_field_name_list[j]][i])
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Add soil data points:    
# =============================================================================
# =============================================================================
# =============================================================================
                soil_sample_trace ={
                    'x': data[x_axis_parameter], 
                    'y': (data['Elevation Top']+data['Elevation Base'])/2,
                    'customdata': list(data.index),
                    'mode': 'markers',
                    'name': x_axis_parameter.replace('Percentage Passing at 0_075', '#200 Finer'),
                    'type': 'scatter',
                    'marker': {
                        'color': data['Point Color Code'],
                        'size': 8,
                        'line': {
                            'color':'black',
                            'width': 1,
                            },
                        },
                    'text': data['Legend Code'],
                    'visible': True, #'legendonly',
                    'showlegend': True,
                    'hoverinfo': 'text',
                    'hovertext': soil_sample_blocks_hovertext,                     
                    }
                data_profile_fig_data.append(soil_sample_trace)
                if x_axis_parameter == 'Moisture Content':
                    Liquid_Limit_trace ={
                        'x': data['Liquid Limit'], 
                        'y': (data['Elevation Top']+data['Elevation Base'])/2,
                        'customdata': list(data.index),
                        'mode': 'markers',
                        'name': 'Liquid Limit',
                        'type': 'scatter',
                        'marker': {
                            'color': data['Point Color Code'],
                            'symbol': "arrow-right",
                            'size': 8,
                            'line': {
                                'color':'black',
                                'width': 1,
                                },
                            },
                        'text': data['Legend Code'],
                        'visible': True, #'legendonly',
                        'showlegend': True,
                        'hoverinfo': 'text',
                        'hovertext': soil_sample_blocks_hovertext,                     
                        }
                    Plastic_Limit_trace ={
                        'x': data['Plastic Limit'], 
                        'y': (data['Elevation Top']+data['Elevation Base'])/2,
                        'customdata': list(data.index),
                        'mode': 'markers',
                        'name': 'Plastic Limit',
                        'type': 'scatter',
                        'marker': {
                            'color': data['Point Color Code'],
                            'symbol': "arrow-left",
                            'size': 8,
                            'line': {
                                'color':'black',
                                'width': 1,
                                },
                            },
                        'text': data['Legend Code'],
                        'visible': True, #'legendonly',
                        'showlegend': True,
                        'hoverinfo': 'text',
                        'hovertext': soil_sample_blocks_hovertext,                     
                        }
                    if interpretation_mode_select == 'Visualization Mode':                        
                        data_profile_fig_data.append(Liquid_Limit_trace)                    
                        data_profile_fig_data.append(Plastic_Limit_trace)
                    else:
# trace_name_list
                        trace_name_list = [a['name'] for a in data_profile_fig_data]                    
                        if 'Liquid Limit' in trace_name_list:
                            data_profile_fig_data.remove(Liquid_Limit_trace) 
                        if 'Plastic Limit' in trace_name_list:
                            data_profile_fig_data.remove(Plastic_Limit_trace) 
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update y axis range:    
# =============================================================================
# =============================================================================
# =============================================================================
                y_axis_offset = 0.3* (np.nanmax(data['Elevation Top']) - np.nanmin(data['Elevation Base']))
                data_profile_fig_layout['yaxis']['range'] = [
                    np.nanmin(data['Elevation Base']) - y_axis_offset,
                    np.nanmax(data['Elevation Top']) + y_axis_offset*0.5, 
                    ]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update x axis range:    
# =============================================================================
# =============================================================================
# =============================================================================
                if np.nanmax(data[x_axis_parameter]) > np.nanmin(data[x_axis_parameter]):
                    x_axis_offset = 0.2* (np.nanmax(data[x_axis_parameter]) - np.nanmin(data[x_axis_parameter]))
                else:
                    x_axis_offset = 0.2*np.nanmax(data[x_axis_parameter])
                data_profile_fig_layout['xaxis']['range'] = [
                    np.nanmin(data[x_axis_parameter]) - x_axis_offset,
                    np.nanmax(data[x_axis_parameter]) + x_axis_offset, 
                    ]
                if interpretation_mode_select == 'Visualization Mode' and x_axis_parameter == 'Moisture Content':
                    data_list = list(data['Moisture Content']) + list(data['Liquid Limit']) + list(data['Plastic Limit'])
                    if np.nanmax(data_list) > np.nanmin(data_list):
                        x_axis_offset = 0.2* (np.nanmax(data_list) - np.nanmin(data_list))
                    else:
                        x_axis_offset = 0.2*np.nanmax(data_list)
                    data_profile_fig_layout['xaxis']['range'] = [
                        np.nanmin(data_list) - x_axis_offset,
                        np.nanmax(data_list) + x_axis_offset, 
                        ]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Interpretation Mode:
# =============================================================================
# =============================================================================
# =============================================================================
                if interpretation_mode_select == 'Interpretation Mode':
                    data_profile_fig_data = update_data_profile4_interpretation_mode_func(
                        data_profile_fig_data,
                        data_window_size,
                        )
        return data_profile_fig_data, data_profile_fig_layout 
def update_design_lines_func(
        design_profile_fig_data,
        design_line_elevation,
        design_soil_types,
        quantile_range,
                    ):
                    
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Design Table:
# =============================================================================
# =============================================================================
# =============================================================================
        data = pd.DataFrame()
        if "CPT, Nkt Correlation" not in design_profile_fig_data[0]['name']:
            data['x'] = [a for a in design_profile_fig_data[0]['x']]
            data['y'] = [a for a in design_profile_fig_data[0]['y']]
            data.dropna(subset=['x'], inplace=True)
            data.sort_values(by=['y'], inplace=True, ascending=False)
            soil_parameter_name = design_profile_fig_data[0]['name']
        else:
            data['x'] = [a for a in design_profile_fig_data[1]['x']]
            data['y'] = [a for a in design_profile_fig_data[1]['y']]
            data.dropna(subset=['x'], inplace=True)
            data.sort_values(by=['y'], inplace=True, ascending=False)
            soil_parameter_name = design_profile_fig_data[1]['name']
        design_table = pd.DataFrame()
        design_table['Top Elevation'] = design_line_elevation[:-1]
        design_table['Base Elevation'] = design_line_elevation[1:]
        design_table['Soil Type'] = design_soil_types[:-1]
        data_group_list=[[]]*len(design_table)
        mean_list=[np.float("NaN")]*len(design_table)
        lower_bound_list=[np.float("NaN")]*len(design_table)
        upper_bound_list=[np.float("NaN")]*len(design_table)
        COV_list=[np.float("NaN")]*len(design_table)
# group data based on layer elevations:            
        for i in range(0, len(design_table)):
            data_group_list[i] = [a for a, b in zip(data['x'], data['y']) if b<=design_table['Top Elevation'][i] and b>design_table['Base Elevation'][i]]
# =============================================================================
#             if data['y'][-1] == design_table['Base Elevation'][-1] and data['x'][-1] not in data_group_list[-1]:
#                 data_group_list[-1].append(data['x'][-1])
# =============================================================================
# calc design lines:
        for i in range(0, len(data_group_list)):
            if len(data_group_list[i])>0:
                mean_list[i] = np.mean(data_group_list[i])
                lower_bound_list[i]=np.quantile(np.array(data_group_list[i]), float(quantile_range[0]))
                upper_bound_list[i]=np.quantile(np.array(data_group_list[i]), float(quantile_range[-1]))
                if len(data_group_list[i]) > 1:
                    COV_list[i]=round(np.std(data_group_list[i], ddof=1)*np.sqrt(1+1/len(data_group_list[i]))/np.mean(data_group_list[i]),3)
        for i in range(0, len(design_table)):
            if (soil_parameter_name in [
                    'Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                    'Compressive Strength','Undrained Shear Strength',
                    'Total Unit Weight','Dry Density',
                    ] and
                design_table['Soil Type'][i] not in ["Clay", "Silt", "Clay or Silt"]):
                mean_list[i] = np.float("NaN")
                lower_bound_list[i] = np.float("NaN")
                upper_bound_list[i] = np.float("NaN")
                COV_list[i] = np.float("NaN")
            elif (soil_parameter_name in ['SPT N'] and
                design_table['Soil Type'][i] in ["Clay", "Silt", "Clay or Silt"]):
                mean_list[i] = np.float("NaN")
                lower_bound_list[i] = np.float("NaN")
                upper_bound_list[i] = np.float("NaN")
                COV_list[i] = np.float("NaN")
        design_table['Mean'] = [a for a in mean_list]
        design_table['Lower Bound'] = [a for a in lower_bound_list]
        design_table['Upper Bound'] = [a for a in upper_bound_list]              
        design_table['COV, model'] = [a for a in COV_list] 
# =============================================================================
#         print(soil_parameter_name, COV_list)
# =============================================================================
# trace_name_list
        trace_name_list = [a['name'] for a in design_profile_fig_data]
# Plot design lines:
        design_line_name_list = ['Lower Bound', 'Upper Bound', 'Mean']
        design_line_color_list = [ 'green', 'blue', 'red']
        for i in range(0, len(design_line_name_list)):               
# define x and y lists:
            y_list = [np.float('NaN')]*(len(design_table[design_line_name_list[i]])*3)
            y_list[::3] = [a for a in design_table['Top Elevation']]
            y_list[1::3] = [a for a in design_table['Base Elevation']]
            x_list = [np.float('NaN')]*(len(design_table[design_line_name_list[i]])*3)
            x_list[::3] = [a for a in design_table[design_line_name_list[i]]]
            x_list[1::3] = [a for a in design_table[design_line_name_list[i]]]
# design_line_trace               
            design_line_trace ={
                'x': x_list, 
                'y': y_list,
                'customdata': x_list,
                'mode': 'lines',
                'name': design_line_name_list[i],
                'type': 'scatter',
                'line': {
                    'color': design_line_color_list[i],
                    'width': 2,
                    'dash': 'solid',
                    },
                'visible': True, #'legendonly',
                'showlegend': True,
                'legendgroup': design_line_name_list[i],               
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if design_line_name_list[i] not in trace_name_list:
                design_profile_fig_data.append(design_line_trace) 
            else:
                design_profile_fig_data[trace_name_list.index(design_line_name_list[i])] = design_line_trace             
# design_line_text_trace               
            design_line_text_trace ={
                'x': design_table[design_line_name_list[i]], 
                'y': design_table['Top Elevation'],
                'customdata': design_table[design_line_name_list[i]],
                'mode': 'text',
                'name': design_line_name_list[i] + ' Text',
                'type': 'scatter',
                'text': [a if pd.isnull(a) == True else round(a,0) for a in design_table[design_line_name_list[i]]],
                'textposition': ["top left" if design_line_name_list[i]=='Lower Bound' else "top right"][0],
                'textfont': {
                    'size': 6,
                    'color': design_line_color_list[i],
                    },
                'visible': True, #'legendonly',
                'showlegend': False,
                'legendgroup': design_line_name_list[i],               
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if design_line_name_list[i] + ' Text' not in trace_name_list:
                design_profile_fig_data.append(design_line_text_trace) 
            else:
                design_profile_fig_data[trace_name_list.index(design_line_name_list[i] + ' Text')] = design_line_text_trace             
# COV_model_trace
        if len(COV_list)>0:
            text4COV_model = [a if pd.isnull(a) == True else 'COV_t: ' + str(round(a,3)) for a in COV_list]
            if np.nanmax(data['x']) > np.nanmin(data['x']):
                x_axis_offset = 0.2* (np.nanmax(data['x']) - np.nanmin(data['x']))
            else:
                x_axis_offset = 0.2*np.nanmax(data['x']) 
            x4COV_model_text=[np.nanmax(data['x']) + x_axis_offset]*len(COV_list)
            COV_model_trace ={
                'x': x4COV_model_text, 
                'y': [a-1 for a in design_table['Top Elevation']],
                'customdata': COV_list,
                'mode': 'text',
                'name': 'COV, total',
                'type': 'scatter',
                'line': {
                    'color': 'gray',
                    'width': 1,
                    'dash': 'dashdot',
                    },
                'text': text4COV_model,
                'textposition': "bottom left",
                'textfont': {
                    'size': 8,
                    'color': ['red' if a >= 0.3 else 'green' for a in COV_list],
                    },
                'visible': True, #'legendonly',
                'showlegend': True,
                'hoverinfo': 'text',
                #'hovertext': None,                     
                }
            if 'COV, model' not in trace_name_list:
                design_profile_fig_data.append(COV_model_trace) 
            else:
                design_profile_fig_data[trace_name_list.index('COV, model')] = COV_model_trace             
# =============================================================================
#             if soil_parameter_name=="#200 Finer":
#                 print(soil_parameter_name, 'COV_list', COV_list)           
#                 print(soil_parameter_name, 'text4COV_model', text4COV_model)           
# =============================================================================
# =============================================================================
#         print(design_table['Soil Type'])
#         print(soil_parameter_name)
#         print('mean_list: ', mean_list)
#         print('lower_bound_list: ', lower_bound_list)
#         print('upper_bound_list: ', upper_bound_list)
# =============================================================================
        return design_profile_fig_data 
def update_design_profile_func(
        # design_profile_fig_text_size, 
        dataset1_selected_soil_boring_data_table_data,
        dataset1_selected_CPT_data_table_data,
        design_profile_fig_layout,
        x_axis_parameter,
        x_axis_parameter_unit,
        design_line_elevation,
        design_soil_types,
        water_level_elevation,
                    ):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # change x axis label:    
# =============================================================================
# =============================================================================
# =============================================================================
        if x_axis_parameter_unit != '':
            design_profile_fig_layout['xaxis']['title']['text'] = x_axis_parameter.replace('Percentage Passing at 0_075', '#200 Finer') + ', ' + x_axis_parameter_unit
        else:
            design_profile_fig_layout['xaxis']['title']['text'] = x_axis_parameter
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add water table line:    
# =============================================================================
# =============================================================================
# =============================================================================
        if water_level_elevation is not None:
            water_table_line = {
                'type': 'line',
                'xref': 'paper',
                'yref': 'y',
                'x0': 0,
                'y0': water_level_elevation,
                'x1': 1,
                'y1': water_level_elevation,
                'opacity': 0.8,
                'line': {
                    'color': 'lightblue',
                    'width': 3,
                  },                                       
                }
            design_profile_fig_layout['shapes']= []
            design_profile_fig_layout['shapes'].append(water_table_line)
        else:
            design_profile_fig_layout['shapes']= []
        design_profile_fig_data = []
        design_profile_fig_layout = design_profile_fig_layout
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Add CPT data: 
# =============================================================================
# =============================================================================
# =============================================================================
        if dataset1_selected_CPT_data_table_data and x_axis_parameter == "Undrained Shear Strength":            
            CPT_data=pd.DataFrame.from_records(dataset1_selected_CPT_data_table_data)
            CPT_data_trace ={
                'x': CPT_data["Su (psf), Nkt"], 
                'y': (CPT_data['Elevation Top']+CPT_data['Elevation Base'])/2,
                'customdata': list(CPT_data.index),
                'mode': 'markers',
                'name': "CPT, Nkt Correlation",
                'type': 'scatter',
                'marker': {
                    'color': 'lightgray',
                    'size': 6,
                    'line': {
                        'color':'black',
                        'width': 0,
                        },
                    },
                'text': CPT_data['Su (psf), Nkt'],
                'visible': True, #'legendonly',
                'showlegend': True,
                'hoverinfo': 'text',
                'hovertext': None,                     
                }
            design_profile_fig_data.append(CPT_data_trace)
# =============================================================================
# =============================================================================
# =============================================================================
# # # # add Soil Sample data:
# =============================================================================
# =============================================================================
# =============================================================================
        if dataset1_selected_soil_boring_data_table_data:            
            data=pd.DataFrame.from_records(dataset1_selected_soil_boring_data_table_data)
            if x_axis_parameter in data.keys():
# define soil_sample_blocks_hovertext:
                display_field_name_list = [
                    'Location ID',
                    'Elevation Top','Elevation Base',
                    'Legend Code',
                    'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                    'Total Unit Weight','Dry Density',
                    'Test Type','Failure Mode','Chamber Pressure','Compressive Strength','Undrained Shear Strength',
                    'Percentage Passing at 0_075',
                    'SPT N',
                    #'USCS Symbol','USCS Group Name',
                    #'AASHTO Classification',
                    #'Specific Gravity',
                    ]
                soil_sample_blocks_hovertext= ["Project Number: "+a for a in data["Project Number"]]
                for i in range(0, len(soil_sample_blocks_hovertext)):
                    for j in range(0, len(display_field_name_list)):
# =============================================================================
#                     if pd.isnull(dataset1_selected_soil_boring_data_table_data_df[display_field_name_list[j]][i]) == False:
# =============================================================================
                        if (display_field_name_list[j] in list(data.keys()) and 
                            pd.isnull(data[display_field_name_list[j]][i]) == False):                           
                            soil_sample_blocks_hovertext[i]+='<br>'+ display_field_name_list[j].replace('Percentage Passing at 0_075', '#200 Sieve Percentage Passing').replace("_", " ") + ": " + str(data[display_field_name_list[j]][i])
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Add soil data points:    
# =============================================================================
# =============================================================================
# =============================================================================
                soil_sample_trace ={
                    'x': data[x_axis_parameter], 
                    'y': (data['Elevation Top']+data['Elevation Base'])/2,
                    'customdata': list(data.index),
                    'mode': 'markers',
                    'name': x_axis_parameter.replace('Percentage Passing at 0_075', '#200 Finer'),
                    'type': 'scatter',
                    'marker': {
                        'color': data['Point Color Code'],
                        'size': 8,
                        'line': {
                            'color':'black',
                            'width': 1,
                            },
                        },
                    'text': "Boring Data",
                    'visible': True, #'legendonly',
                    'showlegend': True,
                    'hoverinfo': 'text',
                    'hovertext': soil_sample_blocks_hovertext,                     
                    }
                design_profile_fig_data.append(soil_sample_trace)
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update y axis range:    
# =============================================================================
# =============================================================================
# =============================================================================
                y_axis_offset = 0.3* (np.nanmax(data['Elevation Top']) - np.nanmin(data['Elevation Base']))
                design_profile_fig_layout['yaxis']['range'] = [
                    np.nanmin(data['Elevation Base']) - y_axis_offset,
                    np.nanmax(data['Elevation Top']) + y_axis_offset*0.5, 
                    ]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update x axis range:    
# =============================================================================
# =============================================================================
# =============================================================================
                if np.nanmax(data[x_axis_parameter]) > np.nanmin(data[x_axis_parameter]):
                    x_axis_offset = 0.2* (np.nanmax(data[x_axis_parameter]) - np.nanmin(data[x_axis_parameter]))
                else:
                    x_axis_offset = 0.2*np.nanmax(data[x_axis_parameter])                
                design_profile_fig_layout['xaxis']['range'] = [
                    np.nanmin(data[x_axis_parameter]) - x_axis_offset,
                    np.nanmax(data[x_axis_parameter]) + x_axis_offset, 
                    ]
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_trace               
# =============================================================================
# =============================================================================
# =============================================================================
                final_layer_elevation4plotting = [np.float('NaN')]*(len(design_line_elevation)*3)
                final_layer_elevation4plotting[::3] = design_line_elevation
                final_layer_elevation4plotting[1::3] = design_line_elevation
                x4final_layer_elevation4plotting  = [np.float('NaN')]*(len(design_line_elevation)*3)
                x4final_layer_elevation4plotting[::3] = [design_profile_fig_layout['xaxis']['range'][0]]*len(design_line_elevation)
                x4final_layer_elevation4plotting[1::3] = [design_profile_fig_layout['xaxis']['range'][1]]*len(design_line_elevation)        
                stratification_line_trace ={
                    'x': x4final_layer_elevation4plotting, 
                    'y': final_layer_elevation4plotting,
                    'customdata': final_layer_elevation4plotting,
                    'mode': 'lines',
                    'name': 'Stratification',
                    'type': 'scatter',
                    'line': {
                        'color': 'gray',
                        'width': 1,
                        'dash': 'dashdot',
                        },
                    'visible': True, #'legendonly',
                    'showlegend': True,
                    'legendgroup': 'Stratification',            
                    'hoverinfo': 'text',
                    #'hovertext': None,                     
                    }
                trace_name_list = [a['name'] for a in design_profile_fig_data]
                if 'Stratification' not in trace_name_list:
                    design_profile_fig_data.append(stratification_line_trace) 
                else:
                    design_profile_fig_data[trace_name_list.index('Stratification')] = stratification_line_trace    
# =============================================================================
# =============================================================================
# =============================================================================
# # # stratification_line_text_trace               
# =============================================================================
# =============================================================================
# =============================================================================
                final_layer_elevation_text_list=[str(round(a,1)) + ' ft.' for a in design_line_elevation]
                x4final_layer_elevation_text_list = [design_profile_fig_layout['xaxis']['range'][0]] * len(design_line_elevation)       
                stratification_line_text_trace ={
                    'x': x4final_layer_elevation_text_list, 
                    'y': design_line_elevation,
                    'customdata': design_soil_types,
                    'mode': 'text',
                    'name': 'Stratification Text',
                    'type': 'scatter',
                    'line': {
                        'color': 'gray',
                        'width': 1,
                        'dash': 'dashdot',
                        },
                    'text': final_layer_elevation_text_list,
                    'textposition': "top right",
                    'textfont': {
                        'size': 8,                    
                        },
                    'visible': True, #'legendonly',
                    'showlegend': False,
                    'legendgroup': 'Stratification',
                    'hoverinfo': 'text',
                    #'hovertext': None,                     
                    }
                trace_name_list = [a['name'] for a in design_profile_fig_data]
                if 'Stratification Text' not in trace_name_list:
                    design_profile_fig_data.append(stratification_line_text_trace) 
                else:
                    design_profile_fig_data[trace_name_list.index('Stratification Text')] = stratification_line_text_trace    
        return design_profile_fig_data, design_profile_fig_layout 
def update_Su_over_p_lines_in_design_profile_func(
        design_profile_fig_layout,
        design_profile_fig_data,
        design_line_elevation,
        design_soil_types,
        design_bulk_density_list,
        Su_over_p_ratio_range_slider_value_list,
        water_level_elevation,
                    ):
        #elevation_list = [a for a in design_line_elevation]
    #soil_types_list = [a for a in design_soil_types]
    # bulk_density_list = [a for a in design_bulk_density_list]
    elevation_list = list(design_line_elevation)
    soil_types_list = list(design_soil_types)
    soil_types_list[-1] = design_soil_types[-2]
    # assume sand Total Unit Weight is 125 pcf
    bulk_density_list = [125 if pd.isnull(x) else x for x in design_bulk_density_list]
    bulk_density_list[-1] = design_bulk_density_list[-2]
    if (water_level_elevation not in design_line_elevation and 
        water_level_elevation is not None and 
        water_level_elevation<design_line_elevation[0] and 
        water_level_elevation>design_line_elevation[-1]):
        temp = [a for a in design_line_elevation if a<water_level_elevation][0]
        idx=design_line_elevation.index(temp)
        elevation_list.insert(idx,water_level_elevation)
        soil_types_list.insert(idx,soil_types_list[idx-1])
        bulk_density_list.insert(idx,bulk_density_list[idx-1])
    effective_overburden_pressure = [0]
    if (water_level_elevation is None):
        for i in range(1,len(elevation_list)):
            temp = (elevation_list[i-1] - elevation_list[i])*bulk_density_list[i-1] + effective_overburden_pressure[i-1]
            effective_overburden_pressure.append(temp)
    else:
        # consider the scenario that ground is below water
        if elevation_list[0] < water_level_elevation:
            effective_overburden_pressure = [(water_level_elevation-elevation_list[0])*62.4]
        for i in range(1,len(elevation_list)):
            if elevation_list[i] < water_level_elevation:
                temp = (elevation_list[i-1] - elevation_list[i])*(bulk_density_list[i-1]-62.4) + (effective_overburden_pressure[i-1])
            elif elevation_list[i] >= water_level_elevation:
                temp = (elevation_list[i-1] - elevation_list[i])*bulk_density_list[i-1] + effective_overburden_pressure[i-1]
            effective_overburden_pressure.append(temp)
    Su_over_p_ratio_min = [a*Su_over_p_ratio_range_slider_value_list[0] for a in effective_overburden_pressure]
    Su_over_p_ratio_max = [a*Su_over_p_ratio_range_slider_value_list[1] for a in effective_overburden_pressure]
# =============================================================================
# # =============================================================================
# # =============================================================================
# # =============================================================================
# # # # # update x axis range:    
# # =============================================================================
# # =============================================================================
# # =============================================================================
#                 
#                 if np.nanmax(data[x_axis_parameter]) > np.nanmin(data[x_axis_parameter]):
#                     x_axis_offset = 0.2* (np.nanmax(data[x_axis_parameter]) - np.nanmin(data[x_axis_parameter]))
#                 else:
#                     x_axis_offset = 0.2*np.nanmax(data[x_axis_parameter])                
#                 
#                 design_profile_fig_layout['xaxis']['range'] = [
#                     np.nanmin(data[x_axis_parameter]) - x_axis_offset,
#                     np.nanmax(data[x_axis_parameter]) + x_axis_offset, 
#                     ]
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # Su_over_p_ratio_min_trace               
# =============================================================================
# =============================================================================
# =============================================================================
    Su_over_p_ratio_min_trace ={
        'x': Su_over_p_ratio_min, 
        'y': elevation_list,
        'customdata': Su_over_p_ratio_min,
        'mode': 'lines',
        'name': 'Su/p = ' + str(Su_over_p_ratio_range_slider_value_list[0]),
        'type': 'scatter',
        'line': {
            'color': 'purple',
            'width': 1,
            'dash': 'dash',
            },
        'visible': True, #'legendonly',
        'showlegend': True,
        'hoverinfo': 'text',
        #'hovertext': None,                     
        }
    trace_name_list = [a['name'] for a in design_profile_fig_data]
    index = [idx for idx, s in enumerate(trace_name_list) if 'Su/p' in s]
    if len (index) > 0:
        design_profile_fig_data[index[0]] = Su_over_p_ratio_min_trace    
    else:
        design_profile_fig_data.append(Su_over_p_ratio_min_trace) 
# =============================================================================
# =============================================================================
# =============================================================================
# # # Su_over_p_ratio_min_trace               
# =============================================================================
# =============================================================================
# =============================================================================
    Su_over_p_ratio_max_trace ={
        'x': Su_over_p_ratio_max, 
        'y': elevation_list,
        'customdata': Su_over_p_ratio_min,
        'mode': 'lines',
        'name': 'Su/p = ' + str(Su_over_p_ratio_range_slider_value_list[1]),
        'type': 'scatter',
        'line': {
            'color': 'purple',
            'width': 1,
            'dash': 'dot',
            },
        'visible': True, #'legendonly',
        'showlegend': True,
        'hoverinfo': 'text',
        #'hovertext': None,                     
        }
    trace_name_list = [a['name'] for a in design_profile_fig_data]
    index = [idx for idx, s in enumerate(trace_name_list) if 'Su/p' in s]
    if len (index) > 1:
        design_profile_fig_data[index[1]] = Su_over_p_ratio_max_trace    
    else:
        design_profile_fig_data.append(Su_over_p_ratio_max_trace) 
    return design_profile_fig_data 

# =============================================================================
# =============================================================================
# =============================================================================
# # # # export_security_layout_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def export_security_layout_callbacks(app, cache):
    @app.callback(
        [
            Output('config-file-download', 'data'),
            Output('config-file-export-loading-hidden-div', 'children'),
            ],
        [
            Input('save-config-file-button', 'n_clicks'),
            ],
        [
          State('security-section-layout', 'children'),
          ],
                  prevent_initial_call=True,                  
                  )
    @cache.memoize(timeout=200)
    def clicks(n_clicks, security_section_layout):
        if security_section_layout:
# =============================================================================
#             print(security_section_layout)
# =============================================================================
            df = pd.DataFrame.from_records(security_section_layout)
# =============================================================================
#             print(df.keys())
#             print(len(df['props']))
#             print(len(df['type']))
#             print(len(df['namespace']))
#             print(df['namespace'])
# =============================================================================
            df['key'] = ['10cmar-zxcvbn123']*len(df)
            config_file_export_loading_hidden_div = "Exported!"
        else:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate
# =============================================================================
#         return send_data_frame(df.to_json, "Config File.cfg")
# =============================================================================
        return (
            send_data_frame(df.to_pickle, "Config File V010 .cfg"),
            config_file_export_loading_hidden_div,
                )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # load_security_layout_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def load_security_layout_callbacks(app, cache):
    @app.callback([
        Output('security-section-layout', 'children'),
        Output('config-file-upload-loading-hidden-div', 'children'),
                   ],
                  [
                      Input('upload-config-file', 'contents')
                      ],
                  [
                      State('upload-config-file', 'filename'),
                      State('security-section-layout', 'children'),
                    ],
                  prevent_initial_call=True,                  
                  )
    @cache.memoize(timeout=200)
    def load_security_layout_callbacks(file_input_contents, file_filenames, security_section_layout):
        layout = security_section_layout
        if '.cfg' in file_filenames:            
            print("data upload succeeded")
            content_type, content_string = file_input_contents.split(',')
            new = content_string
            decoded = b64decode(new)
            f = io.BytesIO(decoded)
# =============================================================================
#             df = pd.read_json(f)
# =============================================================================
            df = pd.read_pickle(f)
            if 'key' in list(df.keys()) and df['key'][0] == '10cmar-zxcvbn123': 
                df.drop(columns=['key'], inplace=True)
                layout = df.to_dict(orient='records') 
                config_file_upload_loading_hidden_div = "Loading Complete!"
            else:
                # PreventUpdate prevents ALL outputs updating
                raise dash.exceptions.PreventUpdate
        else:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate
        return (
            layout,
            config_file_upload_loading_hidden_div,                
                )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # CPT_point_selection_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def login_callbacks(app, cache, token, Boring_data_dataset1):
    @app.callback(
        [
            Output('load-database-button', 'disabled'),
            Output('save-config-file-button', 'disabled'),
            Output('upload-config-file', 'disabled'),
            Output('login-password-input', 'value'),
            Output('login-confirm-button', 'children'),
            Output('login-confirm-button', 'color'),
            ],
        [
            Input('login-confirm-button', 'n_clicks'),         
         ],
        [
            State('login-email-input', 'value'),
            State('login-password-input', 'value'),
         ],
        )
    @cache.memoize(timeout=60)
    def login_callbacks(
            login_confirm_button_nclicks,
            login_email_input_value,
            login_password_input_value,
            ):
        ctx = dash.callback_context
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        login_confirm_button_children= 'Confirm'
        login_confirm_button_color= 'primary'
        load_database_button_disabled = True
        save_config_file_button_disabled = True
        upload_config_file_button_disabled = True        
# read user list:
        user_info_key = b'h8BlCyJ1rbMsbHPpDDAJ9zF5DhmoKrzp66k1NsWNX3M='
        cipher_suite = Fernet(user_info_key)
        with open('user_info.bin', 'rb') as file_object:
            for line in file_object:
                encryptedpwd = line
        uncipher_text = (cipher_suite.decrypt(encryptedpwd))
        plain_text_encryptedpassword = bytes(uncipher_text).decode("utf-8") #convert to string
        users_list_df = pd.read_csv(io.StringIO(plain_text_encryptedpassword), sep='\s+')            
        if login_email_input_value in users_list_df['username'].tolist() and login_password_input_value==users_list_df['password'].tolist()[users_list_df['username'].tolist().index('xpeng@ardaman.com')] and login_confirm_button_nclicks and login_confirm_button_nclicks>0:
            login_password_input_value=""
            login_confirm_button_children='Loaded!'
            login_confirm_button_color='success'
# update layout:            
            load_database_button_disabled = False
            save_config_file_button_disabled = False
            upload_config_file_button_disabled = False
        elif triggered_input_id == 'login-confirm-button':
            load_database_button_disabled = True
            save_config_file_button_disabled = True
            upload_config_file_button_disabled = True
            login_confirm_button_children= 'Incorrect, try it again!'
            login_confirm_button_color= 'warning'
        elif login_confirm_button_nclicks and login_confirm_button_nclicks>0:
            load_database_button_disabled = False
            save_config_file_button_disabled = False
            upload_config_file_button_disabled = False        
        else:
            load_database_button_disabled = True
            save_config_file_button_disabled = True
            upload_config_file_button_disabled = True
        return (
            load_database_button_disabled,
            save_config_file_button_disabled,
            upload_config_file_button_disabled,
            login_password_input_value,
            login_confirm_button_children,
            login_confirm_button_color,
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # change_map_type_and_height_callback:    
# =============================================================================
# =============================================================================
# =============================================================================
def map_callbacks(app, cache):
    @app.callback(
        [
            Output('map-graph', 'figure'),
        ],
        [
            Input('map-type-select', 'value'),
            Input('map-height-slider', 'value'),
            Input('map-boring-marker-size-slider', 'value'),
            Input('map-boring-label-size-slider', 'value'),
            Input('load-database-button', 'n_clicks'),         
# =============================================================================
#             Input('generate-data-profile-button', 'n_clicks'),         
#             Input('generate-W2E-fence-plot-button', 'n_clicks'),         
#             Input('generate-S2N-fence-plot-button', 'n_clicks'),         
# =============================================================================
            ],
        [
            State('loaded-point-datatable', 'data'),         
            State('map-graph', 'figure'),
         ],
# =============================================================================
#         prevent_initial_call=True,
# =============================================================================
        )
    @cache.memoize(timeout=60)
    def update_map_view(type_value, 
                        height_value, 
                        map_marker_size, 
                        map_text_size,
                        login_confirm_button_nclicks,
# =============================================================================
#                         generate_data_profile_button_nclicks,
#                         generate_W2E_fence_plot_button_nclicks,
#                         generate_S2N_fence_plot_button_nclicks,
# =============================================================================
                        loaded_point_datatable_data,                                                                        
                        map_fig,
                        ):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update map-graph:
# =============================================================================
# =============================================================================
# =============================================================================
        ctx = dash.callback_context
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
# =============================================================================
#         print(triggered_input_id)    
# =============================================================================
        # if map_fig:
        if type_value == 'satellite-streets':
            map_style='satellite-streets'
        elif type_value == 'satellite':
            map_style='satellite'
        elif type_value == 'streets':
            map_style='streets'
        elif type_value == 'outdoors':
            map_style='outdoors'
        elif type_value == 'basic':
            map_style='basic'   
        elif type_value == 'light':
            map_style='light'   
        elif type_value == 'dark':
            map_style='dark'
        map_fig['layout']['mapbox']['style'] = map_style 
        map_fig['layout']['height'] = height_value
        for i in range(0,len(map_fig['data'])):
            if 'marker' in map_fig['data'][i].keys(): 
                if map_fig['data'][i]['marker']['color'] == 'black':
                    map_fig['data'][i]['marker'] = go.scattermapbox.Marker(
                        allowoverlap = True,
                        size=map_marker_size/5*6,
                        #symbol='airport',
                        color='black',
                        opacity=1.,
                        )
                else:
                    map_fig['data'][i]['marker'] = go.scattermapbox.Marker(
                        allowoverlap = True,
                        size=map_marker_size,
                        #symbol='airport',
                        color=map_fig['data'][i]['marker']['color'],
                        opacity=0.9,
                        )                     
            if 'textfont' in map_fig['data'][i].keys():            
                map_fig['data'][i]['textfont'] = dict(color='white',size=map_text_size)
        if triggered_input_id == 'load-database-button' and len(loaded_point_datatable_data)>0:
            loaded_point_datatable_data_df = pd.DataFrame.from_dict(loaded_point_datatable_data)
            Boring_point_datatable_data_df = loaded_point_datatable_data_df[loaded_point_datatable_data_df["Location Type"]=="BH"]
            CPT_point_datatable_data_df = loaded_point_datatable_data_df[loaded_point_datatable_data_df["Location Type"]=="CPT"]
            TestPile_point_datatable_data_df = loaded_point_datatable_data_df[loaded_point_datatable_data_df["Location Type"]=='Test Pile']
            MonitorPile_point_datatable_data_df = loaded_point_datatable_data_df[loaded_point_datatable_data_df["Location Type"]=='Monitor Pile']
            zoom_level_tuple = determine_zoom_level(loaded_point_datatable_data_df["Latitude Decimal"].tolist(), loaded_point_datatable_data_df["Longitude Decimal"].tolist())
            map_fig['layout']['mapbox']['zoom'] = zoom_level_tuple[0] 
            map_fig['layout']['mapbox']['center'] ={'lat':zoom_level_tuple[1][1],'lon':zoom_level_tuple[1][0]}
# reset map points:
            map_fig['data'] = []
            df_list = [Boring_point_datatable_data_df,
                       CPT_point_datatable_data_df,
                       TestPile_point_datatable_data_df,
                       MonitorPile_point_datatable_data_df,           
                       ]
            group_name_list = ["Boreholes", "CPTs", 'Test Pile', 'Monitor Pile']
            map_fill_color_list = ['red', 'yellow', 'Fuchsia', 'Aqua']
            map_line_color_list = ['black', 'black', 'black', 'black']
            map_text_color_list = ['white', 'white', 'white', 'white']
            for i in range(0, len(df_list)):                         
                plot_location_point_in_mapbox(map_fig, df_list[i], group_name_list[i], map_fill_color_list[i], map_line_color_list[i], map_marker_size, map_text_color_list[i], map_text_size)
            map_fig['layout']['legend']=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01)        
# =============================================================================
#         if (triggered_input_id in ['generate-data-profile-button', 'generate-W2E-fence-plot-button', 'generate-S2N-fence-plot-button'] and 
#             map_fig['layout']['dragmode'] !="pan"):
#             map_fig['layout']['dragmode'] ="pan"
# =============================================================================
        return (map_fig,                
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # CPT_point_selection_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def map_view_layout_collapse_callbacks(app, cache):
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 is_open,
                 ) {
                     if (is_open == true) {
                             is_open =false;
                             button_chirdren = 'Open Map';
                             } else if (is_open == false) {
                                 is_open =true;
                                 button_chirdren = 'Close Map';
                                 }
                     return [
                         is_open,
                         button_chirdren,
                         is_open,
                             ]
                     }  
        """,  
        [
        Output("map-view-layout-collapse", "is_open"),
        Output("open-map-view-layout-collapse-button", "children"),            
        Output("open-map-view-layout-collapse-button", "active"),            
            ],
        [
            Input('open-map-view-layout-collapse-button', 'n_clicks'),         
         ],
        [
            State("map-view-layout-collapse", "is_open"),
         ],
        prevent_initial_call=True,                  
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # CPT_point_selection_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def notice4users_callbacks(app, cache):
    @app.callback(
        [
            Output("notice4users-modal", "is_open"),
            ],
        [
            Input('login-confirm-button', 'color'),         
            Input('notice4users-close-button', 'n_clicks'),            
            Input('notice4users-info-button', 'n_clicks'),
         ],
        [
            State("notice4users-modal", "is_open"),
         ],
        )
    @cache.memoize(timeout=60)
    def notice4users_callbacks(
            login_confirm_button_color,
            notice4users_close_button_nclicks,
            notice4users_info_button_nclicks,
            notice4users_modal_is_open,
            ):
        ctx = dash.callback_context
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if login_confirm_button_color=='success' or notice4users_info_button_nclicks:
            notice4users_modal_is_open = True
        if triggered_input_id=='notice4users-close-button' and notice4users_close_button_nclicks:
             notice4users_modal_is_open = False
        return (
            notice4users_modal_is_open,
            )



# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_soil_profile_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def composite_soil_profile_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# =============================================================================
# =============================================================================
# # # # data_proifles-update-signal-1 update callback  
# =============================================================================
# =============================================================================
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(data_profile_data_store_1,
                 data_profile_data_store_2,
                 data_profile_data_store_3,
                 data_profile_data_store_4,
                 data_profile_data_store_5,
                 data_proifles_update_signal_1,
                 interpretation_mode_select) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 }                     
                     if (['Data-Profile-1-clientside-figure-data-store', 
                          'Data-Profile-2-clientside-figure-data-store', 
                          'Data-Profile-3-clientside-figure-data-store',
                          'Data-Profile-4-clientside-figure-data-store',
                          'Data-Profile-5-clientside-figure-data-store'].indexOf(triggered_input_id) > -1 && interpretation_mode_select == 'Interpretation Mode') {
                             data_proifles_update_signal_1=data_proifles_update_signal_1+1;
                            }
                     return [data_proifles_update_signal_1];                   
                     };
        """,
        [Output('data-proifles-update-signal-1', 'children')],
        Input('Data-Profile-1-clientside-figure-data-store', 'data'), 
        Input('Data-Profile-2-clientside-figure-data-store', 'data'), 
        Input('Data-Profile-3-clientside-figure-data-store', 'data'), 
        Input('Data-Profile-4-clientside-figure-data-store', 'data'), 
        Input('Data-Profile-5-clientside-figure-data-store', 'data'), 
        State('data-proifles-update-signal-1', 'children'),
        State('interpretation-mode-select', 'value'),        
        prevent_initial_call=True,
    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Update finalize stratification button:
# =============================================================================
# =============================================================================
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 data_proifles_update_signal_1,
                 interpretation_mode_select,
                 composite_thickness_resolution,
                 ) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var finalize_stratification_button_color = 'danger'
                     var finalize_stratification_button_children = 'Finalize Stratification'
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 }
                     if (interpretation_mode_select == 'Interpretation Mode') {
                         finalize_stratification_button_disabled = false
                         if (['finalize-stratification-button'].includes(triggered_input_id) == true) {
                                 finalize_stratification_button_color = 'primary';
                                 finalize_stratification_button_children = 'Finalize Stratification (Updated)';
                                 } else if (['interpretation-mode-select', 'data-proifles-update-signal-1', 'thickness-resolution-slider'].includes(triggered_input_id) == true) {
                                                finalize_stratification_button_color = 'danger';
                                                finalize_stratification_button_children = 'Finalize Stratification (Outdated)';
                                     } else {
                                         finalize_stratification_button_color = 'danger';
                                         finalize_stratification_button_children = 'Finalize Stratification (Outdated)';
                                         }                             
                             } else {
                                 finalize_stratification_button_disabled = true;
                                 }
                     return [finalize_stratification_button_children, 
                             finalize_stratification_button_color,
                             finalize_stratification_button_disabled,
                             ]
                     }  
        """,  
        [
            Output('finalize-stratification-button', 'children'),
            Output('finalize-stratification-button', 'color'),
            Output('finalize-stratification-button', 'disabled'),
            ],
        [
            Input('finalize-stratification-button', 'n_clicks'),
            Input('data-proifles-update-signal-1', 'children'),
            Input('interpretation-mode-select', 'value'),        
            Input('thickness-resolution-slider', 'value'),                     
            ],
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Update all clientside-figure-data-store :
# =============================================================================
# =============================================================================
# =============================================================================
    @app.callback(
        [
            Output('composite-soil-stratification-clientside-figure-data-store', 'data'),            
            Output('composite-soil-stratification-clientside-figure-layout-store', 'data'),            
            Output('composite-soil-stratification-clientside-store-loading-hidden-div', 'children'),
            ],
        [
            Input('generate-data-profile-button', 'n_clicks'),         
            # Input('data-profile-text-size-slider', 'value'),         
            Input('water-level-elevation-input', 'value'),         
            Input('thickness-resolution-slider', 'value'),                     
            Input('finalize-stratification-button', 'n_clicks'),
            ],
        [
            State('dataset1-selected-soil-lithology-table', 'derived_virtual_data'),         
            State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
            State('composite-soil-stratification-graph', 'figure'),
            State('Data-Profile-1-clientside-figure-data-store', 'data'), 
            State('Data-Profile-2-clientside-figure-data-store', 'data'), 
            State('Data-Profile-3-clientside-figure-data-store', 'data'), 
            State('Data-Profile-4-clientside-figure-data-store', 'data'), 
            State('Data-Profile-5-clientside-figure-data-store', 'data'),             
            State('interpretation-mode-select', 'value'),        
            ],
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=TIMEOUT)
    def composite_soil_profile_callbacks(
            generate_data_profile_n_clicks,
            # composite_soil_profile_fig_text_size,
            water_level_elevation,
            composite_thickness_resolution,
            finalize_stratification_button_n_clicks,
            dataset1_selected_soil_lithology_data_table_data,
            dataset1_selected_soil_boring_data_table_data,
            composite_soil_profile_fig,
            data_profile_data_store_1,
            data_profile_data_store_2,
            data_profile_data_store_3,
            data_profile_data_store_4,
            data_profile_data_store_5,
            interpretation_mode_select,
            ):
        ctx = dash.callback_context
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        data = composite_soil_profile_fig['data']
        layout = composite_soil_profile_fig['layout']
        composite_soil_profile_clientside_store_loading_hidden_div = ""
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update data profiles:            
# =============================================================================
# =============================================================================
# =============================================================================
        if triggered_input_id in ['generate-data-profile-button', 
                                  'data-profile-text-size-slider', 
                                  'water-level-elevation-input',
                                  'thickness-resolution-slider',
                                  ]:            
            # composite_soil_profile_fig_text_size = composite_soil_profile_fig_text_size
            composite_soil_profile_fig_layout = composite_soil_profile_fig['layout']
            data,layout = update_composite_soil_profile_func(
                # composite_soil_profile_fig_text_size,                 
                dataset1_selected_soil_boring_data_table_data,
                dataset1_selected_soil_lithology_data_table_data,                
                composite_soil_profile_fig_layout, 
                composite_thickness_resolution,
                water_level_elevation,
                            )
            composite_soil_profile_clientside_store_loading_hidden_div ="Loading Complete!"
            return [data, layout, composite_soil_profile_clientside_store_loading_hidden_div]
        elif (triggered_input_id in ['finalize-stratification-button'] and 
              interpretation_mode_select == 'Interpretation Mode'):
            data = finalize_composite_soil_boring_func(
                data,
                composite_thickness_resolution,
                data_profile_data_store_1,
                data_profile_data_store_2,
                data_profile_data_store_3,
                data_profile_data_store_4,
                data_profile_data_store_5,
                )            
        composite_soil_profile_clientside_store_loading_hidden_div ="Loading Complete!"
        return [data, layout, composite_soil_profile_clientside_store_loading_hidden_div]
# =============================================================================
#         else:
#             raise dash.exceptions.PreventUpdate  
# 
# =============================================================================
# =============================================================================
# # Update fence graph:
# =============================================================================
    app.clientside_callback(
        """
        function(data, layout) {
            if (data !== 'undefined') {
                    return [{'data': data, 'layout': layout}]
                             } else {
                                 return [{'data': [], 'layout': layout}]
                                 }
        }
        """,
        [Output('composite-soil-stratification-graph', 'figure')],
        Input('composite-soil-stratification-clientside-figure-data-store', 'data'),            
        Input('composite-soil-stratification-clientside-figure-layout-store', 'data'),            
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # # data_profile_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
def data_profile_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Update generate graph button:
# =============================================================================
# =============================================================================
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 loaded_data_datatable_update_signal_1,
                 data_profile_fig_1, 
                 data_profile_fig_2, 
                 data_profile_fig_3, 
                 data_profile_fig_4, 
                 data_profile_fig_5, 
                 ) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var generate_data_profile_button_color = 'success'
                     var generate_data_profile_button_children = 'Generate Graph'
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 } 
                     if (['generate-data-profile-button', 'loaded-data-datatable-update-signal-1'].includes(triggered_input_id) == false) {
                             generate_data_profile_button_color = 'success';
                             generate_data_profile_button_children = 'Generate Graph (Updated)';
                             } else if (loaded_data_datatable_update_signal_1 > 1) {
                                            generate_data_profile_button_color = 'danger';
                                            generate_data_profile_button_children = 'Generate Graph (Outdated)';
                                 } else {
                                     generate_data_profile_button_color = 'success';
                                     generate_data_profile_button_children = 'Generate Graph';
                                     }
                     return [generate_data_profile_button_children, 
                             generate_data_profile_button_color,
                             ]
                     }  
        """,  
        [
            Output('generate-data-profile-button', 'children'),
            Output('generate-data-profile-button', 'color'),
            ],
        [
            Input('generate-data-profile-button', 'n_clicks'),
            Input('loaded-data-datatable-update-signal-1', 'children'),
            # Input('data-profile-graph', 'figure'),
            ] + [Input('Data-Profile-' + str(a) +'-data-profile-graph', 'figure')  for a in list(range(1,6))],
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update all clientside-figure-data-store and window-size-sliders:
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
    data_profile_name_list = ['Data Profile ' + str(a) for a in list(range(1,6))]
    for i in range(0, len(data_profile_name_list)):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update window size sliders:
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # update -window-size-slider-store:    
# =============================================================================
# =============================================================================
        @app.callback(
            Output(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider-store', 'data'),                     
            [
                Input('generate-data-profile-button', 'n_clicks'),         
                Input('interpretation-mode-select', 'value'),         
                Input(data_profile_name_list[i].replace(" ", "-") + '-x-axis-parameter-select', 'value'),         
                ],
            [
                State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
             ],                    
            prevent_initial_call=True,
            )
        @cache.memoize(timeout=TIMEOUT)
        def data_profile_window_size_callbacks(
                generate_data_profile_n_clicks,
                interpretation_mode_select,
                x_axis_parameter_select,
                dataset1_selected_soil_boring_data_table_data,
                ):
            ctx = dash.callback_context
            if not ctx.triggered:
                triggered_input_id = []
            else:
                triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if (interpretation_mode_select == 'Interpretation Mode' and 
                triggered_input_id in ['generate-data-profile-button', 
                                       'interpretation-mode-select',
                                       data_profile_name_list[i].replace(" ", "-") + '-x-axis-parameter-select',
                                       ]):
                if dataset1_selected_soil_boring_data_table_data: 
                    data_0=pd.DataFrame.from_records(dataset1_selected_soil_boring_data_table_data)
                    if x_axis_parameter_select in data_0.keys():
                        data = data_0[x_axis_parameter_select].dropna()
                        window_size_slider_min = int(math.ceil(len(data)/200))
                        window_size_slider_max = int(math.ceil(len(data)/5))                                        
                        window_size_slider_step = max(1,int(math.ceil((window_size_slider_max-window_size_slider_min)/10)))
                        window_size_slider_value_list = list(range(window_size_slider_min,window_size_slider_max+1,window_size_slider_step))
                        if len(window_size_slider_value_list)>1:
                            window_size_slider_value = window_size_slider_value_list[int(math.floor(len(window_size_slider_value_list)/2))]
                        else:
                            window_size_slider_value = 1
                            window_size_slider_value_list = list(range(1,min(2,len(data)+1)))
                            window_size_slider_min = 1
                            window_size_slider_max = min(2,len(data))
                            window_size_slider_step = 1
                        window_size_slider_marks= {a: {'label': str(a)} for a in window_size_slider_value_list}
                        data = [window_size_slider_value, 
                                window_size_slider_min, 
                                window_size_slider_max,
                                window_size_slider_step,
                                window_size_slider_marks,
                                ]
                        return data
                    else:
                        raise dash.exceptions.PreventUpdate                    
                else:
                    raise dash.exceptions.PreventUpdate                      
            else:
                raise dash.exceptions.PreventUpdate                    
# =============================================================================
# =============================================================================
# # #  update-window-size-slider:
# =============================================================================
# =============================================================================
        app.clientside_callback(
            """
            function(data) {
                if (data !== 'undefined') {
                        return data
                                 } 
            }
            """,
            [
                Output(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider', 'value'),         
                Output(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider', 'min'),         
                Output(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider', 'max'),         
                Output(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider', 'step'),         
                Output(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider', 'marks'),         
                ],
            Input(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider-store', 'data'),         
            prevent_initial_call=True,
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update all clientside-figure-data-store :
# =============================================================================
# =============================================================================
# =============================================================================        
        @app.callback(
            [
                Output(data_profile_name_list[i].replace(" ", "-") + '-clientside-figure-data-store', 'data'),            
                Output(data_profile_name_list[i].replace(" ", "-") + '-clientside-figure-layout-store', 'data'),            
                Output(data_profile_name_list[i].replace(" ", "-") + '-clientside-store-loading-hidden-div', 'children'),
                ],
            [
                Input('generate-data-profile-button', 'n_clicks'),         
                Input(data_profile_name_list[i].replace(" ", "-") + '-x-axis-parameter-select', 'value'),         
                Input('water-level-elevation-input', 'value'),         
                Input('delete-data-selection-button', 'n_clicks'),
                Input('interpretation-mode-select', 'value'),         
                Input(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider-store', 'data'),         
                Input(data_profile_name_list[i].replace(" ", "-") + '-window-size-slider', 'value'),         
                ],
            [
                State(data_profile_name_list[i].replace(" ", "-") + '-data-profile-graph', 'selectedData'),
                State('map-graph', 'selectedData'), 
                State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
                State(data_profile_name_list[i].replace(" ", "-") + '-data-profile-graph', 'figure'),
             ],
            prevent_initial_call=True,
            )
        @cache.memoize(timeout=TIMEOUT)
        def data_profile_callbacks(
                generate_data_profile_n_clicks,
                x_axis_parameter_select,
                water_level_elevation,
                delete_data_selection_n_clicks,
                interpretation_mode_select,
                data_window_size_data,
                data_window_size_value,
                data_profile_selection_points,
                map_selection_points,               
                dataset1_selected_soil_boring_data_table_data,
                data_profile_fig,
                ):
            ctx = dash.callback_context
            if not ctx.triggered:
                triggered_input_id = []
            else:
                triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
            print(triggered_input_id)
            data = data_profile_fig['data']
            layout = data_profile_fig['layout']
            data_profile_clientside_store_loading_hidden_div = ""
            data_window_size =data_window_size_data[0]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update data profiles:            
# =============================================================================
# =============================================================================
# =============================================================================
            if triggered_input_id not in ['delete-data-selection-button'] + [a.replace(" ", "-") + '-window-size-slider' for a in data_profile_name_list]:            
                x_axis_parameter = x_axis_parameter_select
# =============================================================================
#                 x_axis_parameter = x_axis_parameter.replace('#200 Finer', 'Percentage Passing at 0_075'),
# =============================================================================
                x_axis_parameter_unit = ''
                if x_axis_parameter in ['Moisture Content', 'Percentage Passing at 0_075']:
                    x_axis_parameter_unit = '%'
                elif x_axis_parameter in ['Total Unit Weight', 'Dry Density']:
                    x_axis_parameter_unit = 'pcf.'
                elif x_axis_parameter in ['Compressive Strength', 'Undrained Shear Strength']:
                    x_axis_parameter_unit = 'psf.'
                elif x_axis_parameter in ['SPT N']:
                    x_axis_parameter_unit = 'blows/ft.'
                else: 
                    x_axis_parameter_unit = ''
                data_profile_fig_layout = data_profile_fig['layout']
                data,layout = update_data_profile_func(
                    map_selection_points,
                    dataset1_selected_soil_boring_data_table_data,
                    data_profile_fig_layout,
                    x_axis_parameter,
                    x_axis_parameter_unit,
                    water_level_elevation,
                    interpretation_mode_select,
                    data_window_size,
                                )
                data_profile_clientside_store_loading_hidden_div ="Loading Complete!"
                return [data, layout, data_profile_clientside_store_loading_hidden_div]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # delete data point selection:
# =============================================================================
# =============================================================================
# =============================================================================
            elif (triggered_input_id == 'delete-data-selection-button' 
                  and 'selectedpoints' in data[0].keys()):
                data_selection_index_list = data[0]['selectedpoints']
# =============================================================================
#                 print(data_selection_index_list)
#                 print(data[0].keys())
# =============================================================================
                data_keys = list(data[0].keys())
                data_len = len(data[0]['x'])
                for i in data_keys:
                    if isinstance(data[0][i], bool) == False and len(data[0][i]) == data_len:
                        data[0][i]  = [a for b, a in enumerate(data[0][i]) if b not in data_selection_index_list]
                del data[0]['selectedpoints']
                if interpretation_mode_select == 'Interpretation Mode':
                    data = update_data_profile4_interpretation_mode_func(
                        data,
                        data_window_size_value,
                        )
                return [data, layout, data_profile_clientside_store_loading_hidden_div]
            elif (triggered_input_id in [a.replace(" ", "-") + '-window-size-slider' for a in data_profile_name_list]):
                if interpretation_mode_select == 'Interpretation Mode':
                    data = update_data_profile4_interpretation_mode_func(
                        data,
                        data_window_size_value,
                        )
                return [data, layout, data_profile_clientside_store_loading_hidden_div]
            else:
                raise dash.exceptions.PreventUpdate  
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update fence graph:
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
        app.clientside_callback(
            """
            function(data, layout) {
                if (data !== 'undefined') {
                        return [{'data': data, 'layout': layout}]
                                 } else {
                                     return [{'data': [], 'layout': layout}]
                                     }
            }
            """,
            [Output(data_profile_name_list[i].replace(" ", "-") + '-data-profile-graph', 'figure')],
            Input(data_profile_name_list[i].replace(" ", "-") + '-clientside-figure-data-store', 'data'),            
            Input(data_profile_name_list[i].replace(" ", "-") + '-clientside-figure-layout-store', 'data'),            
            prevent_initial_call=True,
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # design_layer_datatable_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def design_layer_datatable_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# =============================================================================
# =============================================================================
# # # # design_layer_datatable_callbacks:
# =============================================================================
# =============================================================================
# =============================================================================
    @app.callback(
        [
            Output('design-layer-datatable', 'data'),            
            ],
        [
            Input('composite-soil-stratification-clientside-figure-data-store', 'data'),         
            Input('add-design-layer-button', 'n_clicks'),         
            Input('design-layer-datatable', 'data'),            
            ],
        [
            State('design-layer-datatable', 'selected_rows'),            
            ],
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=TIMEOUT)
    def design_layer_datatable_callbacks(
            composite_stratification_data_store,
            add_design_layer_n_clicks,
            data,
            selected_rows,
            # active_cell,
            ):
        ctx = dash.callback_context
        style_data_conditional= []
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if (triggered_input_id in ['composite-soil-stratification-clientside-figure-data-store'] and 
            len(composite_stratification_data_store) > 0):
            composite_stratification_trace_name_list = [a['name'] for a in composite_stratification_data_store]
            if 'Stratification Text' in composite_stratification_trace_name_list:
                design_line_elevation = composite_stratification_data_store[composite_stratification_trace_name_list.index('Stratification Text')]['y']
                design_line_elevation = [round(a,2) for a in design_line_elevation]
                design_soil_types = composite_stratification_data_store[composite_stratification_trace_name_list.index('Stratification Text')]['customdata']
                design_line_table = pd.DataFrame()
                design_line_table['Top Elevation'] = design_line_elevation[:-1]
                design_line_table['Base Elevation'] = design_line_elevation[1:]
                design_line_table['Soil Type'] = design_soil_types[:-1]
                soil_symbol_list = [""]*len(design_line_table)
                if 'Soil Lithology Columns' in composite_stratification_trace_name_list:
                    temp = composite_stratification_data_store[composite_stratification_trace_name_list.index("Soil Lithology Columns")]
                    for i in range(0, len(soil_symbol_list)):
                        for j in range(0, len(temp['y'])):
                            if (round(design_line_table['Top Elevation'][i],2) > round(temp['base'][j],2) and 
                                round(design_line_table['Top Elevation'][i],2) <= round(temp['base'][j] + temp['y'][j],2) 
                                ):
                                soil_symbol_list[i] = temp['text'][j]
                    design_line_table['Soil Symbol'] = [a for a in soil_symbol_list]
# auto fill 'Soil Type':
                soil_type_list = [a for a in design_line_table['Soil Type']]
                for_loop_repeat_idx=0
                while for_loop_repeat_idx <len(design_line_table):
                    for i in range(0, len(design_line_table)-1):
                        if (soil_type_list[i] not in ["Clay", "Silt", "Sand", "Gravel"] and 
                            soil_type_list[i+1] in ["Clay", "Silt", "Sand", "Gravel"]):
                            soil_type_list[i] = soil_type_list[i+1]
                    for_loop_repeat_idx+=1
                if soil_type_list[len(design_line_table)-1] not in ["Clay", "Silt", "Sand", "Gravel"]:
                    soil_type_list[len(design_line_table)-1] = soil_type_list[len(design_line_table)-2]
                design_line_table['Soil Type'] = [a for a in soil_type_list]
# export to dict:                
                data = design_line_table.to_dict(orient='records')
# append empty row:
                if (data[-1] != {'Top Elevation': "", 'Base Elevation': "", 'Soil Type': "", 'Soil Symbol': "",}):
                    data.append({'Top Elevation': "", 'Base Elevation': "", 'Soil Type': "", 'Soil Symbol': "",})
                return [data]
            else:
                raise dash.exceptions.PreventUpdate
        elif (triggered_input_id in ['add-design-layer-button'] and len(selected_rows)>0):
            data.insert(selected_rows[0], data[selected_rows[0]])            
            return [data]
        elif (triggered_input_id in ['design-layer-datatable']):
            if (data[-1] != {'Top Elevation': "", 'Base Elevation': "", 'Soil Type': "", 'Soil Symbol': "",}):
                data.append({'Top Elevation': "", 'Base Elevation': "", 'Soil Type': "", 'Soil Symbol': "",})
            for i in range(0, len(data)-2):
                data[i]['Base Elevation'] = data[i+1]['Top Elevation']
            return [data]                    
        else:
            raise dash.exceptions.PreventUpdate
# =============================================================================
# =============================================================================
# =============================================================================
# # # # design_layer_column_callbacks:
# =============================================================================
# =============================================================================
# =============================================================================
    @app.callback(
        [
            Output('composite-design-stratification-clientside-figure-data-store-A', 'data'),         
            Output('composite-design-stratification-clientside-figure-layout-store-A', 'data'),         
            ],
        [
            Input('generate-design-profile-button', 'n_clicks'),
            ],
        [
            State('design-layer-datatable', 'data'),            
            State('composite-soil-stratification-clientside-figure-layout-store', 'data'),         
            State('water-level-elevation-input', 'value'),         
            # State('data-profile-text-size-slider', 'value'),         
            ],
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=TIMEOUT)
    def design_layer_column_callbacks(
            generate_design_profile_n_clicks,
            design_layer_datatable_data,
            composite_stratification_layout_store,
            water_level_elevation,
            # data_profile_fig_text_size,
            ):
        if generate_design_profile_n_clicks >0:
            data=pd.DataFrame.from_records(design_layer_datatable_data)
            if "" not in list(data['Top Elevation'][:-1]):
                layout = composite_stratification_layout_store.copy()
                data, layout = update_composite_design_column_func(
                    data,
                    layout,
                    water_level_elevation,
                    # data_profile_fig_text_size,                    
                    )
                return [data, layout]
            else:
                raise dash.exceptions.PreventUpdate
        else:
            raise dash.exceptions.PreventUpdate
# =============================================================================
# # Update fence graph:
# =============================================================================
    app.clientside_callback(
        """
        function(data, layout) {
            if (data !== 'undefined') {
                    return [{'data': data, 'layout': layout}]
                             } else {
                                 return [{'data': [], 'layout': layout}]
                                 }
        }
        """,
        [Output('composite-design-stratification-graph-A', 'figure')],
        Input('composite-design-stratification-clientside-figure-data-store-A', 'data'),            
        Input('composite-design-stratification-clientside-figure-layout-store-A', 'data'),            
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # # design_profile_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
def design_profile_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Update generate graph button:
# =============================================================================
# =============================================================================
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 design_layer_datatable_data,
                 Nkt_value_slider_value,
                 selected_CPT_method,
                 ) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var generate_design_profile_button_color = 'success'
                     var generate_design_profile_button_children = 'Generate Graph'
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 } 
                     if (['generate-design-profile-button'].includes(triggered_input_id) == true) {
                             generate_design_profile_button_color = 'success';
                             generate_design_profile_button_children = 'Generate Graph (Updated)';
                             } else if (['design-layer-datatable', 'Nkt-value-slider', 'CPT-method-select'].includes(triggered_input_id) == true) {
                                            generate_design_profile_button_color = 'danger';
                                            generate_design_profile_button_children = 'Generate Graph (Outdated)';
                                 } else {
                                     generate_design_profile_button_color = 'success';
                                     generate_design_profile_button_children = 'Generate Graph';
                                     }
                     return [generate_design_profile_button_children, 
                             generate_design_profile_button_color,
                             ]
                     }  
        """,  
        [
            Output('generate-design-profile-button', 'children'),
            Output('generate-design-profile-button', 'color'),
            ],
        [
            Input('generate-design-profile-button', 'n_clicks'),
            Input('design-layer-datatable', 'data'),            
            Input('Nkt-value-slider', 'value'),
            Input('CPT-method-select', 'value'),
            ],
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update all clientside-figure-data-store and window-size-sliders:
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
    design_profile_name_list = ['Design Profile A' + str(a) for a in list(range(1,6))]
    for i in range(0, len(design_profile_name_list)):
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update all clientside-figure-data-store :
# =============================================================================
# =============================================================================
# =============================================================================        
        @app.callback(
            [
                Output(design_profile_name_list[i].replace(" ", "-") + '-clientside-figure-data-store', 'data'),            
                Output(design_profile_name_list[i].replace(" ", "-") + '-clientside-figure-layout-store', 'data'),            
                Output(design_profile_name_list[i].replace(" ", "-") + '-clientside-store-loading-hidden-div', 'children'),
                ],
            [
                Input('generate-design-profile-button', 'n_clicks'),         
                #Input('design-profile-text-size-slider', 'value'),         
                Input(design_profile_name_list[i].replace(" ", "-") + '-x-axis-parameter-select', 'value'),         
                Input('water-level-elevation-input', 'value'),         
                Input('delete-data-selection4design-button', 'n_clicks'),
                Input(design_profile_name_list[i].replace(" ", "-") + '-quantile-range-slider', 'value'),         
                ],
            [
                State(design_profile_name_list[i].replace(" ", "-") + '-data-profile-graph', 'selectedData'),
                State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
                State('dataset1-selected-CPT-data-table', 'derived_virtual_data'),         
                State(design_profile_name_list[i].replace(" ", "-") + '-data-profile-graph', 'figure'),
                #State('composite-design-stratification-clientside-figure-data-store', 'data'),
                State('design-layer-datatable', 'data'),            
             ],
            prevent_initial_call=True,
            )
        @cache.memoize(timeout=TIMEOUT)
        def design_profile_callbacks(
                generate_design_profile_n_clicks,
                #design_profile_fig_text_size,
                x_axis_parameter_select,
                water_level_elevation,
                delete_data_selection_n_clicks,
                quantile_range,
                design_profile_selection_points,
                dataset1_selected_soil_boring_data_table_data,
                dataset1_selected_CPT_data_table_data,
                design_profile_fig,
                design_layer_datatable_data,
                ):
            ctx = dash.callback_context
            if not ctx.triggered:
                triggered_input_id = []
            else:
                triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
            print(triggered_input_id)
            data = design_profile_fig['data']
            layout = design_profile_fig['layout']
            design_profile_clientside_store_loading_hidden_div = ""
            design_layer_datatable_data=pd.DataFrame.from_records(design_layer_datatable_data)
            if design_layer_datatable_data['Top Elevation'][len(design_layer_datatable_data)-1] == "":
                design_layer_datatable_data = design_layer_datatable_data.iloc[:-1].copy()            
            if "" not in list(design_layer_datatable_data['Top Elevation'][:-1]):
                design_line_elevation = design_layer_datatable_data["Top Elevation"].tolist() + [design_layer_datatable_data["Base Elevation"].tolist()[-1]]
                design_soil_types = design_layer_datatable_data["Soil Type"].tolist() + [None]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update design profiles:            
# =============================================================================
# =============================================================================
# =============================================================================
                if triggered_input_id not in ['delete-data-selection4design-button'] + [a.replace(" ", "-") + '-quantile-range-slider' for a in design_profile_name_list]:            
                    x_axis_parameter = x_axis_parameter_select
                    x_axis_parameter_unit = ''
                    if x_axis_parameter in ['Moisture Content', 'Percentage Passing at 0_075']:
                        x_axis_parameter_unit = '%'
                    elif x_axis_parameter in ['Total Unit Weight', 'Dry Density']:
                        x_axis_parameter_unit = 'pcf.'
                    elif x_axis_parameter in ['Compressive Strength', 'Undrained Shear Strength']:
                        x_axis_parameter_unit = 'psf.'
                    elif x_axis_parameter in ['SPT N']:
                        x_axis_parameter_unit = 'blows/ft.'
                    else: 
                        x_axis_parameter_unit = ''
                    # design_profile_fig_text_size = design_profile_fig_text_size
                    design_profile_fig_layout = design_profile_fig['layout']
                    data,layout = update_design_profile_func(
                        # design_profile_fig_text_size, 
                        dataset1_selected_soil_boring_data_table_data,
                        dataset1_selected_CPT_data_table_data,
                        design_profile_fig_layout,
                        x_axis_parameter,
                        x_axis_parameter_unit,
                        design_line_elevation,
                        design_soil_types,
                        water_level_elevation,
                                    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # delete data point selection:
# =============================================================================
# =============================================================================
# =============================================================================
                elif (triggered_input_id == 'delete-data-selection4design-button' 
                      and 'selectedpoints' in data[0].keys()):
                    data_selection_index_list = data[0]['selectedpoints']
                    data_keys = list(data[0].keys())
                    data_len = len(data[0]['x'])
                    for i in data_keys:
                        if isinstance(data[0][i], bool) == False and len(data[0][i]) == data_len:
                            data[0][i]  = [a for b, a in enumerate(data[0][i]) if b not in data_selection_index_list]
                    del data[0]['selectedpoints']
# =============================================================================
#                 elif (triggered_input_id in [a.replace(" ", "-") + '-quantile-range-slider' for a in design_profile_name_list]):
# =============================================================================
                if len(data)>0 and len(design_line_elevation)>0:
                    data = update_design_lines_func(
                        data,
                        design_line_elevation,
                        design_soil_types,
                        quantile_range,
                        )
                design_profile_clientside_store_loading_hidden_div ="Loading Complete!"
                return [data, layout, design_profile_clientside_store_loading_hidden_div]
            else:
                raise dash.exceptions.PreventUpdate  
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update design profiles A:
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
        app.clientside_callback(
            """
            function(data, layout) {
                if (data !== 'undefined') {
                        return [{'data': data, 'layout': layout}]
                                 } else {
                                     return [{'data': [], 'layout': layout}]
                                     }
            }
            """,
            [Output(design_profile_name_list[i].replace(" ", "-") + '-data-profile-graph', 'figure')],
            Input(design_profile_name_list[i].replace(" ", "-") + '-clientside-figure-data-store', 'data'),            
            Input(design_profile_name_list[i].replace(" ", "-") + '-clientside-figure-layout-store', 'data'),            
            prevent_initial_call=True,
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # download_soil_design_parameter_datatable_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def download_soil_design_parameter_datatable_callbacks(app, cache):
    @app.callback(Output('soil-design-parameters-download', 'data'),
                  [
                      Input('download-soil-design-parameters-button', 'n_clicks'),
                      ],
                  [
                    State('soil-design-parameter-datatable', 'derived_virtual_data'),
                    ],                       
                  )
    @cache.memoize(timeout=200)
    def clicks(n_clicks, soil_design_parameter_datatable):
        if soil_design_parameter_datatable and len(soil_design_parameter_datatable)>0 and n_clicks > 0:
            df0=pd.DataFrame.from_records(soil_design_parameter_datatable)[:-1]
            df_key_list = list(df0.keys())
            df_key_list.remove('Layer #')
            df_key_list = ['Layer #'] + df_key_list
            df = pd.DataFrame()
            for a in df_key_list:
                try:
                    df[a] = [round(a,0) if type(a) is float else a for a in df0[a]]
                except:
                    pass
        else:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate
        return send_data_frame(df.to_csv, "Soil Design Parameter for  .csv", index=False)
# =============================================================================
# =============================================================================
# =============================================================================
# # # # CPT_point_selection_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def loaded_data_datatables_update_signal_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# =============================================================================
# # # selected_soil_boring_data_datatable_update_signal_callbacks   
# =============================================================================
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(dataset1_selected_soil_boring_data_table_data,
                 dataset1_selected_soil_lithology_data_table_data,
                 dataset1_selected_CPT_data_table_data, 
                 loaded_data_datatable_update_signal_1) {
                     console.log(dash_clientside.callback_context)
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var W2E_fence_plot_loading_hidden_div = [];
                     var S2N_fence_plot_loading_hidden_div = [];
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 }                     
                     if (['dataset1-selected-soil-boring-data-table', 'dataset1-selected-soil-lithology-table', 'dataset1-selected-CPT-data-table'].indexOf(triggered_input_id) > -1) {
                             loaded_data_datatable_update_signal_1=loaded_data_datatable_update_signal_1+1;
                             W2E_fence_plot_loading_hidden_div ="Loading Complete!";
                             S2N_fence_plot_loading_hidden_div ="Loading Complete!";
                            }
                     return [loaded_data_datatable_update_signal_1];                   
                     };
        """,
        [
            Output('loaded-data-datatable-update-signal-1', 'children'),
            ],
        [
            Input('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
            Input('dataset1-selected-soil-lithology-table', 'derived_virtual_data'),
            Input('dataset1-selected-CPT-data-table', 'derived_virtual_data'),
         ],
        [
            State('loaded-data-datatable-update-signal-1', 'children'),
            ],        
        prevent_initial_call=True,
    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # map_point_selection_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def map_point_selection_callbacks(app, cache, Boring_data_dataset1):
    @app.callback(
        [
            Output('dataset1-selected-point-table', 'columns'),
            Output('dataset1-selected-point-table', 'data'),
            Output('dataset1-selected-soil-boring-data-table', 'columns'),
            Output('dataset1-selected-soil-boring-data-table', 'data'),
            Output('dataset1-selected-soil-lithology-table', 'columns'),
            Output('dataset1-selected-soil-lithology-table', 'data'),
            Output('dataset1-selected-CPT-data-table', 'columns'),
            Output('dataset1-selected-CPT-data-table', 'data'),
            Output('dataset1-selected-test-pile-table', 'columns'),
            Output('dataset1-selected-test-pile-table', 'data'),
            Output('dataset1-selected-test-pile-event-data-table', 'columns'),
            Output('dataset1-selected-test-pile-event-data-table', 'data'),
            Output('dataset1-selected-test-pile-static-data-table', 'columns'),
            Output('dataset1-selected-test-pile-static-data-table', 'data'),
            Output('W2E-fence-plot-bar-width-slider', 'min'),
            Output('W2E-fence-plot-bar-width-slider', 'max'),
            Output('W2E-fence-plot-bar-width-slider', 'value'),
            Output('W2E-fence-plot-bar-width-slider', 'step'),
            Output('W2E-fence-plot-bar-width-slider', 'marks'),
            Output('S2N-fence-plot-bar-width-slider', 'min'),
            Output('S2N-fence-plot-bar-width-slider', 'max'),
            Output('S2N-fence-plot-bar-width-slider', 'value'),
            Output('S2N-fence-plot-bar-width-slider', 'step'),
            Output('S2N-fence-plot-bar-width-slider', 'marks'),
            Output('clientside-point-legend-figure-data-store', 'data'),
# =============================================================================
#             Output('load-project-data-button', 'color'),
# =============================================================================
            ],
        [
            Input('map-graph', 'selectedData'),         
            Input('Nkt-value-slider', 'value'),
            Input('CPT-method-select', 'value'),
         ],
        [
            State('map-graph', 'figure'),
            ],        
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=60)
    def map_point_selection_callbacks(
            map_selection_points,
            Nkt_value_slider_value,
            selected_CPT_method,
            map_graph_fig,
            ):
        start_time = time.time()
        ctx = dash.callback_context
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]            
        dataset1_selected_soil_boring_data_table_columns=[]
        dataset1_selected_soil_boring_data_table_data=[]
        dataset1_selected_soil_lithology_data_table_columns=[]
        dataset1_selected_soil_lithology_data_table_data=[]
        dataset1_selected_CPT_data_table_columns=[]
        dataset1_selected_CPT_data_table_data=[]
        dataset1_selected_test_pile_table_columns=[]
        dataset1_selected_test_pile_table_data=[]        
        dataset1_selected_test_pile_event_data_table_columns=[]
        dataset1_selected_test_pile_event_data_table_data=[]        
        dataset1_selected_test_pile_static_data_table_columns=[]
        dataset1_selected_test_pile_static_data_table_data=[]        
        if map_selection_points and map_selection_points['points']:
            selected_point_list_df = pd.DataFrame.from_dict(map_selection_points['points'])#.dropna(subset=['hovertext'])
            selected_point_list_df=selected_point_list_df[pd.isnull(selected_point_list_df['text'])==False]
            selected_point_list_df.reset_index(drop=True, inplace=True)
# =============================================================================
#             print(selected_point_list_df)
# =============================================================================
# =============================================================================
#             selected_point_list_df["Project Number"] = [a.split('<br>')[[i for i, s in enumerate(a.split('<br>')) if 'Project Number: ' in s][0]].replace('Project Number: ', '') for a in selected_point_list_df['hovertext']]
#             selected_point_list_df["Ground Elevation"] = [a.split('<br>')[[i for i, s in enumerate(a.split('<br>')) if 'Ground Elevation (ft.): ' in s][0]].replace('Ground Elevation (ft.): ', '') for a in selected_point_list_df['hovertext']] 
# =============================================================================
            project_data_combined_column_names_sort_order = [
                "Client",
                'Lead Project',
                'Name',
                'Number',
                'Purpose',
                ]
            point_data_combined_column_names_sort_order = [
                "Project Number",
                'Location ID',
                'Location Type',
                'Elevation',
                'Final Depth',
                'Latitude Decimal','Longitude Decimal',
                ]
            soil_boring_data_combined_column_names_sort_order = [
                                                'Project Number',
                                                'Location ID',
                                                #'Latitude Decimal','Longitude Decimal','Northing','Easting', 'Elevation',
                                                'Sample Reference','Type',
                                                'Depth Top','Depth Base','Elevation Top','Elevation Base',
                                                'Legend Code',
                                                'Recovery Length',
                                                'RQD Length',
                                                'Blows Seating 1','Blows Main 1','Blows Main 2','SPT N',
                                                'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                                                'Total Unit Weight','Dry Density',
                                                'Test Type','Failure Mode','Chamber Pressure','Compressive Strength','Undrained Shear Strength',
                                                'Percentage Passing at 0_075',
                                                'USCS Symbol','USCS Group Name',
                                                'AASHTO Classification',
                                                'Specific Gravity',
                                                ]
            soil_lithology_combined_column_names_sort_order = [
                'Project Number',
                'Location ID',
                #'Latitude Decimal','Longitude Decimal','Northing','Easting','Elevation',
                'Depth Top', 'Depth Base',
                'Elevation Top','Elevation Base',
                'Legend Code','Additional Description',
                'Percent Gravel','Percent Sand','Percent Fines',
                ]            
            CPT_data_combined_column_names_sort_order = [
                'Project Number',
                'Location ID',
                #'Latitude Decimal','Longitude Decimal',
                'Depth Top', 'Depth Base',
                'Elevation Top','Elevation Base',
                'SBTn Description',#'SBTn',
                'SBT Description',#'SBTn',
                'fs','qc','u2',
                #'qt', 
                'Rf (%)', 'Fr (%)',
                'Estimated Total Unit Weight (pcf)',
                #'Effective Vertical Stress (tsf)',
                #'Total Vertical Stress (tsf)',
                'Su (psf), Nkt',
                "Probabilistic Soil Classification",
                "PSC Clay, %",
                "PSC Silt, %",
                "PSC Sand, %",
                ]
            test_pile_combined_column_names_sort_order = [
                'Project Number',
                'Location ID',
                'Latitude Decimal','Longitude Decimal',
                'Test Pile Category',
                'Test Pile Type ID',
                'Elastic Modulus, ksi',
                'Hammer ID',
                'Pile Length, ft',
                'EOD Tip Elevation, ft',
                'Design Tip Elevation, ft',
                'Soil Type At Tip',
                'Casing Elevation, ft',
                'Cutoff Elevation, ft',
                'Splice Elevation, ft',
                'Scour Elevation, ft',
                'Target Load, tonf',
                'Design Load, tonf',
                'Factored Load, tonf', 
                'Resistance Factor, tonf',
                'Setup Factor',
                'Blow Count End of Initial Drive',
                'Stroke End of Initial Drive, ft',
                'Instrumented',
                'Pile Spliced',
                'End Of Drive Notes',
                'Designer',
                ]
            test_pile_event_data_combined_column_names_sort_order = [
                'Project Number',
                'Location ID',
                #'Latitude Decimal','Longitude Decimal',
                'Event Type',
                'Elapsed Time, hr',
                'Blow Count Average',
                'Stroke, ft',
                'Hammer Energy, kip-ft',
                'Elevation Pile Tip EOD, ft',
                'Capacity Ultimate, tonf',
                'Capacity Skin Friction, tonf',
                'Capacity End Bearing, tonf',
                'Full Capacity Mobilized',
                'Match Quality',
                'JRx',
                'Interpretation Notes',
                'Ultimate Capacity Method',
                'Test Date',
                ]            
            test_pile_static_data_combined_column_names_sort_order = [
                'Project Number',
                'Location ID',
                #'Latitude Decimal','Longitude Decimal',
                'Load, t',
                'Deflection, in',
                'Elapsed Time, min',
                'Test Date',
                ]      
            data_dict_list = [Boring_data_dataset1, Boring_data_dataset1, Boring_data_dataset1, Boring_data_dataset1]
            selected_point_location_ID = selected_point_list_df['text'].tolist()
            collection_name_list = ["POINT", 'SOIL SAMPLES', 'LITHOLOGY SOIL', 'CPT DATA', 
                                    #"Test Pile", "Test Pile Event Data", "Test Pile Static Data",
                                    ]
            combined_column_names_sort_order_list = [
                point_data_combined_column_names_sort_order,
                soil_boring_data_combined_column_names_sort_order,
                soil_lithology_combined_column_names_sort_order,
                CPT_data_combined_column_names_sort_order,
# =============================================================================
#                                                      test_pile_combined_column_names_sort_order,
#                                                      test_pile_event_data_combined_column_names_sort_order,
#                                                      test_pile_static_data_combined_column_names_sort_order,
# =============================================================================
                                                     ]
            for i in range(0,len(collection_name_list)):
                selected_point_data_table_columns,  selected_point_data_table_data = map_point_selection_func(data_dict_list[i],
                                                                                      selected_point_location_ID,
                                                                                      combined_column_names_sort_order_list[i],
                                                                                      collection_name_list[i])
                if collection_name_list[i] =='POINT' and len(selected_point_data_table_data)>0:
                    dataset1_selected_point_data_table_columns = [a for a in selected_point_data_table_columns]
                    dataset1_selected_point_data_table_data = [a for a in selected_point_data_table_data]
                elif collection_name_list[i] =='SOIL SAMPLES' and len(selected_point_data_table_data)>0:
                    dataset1_selected_soil_boring_data_table_columns = [a for a in selected_point_data_table_columns]
                    dataset1_selected_soil_boring_data_table_data = [a for a in selected_point_data_table_data]
# add Point Color Code:
                    df = pd.DataFrame.from_dict(dataset1_selected_soil_boring_data_table_data)
                    unique_location_ID_list = list(df['Location ID'].drop_duplicates(keep='first'))
                    color_code_list =[]
                    for i in range(0,len(unique_location_ID_list)):
                        for j in range(0,len(selected_point_list_df)):
                            if unique_location_ID_list[i] == selected_point_location_ID[j]:
                                temp = [selected_point_list_df['customdata'].tolist()[j]]*len(df[df["Location ID"] == unique_location_ID_list[i]])
                                color_code_list += temp
                    df['Point Color Code'] = [a for a in color_code_list]
                    dataset1_selected_soil_boring_data_table_data = df.to_dict(orient='records')
                    dataset1_selected_soil_boring_data_table_columns= dataset1_selected_soil_boring_data_table_columns + [{"name": 'Point Color Code', "id": 'Point Color Code'}]
                elif collection_name_list[i] =='LITHOLOGY SOIL' and len(selected_point_data_table_data)>0:
                    dataset1_selected_soil_lithology_data_table_columns = [a for a in selected_point_data_table_columns]
                    dataset1_selected_soil_lithology_data_table_data = [a for a in selected_point_data_table_data]
                elif collection_name_list[i] =='CPT DATA' and len(selected_point_data_table_data)>0:
                    dataset1_selected_CPT_data_table_columns = [a for a in selected_point_data_table_columns]
                    dataset1_selected_CPT_data_table_data = [a for a in selected_point_data_table_data]
# =============================================================================
#                 elif collection_name_list[i] =='Test Pile':
#                     dataset1_selected_test_pile_table_columns = [a for a in selected_point_data_table_columns]
#                     dataset1_selected_test_pile_table_data = [a for a in selected_point_data_table_data]
# 
#                 elif collection_name_list[i] =='Test Pile Event Data':
#                     dataset1_selected_test_pile_event_data_table_columns = [a for a in selected_point_data_table_columns]
#                     dataset1_selected_test_pile_event_data_table_data = [a for a in selected_point_data_table_data]
# 
#                 elif collection_name_list[i] =='Test Pile Static Data':
#                     dataset1_selected_test_pile_static_data_table_columns = [a for a in selected_point_data_table_columns]
#                     dataset1_selected_test_pile_static_data_table_data = [a for a in selected_point_data_table_data]
# =============================================================================
# change Nkt for CPT-Su correlations:
            for i in range(0, len(dataset1_selected_CPT_data_table_data)):
                if "Su (psf), Nkt, Original" in dataset1_selected_CPT_data_table_data[i].keys():
                    dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = round(dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt, Original"]*18/Nkt_value_slider_value,0)
                if selected_CPT_method == "SBTn":
                    if "SBTn Description" in dataset1_selected_CPT_data_table_data[i].keys() and dataset1_selected_CPT_data_table_data[i]["SBTn Description"][0] in ["1" , "2", "3", "4"]:
                        dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = int(dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"])
                    else:
                        dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = float("NaN") 
                elif selected_CPT_method == "SBT":
                    if "SBTn Description" in dataset1_selected_CPT_data_table_data[i].keys() and dataset1_selected_CPT_data_table_data[i]["SBT Description"][0] in ["1" , "2", "3", "4"]:
                        dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = int(dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"])
                    else:
                        dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = float("NaN") 
                elif "PSC Silt, %" in dataset1_selected_CPT_data_table_data[i].keys() and "PSC Clay, %" in dataset1_selected_CPT_data_table_data[i].keys() and selected_CPT_method == "PSC":
                    if dataset1_selected_CPT_data_table_data[i]["PSC Silt, %"] + dataset1_selected_CPT_data_table_data[i]["PSC Clay, %"] >= 80:
                        dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = int(dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"])
                    else:
                        dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = float("NaN") 
                else:
                    dataset1_selected_CPT_data_table_data[i]["Su (psf), Nkt"] = float("NaN") 
            dataset1_selected_CPT_data_table_columns = [{"name": 'Su (psf), Nkt='+str(Nkt_value_slider_value), "id": "Su (psf), Nkt" } if x=={"name": "Su (psf), Nkt", "id": "Su (psf), Nkt"} else x for x in dataset1_selected_CPT_data_table_columns]
# =============================================================================
#             if triggered_input_id=='Nkt-value-slider':
#                 for i in range(0, len(dataset1_selected_CPT_data_table_data)):
#                     if "Su (psf)" in dataset1_selected_CPT_data_table_data[i].keys():
#                         dataset1_selected_CPT_data_table_data[i]["Su (psf)"] = round(dataset1_selected_CPT_data_table_data[i]["Su (psf)"]*18/Nkt_value_slider_value,0)
#                 
#                 dataset1_selected_CPT_data_table_columns = [{"name": 'Su (psf), Nkt='+str(Nkt_value_slider_value), "id": "Su (psf)" } if x=={"name": "Su (psf)", "id": "Su (psf)"} else x for x in dataset1_selected_CPT_data_table_columns]
#             else:
#                 dataset1_selected_CPT_data_table_columns = [{"name": 'Su (psf), Nkt=18', "id": "Su (psf), SBTn" } if x=={"name": "Su (psf)", "id": "Su (psf)"} else x for x in dataset1_selected_CPT_data_table_columns]
# =============================================================================
            if len(selected_point_list_df['lon']) > 0:
# =============================================================================
# =============================================================================
# # # W2E-fence-plot-bar-width-slider:
# =============================================================================
# =============================================================================
                selected_lon_list = np.unique(selected_point_list_df['lon'])
                W2E_fence_plot_bar_width_slider_min = (max(selected_lon_list)-min(selected_lon_list))/200
                W2E_fence_plot_bar_width_slider_max = W2E_fence_plot_bar_width_slider_min*10
                W2E_fence_plot_bar_width_slider_value = W2E_fence_plot_bar_width_slider_min*4
                W2E_fence_plot_bar_width_slider_step = W2E_fence_plot_bar_width_slider_min*1
                W2E_fence_plot_bar_width_slider_marks= {a*W2E_fence_plot_bar_width_slider_step: {'label': str(a)} for a in range(1,11,2)}
# =============================================================================
# =============================================================================
# # # S2N-fence-plot-bar-width-slider:
# =============================================================================
# =============================================================================
                selected_lat_list = np.unique(selected_point_list_df['lat'])
                S2N_fence_plot_bar_width_slider_min = (max(selected_lat_list)-min(selected_lat_list))/200
                S2N_fence_plot_bar_width_slider_max = S2N_fence_plot_bar_width_slider_min*10
                S2N_fence_plot_bar_width_slider_value = S2N_fence_plot_bar_width_slider_min*4
                S2N_fence_plot_bar_width_slider_step = S2N_fence_plot_bar_width_slider_min*1
                S2N_fence_plot_bar_width_slider_marks= {a*S2N_fence_plot_bar_width_slider_step: {'label': str(a)} for a in range(1,11,2)}
                point_list_legend_data = point_list_legend_func(selected_point_list_df)
            else:
                # PreventUpdate prevents ALL outputs updating
                raise dash.exceptions.PreventUpdate  
        else:
            # PreventUpdate prevents ALL outputs updating
            raise dash.exceptions.PreventUpdate  
        print("map_point_selection_callbacks --- %s seconds ---" % (time.time() - start_time))
        return (
            dataset1_selected_point_data_table_columns,
            dataset1_selected_point_data_table_data,
            dataset1_selected_soil_boring_data_table_columns,
            dataset1_selected_soil_boring_data_table_data,
            dataset1_selected_soil_lithology_data_table_columns,
            dataset1_selected_soil_lithology_data_table_data,
            dataset1_selected_CPT_data_table_columns,
            dataset1_selected_CPT_data_table_data,
            dataset1_selected_test_pile_table_columns,
            dataset1_selected_test_pile_table_data,      
            dataset1_selected_test_pile_event_data_table_columns,
            dataset1_selected_test_pile_event_data_table_data,        
            dataset1_selected_test_pile_static_data_table_columns,
            dataset1_selected_test_pile_static_data_table_data, 
            W2E_fence_plot_bar_width_slider_min,
            W2E_fence_plot_bar_width_slider_max,
            W2E_fence_plot_bar_width_slider_value,
            W2E_fence_plot_bar_width_slider_step,
            W2E_fence_plot_bar_width_slider_marks,
            S2N_fence_plot_bar_width_slider_min,
            S2N_fence_plot_bar_width_slider_max,
            S2N_fence_plot_bar_width_slider_value,
            S2N_fence_plot_bar_width_slider_step,
            S2N_fence_plot_bar_width_slider_marks,
            point_list_legend_data,
                )
# =============================================================================
# # Update fence graph:
# =============================================================================
    app.clientside_callback(
        """
        function(data, figure) {
            if (data !== 'undefined' && data.length >0) {
                    return [{'data': data, 'layout': figure.layout}]
                             }
        }
        """,
        [Output('point-legend-graph', 'figure')],
        Input('clientside-point-legend-figure-data-store', 'data'),            
        State('point-legend-graph', 'figure'),                 
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # S2N_fence_plot_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def S2N_fence_plot_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# # Update generate graph button:
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 loaded_data_datatable_update_signal_1,
                 S2N_fence_graph_fig, 
                 S2N_fence_graph_fig_bar_width,
                 selected_CPT_method,
                 ) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var fence_graph_data = []
                     var generate_S2N_fence_plot_button_color = 'success'
                     var generate_S2N_fence_plot_button_children = 'Generate Graph'
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 } 
                     if (S2N_fence_graph_fig['data'] !== 'undefined' &&
                         S2N_fence_graph_fig['data'].length >0 &&
                         triggered_input_id == 'S2N-fence-graph') {
                             generate_S2N_fence_plot_button_color = 'success';
                             generate_S2N_fence_plot_button_children = 'Generate Graph (Updated)';
                             } else if (loaded_data_datatable_update_signal_1 > 1 ||
                                        triggered_input_id=='S2N-fence-plot-bar-width-slider') {
                                            generate_S2N_fence_plot_button_color = 'danger';
                                            generate_S2N_fence_plot_button_children = 'Generate Graph (Outdated)';
                                 } else {
                                     generate_S2N_fence_plot_button_color = 'success';
                                     generate_S2N_fence_plot_button_children = 'Generate Graph';
                                     }
                     return [generate_S2N_fence_plot_button_children, 
                             generate_S2N_fence_plot_button_color,
                             ]
                     }  
        """,  
        [
            Output('generate-S2N-fence-plot-button', 'children'),
            Output('generate-S2N-fence-plot-button', 'color'),
            ],
        [
            Input('generate-S2N-fence-plot-button', 'n_clicks'),
            Input('loaded-data-datatable-update-signal-1', 'children'),
            Input('S2N-fence-graph', 'figure'),
            Input('S2N-fence-plot-bar-width-slider', 'value'), 
            Input('CPT-method-select', 'value'),
            ],
        prevent_initial_call=True,
        )
# =============================================================================
# # Update clientside-S2N-fence-figure-store data:
# =============================================================================
    @app.callback(
        [
            Output('clientside-S2N-fence-figure-store', 'data'),            
            Output('S2N-fence-clientside-store-loading-hidden-div', 'children'),
            ],
        [
            Input('generate-S2N-fence-plot-button', 'n_clicks'),         
            Input('S2N-fence-plot-text-size-slider', 'value'),         
            ],
        [
            State('S2N-fence-plot-bar-width-slider', 'value'),       
            State('map-graph', 'selectedData'), 
            State('dataset1-selected-soil-lithology-table', 'derived_virtual_data'),         
            State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
            State('dataset1-selected-CPT-data-table', 'derived_virtual_data'),         
            State('dataset1-selected-test-pile-table', 'derived_virtual_data'),         
            State('S2N-fence-graph', 'figure'),
            State('CPT-method-select', 'value'),
         ],
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=TIMEOUT)
    def S2N_fence_plot_callbacks(
            n_clicks,
            S2N_fence_graph_fig_text_size,
            S2N_fence_graph_fig_bar_width,
            map_selection_points,
            dataset1_selected_soil_lithology_data_table_data,
            dataset1_selected_soil_boring_data_table_data,
            dataset1_selected_CPT_data_table_data,            
            dataset1_selected_test_pile_data_table_data,            
            S2N_fence_graph_fig,
            selected_CPT_method,
            ):
        ctx = dash.callback_context
        fence_graph_fig_text_size = S2N_fence_graph_fig_text_size
        fence_graph_fig_bar_width = S2N_fence_graph_fig_bar_width
        fence_graph_fig = S2N_fence_graph_fig
        x_axis_key_name4bars = 'Latitude Decimal'
        x_axis_key_name4ID_and_elevation_line = 'lat'
        fence_graph_direction = 'S2N'
        data = fence_plot_func(
            ctx,
            fence_graph_fig_text_size, 
            fence_graph_fig_bar_width,
            map_selection_points,
            dataset1_selected_soil_lithology_data_table_data,
            dataset1_selected_soil_boring_data_table_data,
            dataset1_selected_CPT_data_table_data,
            dataset1_selected_test_pile_data_table_data,
            fence_graph_fig,
            x_axis_key_name4bars,
            x_axis_key_name4ID_and_elevation_line,
            fence_graph_direction,
            selected_CPT_method,
                        )
        S2N_fence_clientside_store_loading_hidden_div ="Loading Complete!"
# =============================================================================
#         print(data)
# =============================================================================
        if data is not None and len(data) > 0:
            return [data, S2N_fence_clientside_store_loading_hidden_div]
        else:
            raise dash.exceptions.PreventUpdate  
# =============================================================================
# # Update fence graph:
# =============================================================================
    app.clientside_callback(
        """
        function(data, figure) {
            return [{'data': data, 'layout': figure.layout}]
        }
        """,
        [Output('S2N-fence-graph', 'figure')],
        Input('clientside-S2N-fence-figure-store', 'data'),            
        State('S2N-fence-graph', 'figure'),                 
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # soil_design_parameter_datatable_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def soil_design_parameter_datatable_callbacks(app, cache):
    TIMEOUT=200
    design_profile_name_list_A = ['Design Profile A' + str(a) for a in list(range(1,6))]
    design_profile_name_list_B = ['Design Profile B' + str(a) for a in list(range(1,6))]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update soil-parameters4design-select :
# =============================================================================
# =============================================================================
# =============================================================================
    for i in range(0, len(design_profile_name_list_B)):
        @app.callback(
            [
            Output(design_profile_name_list_B[i].replace(" ", "-") + '-design-line-checkbox', 'checked'),         
            Output(design_profile_name_list_B[i].replace(" ", "-") + '-design-line-checkbox-label', 'children'),         
                ],
            [Input(design_profile_name_list_A[i].replace(" ", "-") + '-clientside-store-loading-hidden-div', 'children')],
            [State(design_profile_name_list_A[i].replace(" ", "-").replace(" ", "-") + '-x-axis-parameter-select', 'value')],
    # https://dash.plotly.com/advanced-callbacks#prevent-callbacks-from-being-executed-on-initial-load        
            prevent_initial_call=True,
            )
        @cache.memoize(timeout=TIMEOUT)
        def design_profile_callbacks(
                design_profile_A_update_signial,    
                design_profile_A_x_axis,
                ):
                default_activation_list = [
                    'Total Unit Weight', 'Dry Density', 
                    'Compressive Strength', 'Undrained Shear Strength',
                    'SPT N',
                    ]
                design_line_checkbox = True
                design_line_checkbox_label = design_profile_A_x_axis.replace('Percentage Passing at 0_075', '#200 Finer')
                if design_profile_A_x_axis not in default_activation_list:
                    design_line_checkbox = False
                return [design_line_checkbox, design_line_checkbox_label]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # soil_design_parameter_datatable_callbacks:
# =============================================================================
# =============================================================================
# =============================================================================
    @app.callback(
        [
            Output('soil-design-parameter-datatable', 'data'),            
            Output('soil-design-parameter-datatable', 'columns'),            
            ],
        [Input(a.replace(" ", "-") + '-design-line-checkbox', 'checked') for a in design_profile_name_list_B] +
        [Input(a.replace(" ", "-") + '-baseline-design-parameters-select', 'value') for a in design_profile_name_list_B],
        [State(a.replace(" ", "-") + '-design-line-checkbox-label', 'children') for a in design_profile_name_list_B] + 
        [State(a.replace(" ", "-") + '-clientside-figure-data-store', 'data') for a in design_profile_name_list_A] + 
        [
            State('design-layer-datatable', 'data'), 
            State('design-layer-datatable', 'columns'), 
            ],
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=TIMEOUT)
    def soil_design_parameter_datatable_callbacks(
            soil_parameter_check_1,
            soil_parameter_check_2,
            soil_parameter_check_3,
            soil_parameter_check_4,
            soil_parameter_check_5,
            baseline_case_1,
            baseline_case_2,
            baseline_case_3,
            baseline_case_4,
            baseline_case_5,
            soil_parameter_name_1,            
            soil_parameter_name_2,            
            soil_parameter_name_3,            
            soil_parameter_name_4,            
            soil_parameter_name_5,            
            design_profile_A_fig_data_1,
            design_profile_A_fig_data_2,
            design_profile_A_fig_data_3,
            design_profile_A_fig_data_4,
            design_profile_A_fig_data_5,
            design_layer_datatable_data,
            design_layer_datatable_columns,
            ):
        ctx = dash.callback_context
        if not ctx.triggered:
            triggered_input_id = []
        else:
            triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        data = design_layer_datatable_data
        columns = [{"name": 'Layer #', "id": 'Layer #', 'editable': False}]
        columns += design_layer_datatable_columns
        columns_name_list = [a['name'] for a in columns]
        for i in range(0, len(design_profile_name_list_B)):
            if vars()['soil_parameter_check_' + str(i+1)] == True:
                if vars()['soil_parameter_name_' + str(i+1)] not in columns_name_list:
                    columns += [{"name": vars()['soil_parameter_name_' + str(i+1)], "id": vars()['soil_parameter_name_' + str(i+1)].replace('#200 Finer', 'Percentage Passing at 0_075'), "type": 'numeric', 'format': Format(precision=2, scheme=Scheme.decimal_integer), 'editable': True}]
                    fig_trace_name_list = [a['name'] for a in vars()['design_profile_A_fig_data_' + str(i+1)]]
                    if vars()['baseline_case_' + str(i+1)] + ' Text' in fig_trace_name_list:
                        fig_trace_idx4baseline = fig_trace_name_list.index(vars()['baseline_case_' + str(i+1)] + ' Text')
                        design_parameter_list4baseline = vars()['design_profile_A_fig_data_' + str(i+1)][fig_trace_idx4baseline]['customdata']+[None]
                        data=pd.DataFrame.from_records(data)
                        data[vars()['soil_parameter_name_' + str(i+1)].replace('#200 Finer', 'Percentage Passing at 0_075')] = design_parameter_list4baseline
                        data['Layer #'] = list(range(1,len(data))) + [np.nan]
                        data = data.to_dict(orient='records')
        return [data, columns]
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Update generate graph button:
# =============================================================================
# =============================================================================
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 soil_design_parameter_datatable,
                 ) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var finalize_design_profile_button_color = 'success'
                     var finalize_design_profile_button_children = 'Finalize Design Profiles'
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 } 
                     if (['finalize-design-profile-button'].includes(triggered_input_id) == true) {
                             finalize_design_profile_button_color = 'success';
                             finalize_design_profile_button_children = 'Finalize Design Profiles (Updated)';
                             } else if (['soil-design-parameter-datatable'].includes(triggered_input_id) == true) {
                                            finalize_design_profile_button_color = 'danger';
                                            finalize_design_profile_button_children = 'Finalize Design Profiles (Outdated)';
                                 } else {
                                     finalize_design_profile_button_color = 'success';
                                     finalize_design_profile_button_children = 'Finalize Design Profiles';
                                     }
                     return [finalize_design_profile_button_children, 
                             finalize_design_profile_button_color,
                             ]
                     }  
        """,  
        [
            Output('finalize-design-profile-button', 'children'),
            Output('finalize-design-profile-button', 'color'),
            ],
        [
            Input('finalize-design-profile-button', 'n_clicks'),
            Input('soil-design-parameter-datatable', 'data'),            
            ],
        prevent_initial_call=True,
        )
# =============================================================================
# # Update composite-design-stratification-graph-B:
# =============================================================================
    app.clientside_callback(
        """
        function(data, layout) {
            if (data !== 'undefined') {
                    return [{'data': data, 'layout': layout}]
                             } else {
                                 return [{'data': [], 'layout': layout}]
                                 }
        }
        """,
        [Output('composite-design-stratification-graph-B', 'figure')],
        Input('composite-design-stratification-clientside-figure-data-store-A', 'data'),            
        Input('composite-design-stratification-clientside-figure-layout-store-A', 'data'),            
        prevent_initial_call=True,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # design_profiles_B_callbacks:
# =============================================================================
# =============================================================================
# =============================================================================
    for i in range(0, len(design_profile_name_list_B)):
        @app.callback(
            [
                Output(design_profile_name_list_B[i].replace(" ", "-") + '-clientside-figure-data-store', 'data'),            
                Output(design_profile_name_list_B[i].replace(" ", "-") + '-clientside-figure-layout-store', 'data'),            
                Output(design_profile_name_list_B[i].replace(" ", "-") + '-clientside-store-loading-hidden-div', 'children'),
                ],
            [
                Input('finalize-design-profile-button', 'n_clicks'),
                Input('water-level-elevation-input', 'value'),         
                Input('Su-over-p-ratio-range-slider', 'value'),         
                ],
            [
                State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
                State(design_profile_name_list_B[i].replace(" ", "-") + '-data-profile-graph', 'figure'),
                State('soil-design-parameter-datatable', 'data'),            
                State(design_profile_name_list_A[i].replace(" ", "-") + '-x-axis-parameter-select', 'value'),         
                ],
    # https://dash.plotly.com/advanced-callbacks#prevent-callbacks-from-being-executed-on-initial-load        
            prevent_initial_call=True,
            )
        @cache.memoize(timeout=TIMEOUT)
        def design_profiles_B_callbacks(
                finalize_design_profile_n_clicks,
                water_level_elevation,
                Su_over_p_ratio_range_slider_value_list,
                dataset1_selected_soil_boring_data_table_data,
                design_profile_fig,
                soil_design_parameter_datatable_data,
                x_axis_parameter_select,
                ):
            ctx = dash.callback_context
            if not ctx.triggered:
                triggered_input_id = []
            else:
                triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0]
            data = design_profile_fig['data']
            layout = design_profile_fig['layout']
            design_profile_clientside_store_loading_hidden_div = ""
            #x_axis_parameter_select = x_axis_parameter_select.replace('Percentage Passing at 0_075', '#200 Finer')
            soil_design_parameter_datatable_data=pd.DataFrame.from_records(soil_design_parameter_datatable_data)
            if soil_design_parameter_datatable_data['Top Elevation'][len(soil_design_parameter_datatable_data)-1] == "":
                soil_design_parameter_datatable_data = soil_design_parameter_datatable_data.iloc[:-1].copy()            
            if "" not in list(soil_design_parameter_datatable_data['Top Elevation'][:-1]):
                design_line_elevation = soil_design_parameter_datatable_data["Top Elevation"].tolist() + [soil_design_parameter_datatable_data["Base Elevation"].tolist()[-1]]
                design_soil_types = soil_design_parameter_datatable_data["Soil Type"].tolist() + [None]
                soil_design_values = None
                if x_axis_parameter_select in soil_design_parameter_datatable_data.keys():
                    soil_design_values = soil_design_parameter_datatable_data[x_axis_parameter_select].tolist() + [None]
                x_axis_parameter = x_axis_parameter_select
                x_axis_parameter_unit = ''
                design_profile_fig_layout = design_profile_fig['layout']
# =============================================================================
# =============================================================================
# =============================================================================
# # # # update design profiles:            
# =============================================================================
# =============================================================================
# =============================================================================
                if triggered_input_id in ['finalize-design-profile-button']:            
                    if x_axis_parameter in ['Moisture Content', 'Percentage Passing at 0_075']:
                        x_axis_parameter_unit = '%'
                    elif x_axis_parameter in ['Total Unit Weight', 'Dry Density']:
                        x_axis_parameter_unit = 'pcf.'
                    elif x_axis_parameter in ['Compressive Strength', 'Undrained Shear Strength']:
                        x_axis_parameter_unit = 'psf.'
                    elif x_axis_parameter in ['SPT N']:
                        x_axis_parameter_unit = 'blows/ft.'
                    else: 
                        x_axis_parameter_unit = ''
                    # design_profile_fig_text_size = design_profile_fig_text_size
                    dataset1_selected_CPT_data_table_data = None
                    data,layout = update_design_profile_func(
                        # design_profile_fig_text_size, 
                        dataset1_selected_soil_boring_data_table_data,
                        dataset1_selected_CPT_data_table_data,
                        design_profile_fig_layout,
                        x_axis_parameter,
                        x_axis_parameter_unit,
                        design_line_elevation,
                        design_soil_types,                        
                        water_level_elevation,
                                    )
                    if soil_design_values is not None and len(soil_design_values)>0:
                        data = finalize_design_lines_func(
                            data,
                            design_line_elevation,
                            design_soil_types,
                            soil_design_values,
                            )
                if (triggered_input_id in ['Su-over-p-ratio-range-slider', 'finalize-design-profile-button'] and 
                    x_axis_parameter == 'Undrained Shear Strength' and 
                    'Total Unit Weight' in list(soil_design_parameter_datatable_data.keys())):
                    design_bulk_density_list = soil_design_parameter_datatable_data["Total Unit Weight"].tolist() + [None]
                    data = update_Su_over_p_lines_in_design_profile_func(
                        design_profile_fig_layout,
                        data,
                        design_line_elevation,
                        design_soil_types,
                        design_bulk_density_list,
                        Su_over_p_ratio_range_slider_value_list,
                        water_level_elevation,
                        )
                design_profile_clientside_store_loading_hidden_div ="Loading Complete!"
# =============================================================================
#                     return [data, layout, design_profile_clientside_store_loading_hidden_div]
# =============================================================================
            return [data, layout, design_profile_clientside_store_loading_hidden_div]
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # Update design profiles B:
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
        app.clientside_callback(
            """
            function(data, layout) {
                if (data !== 'undefined') {
                        return [{'data': data, 'layout': layout}]
                                 } else {
                                     return [{'data': [], 'layout': layout}]
                                     }
            }
            """,
            [Output(design_profile_name_list_B[i].replace(" ", "-") + '-data-profile-graph', 'figure')],
            Input(design_profile_name_list_B[i].replace(" ", "-") + '-clientside-figure-data-store', 'data'),            
            Input(design_profile_name_list_B[i].replace(" ", "-") + '-clientside-figure-layout-store', 'data'),            
            prevent_initial_call=True,
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # W2E_fence_plot_callbacks:    
# =============================================================================
# =============================================================================
# =============================================================================
def W2E_fence_plot_callbacks(app, cache):
    TIMEOUT=200
# =============================================================================
# # Update generate graph button:
# =============================================================================
#client side implementation
    app.clientside_callback(
        """
        function(n_clicks,
                 loaded_data_datatable_update_signal_1,
                 W2E_fence_graph_fig, 
                 W2E_fence_graph_fig_bar_width,
                 selected_CPT_method,
                 ) {
                     var ctx =  dash_clientside.callback_context;
                     var triggered_input_id = [];
                     var fence_graph_data = []
                     var generate_W2E_fence_plot_button_color = 'success'
                     var generate_W2E_fence_plot_button_children = 'Generate Graph'
                     if (typeof ctx.triggered[0] !== 'undefined') {
                             triggered_input_id = ctx.triggered[0]['prop_id'].split('.')[0];
                             } else {
                                 riggered_input_id = [];
                                 } 
                     if (W2E_fence_graph_fig['data'] !== 'undefined' &&
                         W2E_fence_graph_fig['data'].length >0 &&
                         triggered_input_id == 'W2E-fence-graph') {
                             generate_W2E_fence_plot_button_color = 'success';
                             generate_W2E_fence_plot_button_children = 'Generate Graph (Updated)';
                             } else if (loaded_data_datatable_update_signal_1 > 1 ||
                                        triggered_input_id=='W2E-fence-plot-bar-width-slider') {
                                            generate_W2E_fence_plot_button_color = 'danger';
                                            generate_W2E_fence_plot_button_children = 'Generate Graph (Outdated)';
                                 } else {
                                     generate_W2E_fence_plot_button_color = 'success';
                                     generate_W2E_fence_plot_button_children = 'Generate Graph';
                                     }
                     return [generate_W2E_fence_plot_button_children, 
                             generate_W2E_fence_plot_button_color,
                             ]
                     }  
        """,  
        [
            Output('generate-W2E-fence-plot-button', 'children'),
            Output('generate-W2E-fence-plot-button', 'color'),
            ],
        [
            Input('generate-W2E-fence-plot-button', 'n_clicks'),
            Input('loaded-data-datatable-update-signal-1', 'children'),
            Input('W2E-fence-graph', 'figure'),
            Input('W2E-fence-plot-bar-width-slider', 'value'), 
            Input('CPT-method-select', 'value'),
            ],
        prevent_initial_call=True,
        )
# =============================================================================
# # Update clientside-W2E-fence-figure-store data:
# =============================================================================
    @app.callback(
        [
            Output('clientside-W2E-fence-figure-store', 'data'),            
            Output('W2E-fence-clientside-store-loading-hidden-div', 'children'),
            ],
        [
            Input('generate-W2E-fence-plot-button', 'n_clicks'),         
            Input('W2E-fence-plot-text-size-slider', 'value'),         
            ],
        [
            State('W2E-fence-plot-bar-width-slider', 'value'),       
            State('map-graph', 'selectedData'), 
            State('dataset1-selected-soil-lithology-table', 'derived_virtual_data'),         
            State('dataset1-selected-soil-boring-data-table', 'derived_virtual_data'),         
            State('dataset1-selected-CPT-data-table', 'derived_virtual_data'),         
            State('dataset1-selected-test-pile-table', 'derived_virtual_data'),         
            State('W2E-fence-graph', 'figure'),
            State('CPT-method-select', 'value'),
         ],
        prevent_initial_call=True,
        )
    @cache.memoize(timeout=TIMEOUT)
    def W2E_fence_plot_callbacks(
            n_clicks,
            W2E_fence_graph_fig_text_size,
            W2E_fence_graph_fig_bar_width,
            map_selection_points,
            dataset1_selected_soil_lithology_data_table_data,
            dataset1_selected_soil_boring_data_table_data,
            dataset1_selected_CPT_data_table_data,            
            dataset1_selected_test_pile_data_table_data,            
            W2E_fence_graph_fig,
            selected_CPT_method,
            ):
        ctx = dash.callback_context
        fence_graph_fig_text_size = W2E_fence_graph_fig_text_size
        fence_graph_fig_bar_width = W2E_fence_graph_fig_bar_width
        fence_graph_fig = W2E_fence_graph_fig
        x_axis_key_name4bars = 'Longitude Decimal'
        x_axis_key_name4ID_and_elevation_line = 'lon'
        fence_graph_direction = 'W2E'
        data = fence_plot_func(
            ctx,
            fence_graph_fig_text_size, 
            fence_graph_fig_bar_width,
            map_selection_points,
            dataset1_selected_soil_lithology_data_table_data,
            dataset1_selected_soil_boring_data_table_data,
            dataset1_selected_CPT_data_table_data,
            dataset1_selected_test_pile_data_table_data,
            fence_graph_fig,
            x_axis_key_name4bars,
            x_axis_key_name4ID_and_elevation_line,
            fence_graph_direction,
            selected_CPT_method,
                        )
        W2E_fence_clientside_store_loading_hidden_div ="Loading Complete!"
# =============================================================================
#         print(data)
# =============================================================================
        if data is not None and len(data) > 0:
            return [data, W2E_fence_clientside_store_loading_hidden_div]
        else:
            raise dash.exceptions.PreventUpdate  
# =============================================================================
# # Update fence graph:
# =============================================================================
    app.clientside_callback(
        """
        function(data, figure) {
            return [{'data': data, 'layout': figure.layout}]
        }
        """,
        [Output('W2E-fence-graph', 'figure')],
        Input('clientside-W2E-fence-figure-store', 'data'),            
        State('W2E-fence-graph', 'figure'),                 
        )
