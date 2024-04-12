import pandas as pd
import random
from math import pi
import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, Container, Stack, colors, FilePicker, icons, Row
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons
)

def main(page: Page):
    page.title = 'Modelos Predictivos'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def create_text_animation():
        size = 40
        gap = 6
        duration = 2000

        c1 = colors.PINK_500
        c2 = colors.AMBER_500
        c3 = colors.LIGHT_GREEN_500
        c4 = colors.DEEP_PURPLE_500

        all_colors = [
            colors.AMBER_400,
            colors.AMBER_ACCENT_400,
            colors.BLUE_400,
            colors.BROWN_400,
            colors.CYAN_700,
            colors.DEEP_ORANGE_500,
            colors.CYAN_500,
            colors.INDIGO_600,
            colors.ORANGE_ACCENT_100,
            colors.PINK,
            colors.RED_600,
            colors.GREEN_400,
            colors.GREEN_ACCENT_200,
            colors.TEAL_ACCENT_200,
            colors.LIGHT_BLUE_500,
        ]

        parts = [
            (0, 0, c1), (0, 1, c1), (0, 2, c1), (0, 3, c1), (0, 4, c1),
            (1, 0, c1), (1, 2, c1), (2, 0, c1),
            (4, 0, c2), (4, 1, c2), (4, 2, c2), (4, 3, c2), (4, 4, c2),
            (5, 0, c2), (5, 4, c2), (6, 0, c2), (6, 4, c2), (7, 0, c2),
            (7, 1, c2), (7, 2, c2), (7, 3, c2), (7, 4, c2),
            (9, 0, c3), (9, 1, c3), (9, 2, c3), (9, 3, c3), (9, 4, c3),
            (10, 2, c3), (11, 2, c3), (10, 0, c3), (11, 1, c3), (11, 4, c3),
            (13, 0, c4), (14, 0, c4), (15, 0, c4), (14, 1, c4),
            (14, 2, c4), (14, 3, c4), (14, 4, c4),
        ]

        width = 16 * (size + gap)
        height = 5 * (size + gap)

        canvas = Stack(
            width=width,
            height=height,
            animate_scale=duration,
            animate_opacity=duration,
        )

        # Distribute parts randomly
        for i in range(len(parts)):
            canvas.controls.append(
                Container(
                    animate=duration,
                    animate_position=duration,
                    animate_rotation=duration,
                )
            )

        def randomize(e):
            random.seed()
            for i in range(len(parts)):
                c = canvas.controls[i]
                part_size = random.randrange(int(size / 2), int(size * 3))
                c.left = random.randrange(0, width)
                c.top = random.randrange(0, height)
                c.bgcolor = all_colors[random.randrange(0, len(all_colors))]
                c.width = part_size
                c.height = part_size
                c.border_radius = random.randrange(0, int(size / 2))
                c.rotate = random.randrange(0, 90) * 2 * pi / 360
            canvas.scale = 5
            canvas.opacity = 0.3
            page.update()

        def assemble(e):
            i = 0
            for left, top, bgcolor in parts:
                c = canvas.controls[i]
                c.left = left * (size + gap)
                c.top = top * (size + gap)
                c.bgcolor = bgcolor
                c.width = size
                c.height = size
                c.border_radius = 5
                c.rotate = 0
                i += 1
            canvas.scale = 1
            canvas.opacity = 1
            page.update()

        randomize(None)

        go_button = ElevatedButton("Go!", on_click=assemble)
        again_button = ElevatedButton("Again!", on_click=randomize)

        return canvas, go_button, again_button
    def pick_files_result(event: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

        if event.files:
            file = event.files[0]  # Assuming only one file is selected
            file_name = file.name
            selected_files.value = file_name
            selected_files.update()

            file_path = file.path
            extension = file_path.split('.')[-1].lower()

            if extension == 'csv':
                try:
                    # Read the CSV file into a pandas DataFrame
                    df = pd.read_csv(file_path)

                    # Convert the DataFrame to an HTML table
                    table_html = df.to_html()

                    # Display the HTML table in the interface
                    table_output = page.get_control_by_path('/hyperparameters/table_output')
                    table_output.value = table_html
                except Exception as e:
                    # Handle errors while processing the CSV file
                    table_output = page.get_control_by_path('/hyperparameters/table_output')
                    table_output.value = f"Error processing CSV file: {str(e)}"
            else:
                # Show a message if the file is not a CSV
                table_output = page.get_control_by_path('/hyperparameters/table_output')
                table_output.value = "File type not supported"

    if page.route == '/':
        # Content of the main view
        canvas, go_button, again_button = create_text_animation()
        page.views.append(
            View(
                '/',
                [
                    AppBar(title=Text('ARIMA-SARIMA Predictive Model'), bgcolor=colors.SURFACE_VARIANT),
                    canvas,
                    go_button,
                    again_button,
                    ElevatedButton('Go to Hyperparameters', on_click=lambda _: page.go('/hyperparameters'))
                ]
            )
        )
    elif page.route == '/hyperparameters':
        upload_button = ElevatedButton("Select File", on_click=lambda _: pick_files_dialog.pick_files())
        table_output = Text(value='', size=20, selectable=True)  # Text control for displaying the table
        page.views.append(
            View(
                '/hyperparameters',
                [
                    AppBar(title=Text('Hyperparameters'), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton('Home', on_click=lambda _: page.go('/')),
                    Row(
                        [
                            ElevatedButton(
                                'Pick Files',
                                icon=icons.UPLOAD_FILE,
                                on_click=lambda _: pick_files_dialog.pick_files()
                            ),
                            selected_files
                        ]
                    ),
                    upload_button,
                    table_output
                ]
            )
        )

    page.update()
    
    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    def route_change(event):
        page.views.clear()

    # Configure route and event handling
    page.on_route_change = route_change

    # Start the flet application
    page.go(page.route)

# Start the flet application with the main function
if __name__ == "__main__":
    ft.app(target=main)