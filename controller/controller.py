from dataclasses import dataclass, field
from controller.action import Action


@dataclass
class ActionController:
    # actions that can be redone
    undo_stack: list[Action] = field(default_factory=list)
    # actions that can be redone
    redo_stack: list[Action] = field(default_factory=list)

    def execute(self, action: Action):
        action.execute()
        self.undo_stack.append(action)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        action = self.undo_stack.pop()
        action.undo()
        self.redo_stack.append(action)

    def redo(self):
        if not self.redo_stack:
            return
        action = self.redo_stack.pop()
        action.execute()
        self.undo_stack.append(action)
