from pathlib import Path

from nicegui import ui


class AuthorizedKeysDialog(ui.dialog):

    def open(self) -> None:
        super().open()
        path = Path('~/.ssh/authorized_keys').expanduser()
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},
            {'name': 'type', 'label': 'Type', 'field': 'type', 'align': 'left'},
            {'name': 'key', 'label': 'Key', 'field': 'key', 'align': 'left'},
        ]
        rows = [
            {'name': line.split()[2], 'type': line.split()[0], 'key': line.split()[1]}
            for line in path.read_text().splitlines()
            if line.split() and not line.startswith('#')
        ]
        self.clear()
        with self.props('full-width'), ui.card():
            ui.label('Authorized keys').classes('text-xl')
            table = ui.table(columns=columns, rows=rows, row_key='name', selection='single').classes('w-full')
            with table.add_slot('bottom'), ui.row().classes('items-center mt-4 w-full'):
                def save_keys():
                    path.write_text(''.join(f'{row["type"]} {row["key"]} {row["name"]}\n' for row in table.rows))

                def add_key():
                    words = key.value.split()
                    assert len(words) == 3
                    table.add_rows({'name': words[2], 'type': words[0], 'key': words[1]})
                    key.value = None
                    save_keys()

                def remove_key():
                    table.remove_rows(*table.selected)
                    save_keys()

                key = ui.input('New key').props('outlined').on('keydown.enter', add_key).classes('flex-grow')
                ui.button('Add', on_click=add_key).bind_enabled_from(key, 'value')
                ui.button('Remove', on_click=remove_key).bind_enabled_from(table, 'selected', bool)
