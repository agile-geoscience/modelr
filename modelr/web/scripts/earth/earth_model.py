from modelr.web.urlargparse import reflectivity_type
from modelr.constants import REFLECTION_MODELS
from modelr.reflectivity import get_reflectivity

def add_arguments(parser):

    
    parser.add_argument('depth', type=float, default=5000.0,
                       help="Depth of the model")
    parser.add_argument('units', type=str, default='depth',
                        help="Model domain",
                        choices=['time', 'depth'])

    parser.add_argument('reflectivity_method',
                        type=reflectivity_type,
                        help='Reflectivity Algorithm',
                        default='zoeppritz',
                        choices=REFLECTION_MODELS.keys()) 
 
    return parser

def run_script():
    pass