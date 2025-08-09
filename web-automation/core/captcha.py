from twocaptcha import TwoCaptcha


class Captcha:
    token = '...'

    def __init__(self, site_key: str, page_url: str):
        self.captcha = TwoCaptcha(self.token)
        self.site_key = site_key
        self.page_url = page_url

    def solve_captcha(self):
        return self.captcha.solve_captcha(site_key=self.site_key, page_url=self.page_url)

    def callback_captcha(self, page, captcha_token: str):
        symbols = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        for symbol in symbols:
            try:
                resp = page.evaluate(f'() => ___grecaptcha_cfg.clients["0"]["{symbol}"]["{symbol}"]')
                if 'callback' in resp:
                    page.evaluate(
                        f'() =>___grecaptcha_cfg.clients["0"]["{symbol}"]["{symbol}"]["callback"]("{captcha_token}")')
                    # return True
            except Exception as ex:
                continue
