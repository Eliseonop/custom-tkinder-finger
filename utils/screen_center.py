def screen_center(screen, app_width, app_height):
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    return screen.geometry(f"{app_width}x{app_height}+{x}+{y}")
