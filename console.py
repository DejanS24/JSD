import sys
import argparse
import re
from 

def pygame_sl():

    class MyParser(argparse.ArgumentParser):

        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser(description="pygame_sl model translator")
    parser.add_argument('model', help="Model file name")

    args = parser.parse_args()

    try:
        model = 1
        # model = pygame_sl_mm.model_from_file(args.model)
    except Exception as e:
        print(e)
        return

    print("Generating code for target")
    try:
        generate(model, target)
    except Exception as e:
        print(str(e))
        return
    finally:
        print("Done")

if __name__ == '__main__':

    path = "C:/Users/Dejan/Desktop/testigrica.pg"
    sys.argv[0] = "pygame_sl"
    sys.argv.append(path)

    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    pygame_sl()