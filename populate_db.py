import os
import django
import requests
from django.core.files.base import ContentFile

# Налаштування середовища Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vulyk_project.settings')
django.setup()

from menu.models import Category, Dish


# Функція для створення чистих латинських слагах
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
categories_data = ['Сніданки', 'Закуски', 'Основні страви']

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
    # Новинки та популярні
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
        'image_url': None
    },
    {
        'name': 'Медальйони з ягідним соусом',
        'price': 395.00,
        'description': 'Ніжні медальйони з внутрішньої яловичої вирізки, обсмажені до ідеальної соковитості, подаються з ароматним ягідним соусом.',
        'category': categories['Основні страви'],
        'is_popular': False,
        'is_new': True,
        'image_url': None
    },
    {
        'name': 'Кабачкові деруни з крем сиром та слабосоленим лососем',
        'price': 325.00,
        'description': 'Ніжні деруни з кабачка додаються зі слабосоленим лососем, свіжим огірком, зеленню та крем сиром.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': True,
        'image_url': None
    },
    {
        'name': 'Вареники з вишнями',
        'price': 195.00,
        'description': 'Ніжне тісто, соковита начинка зі стиглих вишень — класика, що дарує справжній смак літа.',
        'category': categories['Основні страви'],
        'is_popular': False,
        'is_new': True,
        'image_url': None
    },
    {
        'name': 'Люля-кебаб',
        'price': 170.00,
        'description': 'Соковита суміш яловичини, курки та свинини, приправлена спеціями та обсмажена до золотистої скоринки.',
        'category': categories['Основні страви'],
        'is_popular': False,
        'is_new': True,
        'image_url': None
    },

    # Сніданки
    {
        'name': 'Сніданок із домашньою ковбаскою',
        'price': 295.00,
        'description': 'Скребл із смаженою домашньою ковбаскою, подаємо з салатом з помідорів, огірків та листя салату заправлений олією.',
        'category': categories['Сніданки'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Сніданок з беконом',
        'price': 345.00,
        'description': 'Смажена яєчня з беконом, подаємо з свіжими овочами та хрумкими грінками з молочного багету. 340 грам.',
        'category': categories['Сніданки'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Сніданок із червоною рибою',
        'price': 365.00,
        'description': 'Скребл із слабосоленим лососем та сиром філадельфія, подаємо з салатом з помідорів, огірків та листя салату.',
        'category': categories['Сніданки'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },

    # Закуски
    {
        'name': 'Асорті сала з огірочками',
        'price': 365.00,
        'description': 'Сало "Чумацьке", сало біле, сало з м\'ясною прослойкою, огірки квашені, гірчиця, цибуля та грінки з чорного хліба. 600 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'М\'ясне асорті 250 гр',
        'price': 295.00,
        'description': 'Копчений бочок та вирізка, домашня шинка та ковбаска з печі, хрін. 250 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Овочева нарізка',
        'price': 195.00,
        'description': 'Огірок, помідор та болгарський перець. 300 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Оселедець з цибулею',
        'price': 220.00,
        'description': 'Оселедець маринований з цибулею та чорними грінками.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Печінковий паштет з вишнево-імбирним чатні',
        'price': 160.00,
        'description': 'Печінковий паштет подається з грінками з багету та журавлиново-імбирним чатні. 200 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Качинний паштет з в\'яленим інжиром',
        'price': 360.00,
        'description': 'Вишуканий паштет, приготовлений із м\'яса качки з додаванням в\'яленого інжиру, що надає йому легкої солодкавості.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Сало з цибулею',
        'price': 100.00,
        'description': 'Сало з цибулею. 100 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Сало Чумацьке',
        'price': 55.00,
        'description': 'Сало Чумацьке. 100 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Сирне плато',
        'price': 315.00,
        'description': 'Пармезан, брі, ландано, сир з горіхами, дор блю та мед. 170 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Тигрові креветки з гриля',
        'price': 420.00,
        'description': '*на фото подвійна порція. Подаються з вершково-м\'ятним соусом. 200 грам.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
    },
    {
        'name': 'Язик відварний з майонезом',
        'price': 175.00,
        'description': 'Язик відварний з майонезом.',
        'category': categories['Закуски'],
        'is_popular': False,
        'is_new': False,
        'image_url': None
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