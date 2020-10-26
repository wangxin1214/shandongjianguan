
import requests
from lxml import etree
import re
import json
import redis




for page in range(1,10):

    # proxiess = {
    #     "HTTP': '117.94.245.219:3000"
    # }

    url = 'http://60.216.97.253:8899/SYWEB/webSpYouxiaoListAction!getList.do'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }

    data = {
         "searchBean.displayFlag": "0",
         "searchBean.listFlag": "",
         "jumpflag": "2",
         "conditionHtml": "",
         "searchBean.con1": "",
         "searchBean.con4": "",
         "searchBean.con5": "",
         "searchBean.con2": "",
         "searchBean.con3": "",
         "searchBean.con8": "",
         "searchBean.con6": "",
         "jumpPage": page-1 if page > 1 else 1,
         "page": page,
         }
    r = redis.Redis(host="182.92.213.90", password="iZ2ze09u5f5l2hvp4y83toZ", db=0, decode_responses=True, port="3718")
    response = requests.post(url=url, headers=headers,data=data,timeout=30)



    if response.status_code == 200:
        # print(response.text)
        html = etree.HTML(response.text)
        # business_type = html.xpath('//*[@id="listtab"]/tr[1]/th/text()')

        trs = html.xpath("//table[@id='listtab']//tr")[1:]  # 0是表头，跳过

        for tr in trs:
            tds = tr.xpath('td')
            # entname = tr.xpath('//td[@style="text-align: left"]/a/text()')  # 公司名
            entname = tds[0].xpath('string(a/text())').strip() or None

            # dom1 = html.xpath('//*[@id="listtab"]//tr/td[2]/text()')
            dom1 = tds[1].xpath('string(.)').strip() or None

            # uniscid1 = html.xpath('//*[@id="listtab"]/tr/td[3]/a/text()')
            uniscid1 = tds[2].xpath('string(.)').strip() or None

            # date_of_issue1 = html.xpath('//*[@id="listtab"]//tr/td[6]/text()')
            date_of_issue1 = tds[5].xpath('string(.)').strip() or None

            # period_of_validity1 = html.xpath('//*[@id="listtab"]//tr/td[7]/text()')
            period_of_validity1 = tds[6].xpath('string(.)').strip() or None

            # licence_issuing_authority1 = html.xpath('//*[@id="listtab"]//tr/td[9]/text()')
            licence_issuing_authority1 = tds[8].xpath('string(.)').strip() or None

            if not all([entname, dom1, uniscid1, date_of_issue1, period_of_validity1, licence_issuing_authority1]):
                # print('有个变量是空值，在这里处理')
                pass
            else:

                data_json = {
                    "source_url": url,
                    "company_name": entname,
                    "uniscid": "",
                    "regno": "",
                    "nacaoid": "",
                    "legal_person": "",
                    "regcap": "",
                    "enttype_name": "",
                    "esdate": "",
                    "company_city": "",
                    "company_address": dom1,
                    "contact": "",
                    "postal_code": "",
                    "business_type": "",
                    # 安全生产许可证
                    "safety_production_license_qualification": {},
                    # 企业资质证书
                    "building_qualification": {},
                    # 电力业务资质（发电类、输电类、供电类业务许可证/承装（修、试）电力设施许可证）
                    "power_qualification": {},
                    # 电信资质（电信业务经营许可证/电信设备进网许可证）
                    "telecom_qualification": {},
                    # 食药许可（化妆品生产许可/食品生产许可、经营许可）
                    "food_license_qualification": {
                        "qualifications_value_0": {
                            "licence_number": uniscid1,
                            "licence_issuing_authority": licence_issuing_authority1,
                            "licence_end_date": period_of_validity1,
                            "licence_start_date": date_of_issue1,
                            "qualification_classification": "食品生产许可证",
                            "industry_category": "",
                            "assessment_range": "",
                            "assessment_category": "",
                            "management_organization": "",
                            "standard_version": "",
                            "licence_status": "",
                            "assessment_company": "",
                        }
                    },
                    # 排污许可证
                    "blowdown_production_license_qualification": {},
                    # 两化融合管理体系
                    "integration_management_qualification": {},
                    # 商业特许经营备案
                    "commercial_franchise_qualification": {}
                }

                r.lpush("food_license_qualification_shandong", json.dumps(data_json))


                print(data_json)
