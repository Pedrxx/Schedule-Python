# 🔰 Schedule-Python
Este é um Schedule feito em Python que se conecta ao banco de dados Postgres e executa todos os Steps cadastrados pelo PgAgent. O motivo desta aplicação é por conta de não funcionar o PgAgent no meu projeto

# 🔰 PyInstaller e NSSM Service

Foi utilizado o PyInstaller para criar o executável e o NSSM para poder tornar o executável em um serviço.

C:/Schedule/pyinstaller ScheduleService.py

C:/Schedule/NSSM install
- Ao abrir, escolha o executável no campo  "Aplication PATH"
- E defina o "Service Name"
- e "Install Service"

