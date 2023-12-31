import telegram
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import pyodbc

# Thay thế bằng API key của bạn
API_KEY = "6500460826:AAEhdBmolpAG81D96JRdbUvBBe4-WloYLk0"
server = '192.168.1.3'
port = '1433'
database = 'BMQuanLySanXuat'
username = 'sa'
password = 'BiNhMinHGroUp@SqlSv2O18'
# Chuỗi kết nối
conn_str = f'DRIVER=ODBC Driver 18 for SQL Server;SERVER={server},{port};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=Yes'
# Khởi tạo kết nối đến SQL Server
conn = pyodbc.connect(conn_str)

# Hàm để thực hiện truy vấn SQL và trả về kết quả
def run_sql_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
#Ghi lai log
logging.basicConfig(
    level=logging.INFO,  # Chọn mức độ ghi log (INFO, DEBUG, ERROR, vv.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
def my_function():
    # Thực hiện một số thao tác
    logging.info('Thực hiện một số thao tác')
    # Xảy ra lỗi
    try:
        result = 1 / 0
    except Exception as e:
        logging.error('Xảy ra lỗi: %s', e)
# Xử lý lệnh /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Chào {user.mention_markdown_v2()}!',
        reply_markup=None,
    )

# Xử lý menu chức năng
def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Tồn kho ngoài", callback_data='ton_kho_ngoai')],
        [InlineKeyboardButton("Tồn kho thành phẩm", callback_data='ton_kho_thanh_pham')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Chọn một chức năng:', reply_markup=reply_markup)

# Xử lý callback từ menu chức năng
def menu_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'ton_kho_ngoai':
        # Thực hiện truy vấn SQL cho tồn kho ngoài
        result = run_sql_query("SELECT * FROM DM_KhachHang")
        response = "\n".join([f"{row.ProductName}: {row.Quantity}" for row in result])
        query.edit_message_text(text=f'Tồn kho ngoài:\n{response}')
    elif query.data == 'ton_kho_thanh_pham':
        # Thực hiện truy vấn SQL cho tồn kho thành phẩm
        result = run_sql_query("SELECT * FROM tbl_hanmuccongno")
        response = "\n".join([f"{row.ProductName}: {row.Quantity}" for row in result])
        query.edit_message_text(text=f'Tồn kho thành phẩm:\n{response}')

def main() -> None:
    updater = Updater(token=API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CallbackQueryHandler(menu_callback))

    updater.start_polling()
    updater.idle()

if __name__ == 'bmfood':
    main()
