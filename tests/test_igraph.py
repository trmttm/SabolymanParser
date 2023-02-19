import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from sabolyman_parser.sabolyman_visualizer import SabolymanVisualizer

        file = '/Users/yamaka/Documents/Sabolyman/Taro Yamaka/chart_test.sb'
        # file = '/Users/yamaka/Documents/Sabolyman/Taro Yamaka/save.sb'
        target_card_id = '0793e348-51e4-434d-865c-3d96a2c1a792'

        parser = SabolymanVisualizer(file, target_card_id, )
        edges, tasks_map = parser.get_data_from_sabolyman_pickle()

        display_as_an_image = True
        display_it_on_browser = False

        import igraph as ig
        import matplotlib.pyplot as plt
        shapes = ['rectangle', 'circle', 'hidden', 'triangle-up', 'triangle-down', ]

        ig.config["plotting.backend"] = "matplotlib"
        g = ig.Graph(n=len(tasks_map), edges=edges)
        g.vs['name'] = tuple(t.get('name') for t in tasks_map.values())
        g.vs["label"] = g.vs["name"]
        g.vs["color"] = ['green' if len(name) > 20 else 'yellow' for name in g.vs["name"]]
        g.vs["shape"] = [shapes[1] for (n, _) in enumerate(g.vs["name"])]
        g.vs["label_dist"] = [.2 for (n, _) in enumerate(g.vs["name"])]
        g.vs["label_color"] = ['red' if len(name) > 20 else 'blue' for name in g.vs["name"]]
        g.vs["label_size"] = [.5 + n * .2 for (n, _) in enumerate(g.vs["name"])]
        g.vs["size"] = [1 + n * .2 for (n, _) in enumerate(g.vs["name"])]

        def selected_method(i: int):

            return [
                lambda: g.layout_bipartite(),  # 0
                lambda: g.layout_circle(),  # 1
                lambda: g.layout_davidson_harel(),  # 2
                lambda: g.layout_drl(),  # 3
                lambda: g.layout_fruchterman_reingold(),  # 4
                lambda: g.layout_graphopt(),  # 5
                lambda: g.layout_grid(),  # 6
                lambda: g.layout_kamada_kawai(),  # 7
                lambda: g.layout_lgl(),  # 8
                lambda: g.layout_mds(),  # 9
                lambda: g.layout_random(),  # 10
                lambda: g.layout_reingold_tilford(),  # 11
                lambda: g.layout_reingold_tilford_circular(),  # 12
                lambda: g.layout_star(),  # 13
                lambda: g.layout_umap(),  # 14
            ][i]

        selected_layout = 7
        layout = selected_method(selected_layout)()

        fig, ax = plt.subplots()
        visual_style = {}
        visual_style["vertex_size"] = .5
        visual_style["vertex_label"] = g.vs["name"]
        visual_style["edge_width"] = 2
        visual_style["layout"] = layout
        visual_style["bbox"] = (300, 300)
        visual_style["margin"] = 2
        visual_style["target"] = ax
        ig.plot(g, **visual_style)

        if display_as_an_image:
            plt.show()

        if display_it_on_browser:
            import mpld3
            mpld3.show(fig)


if __name__ == '__main__':
    unittest.main()
