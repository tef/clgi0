from clgi import App, Bug, Error, Routes, command
class AppError(Error):
    pass

class cli:
    routes = Routes()
    errors = Routes()

    @errors.on(AppError)
    def app_error(request, code):
        args = request.args
        error_args, original_request = args['args'], args['request']
        code(-1)
        filename = error_args
        if filename:
            return ["app error: {}".format(filename)]

    @routes.on("") # no path given
    @command()
    def Help(ctx):
        app = ctx['app']
        name = ctx['name']
        return list("{} {}".format(name, r) for r in app.routes.keys() if r)

    app = App(
        name="app", 
        version="0.1.1",
        routes=routes,
        errors=errors,
        args={
            'project':'--str?',
            'rollback':'--bool?',
            'read-only':'--bool?'
        },
    )


# Generic exception handler here
cli.app.main(__name__)
