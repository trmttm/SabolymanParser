import webbrowser


def execute(path):
    path_to_html = f'file:///{path}'
    webbrowser.open_new_tab(path_to_html)
