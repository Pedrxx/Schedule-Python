import psycopg2
import schedule
import time
import datetime

data_inicio = datetime.datetime.now()
data_hora_atual = str(data_inicio.strftime("%d/%m/%Y %H:%M:%S"))

def gen_log(retorno): 

    with open('C:/temp/ScheduleServiceLog.txt', 'a') as arquivo:
        arquivo.write(retorno + "\n")

def executar_query():
    try:
        # Conectar ao banco de dados Postgres
        conn = psycopg2.connect(database="postgres", user="postgres", password="senha", host="127.0.0.1", port="5432")
        conn2 = psycopg2.connect(database="postgres", user="postgres", password="senha", host="127.0.0.1", port="5432")

        cur = conn.cursor()
        cur2 = conn2.cursor()

        cur.execute("select count(jstid) from pgagent.pga_jobstep where jstenabled = true")    

        table_len = cur.fetchone()[0]

        cur.execute("select jstid from pgagent.pga_jobstep where jstenabled = true order by jstid")    
        ids = []
        for row in cur.fetchall():
            ids.append(row[0])

        i = int(0)

        agora = datetime.datetime.now()
        data_hora_atual = str(agora.strftime("%d/%m/%Y %H:%M:%S"))

        while i < table_len:

            print(ids[i])
            
            cur.execute("select jstcode from pgagent.pga_jobstep where jstid = %s", (str(ids[i],)))

            query = cur.fetchone()[0]
            cur2.execute(query);
            msg = cur2.statusmessage
            conn2.commit()
            cur.execute("select jstname from pgagent.pga_jobstep where jstid = %s", (str(ids[i],)))
            step_exec = cur.fetchone()[0]
            exec_log = f"[{data_hora_atual}] {msg} | executado com sucesso | {step_exec} "
            print(exec_log)
            i += 1

            gen_log(exec_log)

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar ou executar a query:", error)
        error_log = str("Erro ao conectar ou executar a query:", error)
        gen_log(error_log)

    finally:
        # Fechar a conexão com o banco de dados
        if conn:
            cur.close()
            cur2.close()
            conn.close()
            conn2.close()

inicio_schedule = (f"""
    \n
    ---------------------------------------------
    |Schedule Iniciado!                         | 
    |Autor: Pedro Augusto Costa                 |
    |Data Inicio: {data_hora_atual}           |   
    ---------------------------------------------
""")

print(inicio_schedule)
gen_log(inicio_schedule)
executar_query()

# Programar a execução da query de hora em hora
schedule.every(15).minutes.do(executar_query)

while True:
    schedule.run_pending()
    time.sleep(1)
           