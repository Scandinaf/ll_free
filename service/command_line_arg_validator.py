import getopt


def validate_arg_dict(*args, **kwargs):
    arg_dict = kwargs['arg_dict']
    if arg_dict is None or not arg_dict:
        raise getopt.GetoptError(msg="Read the instruction")

    if '-w' not in arg_dict:
        raise getopt.GetoptError(msg="The parameter -w is required", opt="-w")