"""
Unit tests for the Text-to-KG CLI module.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import argparse

from cleverswarm.text_to_kg.cli import TextToKGCLI, main
from cleverswarm.client.file_type_enum import FileTypeAPI
from cleverswarm.client.job_enums import JobStatus
from cleverswarm.client.exceptions import ClientException


class TestTextToKGCLI(unittest.TestCase):
    """Test cases for the TextToKGCLI class."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "http://test-server.com/"
        # Create patches for path existence checks
        self.path_exists_patch = patch('pathlib.Path.exists', return_value=True)
        self.path_is_dir_patch = patch('pathlib.Path.is_dir', return_value=True)
        self.path_is_file_patch = patch('pathlib.Path.is_file', return_value=True)
        self.mkdir_patch = patch('pathlib.Path.mkdir')
        
        # Start the patches
        self.path_exists_patch.start()
        self.path_is_dir_patch.start()
        self.path_is_file_patch.start()
        self.mkdir_patch.start()
        
        # Mock CleverSwarmClient
        self.client_patch = patch('cleverswarm.text_to_kg.cli.CleverSwarmClient')
        self.mock_client_class = self.client_patch.start()
        self.mock_client = MagicMock()
        self.mock_client_class.return_value = self.mock_client
        
        # Create the CLI instance
        self.cli = TextToKGCLI(
            base_url=self.base_url,
            detailed=True,
            input_prefix="./input",
            output_prefix="./output",
            username="test-user",
            token="test-token"
        )

    def tearDown(self):
        """Tear down test fixtures."""
        self.path_exists_patch.stop()
        self.path_is_dir_patch.stop()
        self.path_is_file_patch.stop()
        self.mkdir_patch.stop()
        self.client_patch.stop()

    def test_create_job_without_wildcards(self):
        """Test creating a job without wildcards."""
        # Set up the mock return value
        self.mock_client.create_unstructured_to_kg_job.return_value = "test-job-id"
        
        # Call the method
        job_id = self.cli.create_job(
            input_text="test.txt",
            ontology_json="ontology.json",
            ontology_owl="ontology.owl"
        )
        
        # Verify the result
        self.assertEqual(job_id, "test-job-id")
        
        # Verify the client method was called correctly
        self.mock_client.create_unstructured_to_kg_job.assert_called_once()
        # We can check that the paths contain the expected file names
        args, kwargs = self.mock_client.create_unstructured_to_kg_job.call_args
        self.assertIn("test.txt", str(args[0]))
        self.assertIn("ontology.json", str(args[1]))
        self.assertIn("ontology.owl", str(args[2]))

    def test_create_job_with_wildcards(self):
        """Test creating a job with wildcards."""
        # Set up the mock return value
        self.mock_client.create_unstructured_to_kg_wildcards_job.return_value = "test-job-id"
        
        # Call the method
        job_id = self.cli.create_job(
            input_text="test.txt",
            ontology_json="ontology.json",
            ontology_owl="ontology.owl",
            wildcards="wildcards.json"
        )
        
        # Verify the result
        self.assertEqual(job_id, "test-job-id")
        
        # Verify the client method was called correctly
        self.mock_client.create_unstructured_to_kg_wildcards_job.assert_called_once()
        args, kwargs = self.mock_client.create_unstructured_to_kg_wildcards_job.call_args
        self.assertIn("test.txt", str(args[0]))
        self.assertIn("ontology.json", str(args[1]))
        self.assertIn("ontology.owl", str(args[2]))
        self.assertIn("wildcards.json", str(args[3]))

    def test_poll_job_to_completion(self):
        """Test polling a job to completion."""
        # Set up the mock return values
        self.mock_client.get_job_status.return_value = JobStatus.Processing
        self.mock_client.poll_job_ready_or_failed.return_value = JobStatus.Completed
        
        # Call the method
        self.cli.poll_job_to_completion("test-job-id")
        
        # Verify the client methods were called correctly
        self.mock_client.get_job_status.assert_called_with("test-job-id")
        self.mock_client.poll_job_ready_or_failed.assert_called_with("test-job-id")

    @patch('cleverswarm.text_to_kg.cli.TextToKGCLI.print_server_jobs')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_mode(self, mock_parse_args, mock_print_jobs):
        """Test the main function in 'list' mode."""
        # Set up the mock return value for parse_args
        mock_args = MagicMock()
        mock_args.mode = 'list'
        mock_args.detailed = True
        mock_args.server_url = "http://test-server.com/"
        mock_args.input_prefix = "./input"
        mock_args.output_prefix = "./output"
        mock_args.username = "test-user"
        mock_args.token = "test-token"
        mock_parse_args.return_value = mock_args
        
        # Mock sys.exit to prevent the test from exiting
        with patch('sys.exit'):
            # Call the main function
            main()
        
        # Verify print_server_jobs was called correctly
        mock_print_jobs.assert_called_with(True)

    @patch('cleverswarm.text_to_kg.cli.TextToKGCLI.delete_server_job')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_delete_mode(self, mock_parse_args, mock_delete_job):
        """Test the main function in 'delete' mode."""
        # Set up the mock return value for parse_args
        mock_args = MagicMock()
        mock_args.mode = 'delete'
        mock_args.job_id = "test-job-id"
        mock_args.server_url = "http://test-server.com/"
        mock_args.input_prefix = "./input"
        mock_args.output_prefix = "./output"
        mock_args.username = "test-user"
        mock_args.token = "test-token"
        mock_parse_args.return_value = mock_args
        
        # Mock sys.exit to prevent the test from exiting
        with patch('sys.exit'):
            # Call the main function
            main()
        
        # Verify delete_server_job was called correctly
        mock_delete_job.assert_called_with("test-job-id")


if __name__ == '__main__':
    unittest.main() 