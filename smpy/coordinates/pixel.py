import numpy as np
from .base import CoordinateSystem

class PixelSystem(CoordinateSystem):
    """
    Implementation for pixel coordinates.
    Handles coordinate transformations and gridding for pixel-based coordinate systems.
    """
    
    def get_grid_parameters(self, config):
        """
        Get pixel-specific grid parameters.
        
        Parameters
        ----------
        config : dict
            Configuration dictionary
            
        Returns
        -------
        dict
            Grid parameters including downsample factor
        """
        pixel_config = config.get('pixel', {})
        if 'downsample_factor' not in pixel_config:
            print("Warning: No downsample_factor specified in pixel config, using default 1")
            
        return {
            'downsample_factor': pixel_config.get('downsample_factor', 1),
            'max_grid_size': 10000  # Safety parameter
        }
    
    def create_grid(self, data_df, boundaries, config):
        """
        Create grid in pixel space.
        
        Parameters
        ----------
        data_df : pd.DataFrame
            DataFrame with columns: coord1(x), coord2(y), g1, g2, weight
        boundaries : dict
            Dictionary with coordinate boundaries
        config : dict
            Configuration dictionary
            
        Returns
        -------
        tuple
            (g1_grid, g2_grid) numpy arrays
        """
        # Ensure data is properly prepared
        data_df = self.prepare_data(data_df)
        
        # Get grid parameters
        grid_params = self.get_grid_parameters(config)
        downsample = grid_params['downsample_factor']
        max_size = grid_params['max_grid_size']
        
        # Get boundaries
        x_min, x_max = boundaries['coord1_min'], boundaries['coord1_max']
        y_min, y_max = boundaries['coord2_min'], boundaries['coord2_max']
        
        # Calculate raw dimensions
        raw_npix_x = int(np.ceil(x_max - x_min))
        raw_npix_y = int(np.ceil(y_max - y_min))
        
        # Calculate downsampled dimensions
        npix_x = int(np.ceil(raw_npix_x / downsample))
        npix_y = int(np.ceil(raw_npix_y / downsample))
        
        # Safety check for grid size
        if npix_x > max_size or npix_y > max_size:
            print(f"Warning: Large grid size detected ({npix_x}x{npix_y})")
            print(f"Original size: {raw_npix_x}x{raw_npix_y}")
            print(f"Adjusting downsample factor to limit grid size to {max_size} pixels")
            min_downsample = max(raw_npix_x, raw_npix_y) / max_size
            downsample = max(downsample, min_downsample)
            npix_x = int(np.ceil(raw_npix_x / downsample))
            npix_y = int(np.ceil(raw_npix_y / downsample))
            print(f"New grid size: {npix_x}x{npix_y} with downsample factor {downsample:.1f}")            
        
        # Create bins for scaled pixels
        x_bins = np.linspace(x_min, x_max, npix_x + 1)
        y_bins = np.linspace(y_min, y_max, npix_y + 1)
        
        # Digitize x and y coordinates
        x_idx = np.digitize(data_df['coord1_scaled'], x_bins) - 1
        y_idx = np.digitize(data_df['coord2_scaled'], y_bins) - 1
        
        return self._create_shear_grid(data_df, x_idx, y_idx, npix_y, npix_x)
    
    def calculate_boundaries(self, coord1, coord2):
        """
        Calculate field boundaries in pixel space.
        
        Parameters
        ----------
        coord1 : array-like
            X pixel coordinates
        coord2 : array-like
            Y pixel coordinates
            
        Returns
        -------
        tuple
            (boundaries, boundaries) identical dictionaries since no scaling is needed
        """
        # For pixel coordinates, we want integers as boundaries
        boundaries = {
            'coord1_min': float(np.floor(np.min(coord1))),
            'coord1_max': float(np.ceil(np.max(coord1))),
            'coord2_min': float(np.floor(np.min(coord2))),
            'coord2_max': float(np.ceil(np.max(coord2))),
            'coord1_name': 'X',
            'coord2_name': 'Y',
            'units': 'pixels'
        }
        
        # Check for potentially problematic coordinate ranges
        if np.ptp(coord1) > 1e5 or np.ptp(coord2) > 1e5:
            print("Warning: Large pixel coordinate range detected")
            print(f"X range: {boundaries['coord1_min']} to {boundaries['coord1_max']}")
            print(f"Y range: {boundaries['coord2_min']} to {boundaries['coord2_max']}")
        
        # For pixel coordinates, scaled and true boundaries are the same
        return boundaries, boundaries
    
    def transform_coordinates(self, data_df):
        """
        Transform pixel coordinates (identity transform for pixel space).
        
        Parameters
        ----------
        data_df : pd.DataFrame
            DataFrame with columns: coord1(x), coord2(y)
            
        Returns
        -------
        pd.DataFrame
            DataFrame with additional columns: coord1_scaled, coord2_scaled
        """
        transformed_df = data_df.copy()
        
        # For pixel coordinates, scaled coordinates are the same as original
        transformed_df['coord1_scaled'] = data_df['coord1'].astype(float)
        transformed_df['coord2_scaled'] = data_df['coord2'].astype(float)
        
        return transformed_df