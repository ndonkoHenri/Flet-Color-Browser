import flet as ft


# It's a container(or list-item) that has a descriptive text in it, and when clicked,
# it copies the text to the clipboard
class Tile(ft.Container):
    def __init__(self, tile_text, color, page):
        super().__init__()
        self.text = ft.Text(tile_text, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, italic=True, )
        self.color_text = f"colors.{tile_text}"
        self.bgcolor = color
        self.expand = True
        self.height = 40
        self.content = self.text
        self.page = page
        self.tooltip = "Click to copy to Clipboard"

    def _build(self):
        def click_event(e):
            """
            It copies the color's text to the clipboard.

            :param e: The event that triggered the function
            """
            print("Copied to clipboard:", self.color_text)
            self.page.set_clipboard(self.color_text)
            self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Copied {self.color_text}!")))

        self.on_click = click_event

        return self


class ColorBrowser2(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.expand = True

        # A reference to the page object that is passed to the constructor of the class.
        self.page = page

        # Creating a reference to the Tabs object that will be created later.
        self.displayed_tabs = ft.Ref[ft.Tabs]()

        # A list of colors that will be used to create the tabs.
        self.original_tab_names = [
            'RED', "BLACK", "WHITE", 'PINK', 'PURPLE', 'DEEP_PURPLE', 'INDIGO', 'BLUE', 'LIGHT_BLUE', "GREY",
            'CYAN', 'TEAL', 'GREEN', 'LIGHT_GREEN', 'LIME', 'YELLOW', 'AMBER', "ORANGE", 'DEEP_ORANGE',
            'BROWN', 'BLUE_GREY'
        ]

    def build(self):

        # Getting all the colors from the colors module.
        list_started = False
        all_flet_colors = list()
        for key in vars(ft.colors).keys():
            if key == "PRIMARY":
                list_started = True
            if list_started:
                all_flet_colors.append(key)

        def create_tabs(tab_names: list) -> list:
            """
            It takes a list of strings where each string represents the name of a tab to be shown, and returns a list
            of tabs, each tab containing a list of tiles(containers) having a specific background color associated with the text in it.

            :param tab_names: list of strings that will be used to create the tabs
            :type tab_names: list
            :return: A list of tabs
            """
            created_tabs = []
            found = []
            # iterate over the tab_names(list containing the tabs to be shown)
            for tab_name in tab_names:
                tab_content = ft.ListView()
                for color in all_flet_colors:
                    tile_bgcolor = color.lower().replace("_", "")
                    tile_content = Tile(color, tile_bgcolor, self.page)
                    # Checking if the color starts with the tab_name and if the tab_name is in the color.
                    if (tab_name in color) and color.startswith(tab_name):
                        tab_content.controls.append(tile_content)
                        found.append(color)

                # Add a tab with the name of the color and the content of the tab is a list of tiles.
                # Also remove underscores from the tab's name.
                created_tabs.append(ft.Tab(tab_name.replace("_", " "), content=tab_content, ))

            # Creating a tab called "OTHERS" and adding all the colors that were not added to any other tab to it.
            others = [i for i in all_flet_colors if i not in found]
            others_content = ft.ListView(
                controls=[Tile(x, x.lower().replace("_", ""), self.page) for x in others]
            )
            created_tabs.append(ft.Tab("OTHERS", content=others_content))

            return created_tabs

        # self.displayed_tabs.current.tabs = create_tabs(self.original_tab_names)

        def filter_tabs(e: ft.ControlEvent):
            """
            If the text in the search field is "ALL", show all tabs. If the search field is not empty, show only the
            tabs that contain the search term.

            :param e: ControlEvent
            :type e: ControlEvent
            """
            # Making the progress bar visible.
            self.page.splash.visible = True
            self.page.update()
            filtered_tab_names = []

            if search_field.value and search_field.value.lower().strip() == "all":
                filtered_tab_names = self.original_tab_names
            else:
                for tab_name in self.original_tab_names:
                    if search_field.value and search_field.value.lower().strip() in tab_name.lower().replace("_", " "):
                        filtered_tab_names.append(tab_name)

            if filtered_tab_names:
                # Removing all the tabs from the Tabs object.
                self.displayed_tabs.current.clean()
                # self.page.update()

                # Updating the tabs of the Tabs object.
                self.displayed_tabs.current.tabs = create_tabs(filtered_tab_names)
                self.displayed_tabs.current.update()
                return

            self.page.update()

        # creating a field which will t=help the user search for specific tabs
        search_field = ft.TextField(
            label="Search Tabs...",
            prefix_icon=ft.icons.SEARCH,
            on_submit=filter_tabs,
            border_radius=50,
            suffix=ft.IconButton(
                icon=ft.icons.CHECK,
                bgcolor=ft.colors.INVERSE_PRIMARY,
                icon_color=ft.colors.ERROR,
                on_click=filter_tabs
            ),
            helper_text="Tip: Enter 'ALL' to show all the tabs",
            height=70, width=450,
            keyboard_type=ft.KeyboardType.TEXT,
            capitalization=ft.TextCapitalization.CHARACTERS,
        )

        return ft.Column(
            controls=[
                search_field,
                ft.Tabs(
                    ref=self.displayed_tabs,
                    expand=True,
                    tabs=create_tabs(self.original_tab_names)
                )
            ]
        )


# (running the app)
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Flet Colors Browser V2"
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
            ft.icons.DARK_MODE, selected_icon=ft.icons.LIGHT_MODE,
            icon_color=ft.colors.BLACK,
            icon_size=35,
            tooltip="change theme",
            on_click=change_theme,
            style=ft.ButtonStyle(color={"": ft.colors.BLACK, "selected": ft.colors.WHITE}),
        )

        # Creating an AppBar object and assigning it to the page.appbar attribute.
        page.appbar = ft.AppBar(
            title=ft.Text("Colors Browser V2", color="white"),
            center_title=True,
            bgcolor="blue",
            actions=[theme_icon_button],
        )

        # Creating an instance of the ColorBrowser2 class and passing the page object to it.
        version_2 = ColorBrowser2(page)

        # adds the color browser to the page
        page.add(
            version_2
        )


    ft.app(target=main)
    # OR flet.app(target=main, view=flet.WEB_BROWSER, port=5050) then open http://localhost:5050/
