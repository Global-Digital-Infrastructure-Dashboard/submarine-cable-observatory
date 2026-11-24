"""Researcher coding of expansion batch 4 (Dominican Republic, Iran, Ethiopia, Indonesia, Montenegro; 10 operators),
coded in-session on 2026-11-23 from the cached v2 searches in data/5g_expansion_searches.jsonl, under Prof. Shen's
revised schema (see schema.py). Values come only from the cited source; anything a source didn't state is
not_disclosed. Share-category vendor claims and computed figures were checked against the primary page at coding
time (Prof. Shen's rule 11); the per-fact log is 5g_expansion/verify_2026-11-23_batch4.csv.
Not cited at all: Wikipedia, personal LinkedIn profiles, eSIM/aggregator sites.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-23'

register(domains={
    'government': ['indotel.gob.do', 'ekip.me', 'gov.me', 'worldbank.org', 'yidaiyilu.gov.cn', 'trade.gov'],
    'company': ['mci.ir', 'irancell.ir', 'mtn.com', 'mtn-investor.com', 'ethiotelecom.et', 'telkomsel.com', 'telkom.co.id',
                'ioh.co.id', 'ooredoo.qa', 'xlsmart.co.id', 'idx.id', 'idx.co.id', 'axiata.com', 'ericssonnikolatesla.com',
                't.ht.hr', 'hrvatskitelekom.hr', '4ig.hu', 'globenewswire.com', 'telecomramblings.com', 'report.telekom.com'],
    'news': ['financialtribune.com', 'digiato.global', 'ecofinagency.com', 'reuters.com', 'telecoms.com', 'vijesti.me',
             'totaltele.com', 'balkaninsight.com', 'akm.ru', 'ensegundos.do', 'listindiario.com', 'iranintl.com'],
    'research_industry_group': ['aiddata.org', 'stlpartners.com', 'scriptaintelektual.com'],
})

NBIM = 'https://www.nbim.no/api/investments/v2/report/?assetType=eq&date=2025-12-31&fileType=xlsx'
# Dominican Republic: INDOTEL raw data, Q3 2024 (mobile lines by operator, September 2024; computed by the researcher).
DR_XLSX = 'https://indotel.gob.do/wp-content/uploads/2025/03/Data-Cruda-Trimetre-3-2024.xlsx'
DR_NOTE = ('computed from INDOTEL raw data, mobile lines at Sep 2024 (residential + non-residential, prepaid + postpaid): '
           'Claro 6,708,433; Altice 3,602,836; Trilogy 397,447; total 10,708,716. Altice reports no non-residential '
           'prepaid row. INDOTEL\'s own Jan-Sep 2021 report gives Claro 61.35 / Altice 33 / Trilogy 5.65')
OAPEN = 'https://library.oapen.org/bitstream/handle/20.500.12657/99202/9781003489450_10.4324_9781003489450-11.pdf?sequence=1&isAllowed=y'
# Iran: CRA spring-2025 quarterly report as reported by Digiato.
IR_SHARE = 'https://digiato.global/report/iran-telecom-report-2025-spring/'
IR_NOTE = ("Communications Regulatory Authority report for spring 2025, via Digiato (8 Sep 2025): MCI >88m active "
           "subscribers (54%), Irancell 69m (42%), Rightel 5.7m (3.52%). The search also gave 53.26/43.01/3.72 from "
           "Financial Tribune, but that article is dated 4 Sep 2021, not 2025, so it is not coded")
# Indonesia: one source for all three operators.
ID_SHARE = 'https://scriptaintelektual.com/scripta-economica/article/download/1471/1199'
ID_NOTE = ('academic article (Scripta Economica, 2026), Table: Q1 2026 subscriber market share Telkomsel 48.77, Indosat '
           'Ooredoo Hutchison 29.83, XLSmart 21.39 (subscribers 153.67m / 94.00m / 67.40m); no regulator publishes '
           'operator shares. Telkomsel\'s own 2024 annual report claims ~50.3% (a table in the same report says 50.9%)')
OOREDOO_AR = 'https://www.ooredoo.com/wp-content/uploads/2026/03/2025-Ooredoo-Annual-Report_English_FINAL.pdf'
OOREDOO_GOV = 'https://www.ooredoo.com/2025-annual-report/pdfs/Ooredoo_English_2025_Corporate-Governance.pdf'
IOH_OWN = 'https://ioh.co.id/EN/ioh-corp-kepemilikan-saham'
IOH_CHAIN = 'Ooredoo Q.P.S.C. 50% of Ooredoo Hutchison Asia Pte. Ltd. -> 65.644% of Indosat Ooredoo Hutchison'
SINGTEL_LETTER = 'https://cdn1.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2026/Letter-to-Shareholders.pdf'
TEMASEK_TYPE_NOTE = ('holder_type is a researcher classification; the state link comes from data/state_holders.csv '
                     '(wholly owned by the Minister for Finance)')
# Montenegro: EKIP annual report 2025 (all three operators).
ME_SHARE = 'https://ekip.me/media/documents/general/1789388284_GI%202025%2025052026.pdf'
ME_NOTE = ('EKIP annual report 2025 (p.29): mobile users at end-2025 Mtel 613,264 (41.36%), Crnogorski Telekom 536,236 '
           '(36.17%), One Crna Gora 333,164 (22.47%), total 1,482,664')
DT_EQUITY = 'https://report.telekom.com/annual-report-2025/notes/notes-to-the-statement-of-financial-position/19-shareholders-equity.html'
HT_AR = 'https://static.hrvatskitelekom.hr/webresources/tht/pdf/investitori/izvjesca/ANNUAL_REPORT_ENG_2025.pdf'
CT_CHAIN = ('Deutsche Telekom AG -> Deutsche Telekom Europe Holding GmbH 100% -> Deutsche Telekom Europe Holding B.V. 100% -> '
            'Deutsche Telekom Europe B.V. 100% -> 54.6% of Hrvatski Telekom -> 79.2% of Crnogorski Telekom (HT annual report 2025, p.8)')

CHECKED_NOT_ADDED = {
    'Montenegro|Mtel': ('largest operator (41.36%, EKIP 2025) but no commercial 5G launch found: first NR base station Jul 2022 and '
                        '5G construction through 2023 per Telekom Srbija reports, no launch date (exp|supp|mtel-me-5g)'),
}

OPERATORS = [
    # ------------------------------------------------------------------ Dominican Republic
    dict(region='Latin America & Caribbean', country='Dominican Republic', operator_name='Claro',
         name_note='Compania Dominicana de Telefonos S.A. (Claro Dominicana)',
         share=V(62.64, DR_XLSX, DR_NOTE, 2024),
         launch=V(2021, 'https://www.telecompaper.com/news/claro-dominicana-launches-5g-in-santo-domingo--1406498',
                  'Santo Domingo, 3 Dec 2021, on 3.5 GHz won in the Oct 2021 auction'),
         ran5=[R('Nokia', 'not_disclosed', OAPEN, "academic book (2025) deployment table: 'Claro — Nokia' (2021); no share wording")],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.lightreading.com/2g-3g-4g/alcatel-lucent-wins-4g-lte-deal-in-dominican-republic',
                 "supplier named as Alcatel-Lucent (now part of Nokia): 4G LTE 'network overlay solution' (Jul 2014)")],
         gov=[], gov_note='100% owned by America Movil (Sep 2025 subsidiary table); its >5% holders are the Slim family and BlackRock (private)',
         gov_dropped=['Norges Bank Investment Management 0.07% of America Movil (2025-12-31; board seat not checked)'],
         core=ND('no source names the 5G core or NSA EPC vendor'),
         first_contract=ND('spectrum award Oct 2021 and launch Dec 2021; no vendor contract date'),
         vendor_operates=ND('FirstWave NMIS monitoring contract (Dec 2022) is a monitoring platform, not network operation')),
    dict(region='Latin America & Caribbean', country='Dominican Republic', operator_name='Altice',
         name_note='Altice Dominicana S.A. (formerly Orange Dominicana)',
         share=V(33.64, DR_XLSX, DR_NOTE, 2024),
         launch=V(2022, 'https://ensegundos.do/2022/02/23/altice-pone-en-funcionamiento-su-red-5g/',
                  "Ensegundos (23 Feb 2022): 'Altice Dominicana puso en funcionamiento su red 5G' in Santo Domingo's Ciudad Colonial and "
                  "Santiago de los Caballeros (verified); Listín Diario dates the launch event 24 Feb 2022 (page now 404). INDOTEL's 26 Sep 2024 "
                  "permit is for tests of extra frequencies (exp|supp|altice-do-launch)"),
         ran5=[R('Nokia', 'not_disclosed', OAPEN, "academic book (2025) deployment table lists Altice's 2021 5G deployment under Nokia; no share wording")],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.telecompaper.com/news/altice-huawei-sign-dominican-network-expansion-deal--1081901',
                 '3G/4G network expansion deal incl. 1,000 new antennas (May 2015)')],
         gov=[], gov_note='Altice group shareholders are private (Patrick Drahi and institutional investors); no state holder found',
         gov_dropped=[],
         core=ND('Huawei core-node work appears only in personal LinkedIn profiles, which are not cited'),
         first_contract=ND('spectrum award 13 Oct 2021 and concession 13 Dec 2021 are regulator agreements, not vendor contracts'),
         vendor_operates=ND('Huawei core-node operation and management appears only in a personal LinkedIn profile (not cited)')),
    # ------------------------------------------------------------------ Iran
    dict(region='Middle East', country='Iran', operator_name='MCI',
         name_note='Mobile Telecommunication Company of Iran (Hamrah-e Aval)',
         share=V(54.0, IR_SHARE, IR_NOTE, 2025),
         launch=V(2021, 'https://portal.powertec.com.au/industry-resources/companies/mci-hamrahe-aval',
                  '1 Mar 2021 on 3.5 GHz per an industry directory (weak source); MCI had announced 5G by 20 Mar 2021 (Developing Telecoms)'),
         ran5=[], ran5_note='no 5G RAN vendor named outside personal LinkedIn profiles',
         ran4=[], ran4_note=("Ericsson's 2008 Phase V expansion contract (reported 2012) predates LTE and names no generation; "
                             "Huawei/Nokia/ZTE/Siemens appear only in a personal LinkedIn profile"),
         gov=[G('Iran', 'Government of the Islamic Republic of Iran', 'government_ministry', 19.8, 'Telecommunication Company of Iran (TCI)',
                'via_parent', '2025', 'https://exclusive.iranintl.com/iran-internet-control-network-en',
                "Iran International (2026) on TCI's 2025 year-end ownership: the two Etemad Mobin entities 'control more than 49 percent ... "
                "approximately 2.5 times the Islamic Republic government's 19.8 percent stake' (verified)",
                parent_pct=90.0, chain="TCI holds 90% of MCI ('TCI holding (Public)'; 10% listed on the Tehran Stock Exchange, mci.ir)")],
         gov_note=("TCI itself is not coded as a state holder: it is listed, and its controlling holder at end-2025 was Tose'e Etemad Mobin "
                   "(47.02% direct plus 3.9% beneficially via Shahrivar Fifth Financial Intermediary), whose chain the source traces to "
                   "Gostaresh Electronic Tadbir (38%) and EIKO/Setad without calling it state-owned. Financial Tribune's 'state-owned TCI' is "
                   "dated 1 Dec 2019 (the search misdated it to 2026) and is superseded; the 2013 structure (Etemad Mobin 50%+1, government "
                   "20%, Justice Shares 20%) is not current (exp|supp|tci-iran-owners)"),
         gov_dropped=[],
         core=ND('Huawei NSA core work appears only in personal LinkedIn profiles, which are not cited'),
         first_contract=ND(), vendor_operates=ND("Naghsh Aval Keyfiat (NAK) is MCI's own managed-services subsidiary, not an equipment vendor")),
    dict(region='Middle East', country='Iran', operator_name='MTN Irancell',
         share=V(42.0, IR_SHARE, IR_NOTE, 2025),
         launch=V(2021, 'https://www.telecompaper.com/news/mtn-irancell-launches-commercial-5g-service--1372801', 'first commercial 5G 16 Feb 2021'),
         ran5=[], ran5_note='Huawei 5G appears only in a personal LinkedIn profile (not cited)',
         ran4=[], ran4_note=("Ericsson/Nokia LTE and an Ericsson-to-Huawei swap of 200 Tehran sites appear only in personal LinkedIn "
                             "profiles; MTN's 2009 report names Nokia-Siemens, Ericsson and Huawei as BTS build vendors without a generation"),
         gov=[], gov_note=("MTN Group holds 49% (FY2025 statements). The Iranian 51% (Kowsar Sign Paniz / IEDC) has no documented ownership "
                           "chain or percentages; a third-party report links IEDC to Iran Electronics Industries and Bonyad Mostazafan "
                           "without percentages. GEPF (19.94% of MTN Group per MTN's FY2025 statements; 22% at 31 Mar 2022 per GEPF's own "
                           "report) is not coded: GEPF's annual report says it is constituted under the Government Employees Pension Law and "
                           "is reported to Parliament by the Minister of Finance, and calls the PIC (its investment manager) government-owned, "
                           "but no source calls GEPF itself a government or state pension fund, and it is not on data/state_holders.csv "
                           "(exp|supp|gepf-status)"),
         gov_dropped=[],
         core=ND("The Diplomat (Oct 2020): Irancell used 'various vendors' for 5G; Ericsson's 2024 MTN core deal covers South Africa and Nigeria only"),
         first_contract=ND('Ericsson 5G test connection in Tehran, Sep 2017, was a test, not a contract'),
         vendor_operates=ND('a Huawei managed-services project (and its Oct 2025 transfer to Vista Service) appears only in personal LinkedIn profiles')),
    # ------------------------------------------------------------------ Ethiopia
    dict(region='Africa', country='Ethiopia', operator_name='Ethio telecom',
         share=V(91.89, 'https://openknowledge.worldbank.org/server/api/core/bitstreams/cd3c5bfa-7199-4574-8ea2-02e1e8201db3/content',
                 ("computed from World Bank, Ethiopia Telecom Market Assessment (Jul 2025, commissioned by the ECA), Figure 1 (source GSMA): "
                  "2024 SIM subscriptions EthioTel 80.5m, Safaricom Ethiopia 7.1m, total 87.6m; SIMs, not unique subscribers. "
                  "EthioTel's FY2024 mobile revenue share is 80.7%"), 2024),
         launch=V(2023, 'https://www.ethiotelecom.et/ethio-telecom-officially-launches-its-commercial-5g-service/', 'commercial launch 9 Sep 2023, 145 sites in Addis Ababa'),
         ran5=[R('Huawei', 'not_disclosed', 'https://eng.yidaiyilu.gov.cn/p/242237.html', 'deployed the pre-commercial 5G network in Addis Ababa (9 May 2022)'),
               R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/1/2024/ericsson-and-ethio-telecom-launch-5g-in-ethiopias-hawassa-city',
                 'Ericsson Radio System for the 5G launch in Hawassa (2024); Mar 2026 agreement adds 5G in its zone')],
         ran5_note=("vendors run regional network management zones (TechTrends Kenya, Mar 2026: 'Each supplier manages a designated zone'); "
                    "the national split is not stated. Telecoms.com's 'Huawei holds a significant share' is not a share category"),
         ran4=[R('Huawei', 'not_disclosed', 'https://china.aiddata.org/projects/105840', 'Telecom Expansion project (signed 10 Jan 2013, incl. 4G): 7 of 12 circles'),
               R('ZTE', 'not_disclosed', 'https://china.aiddata.org/projects/105840', 'same project: 6 circles, partially implemented; later modernised 462 RAN sites incl. LTE (2026)'),
               R('Ericsson', 'not_disclosed', 'https://china.aiddata.org/projects/105840', 'same project: four southern circles')],
         ran4_note='circle allocations overlap and changed during negotiation, so no national share; Nokia declined its three circles',
         gov=[G('Ethiopia', 'Ethiopian Investment Holdings (EIH)', 'state_holding_company', None, 'Ethio telecom', 'direct', '2024-10-09',
                'https://www.reuters.com/business/media-telecom/ethio-telecom-kick-off-ethopian-stock-trading-with-10-flotation-next-week-2024-10-09/',
                'EIH is the parent organisation; the government floated 10% (Oct 2024) and may offer a further 45%; the post-offering percentage is not disclosed',
                link_url='https://www.akm.ru/eng/news/ethiopian-government-sells-10-stake-in-ethio-telecom/')],
         gov_dropped=[],
         core=ND('Huawei deployed the 2022 pre-commercial 5G network, but no source names the core vendor'),
         first_contract=ND('Huawei pre-commercial launch (9 May 2022) was a partnership, with no contract date'),
         vendor_operates=ND("WRONG IN SEARCH: '1,500 sites under Ericsson's management' (2026) refers to Ericsson's network management zone, "
                            "i.e. regional supply, not managed operations")),
    # ------------------------------------------------------------------ Indonesia
    dict(region='Asia-Pacific', country='Indonesia', operator_name='Telkomsel',
         share=V(48.77, ID_SHARE, ID_NOTE, 2026),
         launch=V(2021, 'https://www.developingtelecoms.com/telecom-technology/wireless-networks/11213-telkomsel-debuts-commercial-5g-in-indonesia.html',
                  'commercial 5G 27 May 2021, Greater Jakarta and other cities'),
         ran5=[R('ZTE', 'not_disclosed', 'https://www.telkomsel.com//en/about-us/news/telkomsel-and-zte-strengthen-collaboration-develop-5g-solutions-corporate-and',
                 "Telkomsel (4 Mar 2023): 'In 2021, ZTE will become one of the network infrastructure partners' for its 5G rollout (verified)")],
         ran5_note=("Ericsson, Huawei and ZTE are named as 'global partners' for 5G Standalone development (2024 annual report), "
                    "which does not say they supply the RAN"),
         ran4=[R('ZTE', 'not_disclosed', 'https://www.telkomsel.com/sites/default/files/upload/Annual-Report-Telkomsel-2024--EN.pdf',
                 'AI/ML network solutions for 4G/LTE in Makassar and Kendari (2024 annual report)')],
         ran4_note="Telkom's 20-F names Huawei, Ericsson and ZTE as leading mobile-network equipment suppliers without a generation",
         gov=[G('Indonesia', 'PT Danantara Asset Management (Persero)', 'state_holding_company', 52.09, 'PT Telkom Indonesia (Persero) Tbk', 'via_parent', '2025-12-31',
                'https://aro.telkom.co.id/minio/show/data/image_upload/page/1787710867977_original_C-1-2-Annual-Report-FY-2025-page-96-98.pdf',
                "Telkom's annual report calls the Government of Indonesia its principal and controlling shareholder, represented by the Ministry of State-Owned Enterprises",
                link_url='https://www.telkom.co.id/minio/show/data/image_upload/page/(B)%20D.1.2%20Annual%20Report%20FY%202025,%20page%20294-295.pdf',
                parent_pct=69.9),
              G('Singapore', 'Temasek Holdings', 'state_holding_company', 50.55, 'Singtel', 'via_parent', '2026-06-30', SINGTEL_LETTER,
                'same figure as coded for Singtel in batch 1 (the search gives 50.29% at Mar 2025). ' + TEMASEK_TYPE_NOTE,
                link='reference_list', chain='Singtel -> Singapore Telecom Mobile Pte Ltd -> 30.1% of Telkomsel')],
         gov_dropped=["Government of Indonesia: one Series A 'Dwiwarna' share in Telkom Indonesia (~0%, special rights; no board seat found)"],
         core=ND("an analyst report hosted by Nokia only lists Telkomsel among the cloud-core customers 'ZTE claims'; it does not "
                 "establish the 5G core vendor (verified)"),
         first_contract=ND('ZTE became a 5G network-infrastructure partner in 2021; no contract date'),
         vendor_operates=ND('Nokia 3G radio, core and managed-services contract (Aug 2006, three years) predates 5G')),
    dict(region='Asia-Pacific', country='Indonesia', operator_name='Indosat Ooredoo Hutchison',
         share=V(29.83, ID_SHARE, ID_NOTE, 2026),
         launch=V(2021, 'https://www.ooredoo.qa/web/en/press-release/corporate-launchof-commercial-5gservices-in-indonesia/', 'Solo (Surakarta), 24 Jun 2021'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://newswire.telecomramblings.com/2021/08/indosat-ooredoo-launches-ericsson-powered-5g-in-jakarta/',
                 "Ericsson release (28 Aug 2021): 'Ericsson is powering the 5G network through Ericsson Radio System' in Jakarta (verified)"),
               R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-selected-by-indosat-ooredoo-hutchison-as-prime-supplier-in-multi-year-network-expansion-deal/',
                 "'principal vendor' for 4G/5G in Sumatra, Kalimantan, Central Java and Surabaya (4 Mar 2022); extended 2025-2027; Jun 2026 low/mid-band 5G modernisation")],
         ran5_note="'principal vendor' is not one of the share categories, so no share is coded",
         ran4=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-selected-by-indosat-ooredoo-hutchison-as-prime-supplier-in-multi-year-network-expansion-deal/',
                 "'principal vendor' for 4G expansion in the same regions (Mar 2022)")],
         gov=[G('Indonesia', 'Government of the Republic of Indonesia', 'government_ministry', 9.632, 'Indosat Ooredoo Hutchison', 'direct', '2024-12-31',
                IOH_OWN, 'plus a golden share; President Commissioner listed as a government representative (1H 2025 profile)'),
              G('Qatar', 'Qatar Investment Authority', 'sovereign_wealth_fund', 53.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR,
                "Ooredoo's annual report calls QIA the State of Qatar's sovereign wealth fund", chain=IOH_CHAIN),
              G('Qatar', 'General Retirement & Social Insurance Authority', 'pension_fund', 13.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR,
                'Qatari government-related entity with a board representative (2025 corporate governance report)', link_url=OOREDOO_GOV,
                chain=IOH_CHAIN, board_seat='yes')],
         gov_note="CK Hutchison (other 50% of Ooredoo Hutchison Asia) and PT Tiga Telekomunikasi Indonesia (8.332%) are not identified as state entities",
         gov_dropped=['General Military Retirement and Social Insurance Authority 2% of Ooredoo Q.P.S.C. (2025-12-31; no board representative)',
                      'Abu Dhabi Investment Authority 4.99% of Ooredoo Q.P.S.C. (2025-12-31; no board representative)',
                      'Norges Bank Investment Management 1.88% of Ooredoo Q.P.S.C. (2025-12-31; board seat not checked)'],
         core=ND('Nokia deals cover RAN; no 5G core vendor named'),
         first_contract=ND('Nokia deal (4 Mar 2022) is the earliest dated agreement found, but Ericsson powered the Aug 2021 Jakarta launch, so it was not the first'),
         vendor_operates=ND("Nokia's 'consolidation services' are integration, not managed operations")),
    dict(region='Asia-Pacific', country='Indonesia', operator_name='XLSmart',
         name_note='PT XLSmart Telecom Sejahtera Tbk, formed 16 Apr 2025 from XL Axiata and Smartfren; Wikipedia list name XLSmart',
         share=V(21.39, ID_SHARE, ID_NOTE + '; XLSmart reports 73.0m subscribers for 2025', 2026),
         launch=V(2026, 'https://www.xlsmart.co.id/en/about-xlsmart/news/smartfren-expanded-5g-coverage-to-makassar-strengthening-the-digital-ecosystem-in-eastern-indonesia',
                  "earliest dated launch in the evidence: Smartfren-brand 5G in Makassar, 2 Feb 2026 (Surabaya 8 Feb; 'XL Ultra 5G+' with ZTE, "
                  "28 Feb 2026). A follow-up search (exp|supp|xl-axiata-launch) found only XL Axiata's plan for limited 5G from mid-Aug 2021 in four cities and a "
                  "merger release saying it 'developed its 5G network in Q3 2021', with no commercial launch date, so 2026 stays"),
         ran5=[R('ZTE', 'not_disclosed', 'https://www.zte.com.cn/global/about/news/XLSMART-Partners-with-ZTE-to-Launch-Indonesia-s-First-Nationwide-5G-Blanket-Coverage-Network.html',
                 "ZTE (28 Feb 2026): 'Indonesia's first nationwide 5G blanket coverage network'; over 7,000 new 5G base stations deployed with ZTE (verified); no share wording")],
         ran4=[R('ZTE', 'not_disclosed', 'https://www.zte.com.cn/global/about/news/XLSMART-Partners-with-ZTE-to-Launch-Indonesia-s-First-Nationwide-5G-Blanket-Coverage-Network.html',
                 "same release: XLSmart and ZTE 'jointly integrated more than 20,000 4G base stations'")],
         ran4_note='Huawei and Ericsson appear only as supporters of a 4G-LTE test run (XL Axiata 2024 report)',
         gov=[G('Malaysia', 'Khazanah Nasional Berhad', 'sovereign_wealth_fund', 36.69, 'Axiata Group Berhad', 'via_parent', '2026-03-31',
                'https://www.axiata.com/2025IAR/documents/Axiata-Integrated-Annual-Report-2025-Overview.pdf',
                "Axiata's audited statements call Khazanah 'the sovereign wealth fund of the Government of Malaysia' (36.71% direct at 31 Dec 2025)",
                link_url='https://www.axiata.com/2025IAR/documents/Axiata-Governance-and-Audited-Financial-Statements-2025.pdf',
                chain='Axiata Group Berhad 36.91% effective of XLSmart (equal with the Sinar Mas shareholders), via Axiata Investments (Labuan) -> Axiata Investments (Indonesia)')],
         gov_note=("Khazanah's basis is stated_in_source (Axiata IAR2025 p.38 and audited statements: 'the sovereign wealth fund of the "
                   "Government of Malaysia'; exp|supp|axiata-holders). EPF 19.36% and PNB 18.28% of Axiata (31 Mar 2026) each have a "
                   "representative director but Axiata does not call them government-owned or state-controlled, and they are not on "
                   "data/state_holders.csv, so they are not coded; Amanah Saham Bumiputera 12.48% likewise. No state holder among the "
                   "Sinar Mas shareholders"),
         gov_dropped=['PT Industri Telekomunikasi Indonesia (Persero) 0.003% of Smart Telecom (pre-merger presentation; no board seat found)'],
         core=V('Ericsson', 'https://idx.id/Portals/0/StaticData/NewsAndAnnouncement/ANNOUNCEMENTSTOCK/From_EREP/202503/110cc1027f_4662632cc3.pdf',
                "XL Axiata 2024 integrated annual report (p.46): 'the first operator to implement a dual-mode 5G core network in partnership with Ericsson' (verified)"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('core', '4G', 'Cisco', 'Huawei', '2015', '2016-12', 'https://stlpartners.com/wp-content/documents/reports/Telco%20Cloud%20Operator%20Profiles.pdf',
                     "STL Partners: XL's 2015 Cisco virtualised packet core 'replaced by Huawei CloudEdge (EPC) at the end of 2016'; XL Axiata, pre-merger")]),
    # ------------------------------------------------------------------ Montenegro
    dict(region='Central Asia & Eastern Europe', country='Montenegro', operator_name='Crnogorski Telekom',
         name_note='Wikipedia list name CT; brand Telekom',
         share=V(36.17, ME_SHARE, ME_NOTE, 2025),
         launch=V(2022, 'https://ekip.me/media/documents/1646720540_2022%2003%2007%20Saop%C5%A1tenje%20za%20medije%20Dan%20EKIP-a.docx',
                  'EKIP: commercial base stations in Podgorica from 7 Mar 2022 (DSS)'),
         ran5=[R('Ericsson', 'all', 'https://ericssonnikolatesla.com/en/news/20221024-cooperation/',
                 "Ericsson Nikola Tesla (24 Oct 2022): five-year EUR 12.5m agreement 'encompasses the introduction of 5G technology across "
                 "Montenegro and modernization of the entire Crnogorski Telekom radio network'; 'the entire project has been realized with "
                 "the support of Ericsson Nikola Tesla' (verified). 'all' is a researcher reading of 'entire radio network'")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://ericssonnikolatesla.com/en/news/20181219-cooperation/',
                 "Dec 2018: 'The radio network of Crnogorski Telekom will be modernized with ... the Ericsson Radio System portfolio' (verified)")],
         gov=[G('Germany', 'Federal Republic of Germany', 'government_ministry', 14.1, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_EQUITY,
                'from the core-panel evidence (Deutsche Telekom annual report 2025, note 19); same figures as the core DT rows', chain=CT_CHAIN),
              G('Germany', 'KfW', 'state_holding_company', 14.2, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_EQUITY,
                'from the core-panel evidence; the DT report describes KfW as the holding vehicle for the indirect federal stake', chain=CT_CHAIN)],
         gov_note=("Croatian War Veterans' Fund (7.1% of HT) is not coded: HT's 2025 annual report names it without saying it is "
                   "state-owned, and it is not on data/state_holders.csv (the core-panel HT row codes it as stated_in_source; see the batch report)"),
         gov_dropped=['CERP (Restructuring and Sale Centre) / Republic of Croatia 1.9% of Hrvatski Telekom (2025-12-31; board seat not checked)'],
         core=V('Ericsson', 'https://www.t.ht.hr/en/Press/press-releases/7129/Hrvatski-Telekom-and-Crnogorski-Telekom-contract-Ericsson-Nikola-Tesla-for-the-deployment-of-Ericsson-s-dual-mode-5G-Core-for-it.html',
                "HT/CT (7 Dec 2023): Ericsson Nikola Tesla sole supplier of software and services for the new 4G/5G core (dual-mode 5G Core). "
                "In Sep 2020 CT said its initial 5G phase used Nokia for the core (Vijesti); no source calls the 2023 core a replacement"),
         first_contract=ND('Dec 2018 Ericsson radio and core investment cycle is described as 5G-ready, not a 5G contract'),
         vendor_operates=V(True, 'https://www.ericsson.com/4ac5d8/assets/local/news/2016/02/managed_services_press_backgrounder.pdf',
                           'seven-year managed-services partnership from 2015: Ericsson operates and maintains the network; renewal after ~2022 not found')),
    dict(region='Central Asia & Eastern Europe', country='Montenegro', operator_name='One',
         name_note='One Crna Gora (formerly Telenor Montenegro)',
         share=V(22.47, ME_SHARE, ME_NOTE, 2025),
         launch=V(2022, 'https://ekip.me/media/documents/general/1703840162_ANNUAL%20REPORT%202022.pdf', 'EKIP annual report 2022: commercial 5G NR in July 2022'),
         ran5=[R('Huawei', 'not_disclosed', 'https://balkaninsight.com/2026/07/01/despite-us-and-eu-calls-montenegro-yet-to-require-removal-of-chinese-telecoms-equipment/bi/',
                 "BIRN citing EKIP (1 Jul 2026): 'its radio access network including the 5GNR network uses Huawei equipment' (verified); no share wording")],
         ran4=[R('Huawei', 'not_disclosed', 'https://balkaninsight.com/2026/07/01/despite-us-and-eu-calls-montenegro-yet-to-require-removal-of-chinese-telecoms-equipment/bi/',
                 "same sentence: the radio access network as a whole 'uses Huawei equipment'; 4G is not named separately")],
         gov=[G('Hungary', 'Corvinus Nemzetközi Befektetési Zrt.', 'state_holding_company', 37.9, '4iG Távközlési Holding Zrt.', 'via_parent', '2025-06-30',
                'https://www.4ig.hu/sw/static/file/4iGConsolidatedfinancialandmanagementreport2025H1.pdf',
                "4iG H1 2025 report: 'the state has a minority ownership of 37.9% in 4iG Távközlési Holding Zrt. through its investment entity'",
                chain="4iG Távközlési Holding Zrt. -> One Crna Gora (percentage not stated)")],
         gov_note='no state holder of 4iG Plc. (iG COM, Rheinmetall, KZF and others are not identified as state entities)',
         gov_dropped=[],
         core=V('ZTE', 'https://balkaninsight.com/2026/07/01/despite-us-and-eu-calls-montenegro-yet-to-require-removal-of-chinese-telecoms-equipment/bi/',
                "BIRN citing EKIP: 'The core network of One Crna Gora ... relies on equipment from ZTE' (verified); NSA/SA not stated"),
         first_contract=ND(), vendor_operates=ND()),
]
