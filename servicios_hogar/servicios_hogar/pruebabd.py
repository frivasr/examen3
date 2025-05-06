from django.db import connection, OperationalError
try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM DUAL")  # Una consulta muy básica de Oracle
    result = cursor.fetchone()
    print("Conexión exitosa:", result)
except OperationalError as e:
    print("Error de conexión:", e)
finally:
    connection.close()