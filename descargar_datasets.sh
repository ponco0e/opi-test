#! /bin/bash

echo "Descargando dataset..."
curl https://transfer.sh/suIPU/examen-opi.tar.gz -o data.tar.gz 
echo "Descomprimiendo..."
tar -xf data.tar.gz
rm data.tar.gz
echo "Listo!"
