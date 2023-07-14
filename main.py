import flet as ft

# importing version 1
from v1 import ColorBrowser1
# importing version 2
from v2 import ColorBrowser2


def main(page: ft.Page):
    """App's entry point."""

    page.title = "Colors Browser"
    # page.window_always_on_top = True

    # set the minimum width and height of the window.
    page.window_min_width = 245
    page.window_min_height = 406

    # Setting the theme of the page to light mode.
    page.theme_mode = "light"

    # set the width and height of the window.
    page.window_width = 562
    page.window_height = 720

    page.splash = ft.ProgressBar(visible=False)

    def change_theme(e):
        """It changes the theme of the page from dark to light and vice versa."""
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    def handle_nav_bar_change(e: ft.ControlEvent):
        """
        The handle_nav_bar_change function is called when the user clicks on a button in the nav bar.
        It clears all controls from the page, and then adds only one control to it: The screen that corresponds to
        the index of the button clicked.
        """
        page.controls.clear()
        page.add(screens[int(e.data)])

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

    page.appbar = ft.AppBar(
        title=ft.Text("Colors Browser", color="white"),
        center_title=True, bgcolor="blue",
        actions=[theme_icon_button],
    )

    page.navigation_bar = ft.NavigationBar(
        selected_index=1,
        destinations=[
            ft.NavigationDestination(
                icon=ft.icons.LOOKS_ONE_OUTLINED,
                selected_icon=ft.icons.LOOKS_ONE,
                label="Version 1"
            ),
            ft.NavigationDestination(
                icon=ft.icons.LOOKS_TWO_OUTLINED,
                selected_icon=ft.icons.LOOKS_TWO,
                label="Version 2"
            ),
        ],
        on_change=handle_nav_bar_change,
        )

    # Creating two versions of the page, one with the colors in a grid, and the other with the colors in a list.
    version_1 = ColorBrowser1()
    version_2 = ColorBrowser2(page)

    screens = [version_1, version_2]

    page.add(
        screens[1]
    )


# (running the app)
if __name__ == "__main__":
    ft.app(target=main)
    # OR flet.app(target=main, view=flet.WEB_BROWSER, port=5050) then open http://localhost:5050/
