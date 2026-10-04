import os
import django
import requests
from django.core.files.base import ContentFile

# Налаштування середовища Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulyk_project.settings')
django.setup()

from menu.models import Category, Dish


# Функція для створення чистих латинських слагів
def slugify_uk(text):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh',
        'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu', 'я': 'ya', '\'': '', '"': '', '`': ''
    }
    text = text.lower()
    res = []
    for char in text:
        if char in translit_dict:
            res.append(translit_dict[char])
        elif char.isalnum():
            res.append(char)
        else:
            res.append('-')

    slug = ''.join(res)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-')


# 1. Створення категорій
categories_data = [
    'Сніданки',
    'Закуски',
    'Основні страви',
    'Перші страви',
    'Салати овочеві',
    'Салати рибні',
    'Салати м\'ясні',
    'Страви з свинини'
]

categories = {}
for cat_name in categories_data:
    cat_slug = slugify_uk(cat_name)
    category, created = Category.objects.get_or_create(
        name=cat_name,
        defaults={'slug': cat_slug}
    )
    categories[cat_name] = category

# 2. Повний список усіх ваших страв
dishes_data = [
    # --- Початкові страви із зображеннями ---
    {
        'name': 'Паштет з яловичої печінки з чебрецевим маслом або ягідним желе',
        'price': 170.00,
        'description': 'Дуже корисний паштет з яловичої печінки з ніжним солодкуватим смаком, доведений до кремової консистенції.',
        'category': categories['Закуски'],
        'is_popular': True,
        'is_new': False,
        'image_url': 'https://img.postershop.me/67d08ccca86b6228a6959134/762a6c49-e498-4b73-9c0c-ecc7e3e01eb1-image.jpeg'
    },
    {
        'name': 'Вареники з чорницею',
        'price': 200.00,
        'description': '* Унікальна сезонна пропозиція - вареники з локальною волинською чорницею - смак, знайомий з дитинства.',
        'category': categories['Основні страви'],
        'is_popular': True,
        'is_new': True,
        'image_url': 'https://img.postershop.me/67d08ccca86b6228a6959134/580fcd76-5f7a-4413-8d36-45718fbf384f-image.jpeg'
    },
    {
        'name': 'Холодний борщ',
        'price': 150.00,
        'description': 'Охолоджений буряковий борщ на вершках з ніжною копченою вирізкою, свіжим огірком, відвареним яйцем та зеленню.',
        'category': categories['Основні страви'],
        'is_popular': True,
        'is_new': True,
        'image_url': 'https://img.postershop.me/67d08ccca86b6228a6959134/1907a7a8-a2ce-478f-92c0-6d9ef02ce223-image.jpeg'
    },
    {
        'name': 'Форель зі спаржею під вершковим соусом',
        'price': 450.00,
        'description': '*Страва попереднього замовлення. Ніжна річкова форель у вершковому соусі подається зі соковитою спаржею.',
        'category': categories['Основні страви'],
        'is_popular': True,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/921a73b4-e70e-45b5-908b-00e4fbecff4b-image.jpeg'
    },
    {
        'name': 'Медальйони з ягідним соусом',
        'price': 395.00,
        'description': 'Ніжні медальйони з внутрішньої яловичої вирізки, обсмажені до ідеальної соковитості, подаються з ароматним ягідним соусом.',
        'category': categories['Основні страви'],
        'is_popular': False,
        'is_new': True,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/dc655e03-069f-457e-93f9-b527b4db7a9b-image.jpeg'
    },
    {
        'name': 'Кабачкові деруни з крем сиром та слабосоленим лососем',
        'price': 325.00,
        'description': 'Ніжні деруни з кабачка додаються зі слабосоленим лососем, свіжим огірком, зеленню та крем сиром.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': True,
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbYATSqLQxYmdht09xFejP2Zjl-e1TaBMVlh5gP7WR53kPlymIp4OTA5k&s=10'
    },
    {
        'name': 'Вареники з вишнями',
        'price': 195.00,
        'description': 'Ніжне тісто, соковита начинка зі стиглих вишень — класика, що дарує справжній смак літа.',
        'category': categories['Основні страви'],
        'is_popular': False,
        'is_new': True,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/be1d07d9-e15a-4d33-9798-271af1a05508-image.jpeg'
    },
    {
        'name': 'Люля-кебаб',
        'price': 170.00,
        'description': 'Соковита суміш яловичини, курки та свинини, приправлена спеціями та обсмажена до золотистої скоринки.',
        'category': categories['Основні страви'],
        'is_popular': False,
        'is_new': True,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/e83af7a8-9c61-4fa1-823a-a97c47a8d989-image.jpeg'
    },

    # --- Сніданки ---
    {
        'name': 'Сніданок із домашньою ковбаскою',
        'price': 295.00,
        'description': 'Скребмл із смаженою домашньою ковбаскою , подаємо з салатом з помідорів, огірків та листя салату заправлений оливковою олією, також додаємо грінки з білого молочного багету. 400 грам.',
        'category': categories['Сніданки'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/8b33cbc4-db02-4c51-a123-913cf6911e97-image.jpeg'
    },
    {
        'name': 'Сніданок з беконом',
        'price': 345.00,
        'description': 'Смажена яєчня з беконом, подаємо з свіжими овочами та хрумкими грінками з молочного багету. 340 грам.',
        'category': categories['Сніданки'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/19407c88-66e4-43d3-8154-b6ba97f0a65c-image.jpeg'
    },
    {
        'name': 'Сніданок із червоною рибою',
        'price': 365.00,
        'description': 'Скребмл із слабосоленим лососем та сиром філадельфія, подаємо з салатом з помідорів, огірків та листя салату заправлений оливковою олією, також додаємо грінки з білого молочного багету. 400 грам.',
        'category': categories['Сніданки'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/7f371344-a063-47b2-8604-2e77af0de265-image.jpeg'
    },

    # --- Закуски ---
    {
        'name': 'Асорті сала з огірочками',
        'price': 365.00,
        'description': 'Сало "Чумацьке", сало біле, сало з м\'ясною прослойкою, огірки квашені, гірчиця ,цибуля та грінки з чорного хліба. 600 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/197ec071-0bdd-4cc5-b46e-9799fcc9548c-image.jpeg'
    },
    {
        'name': 'М\'ясне асорті 250 гр',
        'price': 295.00,
        'description': 'Копчений бочок та вирізка, домашня шинка та ковбаска з печі, хрін. 250 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/95d3159d-7451-4a5a-9147-a9b01b1c5337-image.jpeg'
    },
    {
        'name': 'Овочева нарізка',
        'price': 195.00,
        'description': 'Огірок, помідор та болгарський перець. 300 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/92d8e1f5-1f0f-4258-8381-99350ab36e18_image.jpeg'
    },
    {
        'name': 'Оселедець з цибулею',
        'price': 220.00,
        'description': 'Оселедець маринований з цибулею та чорними грінками.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/303dbb4e-3bd0-4d56-a416-3d874fa98fd4-image.jpeg'
    },
    {
        'name': 'Печінковий паштет з вишнево-імбирним чатні',
        'price': 160.00,
        'description': 'Печінковий паштет подається з грінками з багету та журавлиново- імбирним чатні. 200 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/ebf36f2b-89b7-4691-99db-4833e4be2984-image.jpeg'
    },
    {
        'name': 'Качинний паштет з в\'яленим інжиром',
        'price': 360.00,
        'description': 'Вишуканий паштет, приготований із м’яса качки з додаванням в’яленого інжиру, що надає йому легкої солодкавості та благородного аромату. Подається з хрумким багетом.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/87f9d10b-8975-4d6b-845f-19439352e079-image.jpeg'
    },
    {
        'name': 'Сало з цибулею',
        'price': 100.00,
        'description': 'Сало з цибулею. 100 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/f81885fd-c16e-4c38-8d75-03891f2f3172_image.jpeg'
    },
    {
        'name': 'Сало Чумацьке',
        'price': 55.00,
        'description': 'Сало Чумацьке. 100 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/76c97a1d-00e3-4b46-9516-1a8de2cebc16-image.jpeg'
    },
    {
        'name': 'Сирне плато',
        'price': 315.00,
        'description': 'Пармезан, брі, ландано, сир з горіхами, дор блю та мед. 170 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/b93c6570-9c12-41ab-8a96-9e0da272b79e-image.jpeg'
    },
    {
        'name': 'Тигрові креветки з гриля',
        'price': 420.00,
        'description': '*на фото подвійна порція Подаються з вершково-м\'ятним соусом. 200 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/1f4d3830-0f2c-4c15-9df5-7b779287e782_image.jpeg'
    },
    {
        'name': 'Язик відварний з майонезом',
        'price': 175.00,
        'description': 'Язик відварний з майонезом. 100 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/3bcf3354-1f12-4160-8214-03ae3db3067d_image.jpeg'
    },
    {
        'name': 'Паштет з яловичої печінки на виніс',
        'price': 260.00,
        'description': 'Паштет з яловичої печінки на виніс.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZxOIMYYN4dtiG_M5MdXvv_pR86N8yESOJHRWx6TOl6Q&s'
    },
    {
        'name': 'Закуска з печеним перцем з маслинами та зеленим йогуртовим кремом',
        'price': 195.00,
        'description': 'Легкий та ніжний йогуртовий крем ідеально поєднується з печеним перцем та маслинами.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/ec90176c-57f2-47b5-8967-414d95863ecf-image.jpeg'
    },
    {
        'name': 'Форшмак із оселедця',
        'price': 270.00,
        'description': 'Класичне поєднання оселедця, яблука, яйця та цибулі. Заправлений крафтовим майонезом із лимонним соком. Подається з хрусткими грінками із темного хліба. 300 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/10545693-abf6-4a4d-96ba-f47c91013fba-image.jpeg'
    },

    # --- Перші страви ---
    {
        'name': 'Чанахи з свининою',
        'price': 155.00,
        'description': 'Чанахи – грузинська страва, в якій ніжне м’ясо свинини тушкується з картоплею, томатами, квасолею та спеціями.',
        'category': categories['Перші страви'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/da15d253-d132-4c28-ad70-4f2996455bd2-image.jpeg'
    },
    {
        'name': 'Борщ Український з пампушками',
        'price': 135.00,
        'description': 'Традиційний Український червоний борщ подаємо із "Чумацьким" салом, сметаною та пампушками.',
        'category': categories['Перші страви'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/3f617d00-f80c-4c40-b4bb-d56af2d05862-image.jpeg'
    },
    {
        'name': 'Курячий бульйон з локшиною',
        'price': 95.00,
        'description': 'Наваристий бульйон з домашньої курки, подаємо з вермішеллю, морквою та курячими фрикаделями. 300 грам.',
        'category': categories['Перші страви'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/9af9cf19-59f2-49e3-a2f3-2b0dfbf3abff-image.jpeg'
    },
    {
        'name': 'Солянка',
        'price': 195.00,
        'description': 'Зварена на основі яловичого бульйону з п\'ятьма видами м\'яса. Подається з сметаною та грінками з білого багету. 400 грам.',
        'category': categories['Перші страви'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/Products/4242488_1693921701.9492_original.jpeg'
    },
    {
        'name': 'Крем-суп з білими грибами',
        'price': 175.00,
        'description': 'Крем суп із білих грибів. Подаємо з ароматним часниковим маслом, мікрогріном, печерицями та хлібним кільцем. 250 грам.',
        'category': categories['Перші страви'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/19328130-1662-4c5a-b23e-a13da048a5ba_image.jpeg'
    },

    # --- Салати овочеві ---
    {
        'name': 'Салат Грецький',
        'price': 175.00,
        'description': 'Огірок, помідор, перець болгарський, маслини, цибуля ріпчаста, сир фета та олія оливкова. 245 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/dd4e4be9-7568-4e11-9489-4985201c3a9f-image.jpeg'
    },
    {
        'name': 'Салат Вітамінний',
        'price': 95.00,
        'description': 'Капуста, морква, яблуко. цибуля зелена, гарбузове насіння, журавлина, оливкова олія та соус бальзаміко. 245 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/da090d4c-18ab-4f0e-964a-f22d561e848a-image.jpeg'
    },
    {
        'name': 'Салат з свіжої капусти',
        'price': 95.00,
        'description': 'Капуста, морква, цибуля зелена та заправка на вибір. 220 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/dd808ab1-d177-442f-9944-dfb9e40d585a-image.jpeg'
    },
    {
        'name': 'Салат з помідорів та огірків',
        'price': 75.00,
        'description': 'Огірок, помідор, цибуля та заправка на вибір. 140 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/af418e0d-5dde-4677-8e71-07294d021515_image.jpeg'
    },
    {
        'name': 'Салат з бурячка з домашнім сиром',
        'price': 115.00,
        'description': 'Буряк, сир домашній, часник, зелень, майонез та гранатовий соус. 245 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/1d87a14b-baca-4fdc-8b28-9f710ce7ac6d-image.jpeg'
    },
    {
        'name': 'Салат з буряком та сиром дор блю',
        'price': 175.00,
        'description': 'Мікс салату, буряк, філе апельсину, сир дор блю, грецький горіх та соус бальзаміко. 220 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/3764f7bd-2fb7-45ab-8a7e-c4b8d0205c6c-image.jpeg'
    },
    {
        'name': 'Карпачо з буряка',
        'price': 135.00,
        'description': 'Буряк запечений з спеціями під медово - гірчичною заправкою, руколою, фетою, грецькими горіхами та бальзаміком. 200 грам.',
        'category': categories['Салати овочеві'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/f17fa60b-d047-46ac-aecd-200e3afb79a3-image.jpeg'
    },

    # --- Салати рибні ---
    {
        'name': 'Салат з грильованим лососем',
        'price': 355.00,
        'description': 'Мікс салату, огірок, помідор, перепелине яйце, лосось на грилю та гірчична заправка. 220 грам.',
        'category': categories['Салати рибні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/Products/4242463_1693926703.7822_original.jpeg'
    },
    {
        'name': 'Цезар з тигровими креветками',
        'price': 295.00,
        'description': 'Мікс салату, помідор, яйце перепелине, креветки на грилю, соус, сир пармезан та крутони. 240 грам.',
        'category': categories['Салати рибні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/7c104ef8-c0ed-40ab-b46e-438219be6e51-image.jpeg'
    },
    {
        'name': 'Салат з слабосоленим лососем та філадельфією',
        'price': 355.00,
        'description': 'Мікс салату, помідор, огірок, слабосолений лосось, сир Філадельфія, сир пармезан та гірчична заправка. 235 грам.',
        'category': categories['Салати рибні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/67401cab-b96f-410d-8f15-01c4418e3eee_image.jpeg'
    },

    # --- Салати м'ясні ---
    {
        'name': 'Салат з курки з вершково-сирним соусом',
        'price': 195.00,
        'description': 'Мікс салату, курка, помідор, гриби, броколі та соус. 200 грам.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/Products/4242465_1693921618.7947_original.jpeg'
    },
    {
        'name': 'Салат з прошуто та грушею',
        'price': 265.00,
        'description': 'Мікс салату з медово-гірчичною заправкою, помідори, сир Камамбер, прошуто та груша. 200 грам.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/c2bda633-969a-42a1-87d3-090c0b003dad_image.jpeg'
    },
    {
        'name': 'Салат Цезар',
        'price': 230.00,
        'description': 'Мікс салату, помідор, бекон, яйце перепелине, курка, соус, пармезан та крутони.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/e9b57999-c73e-4e4d-af9f-88cc989c6871-image.jpeg'
    },
    {
        'name': 'Салат Мазовецький',
        'price': 165.00,
        'description': 'Язик, шинка печена, печериці мариновані, огірок квашений, сир моцарела, картопляний хмиз, крафтовий майонез та хлібна паличка. 190 грам.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/c11d23be-cd48-4f93-ae00-1e3bb34577fa-image.jpeg'
    },
    {
        'name': 'Салат Тбілісі',
        'price': 225.00,
        'description': 'Мікс салату, помідор, бастурма, цибуля маринована, фета, соус та хлібна паличка. 190 грам.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/8745e26c-c4a1-4605-af3f-f5b69c4ce2d5_image.jpeg'
    },
    {
        'name': 'Теплий салат з телятиною',
        'price': 285.00,
        'description': 'Мікс салату, телятина, цибуля, болгарський перець та імбирно-оливковий соус. 250 грам.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/Products/4242505_1693927198.6295_original.jpeg'
    },
    {
        'name': 'Салат з яловичої печінки та карамелізованими яблуками',
        'price': 205.00,
        'description': 'Мікс салату з імбирно-оливковим соусом, чері, печериці, яблука та яловича печінка. Подаємо з мікрогріном. 280 грам.',
        'category': categories['Салати м\'ясні'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/471ec220-94a6-4268-84af-7f2ea3f9253d-image.jpeg'
    },

    # --- Страви з свинини ---
    {
        'name': 'Ребра BBQ в медово-соєвому соусі',
        'price': 65.00,
        'description': 'Соковиті ребра, приготовані до м\'якості, в соєво-медовому соусі. Найкраще смакують з пивом, що підкреслює їхній насичений смак. (Ціна вказана за 100 г)',
        'category': categories['Страви з свинини'],
        'is_popular': False,
        'is_new': True,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/e41bc9be-0951-458e-9248-df9f58adfa02_image.jpg'
    },
    {
        'name': 'М\'ясна дошка',
        'price': 860.00,
        'description': 'Люля кебаб, ребра BBQ, стейк зі свиної шиї, картопля печена, соус BBQ та імбирний, цибуля маринована. 1200 грам.',
        'category': categories['Страви з свинини'],
        'is_popular': True,
        'is_new': True,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/Products/4242362_1693834533.4609_original.jpeg'
    },
    {
        'name': 'Три види м\'яса на одній тарелі',
        'price': 970.00,
        'description': 'Шашлик курячий, стейк із свинини та люля кебаб. Подаємо з кисло-солодким соусом, BBQ соусом та маринованою цибулею. 1100 грам.',
        'category': categories['Страви з свинини'],
        'is_popular': True,
        'is_new': True,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/2fecf764-7aae-4015-8758-92f82172d474_image.jpeg'
    },
    {
        'name': 'Стейк на грилі з свинної шиї',
        'price': 125.00,
        'description': 'Соковитий та ніжний стейк з шиї свинини з мармуровим розподілом жиру, має глибокий насичений смак. Джерело білка, вітамінів B6, B12, заліза та цинку. (Ціна вказана за 100 г)',
        'category': categories['Страви з свинини'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/40e4c41b-3953-4bc4-8e73-75ebdffd532f-image.jpeg'
    },
    {
        'name': 'Стейк на грилі з свинної вирізки',
        'price': 105.00,
        'description': 'Соковитий стейк із свиної вирізки, приготований до ідеальної ніжності, подається на тонкому лаваші з маринованою цибулею для додаткового аромату та смаку. (Ціна вказана за 100 г)',
        'category': categories['Страви з свинини'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/c1b61073-b244-437e-8b7f-e31e01953c91-image.jpeg'
    },
    {
        'name': 'Шашлик зі свиної шиї',
        'price': 125.00,
        'description': 'Соковитий шашлик з м\'якої свиної шиї, маринований у спеціях і приготований на грилі до ідеальної ніжності. Подається на тонкому лаваші з маринованою цибулею. (Ціна вказана за 100 г)',
        'category': categories['Страви з свинини'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/67d08ccca86b6228a6959134/8926eca3-e53c-48d9-b1b7-ad4476be3f8f-image.jpeg'
    },
    {
        'name': 'Деруни в горщику',
        'price': 225.00,
        'description': 'Рум’яні деруни, запечені в горщику разом із соковитими шматочками свинини, цибулею та ніжним вершковим соусом. Домашній смак у кожній ложці. 400 грам.',
        'category': categories['Страви з свинини'],
        'is_popular': False,
        'is_new': False,
        'image_url': 'https://img.postershop.me/cdn-cgi/image/width=640,format=webp/https://img.postershop.me/16256/03deca69-d9d4-4b74-a896-158ac0810342_image.jpeg'
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Referer': 'https://menu.ps.me/'
}

print("Заповнення бази даних та завантаження зображень...")

for item in dishes_data:
    slug = slugify_uk(item['name'])

    dish, created = Dish.objects.update_or_create(
        name=item['name'],
        defaults={
            'slug': slug,
            'price': item['price'],
            'description': item['description'],
            'category': item['category'],
            'is_popular': item['is_popular'],
            'is_new': item['is_new'],
            'is_available': True,
        }
    )

    if item.get('image_url'):
        try:
            res = requests.get(item['image_url'], headers=headers, timeout=10)
            if res.status_code == 200:
                file_name = f"{slug}.jpg"
                dish.image.save(file_name, ContentFile(res.content), save=True)
                print(f" Успішно завантажено фото для: {dish.name}")
            else:
                print(f" Код {res.status_code} для {dish.name}")
        except Exception as e:
            print(f" Помилка завантаження для {dish.name}: {e}")

print("\n Готово! Всі страви та фотографії оновлено!")