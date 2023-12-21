# ¿Cuál prefieres?
Script para generar automáticamente contenido para redes sociales donde el espectador recibe 2 opciones para elegir.

## Funcionamiento
El programa está completamente hecho en Python. Lo primero que hace es a través de un input (por el momento, luego se deberá poder hacer en lotes a través de un archivo .csv) recibir las 2 opciones que se desean generar para el video. Se genera la voz con ElevenLabs a partir del texto ingresado, se elige una voz aleatoria cada vez que se corre el programa. La voz generada se guarda en un archivo llamado voice.mp3. Luego se obtienen las imágenes a través de bing_image_downloader, se reciben 2 imágenes por cada opción en caso de que la primera no se obtenga. Luego se fusiona el audio de la voz generada con un sonido de reloj que da tiempo hasta que se muestren los resultados.
