import matplotlib
matplotlib.use("Agg")  # для серверів без GUI

import matplotlib.pyplot as plt
from io import BytesIO


def create_usd_chart(dates, rates):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, rates, marker='o', linestyle='-', color='b')
    plt.title('Курс USD/UAH за останні 7 днів')
    plt.xlabel('Дата')
    plt.ylabel('Курс продажу (UAH)')
    plt.grid(True)
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf
