from config import USERNAME, PASSWORD


class LoginPage:

    def __init__(self, page):
        self.page = page

    def login(self):

        # Enter Credentials
        self.page.locator("input[name='login']").fill(USERNAME)
        self.page.locator("input[name='password']").fill(PASSWORD)

        # Login
        self.page.get_by_role("button", name="Log in").click()

        # Wait for Home Page
        self.page.locator(".o_main_navbar").wait_for(timeout=30000)

        print("Login Successfull")