import dash
from dash import dcc, html 
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('carpetasFGJ_2023.csv')  # Asegúrate de que el nombre del archivo sea correcto

# Filtrar para asegurar que todas las filas tengan coordenadas
df = df.dropna(subset=['latitud', 'longitud'])

# Crear la figura del mapa de calor
fig = px.density_mapbox(df, lat='latitud', lon='longitud', 
                        radius=10, 
                        center={"lat": 19.36, "lon": -99.133209},  # Centro en la Ciudad de México
                        zoom=10, 
                        mapbox_style="mapbox://styles/mapbox/light-v10")  # Puedes cambiar el estilo del mapa aquí

fig.update_layout(mapbox_accesstoken='pk.eyJ1IjoiYW1hcmFyaWsiLCJhIjoiY2xwbTZybjVpMDZieDJxbzl5Z2t4a2NvMiJ9.qvB79lcM85Ak0TUrbDYgwA')

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Lista de tipos de crimen únicos
tipos_de_crimen = df['delito'].unique()

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Mapa de Calor de Criminalidad en la Ciudad de México", className='h1'),

    # Dropdown para seleccionar el tipo de crimen
    dcc.Dropdown(
        id='crime-dropdown',
        options=[{'label': crime, 'value': crime} for crime in tipos_de_crimen],
        value=tipos_de_crimen[0],  # Valor predeterminado
        style={'width': '50%'},  # Ajusta el ancho de la barra de selección
        className='dropdown'
    ),

    # Mapa de calor
    dcc.Graph(id='crime-heatmap', figure=fig, className='graph')
], className='body')

# Callback para actualizar el mapa según la selección del usuario
@app.callback(
    Output('crime-heatmap', 'figure'),
    [Input('crime-dropdown', 'value')]
)
def update_map(selected_crime):
    # Filtrar el DataFrame según el tipo de crimen seleccionado
    filtered_df = df[df['delito'] == selected_crime]

    # Crear una nueva figura de mapa de calor con los datos filtrados
    updated_fig = px.density_mapbox(filtered_df, lat='latitud', lon='longitud', 
                                    radius=10, 
                                    center={"lat": 19.36, "lon": -99.133209},
                                    zoom=10, 
                                    mapbox_style="mapbox://styles/mapbox/light-v10")

    updated_fig.update_layout(mapbox_accesstoken='pk.eyJ1IjoiYW1hcmFyaWsiLCJhIjoiY2xwbTZybjVpMDZieDJxbzl5Z2t4a2NvMiJ9.qvB79lcM85Ak0TUrbDYgwA')

    return updated_fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=80)
