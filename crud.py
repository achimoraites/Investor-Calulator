from sqlalchemy import Column, Float, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CompanyTable(Base):
    __tablename__ = "companies"

    ticker = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)


class FinancialTable(Base):
    __tablename__ = "financial"

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


def get_session(db, echo=True):
    engine = create_engine(db, echo=echo)
    Base.metadata.create_all(engine)
    Session: sessionmaker = sessionmaker(bind=engine, autoflush=False)
    return Session()


class Company:

    @staticmethod
    def add(db_session, ticker, name, sector):
        db_session.add(CompanyTable(ticker=ticker, name=name, sector=sector))
        db_session.commit()

    @staticmethod
    def update(db_session, ticker, name, sector):
        query = db_session.query(CompanyTable)
        query_filter = query.filter(CompanyTable.ticker == ticker)

        fields = {
            "name": name,
            "sector": sector
        }

        query_filter.update(fields)
        db_session.commit()

    @staticmethod
    def read(db_session, search_term):
        query = db_session.query(CompanyTable)
        results = list()
        for row in query.filter(CompanyTable.name.contains(search_term)):
            results.append(row)
        return results

    @staticmethod
    def read_all(db_session):
        query = db_session.query(CompanyTable)
        results = list()
        for row in query.order_by(CompanyTable.ticker.asc()):
            results.append(row)
        return results

    @staticmethod
    def delete(db_session, ticker):
        query = db_session.query(CompanyTable)
        query_filter = query.filter(CompanyTable.ticker == ticker)

        query_filter.delete()
        db_session.commit()


class Financial:

    @staticmethod
    def add(db_session, ticker, ebitda, sales, net_profit, market_price, net_debt, assets,
            equity, cash_equivalents, liabilities):
        db_session.add(FinancialTable(ticker=ticker,
                                      ebitda=ebitda,
                                      sales=sales,
                                      net_profit=net_profit,
                                      market_price=market_price,
                                      net_debt=net_debt,
                                      assets=assets,
                                      equity=equity,
                                      cash_equivalents=cash_equivalents,
                                      liabilities=liabilities))
        db_session.commit()

    @staticmethod
    def update(db_session, ticker, ebitda, sales, net_profit, market_price, net_debt, assets,
               equity, cash_equivalents, liabilities):
        query = db_session.query(FinancialTable)
        query_filter = query.filter(FinancialTable.ticker == ticker)
        fields = {
            "ebitda": ebitda,
            "sales": sales,
            "net_profit": net_profit,
            "market_price": market_price,
            "net_debt": net_debt,
            "assets": assets,
            "equity": equity,
            "cash_equivalents": cash_equivalents,
            "liabilities": liabilities
        }

        query_filter.update(fields)
        db_session.commit()

    @staticmethod
    def read(db_session, ticker):
        query = db_session.query(FinancialTable)
        results = list()
        for row in query.filter(FinancialTable.ticker == ticker):
            results.append(row)
        return results

    @staticmethod
    def read_top_k_nd_ebitda(db_session, k=10):

        query = db_session.query(FinancialTable)
        results = list()
        for row in query\
                .filter(FinancialTable.ebitda.isnot(None)) \
                .filter(FinancialTable.net_debt.isnot(None)) \
                .order_by((FinancialTable.net_debt / FinancialTable.ebitda).desc()).limit(k):
            results.append(row)
        return results

    @staticmethod
    def read_top_k_roe(db_session, k=10):

        query = db_session.query(FinancialTable)
        results = list()
        for row in query\
                .filter(FinancialTable.net_profit.isnot(None)) \
                .filter(FinancialTable.equity.isnot(None)) \
                .order_by((FinancialTable.net_profit / FinancialTable.equity).desc()).limit(k):
            results.append(row)
        return results

    @staticmethod
    def read_top_k_roa(db_session, k=10):

        query = db_session.query(FinancialTable)
        results = list()
        for row in query\
                .filter(FinancialTable.net_profit.isnot(None)) \
                .filter(FinancialTable.assets.isnot(None)) \
                .order_by((func.round(FinancialTable.net_profit / FinancialTable.assets, 2)).desc()).limit(k):
            results.append(row)
        return results

    @staticmethod
    def delete(db_session, ticker):
        query = db_session.query(FinancialTable)
        query_filter = query.filter(FinancialTable.ticker == ticker)

        query_filter.delete()
        db_session.commit()


