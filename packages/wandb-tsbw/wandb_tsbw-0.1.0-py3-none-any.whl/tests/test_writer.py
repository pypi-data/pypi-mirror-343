"""
Unit tests for the wandb_tsbw.SummaryWriter class.
"""

import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import tempfile
import os

from wandb_tsbw import SummaryWriter


class TestSummaryWriter(unittest.TestCase):
    """Test cases for the SummaryWriter class."""

    def setUp(self):
        """Set up test cases."""
        self.temp_dir = tempfile.mkdtemp()
        self.patcher = patch('wandb.init')
        self.mock_init = self.patcher.start()
        self.mock_run = MagicMock()
        self.mock_init.return_value = self.mock_run

    def tearDown(self):
        """Tear down test cases."""
        self.patcher.stop()
        
    def test_init_with_wandb_kwargs(self):
        """Test initialization with wandb_kwargs."""
        wandb_kwargs = {
            'project': 'test_project',
            'entity': 'test_entity',
            'tags': ['test', 'unit_test']
        }
        
        writer = SummaryWriter(log_dir=self.temp_dir, wandb_kwargs=wandb_kwargs)
        
        # Verify that wandb.init was called with the correct arguments
        expected_args = {
            'dir': os.path.dirname(self.temp_dir),
            #'name': os.path.basename(self.temp_dir),
            'project': 'test_project',
            'entity': 'test_entity',
            'tags': ['test', 'unit_test']
        }
        
        # Check that each expected argument was passed to wandb.init
        call_args = self.mock_init.call_args[1]
        for key, value in expected_args.items():
            self.assertEqual(call_args[key], value)

    @patch('wandb.log')
    def test_add_scalar(self, mock_log):
        """Test add_scalar method."""
        writer = SummaryWriter(log_dir=self.temp_dir)
        writer.add_scalar('loss', 0.5, 10)
        mock_log.assert_called_once_with({'loss': 0.5}, step=10)

    @patch('wandb.log')
    def test_add_scalars(self, mock_log):
        """Test add_scalars method."""
        writer = SummaryWriter(log_dir=self.temp_dir)
        writer.add_scalars('metrics', {'loss': 0.5, 'accuracy': 0.9}, 10)
        mock_log.assert_called_once_with(
            {'metrics/loss': 0.5, 'metrics/accuracy': 0.9}, 
            step=10
        )

    @patch('wandb.log')
    def test_add_histogram(self, mock_log):
        """Test add_histogram method."""
        writer = SummaryWriter(log_dir=self.temp_dir)
        values = np.random.rand(100)
        with patch('wandb.Histogram') as mock_histogram:
            mock_histogram.return_value = 'histogram_obj'
            writer.add_histogram('dist', values, 10)
            mock_histogram.assert_called_once_with(values)
            mock_log.assert_called_once_with({'dist': 'histogram_obj'}, step=10)

    @patch('wandb.log')
    def test_add_image(self, mock_log):
        """Test add_image method."""
        writer = SummaryWriter(log_dir=self.temp_dir)
        img = np.random.rand(3, 64, 64)  # CHW format
        with patch('wandb.Image') as mock_image:
            mock_image.return_value = 'image_obj'
            writer.add_image('img', img, 10, dataformats='CHW')
            # Check that the image was transposed from CHW to HWC
            mock_image.assert_called_once()
            # Since we're mocking the call, we need to verify the shape
            call_args = mock_image.call_args[0][0]
            self.assertEqual(call_args.shape, (64, 64, 3))  # HWC format
            mock_log.assert_called_once_with({'img': 'image_obj'}, step=10)

    @patch('wandb.log')
    def test_add_text(self, mock_log):
        """Test add_text method."""
        writer = SummaryWriter(log_dir=self.temp_dir)
        with patch('wandb.Html') as mock_html:
            mock_html.return_value = 'html_obj'
            writer.add_text('text', 'Hello world', 10)
            mock_html.assert_called_once_with('<pre>Hello world</pre>')
            mock_log.assert_called_once_with({'text': 'html_obj'}, step=10)

    @patch('wandb.log')
    def test_add_hparams(self, mock_log):
        """Test add_hparams method."""
        # Explicitly patch the wandb.run property for this test
        with patch('wandb.run') as mock_run:
            # Set up the run mock properly
            mock_config = {}
            
            # Create a mock that behaves like a dictionary for config
            class MockConfig:
                def __init__(self):
                    self.data = {}
                
                def __setitem__(self, key, value):
                    self.data[key] = value
                
                def __getitem__(self, key):
                    return self.data[key]
            
            # Set the config attribute of the mock_run
            mock_run.config = MockConfig()
            
            # Initialize writer and call add_hparams
            writer = SummaryWriter(log_dir=self.temp_dir)
            writer.add_hparams(
                {'lr': 0.1, 'batch_size': 32},
                {'accuracy': 0.9, 'loss': 0.1},
                global_step=10
            )
            
            # Check that hyperparameters were added to wandb.config
            self.assertEqual(mock_run.config.data['lr'], 0.1)
            self.assertEqual(mock_run.config.data['batch_size'], 32)
            
            # Check that metrics were logged with hparams/ prefix
            mock_log.assert_called_once_with(
                {'hparams/accuracy': 0.9, 'hparams/loss': 0.1}, 
                step=10
            )

    def test_step_incrementation(self):
        """Test that step gets incremented when global_step is None."""
        writer = SummaryWriter(log_dir=self.temp_dir)
        self.assertEqual(writer.step, 0)
        
        with patch('wandb.log') as mock_log:
            writer.add_scalar('loss', 0.5)
            writer.add_scalar('accuracy', 0.9)
            
        self.assertEqual(writer.step, 2)

    def test_with_statement(self):
        """Test that SummaryWriter works with 'with' statement."""
        with SummaryWriter(log_dir=self.temp_dir) as writer:
            self.assertIsInstance(writer, SummaryWriter)


if __name__ == '__main__':
    unittest.main()
