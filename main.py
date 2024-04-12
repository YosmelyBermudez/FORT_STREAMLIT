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

    def on_dialog_result(e: ft.FilePickerResultEvent):
            if file_picker.result.files != None and file_picker.result.files != None:
                for f in file_picker.result.files:
                    print(f'File:{f.name}')
                    print(f'Path:{f.path}')
                

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