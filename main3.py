import pandas as pd
import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)


def main(page: Page):
    page.title = 'Modelos Predictivos'

    def on_dialog_result(e: FilePickerResultEvent):
            if file_picker.result.files != None and file_picker.result.files != None:
                for f in file_picker.result.files:
                    print(f'File:{f.name}')
                    print(f'Path:{f.path}')
    def dataframe(event):
        if file_picker.result: # Assuming only one file is selected
            file_path = file_picker.result.path
            try:
                    # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(file_path)

                    # Convert the DataFrame to an HTML table
                table_html = df.to_html()

                # Crear un control de texto para mostrar la tabla HTML
                table_output = Text(value=table_html, size=16, selectable=True)

                    # Display the HTML table in the interface
                table_output = page.go('/hyperparameters/table_output')
            except Exception as e:
                    # Handle errors while processing the CSV file
                table_output = page.go('/hyperparameters/table_output')
                print('ERROR')
            else:
                # Show a message if the file is not a CSV
                table_output = page.go('/hyperparameters/table_output')
                print(f"File type not supported")
        page.update()

    file_picker= ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    def route_change(route):
        page.views.clear()

        page.views.append(
            View(
                '/',
                [
                    AppBar(title=Text('App PRED MOD'), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton('Visitar la tienda', on_click=lambda _: page.go('/tienda'))
                ]
            )
        )

        if page.route == '/tienda':
            page.views.append(
                View(
                    '/tienda',
                    [
                        AppBar(title=Text('Tienda'), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton('Inicio', on_click=lambda _: page.go('/')),
                        Row(
            [
                ElevatedButton(
                    "Pick files",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                ),

                ElevatedButton("Show Table", on_click=dataframe),
                table_output

            ]
        )
                    ]
                )
            )
        
        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)