token = "97b5fb2714757cc357b9c1d2f0e72cb14dc7608b8bc7b87719c02c6eac6f1e3af87b903dafbcfd890a9c1"
# token_telegram = '5248571053:AAEVLqq2bpYnKyAQ1tPGJ_wDdr3mhcqrdpk'
token_telegram = "5104477702:AAFWLO4xjFbaglKK9jPPrd5ibq06oxjtmso"
login = "+79626154514"

password = "pobeda2021"
owner_id = 203958116
# owner_id = 110413234
# filial = {'filial': "Энгельс , улица Максима Горького 33",
#           'number': '8 (8453) 53-05-51', }
#
filial = {'filial': "Энгельс , улица Космонавтов 19",
          'number': '8 (8453) 53-03-51', }

# filial = {'filial': "Саратов, улица имени Н.Г. Чернышевского, 217",
#           'number': '8 (8452) 74-05-51', }


filter = r'apple|iphone|macbook|airpods|ipad'


text_message = f"""Дорогие жители и гости нашего города, мы будем рады вас видеть на нашем филиале ПОБЕДЫ по адресу: 
                🏪 {filial['filial']} 
                ☎Звоните по интересующим вопросам по тел. {filial['number']}, а лучше всего приходите, будем рады Вас видеть! 😉 
                👉Производим самую высокую ОЦЕНКУ 🔥🔥 
                👉Онлайн ОЦЕНКУ через наш сайт 🔥🔥 
                👉 Самые приятные ЦЕНЫ на товар 🔥🔥 
                💥Режим работы: КРУГЛОСУТОЧНО! ⏰ 
                ‼Бронируйте товар прямо сейчас на сайте 👉👉👉победа-63.рф👈👈👈 
                ‼‼‼Так же появилось возможность приобрести товар в наших магазинах в кредит через наш сайт проходите по ссылке‼‼‼ 
                💥Так-же на нашем филиале вы можете приобрести любой аксессуар для своего смартфона" Чехол, зу, наушники, бронь стёкла, моноподы (селфи палка), aux.💥 
                🙀При покупки товара вы получаете баллы. 1 балл равняется рублю. за баллы можно приобрести так же товар на ваш выбор 🙀 
                Вся техника абсолютно исправна 😊 
                Поможем вам с выбором любой техники под ваши нужды 😉"""

upload_img = '''SELECT title , price , photo  FROM top_items ti ORDER BY retrieved_time DESC LIMIT 5'''

album_name = 'Repost'

'''Ссылки Горького'''
# link = [
#
#     'https://энгельс.победа-63.рф/catalog/telefony/sotovye-telefony/?k=false&q=20&s=high&c=57&cg=143&a=0&f[]=399&',
#     'https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?k=false&q=20&s=high&c=57&cg=84&a=0&f[]=399&',
#     'https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/avto/?k=false&q=20&s=high&c=57&cg=132&a=0&f[]=399&',
#     'https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/noutbuki/?k=false&q=20&s=high&c=57&cg=101&a=0&f[]=399&'
#
# ]
'''Ссылки Космонавтов'''
link = [

    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/telefony/sotovye-telefony/?k=false&q=20&s=high&c=57&cg=143&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/?k=false&q=20&s=high&c=57&cg=99&a=0&f[]=400&",
    "https://xn--c1aesfx9dc.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?k=false&q=20&s=high&c=57&cg=84&a=0&f[]=400&",
    "https://энгельс.победа-63.рф/catalog/avto/?k=false&q=20&s=high&c=57&cg=132&a=0&f[]=400&",

]

'''Ссылки Чернышевского'''
# link = [
#
#     "https://xn--80aag1ciek.xn---63-5cdesg4ei.xn--p1ai/catalog/telefony/sotovye-telefony/?q=20&s=high&c=11&cg=143&a=0&f[]=693&",
#     "https://xn--80aag1ciek.xn---63-5cdesg4ei.xn--p1ai/catalog/instrument/?q=20&s=high&c=11&cg=84&a=0&f[]=693&",
#     "https://xn--80aag1ciek.xn---63-5cdesg4ei.xn--p1ai/catalog/kompyuternaya-tehnika/?q=20&s=high&c=11&cg=99&a=0&f[]=693&",
#
#
# ]