#!/bin/bash

# Puerto para la demo
PORT=12347

echo "Iniciando servidor en segundo plano..."
python3 servidor_tickets.py &
SERVER_PID=$!

# Esperar un momento a que el servidor esté listo
sleep 2

echo "Pidiendo 3 tickets mediante el cliente..."
RESULTADO=$(python3 cliente_tickets.py 3)

echo "Resultado obtenido: $RESULTADO"

# Comprobar si hay 3 tickets (contando comas, debe haber 2 comas para 3 elementos)
NUM_COMMAS=$(echo "$RESULTADO" | tr -cd ',' | wc -c)

if [ "$NUM_COMMAS" -eq 2 ]; then
    echo "VERIFICACIÓN EXITOSA: Se han recibido 3 tickets."
else
    echo "ERROR: No se recibieron 3 tickets. Resultado: $RESULTADO"
    kill $SERVER_PID
    exit 1
fi

# Limpieza: Matar el servidor
echo "Cerrando servidor..."
kill $SERVER_PID
echo "Demo finalizada."
