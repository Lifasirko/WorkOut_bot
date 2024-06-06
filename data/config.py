from environs import Env
from sqlalchemy import create_engine

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
OWNERS = env.list("OWNERS")
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
COACHES = env.list("COACHES")
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

PGUSER = env.str("DB_USER")
PGPASS = env.str("DB_PASS")
PGNAME = env.str("DB_NAME")
PGHOST = env.str("DB_HOST")
PGPORT = env.str("DB_PORT")
DATABASE = env.str("DATABASE")

LIQPAY_TOKEN = env.str("LIQPAY")
GOOGLE_API_KEY = env.str("GOOGLE_API_KEY")

# db_host = ip

# aiogram_redis = {
#     'host': ip,
# }
#
# redis = {
#     'address': (ip, 6379),
#     'encoding': 'utf8'
# }


engine = create_engine(
    f"postgresql://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGNAME}",
    connect_args={'client_encoding': 'utf8'}
)

conn = engine.connect()

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASS}@{PGHOST}:{PGPORT}/{PGNAME}"
TIMEZONE_BASE_URL = "https://maps.googleapis.com/maps/api/timezone/json"

