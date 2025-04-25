"""
Unit tests for the CleverSwarm client.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import requests
import json

from cleverswarm.client import CleverSwarmClient, JobStatus, FileTypeAPI
from cleverswarm.client.exceptions import ClientException, UnauthorizedException, JobNotFoundException


class TestCleverSwarmClient(unittest.TestCase):
    """Test cases for the CleverSwarmClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_url = "http://test-server.com/"
        self.client = CleverSwarmClient(base_url=self.base_url, token="test-token", username="test-user")

    @patch('requests.get')
    def test_get_jobs_list(self, mock_get):
        """Test getting a list of jobs."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": "job1", "type": "Benchmark", "status": "Completed"},
            {"id": "job2", "type": "UnstructuredWithOntology", "status": "Processing"}
        ]
        mock_get.return_value = mock_response
        
        # Call the method with is_benchmark=True
        jobs = self.client.get_jobs_list(is_benchmark=True)
        
        # Verify the result
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["id"], "job1")
        
        # Call with is_benchmark=False
        jobs = self.client.get_jobs_list(is_benchmark=False)
        
        # Verify the result
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["id"], "job2")
        
        # Verify requests.get was called correctly
        mock_get.assert_called_with(
            self.base_url + 'jobs',
            headers={'Authorization': 'Bearer test-token'},
            timeout=self.client._timeout
        )

    @patch('requests.get')
    def test_get_job_status(self, mock_get):
        """Test getting a job status."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = "Completed"
        mock_get.return_value = mock_response
        
        # Call the method
        status = self.client.get_job_status("job1")
        
        # Verify the result
        self.assertEqual(status, JobStatus.Completed)
        
        # Verify requests.get was called correctly
        mock_get.assert_called_with(
            self.base_url + 'jobs/job1',
            headers={'Authorization': 'Bearer test-token'},
            timeout=self.client._timeout
        )

    @patch('requests.get')
    def test_get_job_status_not_found(self, mock_get):
        """Test getting a non-existent job status."""
        # Mock the response for a 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Job not found"}
        mock_get.return_value = mock_response
        
        # Call the method and expect an exception
        with self.assertRaises(JobNotFoundException):
            self.client.get_job_status("nonexistent")

    @patch('requests.post')
    def test_create_unstructured_to_kg_job(self, mock_post):
        """Test creating an unstructured text to KG job."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"job_id": "new-job"}
        mock_post.return_value = mock_response
        
        # Mock input files
        test_file = Path("test.txt")
        ontology_file = Path("ontology.json")
        ontology_spec_file = Path("ontology.owl")
        
        # Mock open files
        with patch('builtins.open', mock_open(read_data="test data")):
            # Call the method
            job_id = self.client.create_unstructured_to_kg_job(
                test_file, ontology_file, ontology_spec_file,
                force_filetype=FileTypeAPI.AutoDetect
            )
        
        # Verify the result
        self.assertEqual(job_id, "new-job")
        
        # Verify request was called correctly
        mock_post.assert_called_once()
        # We can't check the files parameter easily, but we can check the URL
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], self.base_url + 'jobs/unstructured?force_filetype=AutoDetect')
        self.assertEqual(kwargs['headers'], {'Authorization': 'Bearer test-token'})

    @patch('cleverswarm.client.cleverswarm_client.CleverSwarmClient.get_job_status')
    def test_poll_job_ready_or_failed(self, mock_get_status):
        """Test polling a job until completion."""
        # Mock the responses to simulate a job that completes after two checks
        mock_get_status.side_effect = [
            JobStatus.Processing,
            JobStatus.Completed
        ]
        
        # Patch time.sleep to avoid waiting in the test
        with patch('time.sleep'):
            # Call the method
            status = self.client.poll_job_ready_or_failed("job1")
        
        # Verify the result
        self.assertEqual(status, JobStatus.Completed)
        
        # Verify get_job_status was called the expected number of times
        self.assertEqual(mock_get_status.call_count, 2)


if __name__ == '__main__':
    unittest.main() 