import unittest


class MyTestCase(unittest.TestCase):
    def test_basic_behvior(self):
        screen_width = 600
        screen_height = 600

        number_of_tasks = 5
        importance = [1, 1, 1, 1, 1]
        time_expected = [1, 1, 1, 1, 1]
        urgency = [1, 1, 1, 1, 1]
        values = importance
        mouse_over_titles = ['one', 'two', 'three', 'four', 'five']
        x = [0, 100, 200, 200, 300]
        y = [0, 0, -100, 100, 0]
        labels = ['一', '二', '三', '四', '五']
        colors = ['red', 'red', 'orange', 'orange', 'red']
        shapes = ['text', 'box', 'circle', 'ellipse', 'database']
        html_file_name = 'nx.html'

        from pyvis.network import Network
        nt = Network(f'{screen_height}px', f'{screen_width}px')
        nt.add_nodes(
            list(range(number_of_tasks)),
            value=values,
            title=mouse_over_titles,
            shape=shapes,
            x=x,
            y=y,
            label=labels,
            color=colors,
        )
        nt.add_edge(0, 1, arrows='to', title='Ye', label='Yo', color='black', physics=False)
        nt.add_edge(1, 2, arrows='to', width=1, physics=False)
        nt.add_edge(1, 3, arrows='to', width=1, physics=False)
        nt.add_edge(2, 4, arrows='to', width=1, physics=False)
        nt.add_edge(3, 4, arrows='to', width=1, physics=False)
        nt.show(html_file_name)

    def test_task_visualization(self):
        screen_width = 600
        screen_height = 600

        tasks = [
            'Start Work',  # 0
            'Satisfy EGA requirements',  # 1
            'Arrival',  # 2
            'My Calendar',  # 3
            'Hotel',  # 4
            'Car',  # 5
            'Flight',  # 6
            'VISA',  # 7
            'Training',  # 8
            'PCR',  # 9
        ]
        number_of_tasks = len(tasks)
        importance = list(1 for _ in tasks)
        time_expected = [1, 1, 1, 1, 1]
        urgency = [1, 1, 1, 1, 1]
        values = importance
        mouse_over_titles = tasks
        x = [0, 100, 200, 200, 300]
        y = [0, 0, -100, 100, 0]
        labels = tasks
        colors = list('orange' for _ in tasks)
        shapes = list('box' for _ in tasks)
        html_file_name = 'nx.html'

        from pyvis.network import Network
        nt = Network(f'{screen_height}px', f'{screen_width}px')
        for n, task in enumerate(tasks):
            if n == 0:
                nt.add_node(n, task, 'box', 'orange', fixed={'y': True, 'x': True})
            else:
                nt.add_node(n, task, 'box', 'orange')
        nt.add_edge(1, 0, color='black', arrows='to')
        nt.add_edge(2, 0, color='black', arrows='to')
        nt.add_edge(3, 0, color='black', arrows='to')
        nt.add_edge(4, 2, color='black', arrows='to')
        nt.add_edge(5, 2, color='black', arrows='to')
        nt.add_edge(6, 5, color='black', arrows='to')
        nt.add_edge(6, 4, color='black', arrows='to')
        nt.add_edge(7, 1, color='black', arrows='to')
        nt.add_edge(8, 1, color='black', arrows='to')
        nt.add_edge(9, 1, color='black', arrows='to')
        nt.show_buttons(filter_=['physics', ])
        nt.show(html_file_name)

    def test_visualize_sabolyman_from_pickle_step_by_step(self):
        from sabolyman_parser.sabolyman_visualizer import SabolymanVisualizer
        import datetime

        file = '/Users/yamaka/Documents/Sabolyman/Taro Yamaka/chart_test.sb'
        # file = '/Users/yamaka/Documents/Sabolyman/Taro Yamaka/save.sb'
        target_card_id = '0793e348-51e4-434d-865c-3d96a2c1a792'

        parser = SabolymanVisualizer(file, target_card_id, )
        connections, tasks_map = parser.get_data_from_sabolyman_pickle()

        delta = datetime.timedelta(microseconds=1)
        cutoff_dates = sorted([t.get('date_created') - delta for t in tasks_map.values()])[-5:]

        for i, cutoff_date in enumerate(cutoff_dates):
            parser.save_as_html(cutoff_date=cutoff_date, i=i)

    def test_visualize_sabolyman_from_pickle(self):
        from sabolyman_parser.sabolyman_visualizer import SabolymanVisualizer

        pickle_path = '/Users/yamaka/Documents/Sabolyman/Taro Yamaka/chart_test.sb'
        target_card_id = '0793e348-51e4-434d-865c-3d96a2c1a792'

        parser = SabolymanVisualizer(pickle_path, target_card_id, )
        desktop = '/Users/yamaka/Desktop/'
        kwargs = {
            'folder_path': '',
            'configure_dynamically': True,
        }
        parser.save_as_html(**kwargs)
        parser.open_html_in_browser()


if __name__ == '__main__':
    unittest.main()
