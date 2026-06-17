class RoutingRule:
    def __init__(self, event_type_pattern, target_queue, source_filter=None,
                 conditions=None, transform=None, priority=100):
        pass


class EventRouter:
    def __init__(self, rules, fanout=False, dead_letter_queue=None):
        pass

    def route(self, event):
        raise NotImplementedError

    def add_rule(self, rule):
        raise NotImplementedError

    def _matches(self, rule, event):
        raise NotImplementedError
