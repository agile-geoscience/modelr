'''
===================
modelr.web.server
===================

'''
import sys
from urlparse import urlparse, parse_qs
from argparse import Namespace

class Argument(object):
    '''
    An place holder for an url argument.
    '''
    def __init__(self, name, required=False, default=None, type=str, action='store', help=''):
        self.name = name
        self.required = required
        self.default = default
        self.type = type
        self.action = action
        self.help = help
    
    def parse_arg(self, args):
        if args is None:
            if self.required:
                raise ArgumentError("missing argument %r" % (self.name,))
            else:
                return self.default
        
        arg = args[0]
        if self.action != 'list':
            try:
                arg = self.type(arg)
            except:
                raise ArgumentError("argument %s: invalid %s value: %r" % (self.name, self.type.__name__, arg))
            
            return arg
        else:
            new_args = []
            for arg in arg.split(','):
                try:
                    value = self.type(arg)
                except:
                    raise ArgumentError("argument %s: invalid %s value: %r" % (self.name, self.type.__name__, arg))
                
                new_args.append(value)
            
            return new_args
            
    
    @property
    def html_help(self):
        return '<li><b>%s</b>: %s</li>\n' % (self.name, self.help)
        
        
    
class ArgumentError(Exception):
    '''
    Exception to be called when arguments are not as expected by the parser.
    '''

class SendHelp(Exception):
    '''
    Exception to be called when the help argument is found.
    '''
    def __init__(self, html):
        Exception.__init__(self, html)
        self.html = html

class URLArgumentParser(object):
    '''
    Parse a key=value arguments in a url string.
    
    Modeled after http://docs.python.org/dev/library/argparse.html
    '''
    
    def __init__(self, description):
        '''
        Constructor
        '''
        self.description = description
#        self.arguments = {'help': Argument('help')}
        self.arguments = {}
        
    def add_argument(self, name, required=False, default=None, type=str, action='store', help=''):
        '''
        add an argument
        '''
        arg = Argument(name, required, default, type, action, help)
        self.arguments[name] = arg
        
    def parse_params(self, params):
        '''
        parse the arguments gotten by urlparse.parse_qs
        '''
        result = dict()
        
        if 'help' in params:
            params.pop('help')
            self.raise_help()
        
        for key in self.arguments:
            
            arg = params.pop(key, None)
            
            value = self.arguments[key].parse_arg(arg)
            result[key] = value
            
        if params:
            key, value = params.popitem()
            raise ArgumentError("got unexpected argument %r" % (key,))
            
        return Namespace(**result)
    
    def parse_ulr(self, path):
        '''
        parse a url into its argument. 
        '''

        uri = urlparse(path)
        params = parse_qs(uri.query)
        
        return self.parse_params(params)
        
        
    @property
    def help_html(self):
        
        arguments = '\n'.join(arg.html_help for arg in self.arguments.values())
        return '<p>%s</p><ul>\n%s</ul>' % (self.description, arguments)
        
    def raise_help(self):
        raise SendHelp(self.help_html)
    
    
def main():
    path = sys.argv[1]
    
    parser = URLArgumentParser('description')
    
    parser.add_argument('script', required=True, type=str)
    
    
if __name__ == '__main__':
    main()
