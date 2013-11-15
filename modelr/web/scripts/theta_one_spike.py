'''
Created on Apr 30, 2012

@author: Sean Ross-Ross, Matt Hall

The main purpose of this script is to support the Android
app AVO*, which wants a simple gather for a step function.
The app will gather the parameters and pass them via a
URL, and will get a JPG back in return. 
'''
from argparse import ArgumentParser
from modelr.reflectivity import create_theta_spike
import matplotlib
import matplotlib.pyplot as plt
import tempfile
from os import unlink
from modelr.web.urlargparse import rock_properties_type, \
     reflectivity_type
from modelr.web.util import return_current_figure
from modelr.rock_properties import MODELS
import numpy as np
from modelr.web.util import wiggle

short_description = 'Create a simple gather for a single reflectivity spike'

def add_arguments(parser):
    
    parser.add_argument('title', default='Plot', type=str,
                        help='The title of the plot')
    parser.add_argument('pad', default=50, type=int,
            help='The time in milliseconds above and below the wedge')
    
    parser.add_argument('Rpp0', type=rock_properties_type,
                        help='rock properties of upper rock',
                        required=True)
    parser.add_argument('Rpp1', type=rock_properties_type,
                        help='rock properties of lower rock',
                        required=True)
    
    parser.add_argument('theta', type=float, action='list',
                        help='Angle of incidence', default='0,60,1')
    
    parser.add_argument('f', type=float, help='Frequency of wavelet',
                        default=25)
    parser.add_argument('points', type=int,
                        help='Length of wavelet in samples',
                        default=100)
    parser.add_argument('reflectivity_method', type=reflectivity_type,
                        help='algorithm for calculating reflectivity',
                        default='zoeppritz', choices=MODELS.keys())

    parser.add_argument('colour', type=str,
                        help='Matplotlib colourmap', default='Greys')

    parser.add_argument('display',
                        type=str,
                        help='wiggle, image, or both',
                        default='image'
                        )

    return parser

def run_script(args):
    
    matplotlib.interactive(False)
    
    Rprop0 = args.Rpp0 
    Rprop1 = args.Rpp1    
            
    theta = np.arange(args.theta[0], args.theta[1], args.theta[2])
        
    warray_amp = create_theta_spike(args.pad,
                                    Rprop0, Rprop1, theta,
                                    args.f, args.points,
                                    args.reflectivity_method)
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    plt.gray()
    aspect = float(warray_amp.shape[1]) / warray_amp.shape[0]
    
    if args.display == 'wiggle':        
        wiggle(warray_amp,1)       
    else:
        ax1.imshow( warray_amp, aspect=aspect, cmap=args.colour)
        
    if args.display == 'both':
        wiggle(warray_amp,1)
        plt.gca().invert_yaxis()
        
    
    plt.title(args.title % locals())
    plt.ylabel('time (ms)')
    plt.xlabel('trace')
    
    fig_path = tempfile.mktemp('.jpeg')
    plt.savefig(fig_path)
    
    with open(fig_path, 'rb') as fd:
        data = fd.read()
        
    unlink(fig_path)
        
    return data
    
    
def main():
    parser = ArgumentParser(usage=short_description,
                            description=__doc__)
    add_arguments(parser)
    args = parser.parse_args()
    run_script(args)
    
if __name__ == '__main__':
    main()
