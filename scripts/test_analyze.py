import requests
import base64
import argparse

def test_analyze_endpoint(host="localhost", port=8080, image_path=None):
    """Тестирует эндпоинт /analyze"""
    
    # Если путь к изображению не указан, используем демо-режим
    if not image_path:
        print("❌ Укажите путь к изображению через --image_path")
        return
    
    # Читаем и кодируем изображение в base64
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Ошибка чтения изображения: {e}")
        return
    
    # Формируем URL и данные запроса
    url = f"http://{host}:{port}/analyze"
    payload = {
        "image_data": image_data
    }
    
    try:
        print(f"📤 Отправка запроса на {url}...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(result)
            print("✅ Запрос выполнен успешно!")
            print(f"❓ Вопросы:\n{result.get('questions', 'N/A')}")
            print(f"❓ Дескрипшен: {result.get('rash_description', 'N/A')}")
            
            return result
        else:
            print(f"❌ Ошибка сервера: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Не удалось подключиться к серверу {host}:{port}")
        print("   Убедитесь, что сервер запущен")
    except Exception as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")

def test_analyze_endpoint_with_answers(host="localhost", port=8080, first_result=None):
    """Тестирует эндпоинт /analyze"""
    print('--------------------------------------------')
    # Формируем URL и данные запроса
    url = f"http://{host}:{port}/analyze"
    payload = {
        'questions': first_result.get('questions', 'N/A'),
        'question_answers': """Да, зуд появился два дня назад, боли нет, думаю натёр таки просто""",
        'rash_description': first_result.get('rash_description', 'N/A')
    }
    
    try:
        print(f"📤 Отправка запроса на {url}...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Запрос выполнен успешно!")
            print(f"📄 Ответ модели: {result.get('recommendations', 'N/A')}")
            
            return result
        else:
            print(f"❌ Ошибка сервера: {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Не удалось подключиться к серверу {host}:{port}")
        print("   Убедитесь, что сервер запущен")
    except Exception as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test client for Skin Rash Analyzer API")
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("--image_path", help="Path to image for analysis")
    
    args = parser.parse_args()
    
    print("🧪 Testing Skin Rash Analyzer API...")
    
    # Тестируем analyze endpoint первично
    first_result = test_analyze_endpoint(args.host, args.port, args.image_path)

    # А теперь с вопросами
    test_analyze_endpoint_with_answers(args.host, args.port, first_result)