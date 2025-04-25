"""
Report more  details about  imported items.
"""

import os
import logging

from beets import importer, util
from beets.plugins import BeetsPlugin
import confuse


class LogImport(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.config.add({
            'atlevel': 'INFO'
            })
        register = self.register_listener
        register("import_task_files", self.report_destination)

    def report_destination(self, task, session):
        level = getattr(logging, self.config['atlevel'].get().upper())
        self._log.log(level, "Imported tracks to the following files:")
        for item in task.items:
            self._log.log(level, item.path.decode('utf-8'))
