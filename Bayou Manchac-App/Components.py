import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_table
import pandas as pd
from dash_extensions import Download
import docx
from Callbacks import *


def change_CPT_method_object():
    CPT_method_select_object=dbc.Select(
        id='CPT-method-select',
        options=[
            {'label': 'SBTn, after 1990', 'value': 'SBTn'},
            {'label': 'SBT, 2010', 'value': 'SBT'},
            {'label': 'Probabilistic Soil Classification', 'value': 'PSC'},
        ],
        value='SBTn',
        style={
        'font-size': 'x-small',
        'width': 'auto',
        'margin': '5px 5px 5px 5px',
        'borderWidth': '1px',
        'background-color': '#afeeee',
        },
        )
    change_CPT_method_object = dbc.FormGroup(
        [
            dbc.Label(" CPT Method ", html_for="CPT-method-select", size = 'sm',  id='CPT-method-select-label'),
            CPT_method_select_object,
        ],    
        style={
            'width': 'auto',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 0px 5px 5px',
            'padding': '15px 15px 15px 15px',    
            'background-color': 'white',
        },    
    )
    return change_CPT_method_object
def change_map_height_object():
    map_height_slider_object=dcc.Slider(
        id="map-height-slider", 
        min=600, 
        max=1000, 
        step=100, 
        value=600,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a), 'style':{'font-size': 'x-small'}} for a in range(200,1001,100)},
        )
    change_map_height_object = dbc.FormGroup(
        [
            dbc.Label(" Map Height ", html_for="map-height-slider", size = 'sm',  id='map-height-slider-label'),
            map_height_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_map_height_object
def change_map_soil_boring_label_size_object():
    map_boring_label_size_slider_object=dcc.Slider(
        id="map-boring-label-size-slider", 
        min=1, 
        max=30, 
        step=1, 
        value=15,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a), 'style':{'font-size': 'x-small'}} for a in range(0,31,5)},
        )
    change_map_soil_boring_label_size_object = dbc.FormGroup(
        [
            dbc.Label("Boring Label Size ", html_for="map-boring-label-size-slider", size = 'sm', id='map-boring-label-size-slider-label'),
            map_boring_label_size_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_map_soil_boring_label_size_object
def change_map_soil_boring_marker_size_object():
    map_boring_marker_size_slider_object=dcc.Slider(
        id="map-boring-marker-size-slider", 
        min=0, 
        max=30, 
        step=1, 
        value=15,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a), 'style':{'font-size': 'x-small'}} for a in range(0,31,5)},
        )
    change_map_soil_boring_marker_size_object = dbc.FormGroup(
        [
            dbc.Label("Boring Symbol Size ", html_for="map-boring-marker-size-slider", size = 'sm', id='map-boring-marker-size-slider-label'),
            map_boring_marker_size_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_map_soil_boring_marker_size_object
def change_map_type_object():
    map_type_select_object=dbc.Select(
        id='map-type-select',
        options=[
            {'label': 'Satellite Streets', 'value': 'satellite-streets'},
            {'label': 'Satellite', 'value': 'satellite'},
            {'label': 'Dark', 'value': 'dark'},
            {'label': 'Street', 'value': 'streets'},
            {'label': 'Outdoor', 'value': 'outdoors'},
            {'label': 'Basic', 'value': 'basic'},
            {'label': 'Light', 'value': 'light'},
        ],
        value='satellite-streets',
        style={
        'font-size': 'x-small',
        'width': 'auto',
        'margin': '5px 5px 5px 5px',
        'borderWidth': '1px',
        'background-color': '#afeeee',
        },
        )
    change_map_type_object = dbc.FormGroup(
        [
            dbc.Label(" Map Type ", html_for="map-type-select", size = 'sm',  id='map-type-dropdown-label'),
            map_type_select_object,
        ],    
        style={
            'width': 'auto',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 0px 5px 5px',
            'padding': '15px 15px 15px 15px',    
            'background-color': 'white',
        },    
    )
    return change_map_type_object
def company_banner_object(app):
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Img(src=app.get_asset_url("company-logo.png"), width=300),
        ],
    )
def config_file_save_and_upload_object_group():
# =============================================================================
# # config_file_upload_object:
# =============================================================================
    config_file_upload_object=dcc.Upload(
        id='upload-config-file',
# =============================================================================
#         accept='.XML',
# =============================================================================
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Config File')
        ],
            ),
        style={
            'width': 'auto',
            'minWidth': '300px',
            'minHeight': '70px',
            'lineHeight': 'auto',
            'border-color': 'gray',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '25px',
            'textAlign': 'center',
            'margin': '2px 2px 2px 2px',
            'padding': '25px 25px 25px 25px',
            'background-color': '#00ced1',
            'color': 'white',
        },
        style_active = {
            'width': 'auto',
            'minWidth': '300px',
            'minHeight': '70px',
            'lineHeight': 'auto',
            'border-color': 'gray',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '25px',
            'textAlign': 'center',
            'margin': '2px 2px 2px 2px',
            'padding': '25px 25px 25px 25px',
            'background-color': 'blue',
            'color': 'white',
        },
        style_reject = {
            'width': 'auto',
            'minWidth': '300px',
            'minHeight': '70px',
            'lineHeight': 'auto',
            'border-color': 'gray',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '25px',
            'textAlign': 'center',
            'margin': '2px 2px 2px 2px',
            'padding': '25px 25px 25px 25px',
            'background-color': 'red',
            'color': 'white',
        },
        max_size=-1,
        # Allow multiple files to be uploaded or not
        multiple=False,
        )
# =============================================================================
# # config_file_save_and_upload_object_group_0:
# =============================================================================
    config_file_upload_object_Form = dbc.Form(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
        # =============================================================================
        # # "Save Configuration" Button:   
        # =============================================================================
                                dbc.Row(Download(id="config-file-download")), 
                                dbc.Row(
                                        dbc.Button(
                                            "Export Config File",
                                            color="secondary", 
                                            id="save-config-file-button",
                                            n_clicks=0,
                                            block=True, 
                                            size="lg",
                                            style={
                                                'width': 'auto',
                                                'height': '120px',
                                                # 'font-weight': 'bold',                  
                                                # "color": 'white',
                                                'borderWidth': '0px',
                                                'borderStyle': 'solid',
                                                'borderRadius': '10px',
                                                'textAlign': 'center',
                                                'font-size': '12px',
                                                'vertical-align': 'middle',
                                                'margin': '5px 0px 5px 25px',
                                                'padding': '20px 15px 20px 15px',    
                                                # 'background-color': 'red',
                                            },),
                                        ),                 
                        ], 
                        width=4,
                        ),
                    dbc.Col(
                            dcc.Loading(type='default', fullscreen=False, color="red", children=html.Div(
                                id='config-file-export-loading-hidden-div', children="Ready to Export", 
                                style={'display': 'none'},
                                ),
                                ),                            
                            width = 0, 
                            style={
                                'padding': '0px 0px 0px 0px',
                                'margin': '0px 0px 0px 0px',
                                },                              
                            ),                    
                    dbc.Col(
                        [
                        dbc.Row(config_file_upload_object,                    
                                style={
                                    'padding': '0px 0px 0px 0px',
                                    'margin': '0px 0px 0px 0px',
                                    },                          
                                ),
                        dbc.Row(
                            [
                                dbc.Col(
                                        html.Div(
                                            id='config-file-upload-loading-status-text', children="Loading Status:"),                             
                                        width = 6,
                                        style={
                                            'padding': '0px -20px 0px 0px',
                                            'margin': '0px -10px 0px 0px',
                                            },                              
                                        ),
                                dbc.Col(
                                        dcc.Loading(type='default', fullscreen=False, color="red", children=html.Div(
                                            id='config-file-upload-loading-hidden-div', children="Ready to Load", 
                                            # style={'display': 'none'},
                                            ),
                                            ),                            
                                        width = 6, 
                                        style={
                                            'padding': '0px 0px 0px 0px',
                                            'margin': '0px 0px 0px 0px',
                                            },                              
                                        ),
                        ],
                            style={
                                'padding': '10px 0px 10px 0px',
                                'margin': '0px 0px 0px 0px',
                                },                
                            ),],
                        width = 8,
                        style={
                            'padding': '0px 0px 0px 0px',
                            'margin': '0px 0px 0px 0px',
                            },         
                ),
                ]),
        ])
# =============================================================================
# # config_file_save_and_upload_object_group:
# =============================================================================
    config_file_save_and_upload_object_group = dbc.Card(
        [
        dbc.CardHeader("Export or load your Config file here", 
                       style={
                           'borderRadius': '0px 20px 0px 0px', 
                           'font-weight': 'bold', 
                           'color': '#62698d',
                           },),
        dbc.CardBody(
            [config_file_upload_object_Form]
        ),
        ],
        outline=True,
        style={
            "width": "auto",
            'borderWidth': '1px',
            "border-color": "lightgray",
            'background-color': '#FAFAFA',
            'borderRadius': '0px 20px 20px 0px',
            'margin': '0px 20px 0px 0px',
            },
        )    
    return config_file_save_and_upload_object_group
def loaded_points_datatable(Boring_data_dataset1):
    loaded_point_datatable = dash_table.DataTable(
        id='loaded-point-datatable',
        columns=[{"name": i.replace("_"," "), "id": i} for i in Boring_data_dataset1['POINT'][0].keys()],
        data=Boring_data_dataset1["POINT"],        
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
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
    return loaded_point_datatable
def loaded_projects_datatable(Boring_data_dataset1):
    loaded_projects_datatable = dash_table.DataTable(
        id='loaded-project-table',
        columns=[{"name": i.replace("_"," "), "id": i} for i in Boring_data_dataset1['PROJECT'][0].keys()],
        data=Boring_data_dataset1["PROJECT"],        
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
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
    return loaded_projects_datatable
def login_input_object():    
    email_input = dbc.FormGroup(
        [
            dbc.Label("Email", html_for="login-email-input", width=4),
            dbc.Col(
                dbc.Input(
                    type="email", 
                    id="login-email-input", 
                    placeholder="Enter your email",
                    value="xpeng@ardaman.com",
                ),
                width=8,
            ),
        ],
        row=True,
    )
    password_input = dbc.FormGroup(
        [
            dbc.Label("Password", html_for="login-password-input", width=4),
            dbc.Col(
                dbc.Input(
                    type="password",
                    id="login-password-input",
                    placeholder="Enter your password",
                ),
                width=8,
            ),
        ],
        row=True,
    )
    button_group = dbc.FormGroup(
        [
            dbc.Col(
                dbc.Button("Confirm", color="primary", id="login-confirm-button", block=True, size="sm"),
                width=12,
                ),
        ],
        row=True,
    )    
    form_0 = dbc.Form([
        email_input,
        password_input,
        button_group,
        notice4users_object(),
        ])
    form = dbc.Card(
        [
        dbc.CardHeader([
            "Login to Load Application",
            dbc.Button("Users' Notice", 
                       color="warning", 
                       id="notice4users-info-button", 
                       block=False, 
                       size="sm",
                       style={
                           'padding': '0px 5px 0px 5px', 
                           'margin': '0px 0px 0px 20px',
                           },
                       ),
                        ], 
                       style={
                           'borderRadius': '0px 0px 0px 0px',
                           'font-weight': 'bold', 
                           'color': '#62698d',                                                      
                           },),
        dbc.CardBody(
            [form_0]
        ),
        ],
        outline=True,
        style={
            "width": "600px",
            'borderWidth': '1px',
            "border-color": "lightgray",
            'background-color': '#FAFAFA',
            'borderRadius': '0px 0px 0px 0px',
            },
        )
    return form
def map_graph(token):
    map_fig = go.Figure()
    default_boring_point_dict = dict(Boring_Lon = [-90, -90.5, -91], Boring_Lat = [30, 29.5, 30.5])
    zoom_level_tuple = determine_zoom_level(default_boring_point_dict["Boring_Lat"], default_boring_point_dict["Boring_Lon"])
# =============================================================================
# # Soil boring marker boundary:
# =============================================================================
    map_fig.add_trace(go.Scattermapbox(
            name="Soil Boring",
            lat=default_boring_point_dict["Boring_Lat"],
            lon=default_boring_point_dict["Boring_Lon"],
            mode='markers',
            fillcolor='red',
            marker=go.scattermapbox.Marker(
                size=15,
                color='red',
            ),
            opacity=0.0,
            legendgroup="Soil Boring",
            showlegend=False,
            hoverinfo='none',
            ),
        )
# =============================================================================
# # Soil boring marker fill:
# =============================================================================
    map_fig.add_trace(go.Scattermapbox(
            name="Soil Boring",
            lat=default_boring_point_dict["Boring_Lat"],
            lon=default_boring_point_dict["Boring_Lon"],
            mode='markers',
            fillcolor='red',
            marker=go.scattermapbox.Marker(
                size=15,
                color='red',
            ),
            opacity=0.0,
            legendgroup="Soil Boring",
            showlegend=False,
            hoverinfo='none',
            ),
        )
    map_fig.update_layout(
        #uniformtext_mode='show',
        height=600,
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        clickmode='event+select',
        hovermode='closest',
        dragmode="select", 
        mapbox=dict(
            accesstoken=token,
            style='satellite-streets',
            center=go.layout.mapbox.Center(
                lat=zoom_level_tuple[1][1],
                lon=zoom_level_tuple[1][0],
            ),
            pitch=0,
            bearing=0,
            zoom=zoom_level_tuple[0],
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bordercolor = 'darkgray',
            bgcolor = 'white',
            borderwidth = 1,            
            ),
    )
    map_graph_config={
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 600, # None
            'width': 800, # None
            'scale': 4, # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'edits': {
            'legendPosition': True,
            'legendText': True,
            },
            }
    map_graph=dcc.Graph(
        id='map-graph',
        figure=map_fig,
        config=map_graph_config,
    )
    return map_graph
# embeded in login_input_object
def notice4users_object():
    doc = docx.Document("assets/Users Notice.docx")
    all_paras = doc.paragraphs
    notice4users_object = dbc.Modal(
        [
            dbc.ModalHeader("Users' Notice"),
            dbc.ModalBody(
                [html.P(a.text, style={"text-indent": "3ch","color":"gray"}) if len(a.text)>0 and a.text[0] == '*' else html.P(a.text, style={"text-indent": "0ch",}) for a in all_paras]
                          ),
            dbc.ModalFooter(
                dbc.Button("Agree", id="notice4users-close-button", className="ml-auto")
            ),
        ],
        id="notice4users-modal",
        is_open=False,
        backdrop='static',
        size="lg",
    )
    return notice4users_object


def change_data_profile_text_size_object():
    data_profile_text_size_object=dcc.Slider(
        id="data-profile-text-size-slider", 
        min=4, 
        max=20, 
        step=2, 
        value=12,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a)} for a in range(4,21,4)},
        )
    change_data_profile_text_size_object = dbc.FormGroup(
        [
            dbc.Label("Text Size", html_for="data-profile-text-size-slider", id='data-profile-text-size-slider-label'),
            data_profile_text_size_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_data_profile_text_size_object
def change_Nkt_value_object():
    Nkt_value_slider_object=dcc.Slider(
        id="Nkt-value-slider", 
        min=12, 
        max=22, 
        step=0.5, 
        value=18,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a)} for a in range(12,23,1)},
        )
    change_Nkt_value_object = dbc.FormGroup(
        [
            dbc.Label("Nkt Value", html_for="Nkt-value-slider", id='Nkt-value-slider-label'),
            Nkt_value_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_Nkt_value_object
def change_S2N_fence_plot_bar_width_object():
    S2N_fence_plot_bar_width_slider_object=dcc.Slider(
        id="S2N-fence-plot-bar-width-slider", 
        min=1, 
        max=10, 
        step=1, 
        value=4,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a)} for a in range(1,11,2)},
        )
    change_S2N_fence_plot_bar_width_object = dbc.FormGroup(
        [
            dbc.Label("Column Width", html_for="S2N-fence-plot-bar-width-slider", id='S2N-fence-plot-bar-width-slider-label'),
            S2N_fence_plot_bar_width_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_S2N_fence_plot_bar_width_object
def change_S2N_fence_plot_text_size_object():
    S2N_fence_plot_text_size_object=dcc.Slider(
        id="S2N-fence-plot-text-size-slider", 
        min=4, 
        max=20, 
        step=2, 
        value=12,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a)} for a in range(4,21,4)},
        )
    change_S2N_fence_plot_text_size_object = dbc.FormGroup(
        [
            dbc.Label("Text Size", html_for="S2N-fence-plot-text-size-slider", id='S2N-fence-plot-text-size-slider-label'),
            S2N_fence_plot_text_size_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_S2N_fence_plot_text_size_object
def change_W2E_fence_plot_bar_width_object():
    W2E_fence_plot_bar_width_slider_object=dcc.Slider(
        id="W2E-fence-plot-bar-width-slider", 
        min=1, 
        max=10, 
        step=1, 
        value=4,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a)} for a in range(1,11,2)},
        )
    change_W2E_fence_plot_bar_width_object = dbc.FormGroup(
        [
            dbc.Label("Column Width", html_for="W2E-fence-plot-bar-width-slider", id='W2E-fence-plot-bar-width-slider-label'),
            W2E_fence_plot_bar_width_slider_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_W2E_fence_plot_bar_width_object
def change_W2E_fence_plot_text_size_object():
    W2E_fence_plot_text_size_object=dcc.Slider(
        id="W2E-fence-plot-text-size-slider", 
        min=4, 
        max=20, 
        step=2, 
        value=12,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a)} for a in range(4,21,4)},
        )
    change_W2E_fence_plot_text_size_object = dbc.FormGroup(
        [
            dbc.Label("Text Size", html_for="W2E-fence-plot-text-size-slider", id='W2E-fence-plot-text-size-slider-label'),
            W2E_fence_plot_text_size_object,
        ],
        inline=True,
        style={
            'width': '100%',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 5px 5px 0px',
            'padding': '5px 15px 5px 15px',    
            'background-color': 'white',
        },    
    )
    return change_W2E_fence_plot_text_size_object
def composite_design_stratification_column_A():
# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_design_stratification_graph:    
# =============================================================================
# =============================================================================
# =============================================================================
    composite_design_stratification_fig = go.Figure()
# =============================================================================
#     composite_design_stratification_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
#     composite_design_stratification_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
# =============================================================================
    composite_design_stratification_fig.update_yaxes(autorange=False,
                                    showline=True, linewidth=1, linecolor='gray', mirror=True,
# =============================================================================
#                                     showgrid=True, gridwidth=0.2, gridcolor='lightgray',
# =============================================================================
# =============================================================================
#                                     zeroline=True, zerolinewidth=2, zerolinecolor='Black',
# =============================================================================
                                    #showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across",
                                    )
    composite_design_stratification_fig.update_xaxes(
        range=[-60, 140.], 
        showline=True, linewidth=1, linecolor='gray', mirror=True,
        showticklabels=False,
# =============================================================================
#         showgrid=True, gridwidth=0.1, gridcolor='lightgray',
# =============================================================================
        )
    composite_design_stratification_fig.update_layout(        
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',
        barmode='stack',
        # title='Fence Plot, West to East',
        xaxis=dict(
            title='',
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
            xanchor="right",
            x=0.98,
            bordercolor = 'darkgray',
            bgcolor = 'white',
            borderwidth = 1,
            tracegroupgap = 5,
            font = dict(
                size = 6,                
                ),                        
            ),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=490,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="pan",         
        )
    composite_design_stratification_tab_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 700,# None
            'width': 1700, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'modeBarButtonsToAdd':['drawline',
                               #'drawopenpath',
                               #'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':[#'select2d',
                               'lasso2d',
                               'zoom2d',
                               'zoomIn2d',
                               'zoomOut2d',
                               'hoverCompareCartesian',
                               ],            
            }
    composite_design_stratification_graph=dcc.Graph(
        id='composite-design-stratification-graph-A',
        # animate=False,
        figure=composite_design_stratification_fig,
        config=composite_design_stratification_tab_config,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # composite_design_stratification_group_tab_content:
# =============================================================================
# =============================================================================
# =============================================================================
    composite_design_stratification_tab_content = html.Div(
            [
                dbc.Row(
                    [
                        dcc.Store(
                            id='composite-design-stratification-clientside-figure-data-store-A',
                            data=[],
                        ), 
                        dcc.Store(
                            id='composite-design-stratification-clientside-figure-layout-store-A',
                            data={},
                        ), 
                        dbc.Col(            
                            dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                                id='composite-design-stratification-clientside-store-loading-hidden-div-A', children="Loading Status", style={'display': 'none'})),            
                            width='0',
                            ),                        
                # hidden signal value
                        dbc.Col(
                            html.Div(id='design-proifles-update-signal-1-A', children=0, style={'display': 'none'}), 
                            width='0',
                            ),  
# =============================================================================
#                         dbc.Col(
#                             html.Button('Add Layer', 
#                                         id='add-design-layer-button', 
#                                         n_clicks=0,
#                                         style={
#                                             "color": '#EAECEE',
#                                             'background-color': '#5B2C6F',
#                                             'borderWidth': '1px',
#                                             'borderStyle': 'solid',
#                                             'borderRadius': '7px 7px 0px 0px',
#                                             # 'font-weight': 'bold',                  
#                                             'font-size': '10px',
#                                             'margin': '-50px 5px 5px 10px',
#                                             },                                        
#                                                                     
#                                         ),
#                             width='12',
#                             # className="mt-0 mb-0 mf-0 mb-r",
#                             ),                            
# 
#                         dbc.Col(
#                             design_layer_datatable(),
#                             width='12',
#                             className="mt-0 mb-1 mf-0 mr-0",
#                             ),
# =============================================================================
                        ],
                    style={
                        'width': '97%',            
                        'height': '140px',            
                       'borderWidth': '0px',
                        'borderStyle': 'solid',
                        'borderRadius': '10px',
                        'margin': '10px 5px 5px 5px',
                        'padding': '0px 0px 50px 0px',    
                        'background-color': 'lightgray',
                    },            
                    # className="mt-0 mb-0",
                    ),
                dbc.Row(
                        dbc.Col(composite_design_stratification_graph,width='12'),
                    ),
                ],
        className="mt-0 mb-0 ml-0 mr-0",
    )    
# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_design_stratification_tab:
# =============================================================================
# =============================================================================
# =============================================================================
    composite_design_stratification_tab = dbc.Tab(label= "Design Boring", 
            tab_id='composite-design-boring-tab-A',
            children=[
                composite_design_stratification_tab_content,
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
                "color": '#EAECEE',
                'background-color': '#5B2C6F',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '8px',                  
                },
            active_label_style={
                "color": '#5B2C6F',
                'background-color': '#EAECEE',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '8px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_design_stratification_tab:
# =============================================================================
# =============================================================================
# =============================================================================
    design_layer_datatable_tab = dbc.Tab(label= "Stratification Table", 
            tab_id='stratification-table-tab',
            children=[
                html.Div(
                    [
                        dbc.Col(
                            html.Button('Add Layer', 
                                        id='add-design-layer-button', 
                                        n_clicks=0,
                                        style={
                                            "color": '#EAECEE',
                                            'background-color': '#5B2C6F',
                                            'borderWidth': '1px',
                                            'borderStyle': 'solid',
                                            'borderRadius': '7px 7px 0px 0px',
                                            # 'font-weight': 'bold',                  
                                            'font-size': '10px',
                                            'margin': '-50px 5px 5px 10px',
                                            },                                        
                                        ),
                            width='12',
                            # className="mt-0 mb-0 mf-0 mb-r",
                            ),                            
                        dbc.Col(
                            design_layer_datatable(),
                            width='12',
                            className="mt-0 mb-1 mf-0 mr-0",
                            ),
                        ],
                    className="mt-0 mb-0 ml-0 mr-0",
                    )
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
                "color": '#EAECEE',
                'background-color': '#5B2C6F',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '8px',                  
                },
            active_label_style={
                "color": '#5B2C6F',
                'background-color': '#EAECEE',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '8px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
    composite_design_stratification_tabs = dbc.Tabs(
        [
        composite_design_stratification_tab,
        design_layer_datatable_tab,
        ], 
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
        id="composite-design-stratification-tabs-A",
                                       )
    composite_design_stratification_column_A = dbc.Col(
        composite_design_stratification_tabs, 
        width=2,
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
        )    
    return composite_design_stratification_column_A
def composite_design_stratification_column_B():
# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_design_stratification_graph:    
# =============================================================================
# =============================================================================
# =============================================================================
    composite_design_stratification_fig = go.Figure()
# =============================================================================
#     composite_design_stratification_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
#     composite_design_stratification_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
# =============================================================================
    composite_design_stratification_fig.update_yaxes(autorange=False,
                                    showline=True, linewidth=1, linecolor='gray', mirror=True,
# =============================================================================
#                                     showgrid=True, gridwidth=0.2, gridcolor='lightgray',
# =============================================================================
# =============================================================================
#                                     zeroline=True, zerolinewidth=2, zerolinecolor='Black',
# =============================================================================
                                    #showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across",
                                    )
    composite_design_stratification_fig.update_xaxes(
        range=[-60, 140.], 
        showline=True, linewidth=1, linecolor='gray', mirror=True,
        showticklabels=False,
# =============================================================================
#         showgrid=True, gridwidth=0.1, gridcolor='lightgray',
# =============================================================================
        )
    composite_design_stratification_fig.update_layout(        
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',
        barmode='stack',
        # title='Fence Plot, West to East',
        xaxis=dict(
            title='',
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
            xanchor="right",
            x=0.98,
            bordercolor = 'darkgray',
            bgcolor = 'white',
            borderwidth = 1,
            tracegroupgap = 5,
            font = dict(
                size = 6,                
                ),                        
            ),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=490,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="pan",         
        )
    composite_design_stratification_tab_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 700,# None
            'width': 1700, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'modeBarButtonsToAdd':['drawline',
                               #'drawopenpath',
                               #'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':[#'select2d',
                               'lasso2d',
                               'zoom2d',
                               'zoomIn2d',
                               'zoomOut2d',
                               'hoverCompareCartesian',
                               ],            
            }
    composite_design_stratification_graph=dcc.Graph(
        id='composite-design-stratification-graph-B',
        # animate=False,
        figure=composite_design_stratification_fig,
        config=composite_design_stratification_tab_config,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # composite_design_stratification_group_tab_content:
# =============================================================================
# =============================================================================
# =============================================================================
    composite_design_stratification_tab_content = html.Div(
            [
                dbc.Row(
                    [
                        dcc.Store(
                            id='composite-design-stratification-clientside-figure-data-store-B',
                            data=[],
                        ), 
                        dcc.Store(
                            id='composite-design-stratification-clientside-figure-layout-store-B',
                            data={},
                        ), 
                        dbc.Col(            
                            dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                                id='composite-design-stratification-clientside-store-loading-hidden-div-B', children="Loading Status", style={'display': 'none'})),            
                            width='0',
                            ),                        
                # hidden signal value
                        dbc.Col(
                            html.Div(id='design-proifles-update-signal-1-B', children=0, style={'display': 'none'}), 
                            width='0',
                            ),  
                        ],
                    style={
                        'width': '97%',            
                        'height': '75px',            
                        'borderWidth': '0px',
                        'borderStyle': 'solid',
                        'borderRadius': '10px',
                        'margin': '10px 5px 5px 5px',
                        'padding': '0px 0px 0px 0px',    
                        'background-color': 'lightgray',
                    },            
                    # className="mt-0 mb-0",
                    ),
                dbc.Row(
                        dbc.Col(composite_design_stratification_graph,width='12'),
                    ),
                ],
        className="mt-0 mb-0 ml-0 mr-0",
    )    
# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_design_stratification_tab:
# =============================================================================
# =============================================================================
# =============================================================================
    composite_design_stratification_tab = dbc.Tab(label= "Design Boring", 
            tab_id='composite-design-boring-tab-B',
            children=[
                composite_design_stratification_tab_content,
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
                "color": '#EAECEE',
                'background-color': '#5B2C6F',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '10px',                  
                },
            active_label_style={
                "color": '#5B2C6F',
                'background-color': '#EAECEE',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '10px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
    composite_design_stratification_tabs = dbc.Tabs(
        [
        composite_design_stratification_tab
        ], 
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
        id="composite-design-stratification-tabs-B",
                                       )
    composite_design_stratification_column_B = dbc.Col(
        composite_design_stratification_tabs, 
        width=2,
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
        )    
    return composite_design_stratification_column_B
def composite_soil_stratification_column():
# =============================================================================
# =============================================================================
# =============================================================================
# # # # water_level_elevation_input_object:
# =============================================================================
# =============================================================================
# =============================================================================
    water_level_elevation_input_object = dcc.Input(
        id="water-level-elevation-input", 
        type="number",
        debounce=True, 
        value = 0.0,
        size= '30px',
        placeholder="Input water level",
        style={
        'width': '100%',
        'margin': '2px 2px 2px 2px',
        "color": '#EAECEE',
        'background-color': '#5B2C6F',        
        'borderRadius': '5px',
        'borderWidth': '1px',
        'font-size': 'xx-small',
        },
        )
    water_level_elevation_input_group = dbc.FormGroup(
        [
            dbc.Label(" Water Table Elevation (ft.) ", 
                      size = 'sm', 
                      # className="mt-0 mb-0 ml-0 mr-0",
                      html_for='water-level-elevation-input', 
                      id='water-level-elevation-input-label',
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 5px 0px',
                          'padding': '0px 0px 0px 10px', 
                          },                      
                      ),
            water_level_elevation_input_object,
        ],
        inline=True,
        style={
            'width': '100%',
            #'font-weight': 'bold',                  
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
# # # # thickness_resolution_slider_object:
# =============================================================================
# =============================================================================
# =============================================================================
    thickness_resolution_slider_object=dcc.Slider(
        id="thickness-resolution-slider", 
        min=1, 
        max=20, 
        step=1, 
        value=5,
        included=False,
        updatemode='mouseup', # 'drag', 'mouseup'
        marks={a: {'label': str(a), 'style':{'font-size': 'xx-small'}} for a in range(0,21,5)},
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-4 pl-2 pr-2",
        )
    thickness_resolution_slider_object_group = dbc.FormGroup(
        [
            dbc.Label("Thickness Resolution (ft.)", 
                      size = 'sm', 
                      html_for="thickness-resolution-slider", 
                      id="thickness-resolution-slider-label",
                      style={
                          'font-size': 'xx-small',
                          'margin': '2px 0px 2px 0px',
                          'padding': '0px 0px 0px 10px', 
                          }, 
                      ),
            thickness_resolution_slider_object,
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
# =============================================================================
# # # # composite_soil_stratification_graph:    
# =============================================================================
# =============================================================================
# =============================================================================
    composite_soil_stratification_fig = go.Figure()
# =============================================================================
#     composite_soil_stratification_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
#     composite_soil_stratification_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
# =============================================================================
    composite_soil_stratification_fig.update_yaxes(autorange=False,
                                    showline=True, linewidth=1, linecolor='gray', mirror=True,
# =============================================================================
#                                     showgrid=True, gridwidth=0.2, gridcolor='lightgray',
# =============================================================================
# =============================================================================
#                                     zeroline=True, zerolinewidth=2, zerolinecolor='Black',
# =============================================================================
                                    #showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across",
                                    )
    composite_soil_stratification_fig.update_xaxes(
        range=[-60, 140.], 
        showline=True, linewidth=1, linecolor='gray', mirror=True,
        showticklabels=False,
# =============================================================================
#         showgrid=True, gridwidth=0.1, gridcolor='lightgray',
# =============================================================================
        )
    composite_soil_stratification_fig.update_layout(        
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',
        barmode='stack',
        # title='Fence Plot, West to East',
        xaxis=dict(
            title='',
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
            xanchor="right",
            x=0.98,
            bordercolor = 'darkgray',
            bgcolor = 'white',
            borderwidth = 1,
            tracegroupgap = 5,
            font = dict(
                size = 6,                
                ),                        
            ),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=490,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="pan",         
        )
    composite_soil_stratification_tab_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 700,# None
            'width': 1700, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'modeBarButtonsToAdd':['drawline',
                               #'drawopenpath',
                               #'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':[#'select2d',
                               'lasso2d',
                               'zoom2d',
                               'zoomIn2d',
                               'zoomOut2d',
                               'hoverCompareCartesian',
                               ],            
            }
    composite_soil_stratification_graph=dcc.Graph(
        id='composite-soil-stratification-graph',
        # animate=False,
        figure=composite_soil_stratification_fig,
        config=composite_soil_stratification_tab_config,
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # composite_soil_stratification_group_tab_content:
# =============================================================================
# =============================================================================
# =============================================================================
    composite_soil_stratification_tab_content = html.Div(
            [
                dbc.Row(
                    [
                        dcc.Store(
                            id='composite-soil-stratification-clientside-figure-data-store',
                            data=[],
                        ), 
                        dcc.Store(
                            id='composite-soil-stratification-clientside-figure-layout-store',
                            data={},
                        ), 
                        dbc.Col(            
                            dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                                id='composite-soil-stratification-clientside-store-loading-hidden-div', children="Loading Status", style={'display': 'none'})),            
                            width='0',
                            ),                        
                # hidden signal value
                        dbc.Col(
                            html.Div(id='data-proifles-update-signal-1', children=0, style={'display': 'none'}), 
                            width='0',
                            ),  
                        dbc.Col(water_level_elevation_input_group,width='12'),
                        dbc.Col(thickness_resolution_slider_object_group,width='12'),                        
                        ],
                    style={
                        'width': '99%',            
                        'borderWidth': '0px',
                        'borderStyle': 'solid',
                        'borderRadius': '10px',
                        'margin': '10px 0px 5px 0px',
                        'padding': '0px -10px 0px -10px',    
                        'background-color': 'lightgray',
                    },            
                    # className="mt-0 mb-0",
                    ),
                dbc.Row(
                        dbc.Col(composite_soil_stratification_graph,width='12'),
                    ),
                ],
        className="mt-0 mb-0 ml-0 mr-0",
    )    
# =============================================================================
# =============================================================================
# =============================================================================
# # # # composite_soil_stratification_tab:
# =============================================================================
# =============================================================================
# =============================================================================
    composite_soil_stratification_tab = dbc.Tab(label= "(Composite) Soil Boring", 
            tab_id='composite-soil-boring-tab',
            children=[
                composite_soil_stratification_tab_content,
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
                "color": '#EAECEE',
                'background-color': '#5B2C6F',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                # 'font-weight': 'bold',                  
                'font-size': '10px',                  
                },
            active_label_style={
                "color": '#5B2C6F',
                'background-color': '#EAECEE',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '7px 7px 0px 0px',
                'font-weight': 'bold', 
                'font-size': '10px',                  
                },
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
    composite_soil_stratification_tabs = dbc.Tabs(
        [
        composite_soil_stratification_tab
        ], 
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
        id="composite-soil-stratification-tabs",
                                       )
    composite_soil_stratification_column = dbc.Col(
        composite_soil_stratification_tabs, 
        width=2,
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
        )    
    return composite_soil_stratification_column
def CPT_legend_graph_1():
    CPT_legend_fig = go.Figure()   
    # https://plotly.com/python/axes/
    CPT_legend_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
    CPT_legend_fig.update_yaxes(range=[-0.5, 4.], showticklabels=False, showgrid=False, zeroline=False,)
    #CPT_legend_fig.update_yaxes(autorange="reversed")
    CPT_legend_fig.add_trace(go.Bar(
        x=list(range(10,28,2)),
        y=[2]*9,
        width=[2]*9,
        marker_color=['gray', 'black', 'DarkGreen', 'LimeGreen', 'red', 'orange', 'DarkGoldenrod', 'peru', 'lightgray'],
        text=[
            "1. Sensitive Fine Grained",
            "2. Organic Clay",
            "3. Clay to Silty Clay",
            "4. Clayey Silt & Silty Clay",
            "5. Silty Sand to Sandy Silt",
            "6. Clean Sands to Silty Sands" ,
            "7. Dense Sand to Gravelly Sand",
            "8. Very Stiff Sand to Clayey Sand",
            "9. Very Stiff Fine Grained",
            ],
        hoverinfo='text',
        ))
    CPT_legend_fig.update_traces(textposition='outside', textfont_size=55)
    CPT_legend_fig.update_layout(
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',        
        # barmode='stack',
        # title='SBTn Color Legend',
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=70,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),        
        hovermode='closest',
        # dragmode="select",         
        )
    CPT_legend_graph_config={
        'displayModeBar': False,
        'scrollZoom': False,
        "displaylogo": False,
        'toImageButtonOptions': { 'height': None, 'width': None, },            
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
            }
    CPT_legend_graph=dcc.Graph(
        id='CPT-legend-graph-1',
        # animate=False,
        figure=CPT_legend_fig,
        config=CPT_legend_graph_config,
    )
    return CPT_legend_graph
def CPT_legend_graph_2():
    CPT_legend_fig = go.Figure()   
    # https://plotly.com/python/axes/
    CPT_legend_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
    CPT_legend_fig.update_yaxes(range=[-0.5, 4.], showticklabels=False, showgrid=False, zeroline=False,)
    #CPT_legend_fig.update_yaxes(autorange="reversed")
    CPT_legend_fig.add_trace(go.Bar(
        x=list(range(10,28,2)),
        y=[2]*3,
        width=[2]*3,
        marker_color=['DarkGreen', 'red', 'orange'],
        text=[
            "Clay",
            "Silt",
            "Sand",
            ],
        hoverinfo='text',
        ))
    CPT_legend_fig.update_traces(textposition='outside', textfont_size=12)
    CPT_legend_fig.update_layout(
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',        
        # barmode='stack',
        # title='SBTn Color Legend',
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=70,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),        
        hovermode='closest',
        # dragmode="select",         
        )
    CPT_legend_graph_config={
        'displayModeBar': False,
        'scrollZoom': False,
        "displaylogo": False,
        'toImageButtonOptions': { 'height': None, 'width': None, },            
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
            }
    CPT_legend_graph=dcc.Graph(
        id='CPT-legend-graph-2',
        # animate=False,
        figure=CPT_legend_fig,
        config=CPT_legend_graph_config,
    )
    return CPT_legend_graph
def data_profile_graph():
    data_profile_plot_fig = go.Figure()
    #data_profile_plot_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
    #data_profile_plot_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
    data_profile_plot_fig.update_yaxes(# autorange="reversed",
                                    showline=True, linewidth=1, linecolor='gray', mirror=True,
                                    showgrid=True, gridwidth=0.2, gridcolor='lightgray',
                                    # zeroline=True, zerolinewidth=2, zerolinecolor='Black',
                                    showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across")
    data_profile_plot_fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', mirror=True,
                                    showgrid=True, gridwidth=0.1, gridcolor='lightgray')
    #data_profile_plot_fig.add_trace(go.Bar())
    data_profile_plot_fig.update_layout(        
        plot_bgcolor = '#ffffff',
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="right",
            x=0.98),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=400,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="pan",         
        )
    data_profile_graph_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 700,# None
            'width': 1700, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':['select',
                               'lasso',
                               ],            
            }
    data_profile_graph=dcc.Graph(
        id='data-profile-graph',
        # animate=False,
        figure=data_profile_plot_fig,
        config=data_profile_graph_config,
    )
    return data_profile_graph
def design_layer_datatable():
    design_layer_datatable = html.Div([
    dash_table.DataTable(
        id='design-layer-datatable',
        columns=[
            {"name": 'Top Elevation', "id": 'Top Elevation', "type": 'numeric', 'clearable': False, 'editable': True},
            {"name": 'Base Elevation', "id": 'Base Elevation', "type": 'numeric', 'clearable': False, 'editable': True},
            {"name": 'Soil Type', "id": 'Soil Type', 'presentation': 'dropdown', 'clearable': False, 'editable': True, },
            {"name": 'Soil Symbol', "id": 'Soil Symbol'},
                 ],
        data=[{'Top Elevation': "", 'Base Elevation': "", 'Soil Type': "", 'Soil Symbol': "",}]*10,        
        editable=True,
        # filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="single",
        row_deletable=True,
        dropdown = {
            'Soil Type': {
                'options': [
                    {'label': 'Clay', 'value': 'Clay'},
                    {'label': 'Silt', 'value': 'Silt'},
                    {'label': 'Sand', 'value': 'Sand'},
                    {'label': 'Gravel', 'value': 'Gravel'},
                    ],
                },
            },
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 50,
        style_table={
            'height': '640px', 'overflowY': 'auto', 
            'width': 'auto', 'overflowX': 'auto', 'minWidth': '100%',
            'font-size': '10px',
            #'padding': '5px 5px 5px 5px',
            },    
        style_cell={
            'height': 'auto',
            # 'width': 'auto',
            # all three widths are needed
            'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',
            'whiteSpace': 'normal',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        # fixed_columns={'headers': True, 'data': 1},       
        fixed_rows={'headers': True},
    # Add this line flor dropdown options:
        css=[{"selector": ".Select-menu-outer", "rule": "display: block !important"}],            
    ),
    html.Div(id='design-layer-datatable-dropdown-container')
    ])
    return design_layer_datatable
def point_legend_graph():
    point_legend_fig = go.Figure()   
    # https://plotly.com/python/axes/
    point_legend_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,
                                  #showline=True, linewidth=1, linecolor='gray', mirror=True,
                                  )
    point_legend_fig.update_yaxes(range=[-0.5, 4.], showticklabels=False, showgrid=False, zeroline=False,
                                  #showline=True, linewidth=1, linecolor='gray', mirror=True,
                                  )
    #point_legend_fig.update_yaxes(autorange="reversed")
    point_legend_fig.update_layout(
        plot_bgcolor = '#F8F9F9',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',        
        # barmode='stack',
        # title='SBTn Color Legend',
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=70,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),        
        hovermode='closest',
        dragmode="pan",         
        )
    CPT_legend_graph_config={
        'displayModeBar': False,
        'scrollZoom': False,
        "displaylogo": False,
        'toImageButtonOptions': { 'height': None, 'width': None, },            
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
            }
    point_legend_graph=dcc.Graph(
        id='point-legend-graph',
        # animate=False,
        figure=point_legend_fig,
        config=CPT_legend_graph_config,
    )
    return point_legend_graph
def S2N_fence_graph():
    S2N_fence_plot_fig = go.Figure()   
    #S2N_fence_plot_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
    #S2N_fence_plot_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
    S2N_fence_plot_fig.update_yaxes(# autorange="reversed",
                                    showline=True, linewidth=1, linecolor='gray', mirror=True,
                                    showgrid=True, gridwidth=0.2, gridcolor='lightgray',
                                    # zeroline=True, zerolinewidth=2, zerolinecolor='Black',
                                    showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across")
    S2N_fence_plot_fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', mirror=True,
                                    showgrid=True, gridwidth=0.1, gridcolor='lightgray')
    #S2N_fence_plot_fig.add_trace(go.Bar())
    S2N_fence_plot_fig.update_layout(        
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',
        barmode='stack',
        # title='Fence Plot, West to East',
        xaxis=dict(
            title='Latitude (deg.)',
            #autorange=True,
        ),
        yaxis=dict(
            title='Elevation (ft.)',
            #autorange=True,
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
            ),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=400,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="pan",         
        )
    S2N_fence_graph_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 700,# None
            'width': 1700, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'edits': {
            'legendPosition': True,
            'legendText': True,
            },
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':['select',
                               'lasso',
                               ],            
            }
    S2N_fence_graph=dcc.Graph(
        id='S2N-fence-graph',
        # animate=False,
        figure=S2N_fence_plot_fig,
        config=S2N_fence_graph_config,
    )
    return S2N_fence_graph
def soil_design_parameter_datatable():
    soil_design_parameter_datatable = html.Div([
    dash_table.DataTable(
        id='soil-design-parameter-datatable',
        columns=[
            {"name": 'Top Elevation', "id": 'Top Elevation', "type": 'numeric', 'clearable': False, 'editable': False},
            {"name": 'Base Elevation', "id": 'Base Elevation', "type": 'numeric', 'clearable': False, 'editable': False},
            {"name": 'Soil Type', "id": 'Soil Type', 'clearable': False, 'editable': False},
            {"name": 'Soil Symbol', "id": 'Soil Symbol'},
                 ],
        data=[{'Top Elevation': "", 'Base Elevation': "", 'Soil Type': "", 'Soil Symbol': "",}]*10,        
        # editable=True,
        # filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        # row_selectable="single",
        # row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 50,
        style_table={
            'height': '200px', 'overflowY': 'auto', 
            'width': 'auto', 'overflowX': 'auto', 'minWidth': '100%',
            'font-size': '10px',
            #'padding': '5px 5px 5px 5px',
            },    
        style_cell={
            'height': '30px',
            #'width': 'auto',
            # all three widths are needed
            'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',
            'whiteSpace': 'normal',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        # fixed_columns={'headers': True, 'data': 1},       
        fixed_rows={'headers': True},
    ),
    ])
    return soil_design_parameter_datatable
def W2E_fence_graph():
    W2E_fence_plot_fig = go.Figure()
    #W2E_fence_plot_fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False,)
    #W2E_fence_plot_fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,)
    W2E_fence_plot_fig.update_yaxes(# autorange="reversed",
                                    showline=True, linewidth=1, linecolor='gray', mirror=True,
                                    showgrid=True, gridwidth=0.2, gridcolor='lightgray',
                                    # zeroline=True, zerolinewidth=2, zerolinecolor='Black',
                                    showspikes=True, spikecolor="gray", spikethickness=1, spikesnap="cursor", spikemode="across")
    W2E_fence_plot_fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', mirror=True,
                                    showgrid=True, gridwidth=0.1, gridcolor='lightgray')
    #W2E_fence_plot_fig.add_trace(go.Bar())
    W2E_fence_plot_fig.update_layout(        
        plot_bgcolor = '#ffffff',
        # paper_bgcolor = '#ffffff',
        uniformtext_mode='hide',
        barmode='stack',
        # title='Fence Plot, West to East',
        xaxis=dict(
            title='Longitude (deg.)',
            #autorange=True,
        ),
        yaxis=dict(
            title='Elevation (ft.)',
            #autorange=True,
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
            ),
        # dragmode='drawopenpath',
        newshape_line_color='cyan',
        height=400,
        autosize=True,            
        margin=dict(
            l=5,
            r=5,
            b=5,
            t=5,
            pad=5,
        ),
        hovermode='closest', # ( "x" | "y" | "closest" | False | "x unified" | "y unified" )
        dragmode="pan",         
        )
    W2E_fence_graph_config={
        'scrollZoom': True,
        "displaylogo": False,
        'toImageButtonOptions': {
            'format': 'png',            
            'height': 700,# None
            'width': 1700, # None
            'scale': 10, # 20 # Multiply title/legend/axis/canvas sizes by this factor            
            },
        'edits': {
            'legendPosition': True,
            'legendText': True,
            },
        'modeBarButtonsToAdd':['drawline',
                               'drawopenpath',
                               'drawclosedpath',
                               'drawcircle',
                               'drawrect',
                               'eraseshape',
                               ],
        'modeBarButtonsToRemove':['select',
                               'lasso',
                               ],            
            }
    W2E_fence_graph=dcc.Graph(
        id='W2E-fence-graph',
        # animate=False,
        figure=W2E_fence_plot_fig,
        config=W2E_fence_graph_config,
    )
    return W2E_fence_graph


def layout(app, token, Boring_data_dataset1):
    title_info = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Col(html.H4("DOTD I10-CMAR Geotechnical Data Explorer", className="card-title")),
                        dbc.Col(html.H6("Version 0.0.1", className="card-subtitle")),
                        dbc.Col(html.Hr()),
                        dbc.Row(                        
                            [
                                dbc.Col(company_banner_object(app), width=7,),
                                dbc.Col(dbc.CardLink("Developed by Xin Peng. Maintained by Chang Huang.", href="mailto:yhuang@ardaman.com"), width=12,),
                            ],
                        )
                       ]
                ),
                outline=True,
                style={
                    "width": "auto",
                    "border-color": "lightgray",
                    'background-color': '#FAFAFA',
                    'borderRadius': '20px 0px 0px 20px',
                    'padding': '5px 5px 5px 5px',
                    },
                ),
            login_input_object(),
            config_file_save_and_upload_object_group(),
        ],
        )
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# # # # # final layout    
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
    layout = html.Div([
        dbc.Row(
            [
                dbc.Col(title_info, 
                        width='auto',
                        style={
                        'margin': '10px 10px 10px 10px',
                        'padding': '20px 10px 20px 10px',
                        },                                                
                        ),
            ],
            style={
            'width': 'auto',
            'margin': '15px 15px 15px 15px',
            'background-color': '#E6E6E6',
            },
            ),
        security_section_layout(token, Boring_data_dataset1),
        ],
        id="final-layout",
        style={
        'background-color': 'white',
        },        
        )
    return layout
def map_tab_layout(token):
# =============================================================================
# =============================================================================
# # # map_view_tab_content:    
# =============================================================================
# =============================================================================
    map_view_tab_content = dbc.Card(
        dbc.CardBody(
            [
                dcc.Store(id='MapView-coordinates-range',
                          data = [
                              [-93.49674231323337, 30.75214322346099], 
                              [-82.70965213246285, 30.75214322346099], 
                              [-82.70965213246285, 28.020380340741696], 
                              [-93.49674231323337, 28.020380340741696],
                              ]),
                dbc.Row(
                    [
                        dbc.Col(map_tool_layout(), width=12),
                    ],
                    id="map-tool-layout",
                    style={
                    'width': 'auto',
                    'margin': '0px 2px 0px 2px',
                    'background-color': '#FFFFFF',
                    },                        
                    ),
                dbc.Row(dbc.Col(map_graph(token), width=12))
            ]
        ),
        className="mt-2",
    )
    return map_view_tab_content
def map_tool_layout():
# =============================================================================
# =============================================================================
# # map_view_tab_tool_group
# =============================================================================
# =============================================================================
    map_tool_group = dbc.Row(
        [
            dbc.Col(change_map_type_object(),width='auto'),
            dbc.Col(change_map_height_object(),width='2'),
            dbc.Col(change_map_soil_boring_marker_size_object(),width='2'),
            dbc.Col(change_map_soil_boring_label_size_object(),width='2'),
            dbc.Col(change_CPT_method_object(),width='auto'),
            ],
        style={
            'width': '100%',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '100px',
            'margin': '10px 0px 10px 0px',
            'padding': '10px 10px 10px 10px',    
            'background-color': 'lightgray',
        },            
        className="mt-0 mb-3")
# =============================================================================
# =============================================================================
# # # map_view_tab_content:    
# =============================================================================
# =============================================================================
    map_tool_group_content = dbc.Card(
        dbc.CardBody(
            [
                map_tool_group,
            ]
        ),
        className="mt-2",
    )
    return map_tool_group_content
def security_section_layout(token, Boring_data_dataset1):
# =============================================================================
# =============================================================================
# =============================================================================
# # # security_section_layout_tabs
# =============================================================================
# =============================================================================
# =============================================================================
    security_section_layout_tabs = dbc.Tabs(
        [
            dbc.Tab(label='Site Characterization', 
                    tab_id='site-characterization-tab',
                    children=[
                        dbc.Row(dbc.Col(site_characterization_tab_layout(), width=12)),
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
                        "color": '#FFFFFF',
                        'background-color': '#1A5276',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        #'font-weight': 'bold',                  
                        },
                    active_label_style={
                        "color": '#1A5276',
                        'background-color': '#E5E8E8',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        },
                    ),
            dbc.Tab(label='Data Tables', 
                    tab_id='data-tables-tab',
                    children=[
                        dbc.Row(dbc.Col(table_tab_layout(Boring_data_dataset1), width=12)),
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
                        "color": '#FFFFFF',
                        'background-color': '#1A5276',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        #'font-weight': 'bold',                  
                        },
                    active_label_style={
                        "color": '#1A5276',
                        'background-color': '#E5E8E8',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        },
                    ),
            ],
                id="security-section-layout-view-tabs",
                )        
    layout = html.Div([        
        dbc.Row(
            [
# =============================================================================
# # "Load Database" Button:   
# =============================================================================
                dbc.Button(
                    "Load Database",
                    color="success", 
                    id="load-database-button",
                    n_clicks=0,
                    block=False, 
                    size="md",
                    className="ml-3 mb-3",
                    ),
# =============================================================================
# # "Close Map" Button:   
# =============================================================================
                dbc.Button(
                    children= "Close Map",
                    id="open-map-view-layout-collapse-button",
                    color="primary",
                    n_clicks=0,
                    active=True,
                    size="md",
                    className="ml-3 mb-3",
                    ),                                        
            ],
            style={
            'width': 'auto',
            'margin': '0px 2px 0px 2px',
            'background-color': '#FFFFFF',
            },                        
            ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Collapse(
                        map_tab_layout(token),
                        id="map-view-layout-collapse",
                        is_open=True,
                    ),                
                    width=12),
            ],
            style={
            'width': 'auto',
            'margin': '0px 2px 0px 2px',
            'background-color': '#FFFFFF',
            },                        
            ),
        dbc.Row(
            [
                dbc.Col(
                    security_section_layout_tabs,
                    width=12),
            ],
            style={
            'width': 'auto',
            'margin': '2px 2px 2px 2px',
            'pad': '2px 2px 2px 2px',
            'background-color': '#FFFFFF',
            },                        
            ),
        ],
        id="security-section-layout",
        style={
        'background-color': 'white',
        },        
        )
    return layout
def site_characterization_tab_layout():
# =============================================================================
# =============================================================================
# =============================================================================
# # # # data_plots_view_tabs    
# =============================================================================
# =============================================================================
# =============================================================================
    data_plots_view_tabs = dbc.Tabs(
        [
            data_profile_tab_layout(),
            design_profile_tab_layout_A(),
            design_profile_tab_layout_B(),
            ],
                id="data-plots-view-tabs",
                )
# =============================================================================
# =============================================================================
# =============================================================================
# # # site_characterization_view_tabs
# =============================================================================
# =============================================================================
# =============================================================================
    site_characterization_view_tabs = dbc.Tabs(
        [
            dbc.Tab(label='Data Plots', 
                    tab_id='data-plots-view-tab',
                    children=[
                        dbc.Row(dbc.Col(data_plots_view_tabs, width=12)),
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
                        "color": '#FFFFFF',
                        'background-color': '#641E16',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        #'font-weight': 'bold',                  
                        },
                    active_label_style={
                        "color": '#641E16',
                        'background-color': '#E5E8E8',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        },
                    ),
            dbc.Tab(label='Fence Plots', 
                    tab_id='fence-plots-view-tab',
                    children=[
                        dbc.Row(dbc.Col(fence_plots_tab_layout(), width=12)),
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
                        "color": '#FFFFFF',
                        'background-color': '#641E16',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        #'font-weight': 'bold',                  
                        },
                    active_label_style={
                        "color": '#641E16',
                        'background-color': '#E5E8E8',
                        'borderWidth': '2px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        },
                    ),
            ],
                id="site-characterization-view_tabs",
                )            
    CPT_legend_layout = html.Div([
        dbc.Row(
            [
                dbc.Col(html.H6(children='CPT Color Legend 1 (SBTn, after 1990 & SBT, 2010)', className="graph-title"), width=12),
                dbc.Col(CPT_legend_graph_1(), width=12),
                dbc.Col(html.H6(children='CPT Color Legend 2 (Probabilistic Soil Classification, after 1996)', className="graph-title"), width=12),
                dbc.Col(CPT_legend_graph_2(), width=12),
            ],
            id="CPT-legend-graph-layout",
            style={
            'width': 'auto',
            'margin': '20px 2px 200px 2px',
            'background-color': '#FFFFFF',
            },                        
            ),
        ])
    point_legend_layout = html.Div([
        dbc.Row(
            [
                dbc.Col(html.H6(children='Point List', className="graph-title"), width=12),
                dbc.Col(point_legend_graph(), width=12),
                dcc.Store(
                    id='clientside-point-legend-figure-data-store',
                    data=[],
                ), 
            ],
            id="point-legend-graph-layout",
            style={
            'width': 'auto',
            'margin': '20px 2px 20px 2px',
            'background-color': '#FFFFFF',
            },                        
            ),
        ])
    site_characterization_tab_view_content = html.Div([        
        dbc.Row(
            [
                dbc.Row(site_characterization_view_tabs),
                dbc.Row(point_legend_layout),
                dbc.Row(CPT_legend_layout),                
            ],
            style={
            'width': '100%',
            'margin': '0px 2px 0px 2px',
            'background-color': '#FFFFFF',
            },                        
            ),
        ],
        id="site-characterization-tab-view-content",
        style={
        'background-color': 'white',
        },        
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # site_characterization_view_tab
# =============================================================================
# =============================================================================
# =============================================================================
    site_characterization_view_tab = dbc.Tab(
        label='Site Characterization', 
        tab_id='site-characterization-tab',
        children=[
            site_characterization_tab_view_content,
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
            "color": '#FFFFFF',
            'background-color': '#1A5276',
            'borderWidth': '2px',
            'borderStyle': 'solid',
            'borderRadius': '7px 7px 0px 0px',
            #'font-weight': 'bold',                  
            },
        active_label_style={
            "color": '#1A5276',
            'background-color': '#E5E8E8',
            'borderWidth': '2px',
            'borderStyle': 'solid',
            'borderRadius': '7px 7px 0px 0px',
            'font-weight': 'bold', 
            },
        )
    return site_characterization_view_tab
def table_tab_layout(Boring_data_dataset1):
    data_table_name_list=[
        'point', 
        'soil_boring_data', 
        'soil_lithology', 
        'CPT_data', 
        'test_pile', 
        'test_pile_event_data', 
        'test_pile_static_data',
        ]
    datatable_tab_name_list = [
        'Selected Points',
        'Selected Soil Boring Data',
        'Selected Soil Boring Lithology',
        'Selected CPT Data',
        'Selected Test Pile',
        'Selected Test Pile Event Data',
        'Selected Test Pile Static Data',
        ]
    datatable_tab_color_list = [
        '#2874A6',
        '#2874A6',
        '#2E86C1',
        '#3498DB',
        '#5DADE2',
        '#85C1E9',
        '#AED6F1',
        ]
    datatable_tab_text_color_list = [
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#2C3E50',
        '#2C3E50',
        '#2C3E50',
        ]
    datatable_tab_list = []
    for i in range(0, len(data_table_name_list)):
        data_table = general_datatable_func(data_table_name_list[i])
        datatable_tab = general_datatable_tab_func(
            data_table, 
            datatable_tab_name_list[i],
            datatable_tab_color_list[i], 
            datatable_tab_text_color_list[i],
            )
        datatable_tab_list.append(datatable_tab)
# =============================================================================
# =============================================================================
# # # loaded_projects_datatable_tab_content:
# =============================================================================
# =============================================================================
    loaded_projects_datatable_tab_content = dbc.Card(
        dbc.CardBody(
            [
                loaded_projects_datatable(Boring_data_dataset1),
                ]
        ),
        className="mt-3",
    )
# =============================================================================
# =============================================================================
# # # loaded_point_datatable_tab_content:
# =============================================================================
# =============================================================================
    loaded_points_datatable_tab_content = dbc.Card(
        dbc.CardBody(
            [
                loaded_points_datatable(Boring_data_dataset1),
                # hidden signal value
                html.Div(id='loaded-data-datatable-update-signal-1', children=0, style={'display': 'none'}), 
                ]
        ),
        className="mt-3",
    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # data_tables_view_tabs    
# =============================================================================
# =============================================================================
# =============================================================================
    data_tables_view_tabs = dbc.Tabs(
        [
            dbc.Tab(label='Loaded Projects', 
                    tab_id='Boring-project-tab',
                    children=[
                        loaded_projects_datatable_tab_content,
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
                        "color": '#FFFFFF',
                        'background-color': '#21618C',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        # 'font-weight': 'bold',                  
                        'font-size': '10px',                  
                        },
                    active_label_style={
                        "color": '#21618C',
                        'background-color': '#E5E8E8',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        'font-size': '10px',                  
                        },
                    ),
            dbc.Tab(label='Loaded Points', 
                    tab_id='Boring-point-tab',
                    children=[
                        loaded_points_datatable_tab_content,
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
                        "color": '#FFFFFF',
                        'background-color': '#21618C',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        # 'font-weight': 'bold',                  
                        'font-size': '10px',                  
                        },
                    active_label_style={
                        "color": '#21618C',
                        'background-color': '#E5E8E8',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        'font-size': '10px',                  
                        },
                    ),
            ] + datatable_tab_list,
                id="data-tables-view-tabs",
                )    
    return data_tables_view_tabs

# =============================================================================
# from Site_Characterization.Objects.data_profile_graph import data_profile_graph      
# =============================================================================
def data_profile_tab_layout():
    data_profile_name_list = ['Data Profile ' + str(a) for a in list(range(1,6))]
    x_axis_parameter_list = [
                'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                'Total Unit Weight','Dry Density',
                'Compressive Strength','Undrained Shear Strength',
                'SPT N',
                'Percentage Passing at 0_075',
                ]
    x_axis_parameter_selection_list = ['Moisture Content',
                                       'Total Unit Weight',
                                       'Undrained Shear Strength',
                                       'SPT N',
                                       'Percentage Passing at 0_075',
                                       ]
    data_profile_tab_color_list = [
        '#5B2C6F',
        '#6C3483',
        '#7D3C98',
        '#8E44AD',
        '#9B59B6',
        ]
    data_profile_tab_text_color_list = [
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        ]
    data_profile_graph_tabs_content_list = [composite_soil_stratification_column()]
    for i in range(0, len(data_profile_name_list)):
        data_profile_graph = general_data_profile_func(data_profile_name_list[i])
        data_profile_graph_tab = general_data_profile_tab_func(
            data_profile_graph,
            data_profile_name_list[i], 
            x_axis_parameter_list, 
            x_axis_parameter_selection_list[i],
            data_profile_tab_color_list[i],
            data_profile_tab_text_color_list[i],
            )
        data_profile_graph_tabs = dbc.Tabs(
            [
            data_profile_graph_tab
            ], 
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            id=data_profile_name_list[i].replace(" ", "-") + "-tabs",
                                           )
        data_profile_graph_tabs_content_column = dbc.Col(
            data_profile_graph_tabs, 
            width=2,
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
        data_profile_graph_tabs_content_list.append(data_profile_graph_tabs_content_column)
    data_profile_graph_tabs_content_list_view = dbc.Row(
        data_profile_graph_tabs_content_list,
        className="mt-2 mb-2 ml-3 mr-3 pt-0 pb-0 pl-0 pr-0",
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # fence_and_data_plots_view_tabs    
# =============================================================================
# =============================================================================
# =============================================================================
    data_profile_view_tab = dbc.Tab(label='Data Profiles', 
                                    tab_id='data-profile-graph-tab',
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(data_profile_tool_layout(), width=12),
                                                dbc.Col(
                                                    data_profile_graph_tabs_content_list_view, 
                                                    width=12,
                                                    className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    style={
                                        'margin': '1px 5px 1px 5px',
                                        'padding': '1px 5px 1px 5px',                        
                                        },
                                    tab_style={
                                        'margin': '1px 1px 1px 1px',
                                        'padding': '1px 1px 1px 1px',                        
                                        },
                                    active_tab_style={
                                        'margin': '1px 1px 1px 1px',
                                        'padding': '1px 1px 1px 1px',                        
                                        },
                                    label_style={
                                        "color": '#FFFFFF',
                                        'background-color': '#943126',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '7px 7px 0px 0px',
                                        # 'font-weight': 'bold',                  
                                        'font-size': '10px',                  
                                        },
                                    active_label_style={
                                        "color": '#943126',
                                        'background-color': '#E5E8E8',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '7px 7px 0px 0px',
                                        'font-weight': 'bold', 
                                        'font-size': '10px',                  
                                        },
                                    ) 
    return data_profile_view_tab
# =============================================================================
# from Site_Characterization.Objects.change_data_profile_plot_bar_width_object import change_data_profile_plot_bar_width_object    
# =============================================================================
def data_profile_tool_layout():
    interpretation_mode_select_object=dbc.Select(
        id='interpretation-mode-select',
        options=[
            {'label': 'Visualization Mode', 'value': 'Visualization Mode'},
            {'label': 'Interpretation Mode', 'value': 'Interpretation Mode'},
        ],
        value='Visualization Mode',
        bs_size = "sm",
        style={
        'width': 'auto',
        'margin': '5px 5px 5px 5px',
        'borderWidth': '1px',
        'background-color': '#afeeee',
        },
        )
    interpretation_mode_select_object_group = dbc.FormGroup(
        [
            dbc.Label(" Mode Select ", 
                      html_for="interpretation-mode-select", 
                      id='interpretation-mode-select-label',
                      style={
                          # 'font-size': 'xx-small',
                          'margin': '2px 0px 5px 0px',
                          'padding': '0px 0px 0px 10px', 
                          },                       
                      ),
            interpretation_mode_select_object,
        ],    
        style={
            'width': 'auto',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '15px',
            'textAlign': 'left',
            'margin': '5px 0px 5px 5px',
            'padding': '5px 5px 5px 5px',    
            'background-color': 'white',
        },    
    )
# =============================================================================
# =============================================================================
# # data_profile_plot_tool_group
# =============================================================================
# =============================================================================
    data_profile_tool_group = dbc.Row(
        [
# =============================================================================
# # "Generate Data Profiles" Button:   
# =============================================================================
            dbc.Col(
                    dbc.Button(
                        "Generate Data Profiles",
                        color="success", 
                        id="generate-data-profile-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
# =============================================================================
# # "Delete Data Selection" Button:   
# =============================================================================
            dbc.Col(
                    dbc.Button(
                        "Delete Data Selection",
                        color="warning", 
                        id="delete-data-selection-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
            dbc.Col(interpretation_mode_select_object_group,width='2'),
# =============================================================================
# # "Finalize Stratification" Button:   
# =============================================================================
            dbc.Col(
                    dbc.Button(
                        "Finalize Stratification",
                        color="danger", 
                        id="finalize-stratification-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        disabled=True,
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
            ],
        style={
            'width': '100%',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '100px',
            'margin': '10px 0px 10px 0px',
            'padding': '10px 10px 10px 10px',    
            'background-color': 'lightgray',
        },            
        className="mt-0 mb-0")
# =============================================================================
# =============================================================================
# # # data_profile_plot_tool_group_content:    
# =============================================================================
# =============================================================================
    data_profile_tool_group_content = dbc.Card(
        dbc.CardBody(
            [
                data_profile_tool_group,
            ]
        ),
        className="mt-2",
    )
    return data_profile_tool_group_content
# =============================================================================
# from Site_Characterization.Objects.design_profile_graph import design_profile_graph      
# =============================================================================
def design_profile_tab_layout_A():
    design_profile_name_list = ['Design Profile A' + str(a) for a in list(range(1,6))]
    x_axis_parameter_list = [
                'Moisture Content','Liquid Limit','Plastic Limit','Plasticity Index','Liquidity Index',
                'Total Unit Weight','Dry Density',
                'Compressive Strength','Undrained Shear Strength',
                'SPT N',
                'Percentage Passing at 0_075',
                ]
    x_axis_parameter_selection_list = ['Moisture Content',
                                       'Total Unit Weight',
                                       'Undrained Shear Strength',
                                       'SPT N',
                                       'Percentage Passing at 0_075',
                                       ]
    design_profile_tab_color_list = [
        '#5B2C6F',
        '#6C3483',
        '#7D3C98',
        '#8E44AD',
        '#9B59B6',
        ]
    design_profile_tab_text_color_list = [
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        ]
    design_profile_graph_tabs_content_list = [composite_design_stratification_column_A()]
    for i in range(0, len(design_profile_name_list)):
        design_profile_graph = general_data_profile_func(design_profile_name_list[i])
        design_profile_graph_tab = general_design_profile_tab_func_A(
            design_profile_graph,
            design_profile_name_list[i], 
            x_axis_parameter_list, 
            x_axis_parameter_selection_list[i],
            design_profile_tab_color_list[i],
            design_profile_tab_text_color_list[i],
            )
        design_profile_graph_tabs = dbc.Tabs(
            [
            design_profile_graph_tab
            ], 
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            id=design_profile_name_list[i].replace(" ", "-") + "-tabs",
                                           )
        design_profile_graph_tabs_content_column = dbc.Col(
            design_profile_graph_tabs, 
            width=2,
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
        design_profile_graph_tabs_content_list.append(design_profile_graph_tabs_content_column)
    design_profile_graph_tabs_content_list_view = dbc.Row(
        design_profile_graph_tabs_content_list,
        className="mt-2 mb-2 ml-3 mr-3 pt-0 pb-0 pl-0 pr-0",
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # design_profile_view_tab    
# =============================================================================
# =============================================================================
# =============================================================================
    design_profile_view_tab = dbc.Tab(label='Design Profiles A', 
                                    tab_id='design-profile-graph-tab',
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(design_profile_tool_layout_A(), width=12),
                                                dbc.Col(
                                                    design_profile_graph_tabs_content_list_view, 
                                                    width=12,
                                                    className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    style={
                                        'margin': '1px 5px 1px 5px',
                                        'padding': '1px 5px 1px 5px',                        
                                        },
                                    tab_style={
                                        'margin': '1px 1px 1px 1px',
                                        'padding': '1px 1px 1px 1px',                        
                                        },
                                    active_tab_style={
                                        'margin': '1px 1px 1px 1px',
                                        'padding': '1px 1px 1px 1px',                        
                                        },
                                    label_style={
                                        "color": '#FFFFFF',
                                        'background-color': '#943126',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '7px 7px 0px 0px',
                                        # 'font-weight': 'bold',                  
                                        'font-size': '10px',                  
                                        },
                                    active_label_style={
                                        "color": '#943126',
                                        'background-color': '#E5E8E8',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '7px 7px 0px 0px',
                                        'font-weight': 'bold', 
                                        'font-size': '10px',                  
                                        },
                                    ) 
    return design_profile_view_tab
# =============================================================================
# from Site_Characterization.Objects.design_profile_graph import design_profile_graph      
# =============================================================================
def design_profile_tab_layout_B():
    design_profile_name_list = ['Design Profile B' + str(a) for a in list(range(1,6))]
    design_profile_tab_color_list = [
        '#5B2C6F',
        '#6C3483',
        '#7D3C98',
        '#8E44AD',
        '#9B59B6',
        ]
    design_profile_tab_text_color_list = [
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        '#EAECEE',
        ]
    design_profile_graph_tabs_content_list = [composite_design_stratification_column_B()]
    for i in range(0, len(design_profile_name_list)):
        design_profile_graph = general_data_profile_func(design_profile_name_list[i])
        design_profile_graph_tab = general_design_profile_tab_func_B(
            design_profile_graph,
            design_profile_name_list[i], 
            design_profile_tab_color_list[i],
            design_profile_tab_text_color_list[i],
            )
        design_profile_graph_tabs = dbc.Tabs(
            [
            design_profile_graph_tab
            ], 
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            id=design_profile_name_list[i].replace(" ", "-") + "-tabs",
                                           )
        design_profile_graph_tabs_content_column = dbc.Col(
            design_profile_graph_tabs, 
            width=2,
            className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
            )
        design_profile_graph_tabs_content_list.append(design_profile_graph_tabs_content_column)
    design_profile_graph_tabs_content_list_view = dbc.Row(
        design_profile_graph_tabs_content_list,
        className="mt-2 mb-2 ml-3 mr-3 pt-0 pb-0 pl-0 pr-0",
        )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # design_profile_view_tab    
# =============================================================================
# =============================================================================
# =============================================================================
    design_profile_view_tab = dbc.Tab(label='Design Profiles B', 
                                    tab_id='design-profile-graph-tab-B',
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(design_profile_tool_layout_B(), width=12),
                                                dbc.Col(soil_design_parameter_datatable(), width=12),
                                                dbc.Col(
                                                    design_profile_graph_tabs_content_list_view, 
                                                    width=12,
                                                    className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-0 pl-0 pr-0",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    style={
                                        'margin': '1px 5px 1px 5px',
                                        'padding': '1px 5px 1px 5px',                        
                                        },
                                    tab_style={
                                        'margin': '1px 1px 1px 1px',
                                        'padding': '1px 1px 1px 1px',                        
                                        },
                                    active_tab_style={
                                        'margin': '1px 1px 1px 1px',
                                        'padding': '1px 1px 1px 1px',                        
                                        },
                                    label_style={
                                        "color": '#FFFFFF',
                                        'background-color': '#943126',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '7px 7px 0px 0px',
                                        # 'font-weight': 'bold',                  
                                        'font-size': '10px',                  
                                        },
                                    active_label_style={
                                        "color": '#943126',
                                        'background-color': '#E5E8E8',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '7px 7px 0px 0px',
                                        'font-weight': 'bold', 
                                        'font-size': '10px',                  
                                        },
                                    ) 
    return design_profile_view_tab
def design_profile_tool_layout_A():
# =============================================================================
# =============================================================================
# # design_profile_plot_tool_group
# =============================================================================
# =============================================================================
    design_profile_tool_group = dbc.Row(
        [
# =============================================================================
# # "Generate Design Profiles" Button:   
# =============================================================================
            dbc.Col(
                    dbc.Button(
                        "Generate Design Profiles",
                        color="success", 
                        id="generate-design-profile-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
# =============================================================================
# # "Delete Data Selection" Button:   
# =============================================================================
            dbc.Col(
                    dbc.Button(
                        "Delete Data Selection",
                        color="warning", 
                        id="delete-data-selection4design-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
            dbc.Col(change_Nkt_value_object(),width='3'),
            ],
        style={
            'width': '100%',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '100px',
            'margin': '10px 0px 10px 0px',
            'padding': '10px 10px 10px 10px',    
            'background-color': 'lightgray',
        },            
        className="mt-0 mb-0")
# =============================================================================
# =============================================================================
# # # design_profile_plot_tool_group_content:    
# =============================================================================
# =============================================================================
    design_profile_tool_group_content = dbc.Card(
        dbc.CardBody(
            [
                design_profile_tool_group,
            ]
        ),
        className="mt-2",
    )
    return design_profile_tool_group_content
def design_profile_tool_layout_B():
# =============================================================================
# =============================================================================
# =============================================================================
# # # # Su_over_p_range_slider_object:
# =============================================================================
# =============================================================================
# =============================================================================
    Su_over_p_range_slider_object=dcc.RangeSlider(
        id="Su-over-p-ratio-range-slider", 
        min=0.15, 
        max=0.35, 
        step=0.01, 
        value=[0.18, 0.22],
        included=True,
        allowCross=False,
        pushable=0.01,
        updatemode='mouseup', # 'drag', 'mouseup'
        tooltip = {'always_visible': False, 'placement': 'bottomRight'},
        marks={a/100: {'label': str(a/100), 'style':{'font-size': 'x-small'}} for a in range(15,36,5)},
        className="mt-0 mb-0 ml-0 mr-0 pt-0 pb-4 pl-2 pr-2",
        )
    Su_over_p_range_slider_object_group = dbc.FormGroup(
        [
            dbc.Label("Su/p ratio", 
                      size = 'sm', 
                      html_for="Su-over-p-ratio-range-slider", 
                      id="Su-over-p-ratio-range-slider-label",
                      style={
                          'font-size': 'x-small',
                          'margin': '2px 0px 2px 0px',
                          'padding': '2px 0px 2px 10px', 
                          }, 
                      ),
            Su_over_p_range_slider_object,
        ],
        inline=True,
        style={
            'width': 'auto',
            # 'font-weight': 'bold',                  
            "color": '#515151',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '10px',
            'textAlign': 'left',
            'margin': '5px 0px 10px 0px',
            'padding': '5px 5px 5px 5px', 
            'background-color': 'white',
            'font-size': 'x-small',
        },    
    )
# =============================================================================
# =============================================================================
# # design_profile_plot_tool_group
# =============================================================================
# =============================================================================
    design_profile_tool_group = dbc.Row(
        [
# =============================================================================
# # "Finalize Design Profiles" Button:   
# =============================================================================
            dbc.Col(
                    dbc.Button(
                        "Finalize Design Profiles",
                        color="success", 
                        id="finalize-design-profile-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '8px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
# =============================================================================
# # "Download Soil Design Parameter Table" Button:   
# =============================================================================
            dbc.Col(
                html.Div([
                    dbc.Button(
                        "Download Soil Design Parameters",
                        color="primary", 
                        id="download-soil-design-parameters-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),
                    Download(id="soil-design-parameters-download"), 
                    ]),                    
                width='1',
                ),
# =============================================================================
# # Su_over_p_range_slider_object_group:   
# =============================================================================
            dbc.Col(
                Su_over_p_range_slider_object_group,
                width='2',
                ),
            ],
        style={
            'width': '100%',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '100px',
            'margin': '10px 0px 10px 0px',
            'padding': '10px 10px 10px 10px',    
            'background-color': 'lightgray',
        },            
        className="mt-0 mb-0")
# =============================================================================
# =============================================================================
# # # design_profile_plot_tool_group_content:    
# =============================================================================
# =============================================================================
    design_profile_tool_group_content = dbc.Card(
        dbc.CardBody(
            [
                design_profile_tool_group,
            ]
        ),
        className="mt-2",
    )
    return design_profile_tool_group_content
def fence_plots_tab_layout():
# =============================================================================
# =============================================================================
# # # W2E_fence_graph_tab_content:
# =============================================================================
# =============================================================================
    W2E_fence_graph_tab_content = dbc.Card(
        dbc.CardBody(
            [
                dcc.Loading(W2E_fence_graph(),color='red', type="cube"),
                ]
        ),
        className="mt-3",
    )
# =============================================================================
# =============================================================================
# # # S2N_fence_graph_tab_content:
# =============================================================================
# =============================================================================
    S2N_fence_graph_tab_content = dbc.Card(
        dbc.CardBody(
            [
                dcc.Loading(S2N_fence_graph(),color='red', type="cube"),
                ]
        ),
        className="mt-3",
    )
# =============================================================================
# =============================================================================
# =============================================================================
# # # # fence_and_data_plots_view_tabs    
# =============================================================================
# =============================================================================
# =============================================================================
    fence_graph_view_tabs = dbc.Tabs(
        [
            dbc.Tab(label='Fence Graph, West to East', 
                    tab_id='W2E-fence-graph-tab',
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(W2E_fence_plot_tool_layout(), width=12),
                                dbc.Col(W2E_fence_graph_tab_content, width=12),
                                ],
                            ),
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
                        "color": '#FFFFFF',
                        'background-color': '#943126',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        # 'font-weight': 'bold',                  
                        'font-size': '10px',                  
                        },
                    active_label_style={
                        "color": '#943126',
                        'background-color': '#E5E8E8',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        'font-size': '10px',                  
                        },
                    ),
            dbc.Tab(label='Fence Graph, South to North', 
                    tab_id='S2N-fence-graph-tab',
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(S2N_fence_plot_tool_layout(), width=12),
                                dbc.Col(S2N_fence_graph_tab_content, width=12),
                                ],
                            ),
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
                        "color": '#FFFFFF',
                        'background-color': '#943126',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        # 'font-weight': 'bold',                  
                        'font-size': '10px',                  
                        },
                    active_label_style={
                        "color": '#943126',
                        'background-color': '#E5E8E8',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '7px 7px 0px 0px',
                        'font-weight': 'bold', 
                        'font-size': '10px',                  
                        },
                    ),
            ],
                id="fence-graph-view-tabs",
                )    
    return fence_graph_view_tabs
def S2N_fence_plot_tool_layout():
# =============================================================================
# =============================================================================
# # S2N_fence_plot_tool_group
# =============================================================================
# =============================================================================
    S2N_fence_plot_tool_group = dbc.Row(
        [
            dcc.Store(
                id='clientside-S2N-fence-figure-store',
                data=[],
            ), 
            dbc.Col(            
                dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                    id='S2N-fence-clientside-store-loading-hidden-div', children="Loading Status", style={'display': 'none'})),            
                width='0',
                ),
            dbc.Col(
                    dbc.Button(
                        "Generate Graph",
                        color="success", 
                        id="generate-S2N-fence-plot-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },), 
                width='1',
                ),
            dbc.Col(dcc.Loading(change_S2N_fence_plot_bar_width_object(),type="default", fullscreen=False), width='2'),
            dbc.Col(change_S2N_fence_plot_text_size_object(),width='2'),
            ],
        style={
            'width': '100%',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '100px',
            'margin': '10px 0px 10px 0px',
            'padding': '10px 10px 10px 10px',    
            'background-color': 'lightgray',
        },            
        className="mt-0 mb-0")
# =============================================================================
# =============================================================================
# # # S2N_fence_plot_tool_group_content:    
# =============================================================================
# =============================================================================
    S2N_fence_plot_tool_group_content = dbc.Card(
        dbc.CardBody(
            [
                S2N_fence_plot_tool_group,
            ]
        ),
        className="mt-2",
    )
    return S2N_fence_plot_tool_group_content
def W2E_fence_plot_tool_layout():
# =============================================================================
# =============================================================================
# # W2E_fence_plot_tool_group
# =============================================================================
# =============================================================================
    W2E_fence_plot_tool_group = dbc.Row(
        [
            dcc.Store(
                id='clientside-W2E-fence-figure-store',
                data=[],
            ), 
            dbc.Col(            
                dcc.Loading(type='circle', fullscreen =False, color="red", children=html.Div(
                    id='W2E-fence-clientside-store-loading-hidden-div', children="Loading Status", style={'display': 'none'})),            
                width='0',
                ),
            dbc.Col(
                    dbc.Button(
                        "Generate Graph",
                        color="success", 
                        id="generate-W2E-fence-plot-button",
                        n_clicks=0,
                        block=False, 
                        size="lg",
                        style={
                            'width': '100%',
                            'height': '80px',
                            'max-height': '100%',
                            # 'font-weight': 'bold',                  
                            # "color": 'white',
                            'borderWidth': '0px',
                            'borderStyle': 'solid',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'font-size': '10px',
                            'vertical-align': 'middle',
                            'margin': '5px 0px 5px 5px',
                            'padding': '20px 15px 20px 15px',    
                            # 'background-color': 'red',
                        },),                     
                width='1',
                ),
            dbc.Col(dcc.Loading(change_W2E_fence_plot_bar_width_object(),type="default", fullscreen=False), width='2'),
            dbc.Col(change_W2E_fence_plot_text_size_object(),width='2'),
            ],
        style={
            'width': '100%',
            'borderWidth': '0px',
            'borderStyle': 'solid',
            'borderRadius': '100px',
            'margin': '10px 0px 10px 0px',
            'padding': '10px 10px 10px 10px',    
            'background-color': 'lightgray',
        },            
        className="mt-0 mb-0")
# =============================================================================
# =============================================================================
# # # W2E_fence_plot_tool_group_content:    
# =============================================================================
# =============================================================================
    W2E_fence_plot_tool_group_content = dbc.Card(
        dbc.CardBody(
            [
                W2E_fence_plot_tool_group,
            ]
        ),
        className="mt-2",
    )
    return W2E_fence_plot_tool_group_content
