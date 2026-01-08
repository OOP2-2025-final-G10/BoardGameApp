class FrontendController:

    def __init__(self, driver):
        self.driver = driver

    def send_scroll_position(self, position):
        x, y = position

        self.driver.execute_script(
            "window.scrollTo(arguments[0], arguments[1]);", x, y)
