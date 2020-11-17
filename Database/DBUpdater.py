import psycopg2 as pg
import pandas as pd
from datetime import datetime
import re

class DBUpdater:
    def __init__(self):
        """생성자: Postgresql DB 연결 및 종목코드 딕셔너리 생성"""
        try:
            conn_string = "host=192.168.100.3 dbname=priapus user=postgres password=Sercre1862^^ port=5433"
            self.conn = pg.connect(conn_string)

            self.codes = dict()
            self.update_comp_info() 
            # update_com_info() 매서드로 KRX 주식 코드를 읽어 DB에 업데이트 한다.
        except Exception as e: 
            print (f"Error : ", e) 

    def __del__(self):
        """소멸자: Postgresql DB 연결 종료"""
        if self.conn:
            self.conn.close()
    
    def read_krx_code(self):
        """KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company', '업종':'sector', '주요제품':'industry', '상장일':'listup_date', '결산월':'account_month', '대표자명':'ceo', '홈페이지': 'homepage', '지역':'district'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_stock_market(self):
        """KRX로부터 유가증권목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=stockMkt&searchType=13&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_kosdaq_market(self):
        """KRX로부터 코스닥목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=kosdaqMkt&searchType=13&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_konex_market(self):
        """KRX로부터 코넥스 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=konexMkt&searchType=13&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_admin_manage_share(self):
        """KRX로부터 관리 종목 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=01&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_unfaith_notice_share(self):
        """KRX로부터 불성실 공시 법인 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=05&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_assets_share(self):
        """KRX로부터 자산2조 법인 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=07&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_foreign_share(self):
        """KRX로부터 외국 법인 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=99&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_kosdaq_blue_chip_share(self):
        """KRX로부터 (코스닥) 우량기업부 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=181&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_kosdaq_venture_share(self):
        """KRX로부터 (코스닥) 벤처기업부 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=182&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_kosdaq_middle_standing_share(self):
        """KRX로부터 (코스닥) 중견기업부 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=183&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_kosdaq_growth_tech_share(self):
        """KRX로부터 (코스닥) 기술성장기업부 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=184&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_krx100_tech_share(self):
        """KRX로부터 krs100 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=11&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_kospi200_tech_share(self):
        """KRX로부터 kospi200 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=06&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx
    
    def read_krx_star30_tech_share(self):
        """KRX로부터 STAR30 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=09&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def read_krx_premier_tech_share(self):
        """KRX로부터 PREMIER 목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&pageIndex=1&currentPageSize=5000&comAbbrv=&beginIndex=&orderMode=3&orderStat=D&isurCd=&repIsuSrtCd=&searchCodeType=&marketType=&searchType=10&industry=&fiscalYearEnd=all&comAbbrvTmp=&location=all'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드','회사명']]
        krx = krx.rename(columns={'종목코드':'ticker', '회사명':'company'})
        krx.ticker = krx.ticker.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        """종목코드를 stock_info 데이블에 업데이트한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM stock_info"
        
        df = pd.read_sql(sql, self.conn)

        for idx in range(len(df)):
            self.codes[df['ticker'].values[idx]] = df['company'].values[idx]
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM stock_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y/%m/%d')
            print('------------------------------------------------------------------------------------------------------------------------------------------------------')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    ticker = krx.ticker.values[idx]
                    company = krx.company.values[idx]
                    sector = krx.sector.values[idx]
                    industry = krx.industry.values[idx]
                    if type(industry) == str :
                        industry = re.sub('[\'-=.#/?:$}]','',industry);
                    else:
                        industry = 'None';
                    listup_date = krx.listup_date.values[idx]
                    listup_date = listup_date.replace('-','/');
                    account_month = krx.account_month.values[idx]
                    ceo = krx.ceo.values[idx]
                    homepage = krx.homepage.values[idx]
                    if type(homepage) == str :
                        if homepage == '' or homepage == 'nan':
                            homepage = 'None'
                        homepage = re.sub('[\'-=.#/?:$}]','',homepage);
                    else:
                        homepage = 'None'
                    district = krx.district.values[idx]

                    # stock_info insert or update
                    sql = f"INSERT INTO stock_info(ticker, company, sector, industry, country, last_update) VALUES ('{ticker}', '{company}', '{sector}', '{industry}', 'KOR', to_date('{today}','YYYY/MM/DD')) ON CONFLICT (ticker) DO UPDATE SET (ticker, company, sector, industry, country, last_update) = ('{ticker}', '{company}', '{sector}', '{industry}', 'KOR', to_date('{today}','YYYY/MM/DD')) WHERE stock_info.last_update < excluded.last_update"
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')                    
                    curs.execute(sql)

                    # stock_korea_addition insert or update
                    sql = f"INSERT INTO stock_korea_addition(ticker, listup_date, account_month, ceo, homepage, district, last_update) VALUES ('{ticker}', to_date('{listup_date}','YYYY/MM/DD'),'{account_month}','{ceo}','{homepage}', '{district}', to_date('{today}','YYYY/MM/DD')) ON CONFLICT (ticker) DO UPDATE SET (ticker, listup_date, account_month, ceo, homepage, district, last_update) = ('{ticker}', to_date('{listup_date}','YYYY/MM/DD'),'{account_month}','{ceo}','{homepage}', '{district}', to_date('{today}','YYYY/MM/DD')) WHERE stock_korea_addition.last_update < excluded.last_update"
                    curs.execute(sql);

                    self.codes[ticker] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO stock_info and stock_korea_addition VALUES ({ticker},{company},{sector},{industry},{listup_date},{account_month},{ceo},{homepage},{district},{today})")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')                
                # 유상 증권 구분
                krx2 = self.read_krx_stock_market()
                for idx in range(len(krx2)):
                    ticker = krx2.ticker.values[idx]
                    company = krx2.company.values[idx]
                    sql = f"UPDATE stock_info SET market = 'KRX:' WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the stock market(KOSPI)")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # KOSDAQ 구분
                krx3 = self.read_krx_kosdaq_market()
                for idx in range(len(krx3)):
                    ticker = krx3.ticker.values[idx]
                    company = krx3.company.values[idx]
                    sql = f"UPDATE stock_info SET market = 'KOSDAQ:' WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the KOSDAQ market")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # KONEX 구분
                krx4 = self.read_krx_konex_market()
                for idx in range(len(krx4)):
                    ticker = krx4.ticker.values[idx]
                    company = krx4.company.values[idx]
                    sql = f"UPDATE stock_info SET market = 'KONEX:' WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the KONEX market")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # 관리종목 구분
                krx5 = self.read_krx_admin_manage_share()
                for idx in range(len(krx5)):
                    ticker = krx5.ticker.values[idx]
                    company = krx5.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET issues_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 관리 종목")
                self.conn.commit()
                
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # 불성실 공시 법인 구분
                krx6 = self.read_krx_unfaith_notice_share()
                for idx in range(len(krx6)):
                    ticker = krx6.ticker.values[idx]
                    company = krx6.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET disclousure_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 불성실 공시 법인")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                
                # 자산 2조 법인 구분
                krx7 = self.read_krx_assets_share()
                for idx in range(len(krx7)):
                    ticker = krx7.ticker.values[idx]
                    company = krx7.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET assets_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 자산 2조 법인")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # 외국 법인 구분
                krx8 = self.read_krx_foreign_share()
                for idx in range(len(krx8)):
                    ticker = krx8.ticker.values[idx]
                    company = krx8.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET foreign_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 외국 법인")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # (코스닥) 우량기업부 구분
                krx9 = self.read_krx_kosdaq_blue_chip_share()
                for idx in range(len(krx9)):
                    ticker = krx9.ticker.values[idx]
                    company = krx9.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET bluechip_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 외국 법인")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # (코스닥) 벤처기업부 구분
                krx10 = self.read_krx_kosdaq_venture_share()
                for idx in range(len(krx10)):
                    ticker = krx10.ticker.values[idx]
                    company = krx10.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET venture_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 우량기업부")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # (코스닥) 중견기업부 구분
                krx11 = self.read_krx_kosdaq_middle_standing_share()
                for idx in range(len(krx11)):
                    ticker = krx11.ticker.values[idx]
                    company = krx11.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET middle_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 중견기업부")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # (코스닥) 기술성장기업부 구분
                krx12 = self.read_krx_kosdaq_growth_tech_share()
                for idx in range(len(krx12)):
                    ticker = krx12.ticker.values[idx]
                    company = krx12.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET techgrow_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the 기술성장기업부")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # krs100 구분
                krx13 = self.read_krx_krx100_tech_share()
                for idx in range(len(krx13)):
                    ticker = krx13.ticker.values[idx]
                    company = krx13.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET krx100_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the krs100")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # kospi200 구분
                krx14 = self.read_krx_kospi200_tech_share()
                for idx in range(len(krx14)):
                    ticker = krx14.ticker.values[idx]
                    company = krx14.company.values[idx]
                    sql = f"UPDATE stock_korea_addition SET kospi200_stock = true WHERE ticker = '{ticker}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {ticker},{company} is the kospi200")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                
                """
                # star30 구분
                krx15 = self.read_krx_star30_tech_share()
                for idx in range(len(krx15)):
                    code = krx15.code.values[idx]
                    company = krx15.code.values[idx]
                    sql = f"UPDATE company_info SET star30 = true WHERE code = '{code}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {code},{company} is the star30")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                # premier 구분
                krx16 = self.read_krx_premier_tech_share()
                for idx in range(len(krx16)):
                    code = krx16.code.values[idx]
                    company = krx16.code.values[idx]
                    sql = f"UPDATE company_info SET premier = true WHERE code = '{code}'";
                    curs.execute(sql)
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} {code},{company} is the premier")
                self.conn.commit()
                print('------------------------------------------------------------------------------------------------------------------------------------------------------')
                """
                print('Complete...')

    def read_naver(self, code, company, pages_to_fetch):
        """네이버 금융에서 주식 시세를 읽어서 데이터프레임으로 반환"""

    def replace_into_db(self, df, num, code, company):
        """네이버 금융에서 읽어온 주식 시세를 DB에 REPLACE"""

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""

    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        self.update_comp_info()

if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()