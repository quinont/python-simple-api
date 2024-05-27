import unittest
from unittest.mock import patch, Mock
from flask import Flask
from app import app, get_messages, SERVER_MESSAGES


class FlaskAppTests(unittest.TestCase):

    @patch('app.requests.get')
    def test_index(self, mock_get):
        # Configurar el mock para la solicitud GET
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["Message 1", "Message 2"]
        mock_get.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Message 1", response.data)
            self.assertIn(b"Message 2", response.data)

    @patch('app.requests.post')
    def test_add_message(self, mock_post):
        # Configurar el mock para la solicitud POST
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.post('/add_message', data={'message': 'New Message'})
            self.assertEqual(response.status_code, 302)

    @patch('app.requests.post')
    def test_add_message_error(self, mock_post):
        # Configurar el mock para la solicitud POST
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.post('/add_message', data={'message': 'New Message'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.text, "Error adding message")

    @patch('app.requests.delete')
    def test_delete_message(self, mock_delete):
        # Configurar el mock para la solicitud DELETE
        mock_response = Mock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.post('/delete_message/0')
            self.assertEqual(response.status_code, 302)

    @patch('app.requests.delete')
    def test_delete_message_error(self, mock_delete):
        # Configurar el mock para la solicitud DELETE
        mock_response = Mock()
        mock_response.status_code = 400
        mock_delete.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.post('/delete_message/0')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.text, "Error deleting message")

    @patch('app.requests.put')
    def test_update_message(self, mock_put):
        # Configurar el mock para la solicitud PUT
        mock_response = Mock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.post('/update_message/0', data={'updated_message': 'Updated Message'})
            self.assertEqual(response.status_code, 302)

    @patch('app.requests.put')
    def test_update_message_error(self, mock_put):
        # Configurar el mock para la solicitud PUT
        mock_response = Mock()
        mock_response.status_code = 400
        mock_put.return_value = mock_response

        # Crear un cliente de prueba
        with app.test_client() as client:
            response = client.post('/update_message/0', data={'updated_message': 'Updated Message'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.text, "Error updating message")

    @patch('app.requests.get')
    def test_get_messages(self, mock_get):
        # Configurar el mock para la solicitud GET
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["Message 1", "Message 2"]
        mock_get.return_value = mock_response

        messages, err = get_messages()
        mock_get.assert_called_with(f'http://{SERVER_MESSAGES}/api/messages')
        self.assertEqual(messages, ["Message 1", "Message 2"])
        self.assertEqual(err, "")

    @patch('app.requests.get')
    def test_get_messages_error(self, mock_get):
        # Configurar el mock para la solicitud GET con error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        messages, err = get_messages()
        mock_get.assert_called_with(f'http://{SERVER_MESSAGES}/api/messages')
        self.assertEqual(messages, [])
        self.assertEqual("ERROR: respuesta del servidor 500", err)

    @patch('app.requests.get')
    def test_get_messages_Exception(self, mock_get):
        mock_get.side_effect = Exception

        messages, err = get_messages()
        self.assertEqual(messages, [])
        self.assertEqual("ERROR: , el server esta prendido?", err)


if __name__ == '__main__':
    unittest.main()
