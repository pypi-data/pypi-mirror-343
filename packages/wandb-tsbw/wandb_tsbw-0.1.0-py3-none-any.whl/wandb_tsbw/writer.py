"""
Implementation of the SummaryWriter class that provides a compatibility layer
between TensorBoard's SummaryWriter and Weights & Biases.
"""

import os
import time
import warnings
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np

try:
    import wandb
except ImportError:
    raise ImportError(
        "wandb package is required for wandb_tsbw. "
        "Please install it with `pip install wandb`."
    )


class SummaryWriter:
    """
    A drop-in replacement for TensorBoard's SummaryWriter that logs to Weights & Biases.
    
    This class implements the same interface as TensorBoard's SummaryWriter
    but sends all the data to W&B instead.
    """
    
    def __init__(
        self,
        log_dir: Optional[str] = None,
        run_name: Optional[str] = None,
        comment: str = '',
        purge_step: Optional[int] = None,
        max_queue: int = 10,
        flush_secs: int = 120,
        filename_suffix: str = '',
        wandb_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize a SummaryWriter for W&B logging.
        
        Args:
            log_dir: Directory where W&B will write data. If None, a directory is created.
            run_name: name of the run in W&B.
            comment: Comment appended to the default log_dir.
            purge_step: Step at which to purge data (ignored, kept for compatibility).
            max_queue: Size of the queue for pending events (ignored, kept for compatibility).
            flush_secs: How often to flush pending events (ignored, kept for compatibility).
            filename_suffix: Suffix added to all event files (ignored, kept for compatibility).
            wandb_kwargs: Dictionary of keyword arguments to pass to wandb.init().
            **kwargs: Legacy support for passing wandb.init parameters (wandb_kwargs is preferred).
        """
        self.log_dir = log_dir
        
        # Initialize wandb if it's not already initialized
        if not wandb.run:
            # Extract the run name from log_dir if possible
            # run_name = os.path.basename(log_dir) if log_dir else None
            #if comment and run_name:
            #    run_name = f"{run_name}_{comment}"
            #elif comment:
            #    run_name = comment
                
            # Initialize wandb with the given parameters
            init_kwargs = {
                'dir': os.path.dirname(log_dir) if log_dir else None,
            }
           
            if run_name is not None:
                init_kwargs['name'] = run_name
 
            # Add any parameters from wandb_kwargs (these take precedence)
            if wandb_kwargs is not None:
                init_kwargs.update(wandb_kwargs)
                
            # For backward compatibility, also add any parameters from **kwargs
            # (but wandb_kwargs take precedence if both are provided)
            if kwargs:
                for k, v in kwargs.items():
                    if k not in init_kwargs:
                        init_kwargs[k] = v
            
            # Remove None values
            init_kwargs = {k: v for k, v in init_kwargs.items() if v is not None}
            
            # Initialize wandb
            wandb.init(**init_kwargs)
            
        self.step = 0 if purge_step is None else purge_step
        
    def add_scalar(
        self, 
        tag: str, 
        scalar_value: float, 
        global_step: Optional[int] = None, 
        walltime: Optional[float] = None
    ):
        """
        Add scalar data to W&B.
        
        Args:
            tag: Data identifier
            scalar_value: Value to save
            global_step: Global step value to record
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        wandb.log({tag: scalar_value}, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_scalars(
        self, 
        main_tag: str, 
        tag_scalar_dict: Dict[str, float], 
        global_step: Optional[int] = None, 
        walltime: Optional[float] = None
    ):
        """
        Add multiple scalars to W&B.
        
        Args:
            main_tag: The parent name for the tags
            tag_scalar_dict: Key-value pairs storing tag name and corresponding values
            global_step: Global step value to record
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        # Create prefixed tags
        log_dict = {f"{main_tag}/{tag}": value for tag, value in tag_scalar_dict.items()}
        wandb.log(log_dict, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_histogram(
        self, 
        tag: str, 
        values: Union[np.ndarray, List[float]], 
        global_step: Optional[int] = None, 
        bins: str = 'tensorflow', 
        walltime: Optional[float] = None, 
        max_bins: Optional[int] = None
    ):
        """
        Add histogram data to W&B.
        
        Args:
            tag: Data identifier
            values: Values to build histogram
            global_step: Global step value to record
            bins: Binning method (ignored, handled by W&B)
            walltime: Optional override default walltime (time.time())
            max_bins: Maximum number of bins (ignored, handled by W&B)
        """
        step = global_step if global_step is not None else self.step
        
        # Convert to numpy array if not already
        if not isinstance(values, np.ndarray):
            values = np.array(values)
            
        # Log histogram to W&B
        wandb.log({
            tag: wandb.Histogram(values)
        }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_image(
        self, 
        tag: str, 
        img_tensor: np.ndarray, 
        global_step: Optional[int] = None, 
        walltime: Optional[float] = None, 
        dataformats: str = 'CHW'
    ):
        """
        Add image data to W&B.
        
        Args:
            tag: Data identifier
            img_tensor: Image data
            global_step: Global step value to record
            walltime: Optional override default walltime (time.time())
            dataformats: Format of the input image (CHW|HWC|HW)
        """
        step = global_step if global_step is not None else self.step
        
        # Convert to numpy array if it's a torch tensor
        if hasattr(img_tensor, 'detach') and hasattr(img_tensor, 'cpu') and hasattr(img_tensor, 'numpy'):
            img_tensor = img_tensor.detach().cpu().numpy()
        elif not isinstance(img_tensor, np.ndarray):
            img_tensor = np.array(img_tensor)
            
        # Ensure values are in a valid range for images
        if img_tensor.dtype.kind == 'f':
            # If float values, ensure they're between 0 and 1
            if img_tensor.max() > 1.0 or img_tensor.min() < 0.0:
                img_tensor = np.clip(img_tensor, 0.0, 1.0)
        
        # W&B needs HWC format for image logging
        if dataformats == 'CHW':
            img_tensor = np.transpose(img_tensor, (1, 2, 0))
        elif dataformats == 'HW':
            if len(img_tensor.shape) == 2:
                img_tensor = img_tensor[:, :, np.newaxis]
        
        # Log image to W&B
        wandb.log({
            tag: wandb.Image(img_tensor)
        }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
    
    def add_images(
        self, 
        tag: str, 
        img_tensor: np.ndarray, 
        global_step: Optional[int] = None, 
        walltime: Optional[float] = None, 
        dataformats: str = 'NCHW'
    ):
        """
        Add multiple images to W&B.
        
        Args:
            tag: Data identifier
            img_tensor: Image data
            global_step: Global step value to record
            walltime: Optional override default walltime (time.time())
            dataformats: Format of the input image (NCHW|NHWC|NHW)
        """
        step = global_step if global_step is not None else self.step
        
        # Convert to numpy array if it's a torch tensor
        if hasattr(img_tensor, 'detach') and hasattr(img_tensor, 'cpu') and hasattr(img_tensor, 'numpy'):
            img_tensor = img_tensor.detach().cpu().numpy()
        elif not isinstance(img_tensor, np.ndarray):
            img_tensor = np.array(img_tensor)
            
        # Ensure values are in a valid range for images
        if img_tensor.dtype.kind == 'f':
            # If float values, ensure they're between 0 and 1
            if img_tensor.max() > 1.0 or img_tensor.min() < 0.0:
                img_tensor = np.clip(img_tensor, 0.0, 1.0)
                
        # Process batch of images - W&B needs each image in HWC format
        images = []
        
        if dataformats == 'NCHW':
            for i in range(img_tensor.shape[0]):
                # Convert each image from CHW to HWC
                images.append(np.transpose(img_tensor[i], (1, 2, 0)))
        elif dataformats == 'NHWC':
            for i in range(img_tensor.shape[0]):
                # Already in HWC format
                images.append(img_tensor[i])
        elif dataformats == 'NHW':
            for i in range(img_tensor.shape[0]):
                # Add channel dimension for grayscale
                img = img_tensor[i]
                if len(img.shape) == 2:
                    img = img[:, :, np.newaxis]
                images.append(img)
                
        # Log images to W&B
        wandb.log({
            tag: [wandb.Image(img) for img in images]
        }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_embedding(
        self, 
        mat: np.ndarray, 
        metadata: Optional[Union[np.ndarray, List[Any]]] = None, 
        label_img: Optional[np.ndarray] = None, 
        global_step: Optional[int] = None, 
        tag: str = 'default', 
        metadata_header: Optional[List[str]] = None
    ):
        """
        Add embedding projector data to W&B.
        
        Args:
            mat: A matrix where each row is the feature vector of a data point
            metadata: Labels for each data point
            label_img: Images corresponding to each data point
            global_step: Global step value to record
            tag: Name for the embedding
            metadata_header: Names for each column in metadata
        """
        step = global_step if global_step is not None else self.step
        
        # Convert to numpy array if not already
        if not isinstance(mat, np.ndarray):
            mat = np.array(mat)
            
        # Prepare metadata
        if metadata is not None and not isinstance(metadata, np.ndarray):
            metadata = np.array(metadata)
        
        # Create columns for the table
        columns = ["vector"]
        if metadata is not None:
            columns.append("metadata")
        if label_img is not None:
            columns.append("sprite")
            
        # Create rows for the table
        data = []
        for i in range(len(mat)):
            row = [mat[i].tolist()]
            
            # Add metadata if provided
            if metadata is not None:
                if metadata_header is not None and len(metadata.shape) > 1:
                    # Multi-dimensional metadata with headers
                    meta_dict = {
                        metadata_header[j]: metadata[i, j]
                        for j in range(len(metadata_header))
                    }
                    row.append(meta_dict)
                else:
                    # Single metadata value
                    row.append(metadata[i].item() if hasattr(metadata[i], 'item') else metadata[i])
            
            # Add label_img if provided
            if label_img is not None:
                if len(label_img.shape) == 4:  # NCHW or NHWC
                    img = label_img[i]
                    if label_img.shape[1] == 1 or label_img.shape[1] == 3:  # NCHW
                        img = np.transpose(img, (1, 2, 0))
                    row.append(wandb.Image(img))
                else:
                    row.append(None)
                    
            data.append(row)
            
        # Log embedding to W&B
        wandb.log({
            f"{tag}_embedding": wandb.Table(
                columns=columns,
                data=data
            )
        }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
    
    def add_text(
        self, 
        tag: str, 
        text_string: str, 
        global_step: Optional[int] = None, 
        walltime: Optional[float] = None
    ):
        """
        Add text data to W&B.
        
        Args:
            tag: Data identifier
            text_string: Text to save
            global_step: Global step value to record
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        # Log text to W&B
        wandb.log({
            tag: wandb.Html(f"<pre>{text_string}</pre>")
        }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_figure(
        self, 
        tag: str, 
        figure, 
        global_step: Optional[int] = None, 
        close: bool = True, 
        walltime: Optional[float] = None
    ):
        """
        Add matplotlib figure to W&B.
        
        Args:
            tag: Data identifier
            figure: Figure object to save
            global_step: Global step value to record
            close: Flag to close the figure after logging
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        # Log figure to W&B
        wandb.log({
            tag: wandb.Image(figure)
        }, step=step)
        
        # Close figure if requested
        if close:
            try:
                import matplotlib.pyplot as plt
                plt.close(figure)
            except:
                pass
                
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_hparams(
        self, 
        hparam_dict: Dict[str, Any], 
        metric_dict: Dict[str, float], 
        hparam_domain_discrete: Optional[Dict[str, List[Any]]] = None, 
        run_name: Optional[str] = None, 
        global_step: Optional[int] = None
    ):
        """
        Add hyperparameters and metrics to W&B config and summary.
        
        Args:
            hparam_dict: Dictionary of hyperparameters
            metric_dict: Dictionary of metrics
            hparam_domain_discrete: Dictionary of discrete hyperparameter domains (ignored)
            run_name: Name of the run
            global_step: Global step value to record
        """
        step = global_step if global_step is not None else self.step
        
        # Add hyperparameters to wandb config
        if wandb.run is not None:
            for key, value in hparam_dict.items():
                # Use direct dictionary assignment which calls __setitem__ internally
                wandb.run.config[key] = value
                
        # Log metrics with 'hparams/' prefix
        metric_log = {f"hparams/{k}": v for k, v in metric_dict.items()}
        wandb.log(metric_log, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_pr_curve(
        self, 
        tag: str, 
        labels: np.ndarray, 
        predictions: np.ndarray, 
        global_step: Optional[int] = None, 
        num_thresholds: int = 127, 
        weights: Optional[np.ndarray] = None, 
        walltime: Optional[float] = None
    ):
        """
        Add precision-recall curve to W&B.
        
        Args:
            tag: Data identifier
            labels: Ground truth binary labels (0 or 1)
            predictions: Prediction probability [0, 1]
            global_step: Global step value to record
            num_thresholds: Number of thresholds for the curve
            weights: Optional weights for each sample
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        try:
            from sklearn.metrics import precision_recall_curve
            import matplotlib.pyplot as plt
            
            # Convert to numpy arrays if needed
            if hasattr(labels, 'detach') and hasattr(labels, 'cpu') and hasattr(labels, 'numpy'):
                labels = labels.detach().cpu().numpy()
            if hasattr(predictions, 'detach') and hasattr(predictions, 'cpu') and hasattr(predictions, 'numpy'):
                predictions = predictions.detach().cpu().numpy()
            
            # Generate precision-recall curve
            precision, recall, thresholds = precision_recall_curve(labels, predictions, sample_weight=weights)
            
            # Create figure
            fig = plt.figure()
            plt.plot(recall, precision)
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title(f'Precision-Recall Curve - {tag}')
            plt.grid(True)
            
            # Log figure to W&B
            wandb.log({
                tag: wandb.Image(fig)
            }, step=step)
            
            # Close figure
            plt.close(fig)
            
            # Also log as a custom chart
            data = [[x, y] for (x, y) in zip(recall, precision)]
            table = wandb.Table(data=data, columns=["recall", "precision"])
            wandb.log({
                f"{tag}_pr_curve": wandb.plot.line(
                    table, "recall", "precision", 
                    title=f"Precision-Recall Curve - {tag}"
                )
            }, step=step)
            
        except ImportError:
            warnings.warn(
                "sklearn is required for PR curves. "
                "Please install it with `pip install scikit-learn matplotlib`.",
                ImportWarning,
            )
            
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_mesh(
        self, 
        tag: str, 
        vertices: np.ndarray, 
        colors: Optional[np.ndarray] = None, 
        faces: Optional[np.ndarray] = None, 
        config_dict: Optional[Dict[str, Any]] = None, 
        global_step: Optional[int] = None, 
        walltime: Optional[float] = None
    ):
        """
        Add a 3D mesh to W&B.
        
        Args:
            tag: Data identifier
            vertices: List of 3D vertices
            colors: Colors for vertices
            faces: Faces of the mesh
            config_dict: Config dictionary
            global_step: Global step value to record
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        warnings.warn(
            "add_mesh is not fully supported in W&B. "
            "Use W&B's native 3D visualization tools for better results.",
            UserWarning,
        )
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
    
    def add_video(
        self, 
        tag: str, 
        vid_tensor: np.ndarray, 
        global_step: Optional[int] = None, 
        fps: Optional[int] = 4, 
        walltime: Optional[float] = None
    ):
        """
        Add video to W&B.
        
        Args:
            tag: Data identifier
            vid_tensor: Video data in [N, T, C, H, W] format for N videos, T frames
            global_step: Global step value to record
            fps: Frames per second
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        # Convert to numpy if it's a torch tensor
        if hasattr(vid_tensor, 'detach') and hasattr(vid_tensor, 'cpu') and hasattr(vid_tensor, 'numpy'):
            vid_tensor = vid_tensor.detach().cpu().numpy()
        
        # W&B doesn't directly support batch videos, so we handle each video separately
        for i in range(vid_tensor.shape[0]):
            video = vid_tensor[i]  # [T, C, H, W]
            
            # Convert from TCHW to THWC (what W&B expects)
            video = np.transpose(video, (0, 2, 3, 1))
            
            # Log video to W&B
            video_tag = f"{tag}/video_{i}" if vid_tensor.shape[0] > 1 else tag
            wandb.log({
                video_tag: wandb.Video(video, fps=fps)
            }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
            
    def add_audio(
        self, 
        tag: str, 
        snd_tensor: np.ndarray, 
        global_step: Optional[int] = None, 
        sample_rate: int = 44100, 
        walltime: Optional[float] = None
    ):
        """
        Add audio to W&B.
        
        Args:
            tag: Data identifier
            snd_tensor: Sound data
            global_step: Global step value to record
            sample_rate: Sample rate in Hz
            walltime: Optional override default walltime (time.time())
        """
        step = global_step if global_step is not None else self.step
        
        # Convert to numpy if it's a torch tensor
        if hasattr(snd_tensor, 'detach') and hasattr(snd_tensor, 'cpu') and hasattr(snd_tensor, 'numpy'):
            snd_tensor = snd_tensor.detach().cpu().numpy()
        
        # W&B audio expects shape (channels, samples) or just (samples,)
        if len(snd_tensor.shape) > 2:
            # Handle batch of audio clips
            for i in range(snd_tensor.shape[0]):
                audio = snd_tensor[i]
                audio_tag = f"{tag}/audio_{i}" if snd_tensor.shape[0] > 1 else tag
                wandb.log({
                    audio_tag: wandb.Audio(audio, sample_rate=sample_rate)
                }, step=step)
        else:
            # Single audio clip
            wandb.log({
                tag: wandb.Audio(snd_tensor, sample_rate=sample_rate)
            }, step=step)
        
        # Update internal step counter if global_step is None
        if global_step is None:
            self.step += 1
    
    def flush(self):
        """
        Flushes the writer to W&B.
        
        In W&B, logging happens immediately, so this is mostly a no-op
        kept for compatibility with TensorBoard's SummaryWriter.
        """
        # W&B logs immediately, so nothing to flush
        pass
    
    def close(self):
        """
        Closes the writer.
        
        Note that this does not finish the W&B run, as multiple
        SummaryWriter instances might be logging to the same run.
        """
        # Nothing to close in W&B context
        pass
    
    def __enter__(self):
        """Enter context for 'with' statement."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context for 'with' statement."""
        self.close()
