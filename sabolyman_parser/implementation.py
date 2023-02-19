import pickle


def get_data_from_sabolyman_pickle(file, target_card_id, max_level: int = None):
    cards, sync_state = load_pickle(file)
    dto = parse_data(cards, sync_state, target_card_id, max_level)
    connections = dto.get('connections', ())
    tasks_map = dto.get('tasks_map', {})
    return connections, tasks_map


def load_pickle(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    cards = data.get('cards', {}).get('card', ())
    sync_state = data.get('sync_state', {})
    return cards, sync_state


def parse_data(cards: tuple, sync_state: dict, target_card_id: str, max_level=None, **kwargs):
    alias_actions, connections, id_, policy_action_node_id, tasks_map, level = handle_kwargs(**kwargs)
    if max_level is not None and max_level <= level:
        return create_data_transfer_object(connections, id_, tasks_map)
    level += 1
    for card in cards:
        if card_is_targeted_card(card, target_card_id):
            card_node_id, id_ = register_card(card, id_, policy_action_node_id, tasks_map)
            args = alias_actions, card, card_node_id, cards, connections, id_, sync_state, tasks_map, max_level, level
            id_ = handle_each_action_within_the_card(*args)

    return create_data_transfer_object(connections, id_, tasks_map)


def create_data_transfer_object(connections, id_, tasks_map):
    return {'connections': connections, 'tasks_map': tasks_map, 'id': id_}


def handle_each_action_within_the_card(alias_actions, card, card_node_id, cards, connections, id_, sync_state,
                                       tasks_map, max_level, level):
    for n, action in enumerate(get_actions(card)):
        if action_has_not_been_registered_yet(action, alias_actions):
            args = action, alias_actions, cards, connections, id_, n, sync_state, tasks_map, max_level, level
            action_node_id, id_ = register_action_and_recur_if_implemented(*args)
        else:
            action_node_id = mark_action_to_prevent_action_nodes_duplication_by_alias(action, alias_actions)

        connections.append((action_node_id, card_node_id))
    return id_


def action_has_not_been_registered_yet(action, alias_actions) -> bool:
    return action.get('id') not in alias_actions


def register_action_and_recur_if_implemented(action, alias_actions, cards, connections, id_, n, sync_state, tasks_map,
                                             max_level, level):
    action_node_id, id_ = register_action(action, alias_actions, id_, n, tasks_map)
    args = action, action_node_id, alias_actions, cards, connections, id_, sync_state, tasks_map, max_level, level
    id_ = recur_if_action_has_implementation_card(*args)
    return action_node_id, id_


def register_card(card, id_, policy_action_node_id, tasks_map):
    card_node_id = identify_card_node_id_first(id_, policy_action_node_id)
    id_ = register_card_if_it_is_the_goal_card_as_opposed_to_implementation_card(card, id_, tasks_map)
    return card_node_id, id_


def register(id_: int, tasks_map: dict, **kwargs):
    tasks_map[id_] = kwargs
    id_ += 1
    return id_


def register_action(action: dict, alias_actions: dict, id_, n, tasks_map: dict):
    action_node_id = id_
    data = {
        'client': action.get('client').get('name'),
        'color': action.get('color'),
        'completed_time': action.get('completed_time'),
        'date_created': action.get('date_created'),
        'dead_line': action.get('dead_line'),
        'id': action.get('id'),
        'is_done': action.get('is_done'),
        'name': f"{n} {action.get('name', '')}",
        'owner': action.get('owner').get('name'),
        'time_expected': action.get('time_expected'),
    }
    id_ = register(id_, tasks_map, **data)
    alias_actions[action.get('id')] = action_node_id
    return action_node_id, id_


def recur_if_action_has_implementation_card(action, action_node_id, alias_actions, cards, connections, id_, sync_state,
                                            tasks_map, max_level, level):
    implementation_card_id = action_has_implementation_card(action, sync_state)
    if implementation_card_id is not None:
        kw = {'tasks_map': tasks_map, 'id': id_, 'connections': connections,
              'policy_action_node_id': action_node_id, 'alias_actions': alias_actions, 'level': level}
        dto = parse_data(cards, sync_state, implementation_card_id, max_level, **kw)
        id_ = dto.get('id')
    return id_


def mark_action_to_prevent_action_nodes_duplication_by_alias(action: dict, alias_actions: dict):
    action_id = action.get('id')
    action_node_id = alias_actions[action_id]
    return action_node_id


def get_actions(card):
    return card.get('actions', {}).get('actions_state', ())


def identify_card_node_id_first(id_, policy_action_node_id):
    card_node_id = id_ if policy_action_node_id is None else policy_action_node_id
    return card_node_id


def register_card_if_it_is_the_goal_card_as_opposed_to_implementation_card(card: dict, id_, tasks_map: dict):
    if card_is_the_goal(id_):
        actions = card.get('actions').get('actions_state')
        data = {
            'client': get_current_client_name(actions),
            'color': card.get('color'),
            'completed_time': get_actions_completed_time(actions),
            'date_created': card.get('date_created'),
            'dead_line': get_actions_dead_line(actions),
            'id': card.get('id', ''),
            'is_done': get_if_actions_are_done(actions),
            'name': card.get('name', ''),
            'owner': card.get('owner').get('name'),
            'time_expected': get_actions_total_time_expected(actions),
        }
        id_ = register(id_, tasks_map, **data)
    return id_


def get_actions_completed_time(actions):
    if get_if_actions_are_done(actions):
        return max(a.get('completed_time') for a in actions)
    else:
        return None


def get_actions_total_time_expected(actions):
    time_expected = None
    for a in actions:
        if time_expected is None:
            time_expected = a.get('time_expected')
        else:
            time_expected += a.get('time_expected')
    return time_expected


def get_actions_dead_line(actions):
    return max(tuple(a.get('dead_line') for a in actions))


def get_if_actions_are_done(actions):
    return False not in tuple(a.get('is_done', False) for a in actions)


def get_current_client_name(actions):
    current_client = ''
    for action in actions:
        if not action.get('is_done'):
            current_client = action.get('client').get('name')
            break
    return current_client


def card_is_the_goal(id_):
    return id_ == 0


def card_is_targeted_card(card: dict, target_card_id: str) -> bool:
    return card.get('id', None) == target_card_id


def handle_kwargs(**kwargs):
    if kwargs == {}:
        tasks_map = {}
        id_ = 0
        connections = []
        policy_action_node_id = None
        alias_actions = {}
        level = 0
    else:
        tasks_map = kwargs.get('tasks_map')
        id_ = kwargs.get('id')
        connections = kwargs.get('connections')
        policy_action_node_id = kwargs.get('policy_action_node_id')
        alias_actions = kwargs.get('alias_actions')
        level = kwargs.get('level')
    return alias_actions, connections, id_, policy_action_node_id, tasks_map, level


def action_has_implementation_card(action_data: dict, sync_state: dict):
    action_id = action_data.get('id', None)
    return sync_state.get(action_id, None)
