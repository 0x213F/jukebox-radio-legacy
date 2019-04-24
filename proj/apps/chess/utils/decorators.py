
# - - - - - - - - - - - - - - - -
# `ChessGame` manager decorators
# - - - - - - - - - - - - - - - -

def get_game_by_user(func):
    '''
    @decorator to get game from user.
    '''
    def query(*args, **kwargs):
        self = args[0]
        user = kwargs.get('user')
        if not user:
            raise Exception('User is not authenticated.')
        try:
            kwargs['game'] = (
                self.model
                .objects
                .active()
                .belong_to(user)
                .get_singular()
            )
        except self.model.DoesNotExist:
            raise Exception('Game does not exist.')
        return func(*args, **kwargs)
    return query


def get_game_by_uuid(func):
    '''
    @decorator to get game by `game.uuid`.
    '''
    def query(*args, **kwargs):
        self = args[0]
        uuid = kwargs.get('uuid')
        try:
            kwargs['game'] = self.model.objects.get(uuid=uuid)
        except self.model.DoesNotExist:
            raise Exception('Game does not exist.')
        return func(*args, **kwargs)


def assert_game_started(func):
    '''
    @decorator to assert that at least one move has been taken in the game.
    '''
    def query(*args, **kwargs):
        if kwargs.get('game').steps == 0:
            raise Exception('There are no moves to undo.')
        return func(*args, **kwargs)
    return query


def assert_user_no_active_game(func):
    '''
    @decorator to assert user has no active game.
    '''
    def query(*args, **kwargs):
        self = args[0]
        user = kwargs.get('user')
        if not user:
            raise Exception('User is not authenticated.')
        active_games = (
            self.model
            .objects
            .active()
            .belong_to(user)
        )
        if active_games.exists():
            raise Exception('Already active in game.')
        return func(*args, **kwargs)
    return query


def assert_user_status_my_turn(func):
    '''
    @decorator to assert that it IS the user's turn.
    '''
    def query(*args, **kwargs):
        self = args[0]
        game = kwargs.get('game')
        player = game.get_color(kwargs.get('user'))
        if getattr(game, f'{player}_status') != self.model.STATUS_MY_TURN:
            raise Exception('It is the opponent\'s turn')
        return func(*args, **kwargs)
    return query


def assert_user_status_their_turn(func):
    '''
    @decorator to assert that it IS NOT the user's turn.
    '''
    def query(*args, **kwargs):
        self = args[0]
        game = kwargs.get('game')
        player = game.get_color(kwargs.get('user'))
        if getattr(game, f'{player}_status') != self.model.STATUS_THEIR_TURN:
            raise Exception('It is the user\'s turn')
        return func(*args, **kwargs)
    return query
