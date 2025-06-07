from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class S3StorageTests(TestCase):
    def test_file_upload_and_read(self):
        """Тест загрузки файла в S3 и чтения метаданных"""
        # 1. Тест загрузки файла
        test_content = b"Test content from Django"
        file_path = "test_django.txt"

        # Сохраняем файл
        saved_path = default_storage.save(file_path, ContentFile(test_content))
        print(f"Файл сохранен в: {saved_path}")

        # 2. Проверяем существование файла
        exists = default_storage.exists(saved_path)
        self.assertTrue(exists, "Файл не был загружен в S3")

        # 3. Читаем метаданные (аналог head-object)
        try:
            with default_storage.open(saved_path) as f:
                size = f.size
                print(f"Размер файла: {size} байт")
                self.assertEqual(size, len(test_content))
        except Exception as e:
            self.fail(f"Ошибка чтения файла: {e}")

        # 4. Получаем URL файла
        file_url = default_storage.url(saved_path)
        print(f"URL файла: {file_url}")

        # 5. Удаляем тестовый файл (опционально)
        default_storage.delete(saved_path)
