import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Color,Font,Alignment
from openpyxl.worksheet.table import Table,TableStyleInfo
import xlsxwriter
mywb = openpyxl.Workbook()
ws = mywb.active
workbook = xlsxwriter.Workbook("./test.xlsx")
worksheet = workbook.add_worksheet("mysheet1")
titleformat = workbook.add_format()
titleformat.set_bold()
worksheet.set_row(1,None,titleformat)

colformat = workbook.add_format()
colformat.set_text_wrap()
worksheet.set_column(5,5,colformat)

ws.append(["城市","工作经验","学历","薪资","公司","职位要求"])
#table = Table(displayName="Table1",ref="A1:F1")

jsonstr = [
    ['北京', '5-10年', '本科', '21K-42K', '后端工程师 JAVA/Python\n1. 有 Web 全栈开发经验，能驾驭前端和后端，对前后端分离项目有一定实战经验。\r\n2. 熟悉 Python 的使用，并且对Flask，Tornado，Django 或其他 Web 框架至少熟悉其一。\r\n3.熟悉 MySQL/MariaDB，Redis等数据库的使用，有手写 SQL 的能力。 \n4.能熟练使用 HTML，CSS，JavaScript 进行开发，熟练使用 VUE 及其组件。\n5. 熟悉 Linux 基本操作，能够独立打包部署维护 Python 和前端项目。\n6. 具有较好的产品设计和沟通理解能力。\n                            \n公司成立于2013，专注于教育产品研发和销售的科技型企业，结合互联网 无线互联网打造“线上+线下”“园所到家庭”全方位、一体式幼儿教育系统。团队汇集了互联网 教育行业的许多专家。'],
['东莞', '1-3年', '本科', '10K-13K', '工作职责\n    1. 负责公司网站的WEB后端和机器人后端框架层及业务层的实现\n    2. 负责web后端和机器人后端的相关文档编写\n    3. 负责公司应用设计、功能实现并进行测试，部署及维护\n    \n    任职要求\n    1. 计算机或相关专业本科及以上学历，有扎实的计算机基础知识\n    2. 两年以上服务器端开发经验，熟悉Linux环境下的开发\n    3. 熟悉Python语言，熟练掌握Django、Web.py、Tornado、Flask等至少1个Web开发框架，了解Tornado框架\n    4. 动手搭建过实际上线的产品环境，如Apache,Nginx\n    5. 熟悉多线程编程\n    6. 熟悉Javascript / HTML / XML / JSON / HTML5 / JQuery\n    7. 熟悉SQL语言，熟悉MySQL或者Oracle\n    8. 有MongoDB、Redis、Memcached经验者优先\n    \n    优先条件\n    1. 有过完整的项目开发经验，并有在运行项目的优先\n    2. 有一定前端设计能力者优先能快速阅读英文文献、论文\n    3. 有用Python技术做过相关的机器人项目'],
['西安', '不限', '本科', '8K-10K', '1、完成 Python 功能模块的设计、开发\n3.负责 Python 软件开发和软件设计等工作'],
['上海', '3-5年', '本科', '16K-32K', '工作职责：\n·\xa0\xa0\xa0\xa0\xa0\xa0 基于Linux平台开发数据分析和挖掘平台\n·\xa0\xa0\xa0\xa0\xa0\xa0 开发后台API和前端界面来整合和管理数据和算法方案\n·\xa0\xa0\xa0\xa0\xa0\xa0 和数据科学家一起用机器学习技术分析和挖掘数据\n·\xa0\xa0\xa0\xa0\xa0\xa0 建立模型并用于自动化和智能化应用\n·\xa0\xa0\xa0\xa0\xa0\xa0 跟踪IT前沿技术，对架构和实现方式提供更新建议\n职位要求：\n·\xa0\xa0\xa0\xa0\xa0\xa0 具有良好的编程习惯和项目管理和工作习惯\n·\xa0\xa0\xa0\xa0\xa0\xa0 2年以上 Python编程经验，熟练掌握常见数据结构和算法和OOP编程范式\n·\xa0\xa0\xa0\xa0\xa0\xa0 熟练掌握Linux和Shell的使用，熟悉Git以及基于 Pull Request 的工作流\n·\xa0\xa0\xa0\xa0\xa0\xa0 熟悉PostgreSQL 或MySQL等开源SQL数据库，了解 MongoDB 、Redis 和 HBase 等 NoSQL 技术\n·\xa0\xa0\xa0\xa0\xa0\xa0 掌握常用的 Python Web 框架，如 Django，Flask 等，拥有完整的 web 后端项目经验\n·\xa0\xa0\xa0\xa0\xa0\xa0 了解前端技术、有 Java、Golang、C++等静态语言编程经验的优先\n·\xa0\xa0\xa0\xa0\xa0\xa0 良好的英语阅读和写作能力、强好奇心，善于自主学习和解决问题，对技术热忱，爱读书、求甚解\n·\xa0\xa0\xa0\xa0\xa0\xa0 心智成熟，沟通能力强，善于团队协作\n·\xa0\xa0\xa0\xa0\xa0\xa0 审美能力高于理科生平均水平优先\n                            \n七炅信息科技成立于2016年，由保险行业大数据分析、业务实施专家联合创办。总公司位于杭州智慧交通谷，是交通部科学研究院指定合作企业，七炅专注于成为保险行业数据的加工商和技术专家，填补原始数据到保险应用之间的技术和商业模式断裂层，促进产业链条的高效率运作和互相促进。'],
['武汉', '不限', '本科', '7K-14K', 'Python脚本语言熟悉掌握，了解机器学习，使用过Django'],
['广州', '1-3年', '本科', '5K-10K', '岗位职责：\n1、负责设计和开发分布式的网络爬虫应用，包括调度、抓取、入库等内容，进行互联网相关信息的抓取和分析。\n2、实现大规模文本、图像数据的抓取、抽取，去重、分类，垃圾过滤，质量识别、解析入库等工作 。\n3、网络爬虫架构设计、功能开发及优化。\n4、网页信息抽取等核心算法的研究和优化。负责公司运营平台开发工作。\n5、参与项目整体规划设计过程，制定项目迭代计划。\n6、负责解决项目相关的开发需求以及Bug修正，相关的问题的沟通协调工作。\n岗位要求：\n1、计算机相关专业，具备1年及以上开发项目经验；\n2、掌握网络爬虫开发原理，对互联网各种类型数据交互模式熟悉，知道如何处理需登录网站、动态网页等各种情况下的数据采集方法。\n3、精通html语言，熟悉开源工具，熟悉基于正则表达式、XPath等的信息抽取技术。\n4、有网络爬虫开发经验、有scrapy等开源抓取工具开发经验优先。\n5、熟悉至少一种关系型数据库（Mysql等），熟悉Nosql，hbase等技术优先。\n6、逻辑思维清晰，做事有条理，具备较好的数据分析能力和解决问题的能力。\n7、工作积极主动、严谨负责。学习能力强，有一定的技术狂热，愿意学习和接受新知识和技术，有一定的英语阅读能力，会用GOOGLE，STACKOVERFLOW搜索问题，对全栈工程师的概念有了解。']
           ]

# ws["A2"] = jsonstr['城市']
# ws["B2"] = jsonstr['工作经验']
# ws["C2"] = jsonstr['学历']
# ws["D2"] = jsonstr['薪资']
# ws["E2"] = jsonstr['公司']
# ws["F2"] = jsonstr['职位要求']
col = ws.column_dimensions['E']
ws["E2"].font = Font(bold=True,size=18)
ws["E2"].alignment = Alignment(horizontal='center',vertical='center',wrap_text=True)
for row in jsonstr:
    ws.append(row)
mywb.save("./mytext.xlsx")
