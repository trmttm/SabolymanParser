import sys

from sabolyman_parser import SabolymanVisualizer

if __name__ == '__main__':

    script_path = sys.argv[0]

    try:
        pickle_path = sys.argv[1]
    except IndexError:
        pickle_path = None

    try:
        target_card_id = sys.argv[2]
    except IndexError:
        target_card_id = None
    if (pickle_path is not None) and (target_card_id is not None):

        try:
            folder_path = sys.argv[3]
        except IndexError:
            folder_path = ''

        try:
            configure_dynamically = sys.argv[4]
        except IndexError:
            configure_dynamically = True
        if (type(configure_dynamically) == str) and ('false' in configure_dynamically.lower()):
            configure_dynamically = False

        parser = SabolymanVisualizer(pickle_path, target_card_id, )
        kwargs = {
            'folder_path': folder_path,
            'configure_dynamically': configure_dynamically,
        }

        parser.save_as_html(**kwargs)
        parser.open_html_in_browser()

    elif pickle_path is None:
        print(f'Invalid pickle path {pickle_path}.')
    elif target_card_id is None:
        print(f'Invalid target_card_id [{target_card_id}].')
