from selenium import webdriver

class WebScraper:

    def __init__(self, game_url):
        self.driver = webdriver.Safari()
        self.driver.maximize_window()
        self.open_url(game_url)

    def open_url(self, url):
        self.driver.get(url)

    @staticmethod
    def print_error_output_screenshot(driver, e, error_message, file_name):
        print(error_message)
        driver.save_screenshot(file_name + ".png")
        raise e

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
