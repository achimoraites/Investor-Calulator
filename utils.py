from crud import Company


def cli_input_company(create_mode=False):
    ticker = None
    name = None
    sector = None
    if create_mode:
        ticker = input("Enter ticker (in the format 'MOON'):\n")
        name = input("Enter company (in the format 'Moon Corp'):\n")
        sector = input("Enter industries (in the format 'Technology'):\n")
    ebitda = float_input('ebitda')
    sales = float_input('sales')
    net_profit = float_input('net profit')
    market_price = float_input('market price')
    net_debt = float_input('net debt')
    assets = float_input('assets')
    equity = float_input('equity')
    cash_equivalents = float_input('cash equivalents')
    liabilities = float_input('liabilities')
    return assets, cash_equivalents, ebitda, equity, liabilities, market_price, name, net_debt, net_profit, sales, \
        sector, ticker


def float_input(field):
    return float(input("Enter {} (in the format '987654321'):\n".format(field)))


def search_company(session):
    search_term = input("Enter company name:\n")
    results = Company.read(session, search_term)
    selected_company = None
    if len(results) is 0:
        print("Company not found!\n")
    else:
        for idx, option in enumerate(results):
            print("{} {}".format(idx, option.name))
        selection = int(input("Enter company number:\n"))
        selected_company = results[selection]

    return selected_company

