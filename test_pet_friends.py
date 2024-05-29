import os.path
# import images

from api import PetFriens
from settings import valid_email, valid_password, valid_name, valid_animal_type, valid_age, valid_pet_photo, invalid, invalid1, invalid_key

pf = PetFriens()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # Отправка запроса и получение ответа с кодом статуса 200
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    # Получение списока домашних животных.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name= valid_name, animal_type= valid_animal_type, age= valid_age, pet_photo= valid_pet_photo):
    # Путь к изображению питомца
    pet_photo: os.path.join(os.path.dirname(__file__), pet_photo)
    # получение API ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_update_self_pet_info(name='Енот', animal_type='Енот', age=5):
    # Проверяем возможность обновления информации о питомце

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_delete_pet():
    # Проверяем возможность удаления питомца

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(name=str(valid_name), animal_type=str(valid_animal_type), age=int(valid_age), pet_photo=str(valid_pet_photo))
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_information_about_new_pet_without_photo(name= 'Тим', animal_type= 'Мышонок', age= '3'):
    # Добавляем информацию о новом питомце без фотографии

    # получение API ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo = 'images/Тим.jpg'):
    # Добавляем фото домашнего животного

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, name= 'Тим', animal_type= 'Мышонок', age= '3')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.pets_set_photo_pet_id(auth_key, pet_id, pet_photo)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев питомцев имя нашего обновляемого питомца
    assert status == 200
    assert result['name'] == my_pets['pets'][0]['name']

def test_get_api_key_for_invalid_user(email=invalid, password=invalid1):
    # Отправка запроса c невалидными данными пользователя
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status != 200
    assert 'key' in result
    print('Неправильный логин/пароль')

def test_invalid_user(email='123@ya.ru', password=' '):
    # Отправка запроса c невалидными данными пользователя
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные
    assert status != 200
    assert 'key' in result
    print('Неправильный логин/пароль')

def test_get_invalid_auth_key(filter=''):
    # Проверяем возможность работы с не валидным auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(invalid_key, filter)

    assert status != 200
    assert 'key' in result
    print('Неверный auth_key')

def test_availability_of_pet_cards(filter=''):
    # Проверка колличества карточек в списке животных.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 10
    print('Корректный список карточек питомцев')

def test_validation_of_fields(name= '154дл', animal_type= '123548', age= ''):
    # Проверка валидации полей при заполнении данных в карточке животного
    # получение API ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца с не корректными данными
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] == name
    print('Некорректно заполнены поля')

def test_invalidation_fields(name= '', animal_type= '', age= ''):
    # Проверка создания карточки с пустыми полями
    # получение API ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца с не корректными данными
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] == name
    print('Поля пустые. Некорректно заполнены поля')

def test_update_pet_info(name='', animal_type='слон', age=5):
    # Проверяем возможность изменить данные в существующей карточке

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_txt_file_of_pet(pet_photo = 'images/.txt'):
    # Добавляем текстовый документ вместо фото домашнего животного

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, name= 'KJuh', animal_type= 'KJJh', age= '3')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.pets_set_photo_pet_id(auth_key, pet_id, pet_photo)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев питомцев имя нашего обновляемого питомца
    assert status != 200
    print('Неверный формат')

def test_invalid_data_pet_without_photo(name= '15485', animal_type= '12365', age= '3'):
    # Добавляем информацию о питомце и заполняем поля цифровыми значениями

    # получение API ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status != 200
    assert result['name'] == name
    print('Некорректно заполненные поля')

def test_creating_a_card_with_empty_fields(name= ' ', animal_type= ' ', age= ' ', pet_photo= ' '):
    # Путь к изображению питомца
    pet_photo: os.path.join(os.path.dirname(__file__), pet_photo)
    # получение API ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200
    assert result['name'] == name
    print('Не корректно заполненные поля')













