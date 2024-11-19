import config.init_config as config
import utils.database_utils as dbUtils


def init():
    # Init config file
    config.init_config()

    # Init Database
    dbUtils.setup()
