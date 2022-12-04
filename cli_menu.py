from crud import get_session, Company, Financial
from utils import search_company, cli_input_company

session = get_session("sqlite:///investor.db", echo=False)


def show_menu(title, options, navigation):
    print(title)
    for idx, option in enumerate(options):
        print("{} {}".format(idx, option))
    selection = None
    try:
        selection = int(input('Enter an option:'))
    except ValueError:
        print('Invalid option!')
        show_menu(title, options, navigation)
    if 0 <= selection <= len(options):
        navigate = navigation.get(selection)
        if navigate:
            navigate()
        else:
            print('Not implemented!')
            main_menu()
    else:
        print('Invalid option!')
        # show_menu(title, options, navigation)
        main_menu()


def exit_program():
    print('Have a nice day!')
    exit(0)


def top_10_menu():
    title = 'TOP TEN MENU'
    options = ['Back', 'List by ND/EBITDA', 'List by ROE', 'List by ROA']
    navigation = {0: main_menu, 1: list_by_nd_ebitda, 2: list_by_roe, 3: list_by_roa}
    show_menu(title, options, navigation)


def crud_menu():
    title = '\nCRUD MENU'
    options = ['Back', 'Create a company', 'Read a company',
               'Update a company', 'Delete a company', 'List all companies']
    navigation = {0: main_menu, 1: create_company, 2: read_company, 3: update_company,
                  4: delete_company, 5: list_all_companies}
    show_menu(title, options, navigation)


def main_menu():
    title = 'MAIN MENU'
    options = ['Exit', 'CRUD operations', 'Show top ten companies by criteria']
    navigation = {0: exit_program, 1: crud_menu, 2: top_10_menu}
    show_menu(title, options, navigation)


def safe_division(a, b):
    if a is None or b is None:
        return None
    try:
        return str(round(a / b, 2))
    except (ZeroDivisionError, ValueError):
        return None


# TOP 10 METHODS
def list_by_nd_ebitda():
    print("TICKER ND/EBITDA")

    companies = Financial.read_top_k_nd_ebitda(session)
    for c in companies:
        print("{} {}".format(c.ticker, safe_division(c.net_debt, c.ebitda)))

    session.close()
    main_menu()


def list_by_roe():
    print("TICKER ROE")

    companies = Financial.read_top_k_roe(session)
    for c in companies:
        print("{} {}".format(c.ticker, safe_division(c.net_profit, c.equity)))

    session.close()
    main_menu()


def list_by_roa():
    print("TICKER ROA")

    companies = Financial.read_top_k_roa(session)
    for c in companies:
        print("{} {}".format(c.ticker, safe_division(c.net_profit, c.assets)))

    session.close()
    main_menu()


# CRUD METHODS
def create_company():
    assets, \
        cash_equivalents, \
        ebitda, \
        equity, \
        liabilities, \
        market_price, \
        name, \
        net_debt, \
        net_profit, \
        sales, \
        sector, \
        ticker = cli_input_company(create_mode=True)

    Company.add(session, ticker, name, sector)
    Financial.add(session,
                  ticker,
                  ebitda,
                  sales,
                  net_profit,
                  market_price,
                  net_debt,
                  assets,
                  equity,
                  cash_equivalents,
                  liabilities)
    print('Company created successfully!')
    session.close()
    main_menu()


def update_company():
    selected_company = search_company(session)
    if selected_company is not None:
        assets, \
            cash_equivalents, \
            ebitda, \
            equity, \
            liabilities, \
            market_price, \
            name, \
            net_debt, \
            net_profit, \
            sales, \
            sector, ticker = cli_input_company()

        Financial.update(session,
                         selected_company.ticker,
                         ebitda,
                         sales,
                         net_profit,
                         market_price,
                         net_debt,
                         assets,
                         equity,
                         cash_equivalents,
                         liabilities)
        print('Company updated successfully!\n')
        session.close()
    main_menu()


def read_company():
    selected_company = search_company(session)
    if selected_company is not None:
        data = Financial.read(session, selected_company.ticker)

        market_price = data[0].market_price
        net_profit = data[0].net_profit
        ebitda = data[0].ebitda
        net_debt = data[0].net_debt
        assets = data[0].assets
        sales = data[0].sales
        equity = data[0].equity
        liabilities = data[0].liabilities

        print("{} {}".format(selected_company.ticker, selected_company.name))

        print('P/E = {}'.format(safe_division(market_price, net_profit)))
        print('P/S = {}'.format(safe_division(market_price, sales)))
        print('P/B = {}'.format(safe_division(market_price, assets)))
        print('ND/EBITDA = {}'.format(safe_division(net_debt, ebitda)))
        print('ROE = {}'.format(safe_division(net_profit, equity)))
        print('ROA = {}'.format(safe_division(net_profit, assets)))
        print('L/A = {}'.format(safe_division(liabilities, assets)))
        session.close()

    main_menu()


def delete_company():
    selected_company = search_company(session)
    if selected_company.ticker is not None:
        Company.delete(session, selected_company.ticker)
        Financial.delete(session, selected_company.ticker)
        print('Company deleted successfully!\n')
        session.close()
    main_menu()


def list_all_companies():
    print("COMPANY LIST")
    companies = Company.read_all(session)
    for c in companies:
        print("{} {} {}".format(c.ticker, c.name, c.sector))

    main_menu()
