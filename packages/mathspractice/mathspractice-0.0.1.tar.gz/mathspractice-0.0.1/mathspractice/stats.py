import time

from flask import session


class Statistics:

    def __init__(self):
        self.stats = session.get('stats', {})

    def save(self):
        session['stats'] = self.stats
        session.modified = True
        session.permanent = True

    def correct(self, lesson: str, section: str) -> str:
        stats = self.get_stats(lesson, section)
        return f"{stats['correct']:,}"

    def incorrect(self, lesson: str, section: str) -> str:
        stats = self.get_stats(lesson, section)
        return f"{stats['incorrect']:,}"

    def seconds(self, lesson: str, section: str) -> str:
        stats = self.get_stats(lesson, section)
        return time.strftime('%H:%M:%S', time.gmtime(stats['seconds']))

    def success(self, lesson: str, section: str) -> str:
        stats = self.get_stats(lesson, section)
        if not stats['correct'] and not stats['incorrect']:
            percentage = 0
        else:
            percentage = stats['correct'] * 100 // (stats['correct'] + stats['incorrect'])
        return str(percentage)

    def get_stats(self, lesson: str, section: str) -> dict:
        if lesson not in self.stats:
            self.stats[lesson] = {}
        if section not in self.stats[lesson]:
            self.stats[lesson][section] = {'correct': 0, 'incorrect': 0, 'seconds': 0.0}
        return self.stats[lesson][section]

    def set_stats(self, lesson: str, section: str, stats: dict):
        if lesson not in self.stats:
            self.stats[lesson] = {}
        self.stats[lesson][section] = stats
