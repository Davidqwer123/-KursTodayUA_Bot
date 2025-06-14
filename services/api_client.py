import requests
from config import EXCHANGE_API_URL
from datetime import datetime, timedelta


def get_exchange_rates():
    try:
        response = requests.get(EXCHANGE_API_URL)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def get_historical_rates(days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days - 1)

    dates = []
    usd_rates = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%d.%m.%Y')
        try:
            response = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_str}')
            data = response.json()

            for rate in data['exchangeRate']:
                if rate['currency'] == 'USD':
                    dates.append(current_date)
                    usd_rates.append(float(rate['saleRate'] if 'saleRate' in rate else rate['saleRateNB']))
                    break
        except:
            pass

        current_date += timedelta(days=1)

    return dates, usd_rates


class BinanceAPI:
    BASE_URL = "https://api.binance.com/api/v3"

    @staticmethod
    def get_crypto_price(symbol: str) -> float:
        """Отримати ціну криптовалюти (наприклад, BTCUSDT)"""
        response = requests.get(f"{BinanceAPI.BASE_URL}/ticker/price", params={"symbol": symbol})
        data = response.json()
        return float(data["price"])

    @staticmethod
    def convert_crypto(amount: float, from_asset: str, to_asset: str) -> float:
        """Конвертувати криптовалюту (BTC→USDT) або фіат (USDT→BTC)"""
        symbol = f"{from_asset.upper()}{to_asset.upper()}"
        price = BinanceAPI.get_crypto_price(symbol)

        if from_asset.upper() in ["BTC", "ETH"]:  # Якщо конвертуємо крипто → фіат
            return amount * price
        else:  # Якщо конвертуємо фіат → крипто
            return amount / price

    @staticmethod
    def get_usd_to_uah_rate() -> float:
        """Отримати поточний курс USD → UAH з ПриватБанку"""
        today = datetime.now().strftime('%d.%m.%Y')
        try:
            response = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={today}')
            data = response.json()
            for rate in data['exchangeRate']:
                if rate['currency'] == 'USD':
                    return float(rate['saleRate'] if 'saleRate' in rate else rate['saleRateNB'])
        except:
            pass
        return 0.0

    @staticmethod
    def get_crypto_to_uah(symbol: str) -> float:
        """Отримати курс криптовалюти (BTC/ETH) до гривні"""
        symbol = symbol.upper()
        if symbol not in ["BTC", "ETH"]:
            raise ValueError("Підтримуються лише BTC та ETH")

        crypto_usdt_price = BinanceAPI.get_crypto_price(f"{symbol}USDT")
        usd_to_uah = BinanceAPI.get_usd_to_uah_rate()
        return crypto_usdt_price * usd_to_uah

    @staticmethod
    def convert_to_uah(amount: float, symbol: str) -> float:
        """Конвертувати amount BTC/ETH у гривні"""
        rate = BinanceAPI.get_crypto_to_uah(symbol)
        return amount * rate



def get_all_bank_rates():
    all_rates = {}

    # ПриватБанк
    try:
        response = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
        privat_data = response.json()
        all_rates["ПриватБанк"] = privat_data
    except:
        all_rates["ПриватБанк"] = []

    # НБУ
    try:
        response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
        nbu_data = response.json()
        nbu_rates = [
            {
                "ccy": rate["cc"],
                "base_ccy": "UAH",
                "buy": f"{rate['rate']:.2f}",
                "sale": f"{rate['rate']:.2f}"
            }
            for rate in nbu_data if rate["cc"] in ["USD", "EUR"]
        ]
        all_rates["НБУ"] = nbu_rates
    except:
        all_rates["НБУ"] = []

    # Монобанк
    try:
        response = requests.get("https://api.monobank.ua/bank/currency")
        mono_data = response.json()
        mono_rates = []
        for item in mono_data:
            if item["currencyCodeA"] == 840 and item["currencyCodeB"] == 980:  # USD/UAH
                mono_rates.append({
                    "ccy": "USD",
                    "base_ccy": "UAH",
                    "buy": f"{item['rateBuy']:.2f}",
                    "sale": f"{item['rateSell']:.2f}"
                })
            elif item["currencyCodeA"] == 978 and item["currencyCodeB"] == 980:  # EUR/UAH
                mono_rates.append({
                    "ccy": "EUR",
                    "base_ccy": "UAH",
                    "buy": f"{item['rateBuy']:.2f}",
                    "sale": f"{item['rateSell']:.2f}"
                })
        all_rates["Монобанк"] = mono_rates
    except:
        all_rates["Монобанк"] = []

    return all_rates
