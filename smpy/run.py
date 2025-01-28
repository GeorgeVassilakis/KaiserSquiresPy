"""Main run module for mass mapping."""

import yaml
from smpy import utils
from smpy.coordinates import get_coordinate_system
from smpy.mapping_methods import KaiserSquiresMapper, ApertureMassMapper
from smpy.error_quantification.snr import run as snr_run

def prepare_method_config(config, method):
    """Prepare method-specific configuration with plotting settings.
    
    Parameters
    ----------
    config : dict
        Full configuration dictionary
    method : str
        Method name
        
    Returns
    -------
    dict
        Combined configuration for specified method
    """
    method_config = config['general'].copy()
    method_config.update(config['methods'].get(method, {}))
    method_config.update(config['plotting'])
    return method_config

def run_mapping(config):
    """Run mass mapping with specified method.
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
        
    Returns
    -------
    maps : dict
        Dictionary containing mass maps
    scaled_boundaries : dict
        Scaled coordinate boundaries
    true_boundaries : dict
        True coordinate boundaries
    """
    # Get coordinate system
    coord_system_type = config.get('coordinate_system', 'radec').lower()
    coord_system = get_coordinate_system(coord_system_type)
    coord_config = config.get(coord_system_type, {})
    
    # Load shear data
    shear_df = utils.load_shear_data(
        config['input_path'],
        coord_config['coord1'],
        coord_config['coord2'],
        config['g1_col'],
        config['g2_col'],
        config['weight_col'],
        config['input_hdu']
    )
    
    # Calculate boundaries
    scaled_boundaries, true_boundaries = coord_system.calculate_boundaries(
        shear_df['coord1'],
        shear_df['coord2']
    )
    
    # Transform coordinates
    shear_df = coord_system.transform_coordinates(shear_df)
    
    # Create shear grid
    g1map, g2map = coord_system.create_grid(
        shear_df,
        scaled_boundaries,
        config
    )
    
    # Get correct g2 sign based on coordinate system
    g2_sign = -1 if coord_system_type == 'radec' else 1
    
    # Create mass mapper instance
    method = config['method']
    if method == 'aperture_mass':
        mapper = ApertureMassMapper(config)
    elif method == 'kaiser_squires':
        mapper = KaiserSquiresMapper(config)
    else:
        raise ValueError(f"Unknown mapping method: {method}")
    
    # Run mapping
    maps = mapper.run(g1map, g2_sign * g2map, scaled_boundaries, true_boundaries)
    
    return maps, scaled_boundaries, true_boundaries

def run(config_path):
    """Run mass mapping workflow.
    
    Parameters
    ----------
    config_path : str
        Path to configuration file
    """
    # Read configuration
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Get method and prepare config
    method = config['general']['method']
    method_config = prepare_method_config(config, method)
    
    # Run mass mapping
    maps, scaled_boundaries, true_boundaries = run_mapping(method_config)
    
    # Create SNR map if requested
    if config['general'].get('create_snr', False):
        snr_config = config['general'].copy()
        snr_config.update(config['snr'])
        snr_config.update(config['plotting'])
        snr_run.create_sn_map(snr_config, maps, scaled_boundaries, true_boundaries)

if __name__ == "__main__":
    import sys
    run(sys.argv[1])