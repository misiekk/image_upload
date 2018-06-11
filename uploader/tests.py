from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from io import BytesIO

from .models import ImageUploader


class UploaderTest(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        ImageUploader.objects.create(filename='test',
                                     image=ImageFile(file=BytesIO(b'\x00\x01\x02\x03'), name='image.jpg'))

    def _get_new_image_file(self, image_name):
        gif_file = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        file = SimpleUploadedFile(name=image_name, content=gif_file, content_type='image/gif')
        return ImageFile(file=file, name=file.name)

    def test_urls(self):
        response = self.client.get('/image/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/image/test/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/image/no_existing/')
        self.assertEqual(response.status_code, 404)

    def test_access_image(self):
        response = self.client.get('/image/test/')
        self.assertIn(b'test image', response.content)

    def test_upload_image(self):
        self.assertEqual(len(ImageUploader.objects.all()), 1)

        response = self.client.post('/image/', {
            'name': 'next',
            'image': self._get_new_image_file('next.gif')
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ImageUploader.objects.all()), 2)
        self.assertEqual(response.content, b'next image uploaded!')

        response = self.client.post('/image/', {
            'name': 'next',
            'image': self._get_new_image_file('next.gif')
        })
        self.assertEqual(response.content, b'next image changed!')
        self.assertEqual(len(ImageUploader.objects.all()), 2)

    def test_upload_image_with_empty_name(self):
        uploader = ImageUploader(image=self._get_new_image_file('next.gif'))
        self.assertRaises(ValidationError, uploader.full_clean)
