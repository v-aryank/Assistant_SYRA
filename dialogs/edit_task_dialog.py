# Edit Task Dialog Section

from dialogs.add_task_dialog import AddTaskDialog


class EditTaskDialog(AddTaskDialog):

    def __init__(
        self,
        title,
        date,
        start,
        end
    ):
        super().__init__()

        self.setWindowTitle(
            "Edit Task"
        )

        self.title_input.setText(
            title
        )
