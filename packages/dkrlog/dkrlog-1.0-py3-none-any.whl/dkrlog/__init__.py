import traceback, inspect, traceback, logzero as lz, time, os, requests, logging, datetime as dt, pytz
from typing import Optional

BASE_URL = os.getenv("LOGGER_URL", "http://127.0.0.1:4801")
API_TOKEN = os.getenv("LOGGER_TOKEN", "")
APPLICATION_NAMESPACE = os.getenv("LOGGER_APP_NAME", "")
HEADERS = {"token": API_TOKEN, "Content-Type": "application/json"}


def set_vars(exec_id: str):
    ''' Define o ID da execução '''
    global EXEC_ID

    EXEC_ID = exec_id


class CustomFormatter(logging.Formatter):
    ''' Classe que formata como as mensagens de log vão ser inseridas no sistema '''
    
    def format(self, record):
        ''' Formata o atributo levelname da mensagem de log trazendo apenas a primeira letra'''
        
        record.levelname = record.levelname[0] # Transforma o levelname em uma letra        
        return super().format(record)


def set_logfile(name: str):
    ''' Determina o logfile da execução do script '''

    # Criando pasta se ela não existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Personalizando a formatação do logfile
    formatter = CustomFormatter('[%(levelname)s] %(message)s')
    lz.formatter(formatter)    
    lz.logfile(f'logs/{name}.logs')


def log_exception(msg: str, e: Exception):
    ''' Faz o tratamento da exception e registra no log '''

    # Pega o frame da exception, ou seja, a função onde a exception foi gerada
    frame = inspect.currentframe().f_back

    func_name = frame.f_code.co_name    # Nome da função
    filename = frame.f_code.co_filename # Nome do arquivo
    line_no = frame.f_lineno            # Número da linha

    # Pega os nomes e valores dos argumentos da função chamadora
    arg_info = inspect.getargvalues(frame)
    ''' 
    Aqui ele retorna um tuple com os seguintes valores:
        args: argumentos da função
        varargs: argumentos variáveis da função
        keywords: argumentos com nome da função
        locals: valores locais da função
    Mas vamos apenas capturar os argumentos explicitos (args)
    '''
    params = {arg: arg_info.locals.get(arg) for arg in arg_info.args}
    detailed_exp = traceback.format_exc()

    full_msg = f"{get_date()} {filename}: {msg}\n|===> Função: {func_name}() | Linha: {line_no} | Argumentos: {str(params)[:5000]} | Exception: {e}\n\n{detailed_exp}\n"
    log(full_msg, type='e')
    
    try:
        register_log(
            timestamp = get_date(get_string=False),
            error = str(e),
            func_name = func_name,
            filename = filename,
            line_no = line_no, 
            detailed_exp = str(detailed_exp),
            custom_msg = msg,
            params = str(params)[:5000]
        )
    
    except Exception:
        log(str(traceback.print_exc()))
    
    return full_msg


def log(msg: str, type: Optional[str] = 'i', return_time: Optional[bool] = False):
    ''' Adiciona log no arquivo de log. O tipo de log pode ser "i" para informações, "e" para erros e "w" para avisos '''

    if type == 'i':
        lz.logger.info(f'| {EXEC_ID} |{msg}')
        
    elif type == 'e':
        ERROR_LIST.error_list.append(msg)
        lz.logger.error(f'| {EXEC_ID} |{msg}')
        
    elif type == 'w':
        lz.logger.warning(f'| {EXEC_ID} |{msg}')

    if return_time:
        return time.time()


def register_log(timestamp: dt.datetime, error: str, func_name: str, filename: str, line_no: int, detailed_exp: str, custom_msg: Optional[str] = None, params: Optional[str] = None):
    url = f"{BASE_URL}/register_log"
    payload = {
        "timestamp": timestamp,
        "error": error,
        "custom_msg": custom_msg,
        "func_name": func_name,
        "filename": filename,
        "line_no": line_no,
        "params": params,
        "detailed_exp": detailed_exp,
        "application_namespace": APPLICATION_NAMESPACE
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    
    return response.json()

def get_date(get_string: Optional[bool] = True):
    ''' Retorna o horario com o fuso horário de Brasilia no formato "dd/mm/yyyy hh:mm:ss" '''
 
    now = dt.datetime.now(pytz.timezone('America/Sao_Paulo'))

    return now.strftime("%d/%m/%Y %H:%M:%S") if get_string else now


class Errors():
    ''' Classe que armazena os erros gerados pela aplicação '''
    error_list = []

    def error_len(self):
        ''' Retorna o número de erros gerados '''

        return len(self.error_list)
    
ERROR_LIST = Errors()