from . import identify_html_file_name
from . import open_file_by_browser
from . import open_html_in_webbrowser
from . import save_as_html
from .implementation import get_data_from_sabolyman_pickle


class SabolymanVisualizer:
    def __init__(self, file, target_card_id, max_level: int = None):
        self._file = file
        self._target_card_id = target_card_id
        self._node_id = 0
        self._max_level = max_level

        self._last_saved_html_path = None

    def get_data_from_sabolyman_pickle(self):
        return get_data_from_sabolyman_pickle(self._file, self._target_card_id, self._max_level)

    def save_as_html(self, **kwargs):
        data = self.get_data_from_sabolyman_pickle()
        self._last_saved_html_path = identify_html_file_name.execute(kwargs)
        save_as_html.execute(data, **kwargs)

    def open_html_in_browser(self):
        open_html_in_webbrowser.execute(self._last_saved_html_path)
