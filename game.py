from bootstrapper import __init_logger__, __init_io_loop__, __init_db_layer__
from service.game_service import GameService


async def main():
    game_service = GameService(db_layer)
    print(await game_service.start_game())

if __name__ == '__main__':
    __init_logger__()
    loop = __init_io_loop__()
    db_layer = __init_db_layer__(loop)
    loop.run_until_complete(main())
    loop.close()