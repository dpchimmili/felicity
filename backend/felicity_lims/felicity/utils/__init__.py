def get_passed_args(inspection):
    """
    Retrieve user passed function arguments from the current frame from inspect

    :param inspection: current frame arguments
    :return: dict of arguments passed into function
    """
    _args = inspection.args
    _locals = inspection.locals

    kwargs = None
    if 'kwargs' in _locals.keys():
        kwargs = _locals.get('kwargs')
        del _locals['kwargs']

    if 'self' in _args:
        del _locals['self']

    if 'info' in _args:
        del _locals['info']

    final = {**kwargs, **_locals}
    # [(arg,args.locals[arg]) for arg in args.args]
    print(f"Func Inspector: {final}")
    return final
