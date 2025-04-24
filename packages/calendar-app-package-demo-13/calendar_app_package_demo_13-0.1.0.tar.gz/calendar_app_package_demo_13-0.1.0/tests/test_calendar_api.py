import sys
import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Add src to sys.path so we can import the app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from calendar_app_package.calendar_api import calendar_api
from calendar_app_package.task import Task

class TestGoogleCalendarAPI(unittest.TestCase):

    @patch('calendar_app_package.calendar_api.build')
    @patch('calendar_app_package.calendar_api.pickle.load')
    @patch('calendar_app_package.calendar_api.os.path.exists')
    @patch('calendar_app_package.calendar_api.InstalledAppFlow.from_client_secrets_file')
    @patch('builtins.open', new_callable=mock_open, read_data='{"installed": {"client_id": "test", "client_secret": "test", "auth_uri": "https://...", "token_uri": "https://...", "auth_provider_x509_cert_url": "https://...", "redirect_uris": ["http://localhost"], "project_id": "test"}}')
    def test_authenticate_with_existing_token(self, mock_open_file, mock_flow, mock_path_exists, mock_pickle_load, mock_build):
        # Setup mocks
        mock_path_exists.return_value = False
        mock_creds = MagicMock(valid=True)
        mock_instance = MagicMock()
        mock_instance.run_local_server.return_value = mock_creds
        mock_flow.return_value = mock_instance

        api = calendar_api()

        mock_build.assert_called_once()
        self.assertIsNotNone(api.service)


    @patch('calendar_app_package.calendar_api.build')
    def test_create_event(self, mock_build):
        # Set up mocks
        mock_service = MagicMock()
        mock_events = mock_service.events.return_value
        mock_events.insert.return_value.execute.return_value = {
            'htmlLink': 'https://calendar.google.com/eventlink'
        }

        mock_build.return_value = mock_service

        with patch('calendar_app_package.calendar_api.os.path.exists', return_value=False), \
             patch('calendar_app_package.calendar_api.InstalledAppFlow.from_client_secrets_file') as mock_flow, \
             patch('calendar_app_package.calendar_api.pickle.dump'):
            
            mock_instance = MagicMock()
            mock_instance.run_local_server.return_value = MagicMock(valid=True)
            mock_flow.return_value = mock_instance

            api = calendar_api()
            api.service = mock_service  # manually inject the mock

        task = Task("Mock Event", "A test", "2025-04-21T10:00:00", "2025-04-21T11:00:00")
        result = api.create_event(task)

        self.assertEqual(result, "https://calendar.google.com/eventlink")
        mock_events.insert.assert_called_once()

if __name__ == '__main__':
    unittest.main()


# Chat GPT was used to help make mock tests for API integration.
# The tests cover the authentication process and the event creation process.
# The tests use unittest and unittest.mock to simulate the behavior of the Google Calendar API.