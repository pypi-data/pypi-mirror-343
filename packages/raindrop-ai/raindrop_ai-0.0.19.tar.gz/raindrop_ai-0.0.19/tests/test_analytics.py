import time
import unittest
from unittest.mock import patch
import raindrop.analytics as analytics
from raindrop.version import VERSION
import sys


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        analytics.write_key = "0000"
        analytics.api_url = "http://localhost:3000/"

    def tearDown(self):
        # Clean up any resources or reset any state after each test
        analytics.flush()
        pass

    def test_identify(self):
        with patch('requests.post') as mock_post:
            user_id = "user123"
            traits = {"email": "john@example.com", "name": "John"}

            analytics.identify(user_id, traits)
            analytics.flush()  # Force flush to trigger request

            # Verify the POST request was made
            mock_post.assert_called_once()
            
            # Get the data that was sent
            call_args = mock_post.call_args
            url = call_args[0][0]
            data = call_args[1]['json'][0]  # First event in the batch
            
            # Verify URL and data
            self.assertEqual(url, "http://localhost:3000/users/identify")
            self.assertEqual(data['user_id'], user_id)
            self.assertEqual(data['traits'], traits)

    @patch('requests.post')
    def test_track(self, mock_post):
        # Test data
        user_id = "user123"
        event = "signed_up"
        properties = {"plan": "Premium"}
        
        # Track the event
        analytics.track(user_id, event, properties)
        
        # Force a flush to trigger the HTTP request
        analytics.flush()
        
        # Verify the POST request was made
        mock_post.assert_called_once()
        
        # Get the data that was sent
        call_args = mock_post.call_args
        url = call_args[0][0]
        data = call_args[1]['json'][0]  # First event in the batch
        
        # Verify URL
        self.assertEqual(url, "http://localhost:3000/events/track")
        
        # Verify request structure
        self.assertEqual(data['user_id'], user_id)
        self.assertEqual(data['event'], event)
        self.assertEqual(data['properties']['plan'], "Premium")
        
        # Verify context data
        self.assertEqual(data['properties']['$context']['library']['name'], "python-sdk")
        self.assertEqual(data['properties']['$context']['library']['version'], VERSION)
        self.assertEqual(
            data['properties']['$context']['metadata']['pyVersion'],
            f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        
        # Verify other required fields
        self.assertIn('event_id', data)
        self.assertIn('timestamp', data)

    @patch('requests.post')
    def test_track_ai(self, mock_post):
        # Test data
        user_id = "user123"
        event = "ai_completion"
        model = "gpt-3.5"
        user_input = "Hello"
        output = "Hi there!"
        convo_id = "conv123"
        properties = {"temperature": 0.7}
        
        # Track the AI event
        analytics.track_ai(
            user_id=user_id,
            event=event,
            model=model,
            user_input=user_input,
            output=output,
            convo_id=convo_id,
            properties=properties
        )
        
        # Force a flush
        analytics.flush()
        
        # Verify the POST request was made
        mock_post.assert_called_once()
        
        # Get the data that was sent
        call_args = mock_post.call_args
        data = call_args[1]['json'][0]  # First event in the batch
        
        # Verify AI-specific fields
        self.assertEqual(data['ai_data']['model'], model)
        self.assertEqual(data['ai_data']['input'], user_input)
        self.assertEqual(data['ai_data']['output'], output)
        self.assertEqual(data['ai_data']['convo_id'], convo_id)
        
        # Verify common fields
        self.assertEqual(data['user_id'], user_id)
        self.assertEqual(data['event'], event)
        self.assertEqual(data['properties']['temperature'], 0.7)
        self.assertIn('event_id', data)
        self.assertIn('timestamp', data)

    def test_flush(self):
        with patch('requests.post') as mock_post:
            user_id = "user123"
            event = "ai_chat"
            model = "GPT-3"
            input_text = "Hello"
            output_text = "Hi there!"

            analytics.track_ai(
                user_id, event, model=model, user_input=input_text, output=output_text
            )

            analytics.flush()  # Force flush

            # Verify the buffer is empty after flush
            self.assertEqual(len(analytics.buffer), 0)
            
            # Verify the POST request was made
            mock_post.assert_called_once()

    def test_track_ai_with_size_limit(self):
        with patch('requests.post') as mock_post:
            user_id = "user123"
            event = "ai_chat_test"
            model = "GPT-3"
            input_text = "Hello"
            output_text = "Hi there!"
            properties = {
                "key": "v" * 10000,
                "key2": "v" * 10000,
                "key3": "v" * 1048576,  # 1 MB of data (1024 * 1024 bytes)
            }

            # Capture logged output
            with self.assertLogs('dawnai.analytics', level='WARNING') as log_capture:
                analytics.track_ai(
                    user_id, event, model=model, user_input=input_text, output=output_text, properties=properties
                )
                analytics.flush()  # Force flush

            # Check the logged output
            self.assertTrue(any("[dawn] Events larger than" in message for message in log_capture.output),
                            "Expected size warning is not logged")

            # Verify no request was made since event was too large
            mock_post.assert_not_called()

    @patch('requests.post')
    def test_track_signal(self, mock_post):
        # Test basic signal tracking
        event_id = "event123"
        name = "thumbs_up"
        signal_type = "feedback"
        properties = {"rating": 5}
        comment = "Great response!"
        attachment_id = "attach123"
        after = "Updated content"

        # Track signal with all fields
        analytics.track_signal(
            event_id=event_id,
            name=name,
            signal_type=signal_type,
            properties=properties,
            comment=comment,
            attachment_id=attachment_id,
            after=after
        )
        
        # Force a flush
        analytics.flush()
        
        # Verify the POST request was made
        mock_post.assert_called_once()
        
        # Get the data that was sent
        call_args = mock_post.call_args
        url = call_args[0][0]
        data = call_args[1]['json'][0]  # First event in the batch
        
        # Verify URL
        self.assertEqual(url, "http://localhost:3000/signals/track")
        
        # Verify signal data
        self.assertEqual(data['event_id'], event_id)
        self.assertEqual(data['signal_name'], name)
        self.assertEqual(data['signal_type'], signal_type)
        self.assertEqual(data['attachment_id'], attachment_id)
        
        # Verify properties including comment and after
        self.assertEqual(data['properties']['rating'], 5)
        self.assertEqual(data['properties']['comment'], comment)
        self.assertEqual(data['properties']['after'], after)

        # Test size limit handling
        mock_post.reset_mock()
        large_properties = {
            "key": "v" * 10000,
            "key2": "v" * 10000,
            "key3": "v" * 1048576,  # 1 MB of data
        }

        # Capture logged output for oversized event
        with self.assertLogs('dawnai.analytics', level='WARNING') as log_capture:
            analytics.track_signal(
                event_id=event_id,
                name=name,
                properties=large_properties
            )
            analytics.flush()

        # Check the logged output
        self.assertTrue(any("[dawn] Events larger than" in message for message in log_capture.output),
                       "Expected size warning is not logged")

        # Test different signal types
        mock_post.reset_mock()
        for signal_type in ["default", "feedback", "edit"]:
            analytics.track_signal(
                event_id=event_id,
                name=name,
                signal_type=signal_type
            )
            analytics.flush()
            
            data = mock_post.call_args[1]['json'][0]
            self.assertEqual(data['signal_type'], signal_type)
            mock_post.reset_mock()
