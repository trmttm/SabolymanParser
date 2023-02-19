def execute(kwargs):
    import os
    i = kwargs.get('i', None)
    folder_path = kwargs.get('folder_path', '')
    file_name = f'nx_{i}.html' if i is not None else f'nx.html'
    if folder_path == '':
        html_path = os.path.join(os.getcwd(), file_name)
    else:
        html_path = os.path.join(folder_path, file_name)
    kwargs.update({'html_file_name': html_path})
    return html_path
