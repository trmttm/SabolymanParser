from pyvis.network import Network


def execute(data, **kwargs):
    connections, tasks_map = data
    cutoff_date_created = kwargs.get('cutoff_date', None)
    configure_dynamically = kwargs.get('configure_dynamically', False)
    fo = ['nodes', 'edges', 'layout', 'interaction', 'manipulation', 'physics', 'selection', 'renderer']
    filter_option = kwargs.get('filter_option', [fo[2], fo[5], ])

    color_node_done = kwargs.get('color_node_done', 'grey')
    color_node_not_done = kwargs.get('color_node_not_done', 'orange')
    color_font_my_ball = kwargs.get('color_font_my_ball', 'black')
    color_font_their_ball = kwargs.get('color_font_their_ball', 'yellow')
    color_font_hidden = kwargs.get('color_font_hidden', 'white')
    color_node_hidden = kwargs.get('color_node_hidden', 'white')
    color_node_goal = kwargs.get('color_node_goal', 'red')
    color_edge_hidden = kwargs.get('color_edge_hidden', 'white')
    color_edge_default = kwargs.get('color_edge_default', 'black')
    my_name = kwargs.get('my_name', 'Taro Yamaka')
    html_file_name = kwargs.get('html_file_name', f'nx.html')
    screen_width = kwargs.get('screen_width', 800)
    screen_height = kwargs.get('screen_height', 800)
    print(f'{screen_width} x {screen_height}')

    nt = Network(f'{screen_height}px', f'{screen_width}px')
    edge_options = [
        'dynamic',  # 0
        'continuous',  # 1
        'discrete',  # 2
        'diagonalCross',  # 3
        'straightCross',  # 4
        'horizontal',  # 5
        'vertical',  # 6
        'curvedCW',  # 7
        'curvedCCW',  # 8
        'cubicBezier',  # 9
    ]
    nt.set_edge_smooth(edge_options[2])
    hierarchical = """const options = {
  "layout": {
    "hierarchical": {
      "enabled": true,
      "levelSeparation": 280,
      "nodeSpacing": 1,
      "direction": "LR",
      "sortMethod": "directed"
    }
  },
  "physics": {
    "enabled": true,
    "hierarchicalRepulsion": {
      "centralGravity": 0,
      "avoidOverlap": null
    },
    "minVelocity": 0.75,
    "solver": "hierarchicalRepulsion"
  }
}"""
    options = hierarchical
    if not configure_dynamically:
        nt.set_options(options)
    hidden_nodes = set()
    for n, task_data in tasks_map.items():
        task_name = task_data.get('name')
        color = color_node_done if task_data.get('is_done') else color_node_not_done

        if (cutoff_date_created is None) or (task_data.get('date_created') < cutoff_date_created):
            nt.font_color = color_font_my_ball if task_data.get('owner') == my_name else color_font_their_ball
        else:
            # Virtually hide to keep canvas zoom consistent
            nt.font_color = color_font_hidden
            color = color_node_hidden
            hidden_nodes.add(n)

        if n == 0:
            nt.add_node(n, task_name, 'box', color_node_goal, fixed={'y': True, 'x': True}, x=30 * n, y=20 * n)
        else:
            nt.add_node(n, task_name, 'box', color, x=30 * n, y=20 * n)
    for connection in connections:
        from_, to_ = connection
        edge_color = color_edge_hidden if (from_ in hidden_nodes) or (to_ in hidden_nodes) else color_edge_default
        nt.add_edge(from_, to_, color=edge_color, arrows='to', physics=True)
    if configure_dynamically:
        nt.show_buttons(filter_=filter_option)
    try:
        nt.show(html_file_name)
    except FileNotFoundError:
        # ignore
        pass
