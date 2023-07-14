import os
from itertools import islice
import flet as ft

# Increasing the maximum message size that can be sent over the websocket.
os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "6000000"


class ColorBrowser1(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.expand = True

    def build(self):
        def batches(iterable, batch_size):
            """
            It takes an iterable and a batch size, and returns an iterator that yields batches of the iterable

            :param iterable: An iterable object (e.g. a list)
            :param batch_size: The number of items to process in each batch
            """
            iterator = iter(iterable)
            while batch := list(islice(iterator, batch_size)):
                yield batch

        # fetch all icon constants from colors.py module and store them in a dict(colors_dict)
        colors_dict = dict()
        list_started = False
        for key, value in vars(ft.colors).items():
            if key == "PRIMARY":
                # 'PRIMARY' is the first color-variable (our starting point)
                list_started = True
            if list_started:
                # when this list_started is True, we create new key-value pair in our dictionary
                colors_dict[key] = value

        # Creating a text field
        search_txt = ft.TextField(
            expand=1,
            hint_text="Enter keyword and press search button",
            autofocus=True,
            on_submit=lambda e: display_colors(e.control.value),
            tooltip="search field",
            label="Color Search Field"
        )

        def search_click(e):
            """
            Called when the search button is pressed, it displays the colors.
            """
            display_colors(search_txt.value)

        # Creating a row with a search text field and a search button.
        search_query = ft.Row(
            [search_txt, ft.FloatingActionButton(icon=ft.icons.SEARCH, on_click=search_click, tooltip="search")]
        )

        # Creating a grid view with 10 columns and 150 pixels as the maximum extent of each column.
        search_results = ft.GridView(
            expand=1, runs_count=10, max_extent=150, spacing=5, run_spacing=5, child_aspect_ratio=1,
        )
        status_bar = ft.Text()

        def copy_to_clipboard(e):
            """
            When the user clicks on a color, copy the color key to the clipboard

            :param e: The event object
            """

            color_key = e.control.data
            print("Copied to clipboard:", color_key)
            self.page.set_clipboard(e.control.data)
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Copied {color_key}"), open=True))

        def search_colors(search_term: str):
            """
            It takes a search term as an argument, and then loops through the colors_dict dictionary,
            checking if the search term is in the color name or the color value. If it is, it yields the color key

            :param search_term: The search term that the user entered
            :return color_key: str
            """

            for color_key, color_value in colors_dict.items():
                # the color_key has underscores while the color_value doesn't. We take this into consideration
                if search_term and (search_term in color_value or search_term in color_key.lower()):
                    yield color_key

        def display_colors(search_term: str):
            """
            It takes a search term, disables the search box, cleans the search results(grid view),
            and then loops through the search results in batches of 40, adding each color to the search results

            :param search_term: str
            """

            # disable the text field and the search button, and clean search results
            search_query.disabled = True
            self.update()
            search_results.clean()

            # Adding the colors to the grid view in batches of 40.
            for batch in batches(search_colors(search_term.lower()), 40):
                for color_key in batch:
                    flet_color_key = f"colors.{color_key}"

                    search_results.controls.append(
                        ft.TextButton(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(name=ft.icons.RECTANGLE, size=38, color=colors_dict[color_key], ),
                                        ft.Text(
                                            value=f"{colors_dict[color_key]}", size=14, width=100,
                                            no_wrap=True, text_align=ft.TextAlign.CENTER, color=colors_dict[color_key],
                                        ),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                alignment=ft.alignment.center,
                            ),
                            tooltip=f"{flet_color_key}\nClick to copy to a clipboard",
                            on_click=copy_to_clipboard,
                            data=flet_color_key,
                        )
                    )
                status_bar.value = f"Colors found: {len(search_results.controls)}"
                self.update()

            # It checks if the search results are empty, and if they are, it shows a snack bar some message
            if len(search_results.controls) == 0:
                # if no color was found containing the user's search term
                self.page.show_snack_bar(ft.SnackBar(ft.Text("No colors found"), open=True))
            search_query.disabled = False
            self.update()

        return ft.Column(
            [
                search_query,
                search_results,
                status_bar,
            ],
            expand=True,
        )


# (running the app)
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Flet Colors Browser V1"
        # page.window_always_on_top = True

        # set the width and height of the window.
        page.window_width = 562
        page.window_height = 720

        # Setting the theme of the page to light mode.
        page.theme_mode = "light"

        # set the minimum width and height of the window.
        page.window_min_width = 245
        page.window_min_height = 406

        def change_theme(e):
            page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
            theme_icon_button.selected = not theme_icon_button.selected
            page.update()

        # button to change theme_mode (from dark to light mode, or the reverse)
        theme_icon_button = ft.IconButton(
            ft.icons.DARK_MODE,
            selected_icon=ft.icons.LIGHT_MODE,
            icon_color=ft.colors.BLACK,
            icon_size=35,
            tooltip="change theme",
            on_click=change_theme,
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK, "selected": ft.colors.WHITE},
            ),
        )

        # Creating an AppBar object and assigning it to the page.appbar attribute.
        page.appbar = ft.AppBar(
            title=ft.Text("Colors Browser V1", color="white"),
            center_title=True,
            bgcolor="blue",
            actions=[theme_icon_button],
        )

        # Creating an instance of the ColorBrowser1 class.
        version_1 = ColorBrowser1()

        # adds the color browser to the page
        page.add(
            version_1
        )


    ft.app(target=main)
    # OR flet.app(target=main, view=flet.WEB_BROWSER, port=5050) then open http://localhost:5050/
