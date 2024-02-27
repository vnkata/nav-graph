import dash
import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, DashProxy, NoOutputTransform, BlockingCallbackTransform, MultiplexerTransform, \
    ServersideOutputTransform, TriggerTransform
from dash.dependencies import ClientsideFunction
from dash_extensions.enrich import Input, Output
from components import html_ids, sockets, footer, cache, header

# external JavaScript files
external_scripts = ["https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"]

# external CSS stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]

dash_app = DashProxy(
    __name__,
    use_pages=True, compress=False, serve_locally=True,
    long_callback_manager=cache.long_callback_manager,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    transforms=[
        TriggerTransform(),
        NoOutputTransform(),
        MultiplexerTransform(),
        ServersideOutputTransform(),
        BlockingCallbackTransform()
    ],
    update_title=None,
    external_scripts=external_scripts, external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

dash_app.title = "Navigation Graph @ nphau"

dash_app.renderer = '''
var renderer = new DashRenderer({
    request_pre: (payload) => {
        // print out payload parameter
        console.log(payload);
    },
    request_post: (payload, response) => {
        // print out payload and response parameter
        console.log(payload);
        console.log(response);
    }
})
'''

dash_app.layout = dbc.Container([
    header.create_header(dash_app),
    dash.page_container,
    footer.create_footer(),
    # The memory store reverts to the default on every page refresh
    dcc.Store(id=html_ids.STORE_STARTED_NODE, data={}),
    dcc.Store(id=html_ids.STORE_SOCKET_STARTED_NODE, data="string"),
    dcc.Store(id=html_ids.STORE_PREV_SOCKET_STARTED_NODE, data="string"),
    dcc.Store(id=html_ids.STORE_UUID_FILES),
    dcc.Store(id=html_ids.STORE_ASSERTIONS, data=[]),
    dcc.Store(id=html_ids.STORE_CURRENT_ASSERTION_INDEX, data=-1),
    dcc.Input(id=sockets.WS_INPUT, style={"display": "none"}),
    sockets.create_web_socket()
], fluid=True)

# region clientside_callback
dash_app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="onUserSelectNode"),
    Input(html_ids.ID_GRAPH, 'selected_node'),
    prevent_initial_call=True
)

dash_app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="onSocketListener"),
    Output(html_ids.STORE_SOCKET_STARTED_NODE, "data"),
    Input(sockets.WS_SERVER, "message")
)

# endregion

if __name__ == "__main__":
    dash_app.run_server(port=5050, debug=True, dev_tools_hot_reload=True)
