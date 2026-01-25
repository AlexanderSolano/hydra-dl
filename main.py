"""
import asyncio
import yt_dlp
import aiohttp
import aiofiles
import os

# Configuración
CARPETA_SALIDA = "descargas"
if not os.path.exists(CARPETA_SALIDA):
    os.makedirs(CARPETA_SALIDA)

def obtener_info_video(url):
    print(f"Extrayendo info de: {url}...")
    ydl_opts = {
        'quiet': True,
        'config_location': 'yt-dlp.conf',
        # 1. Forzamos MP4 con video y audio juntos
        'default_search': 'auto',
        # 2. Arreglamos el error de JavaScript usando Node
        'js_runtimes': ['node'],
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'url': info['url'],
            'headers': info.get('http_headers', {}),
            'title': info['title'],
            'ext': info['ext'],
            'filesize': info.get('filesize') # Importante para los segmentos
        }



def listar_formatos(url):
    opciones = {'quiet': True}
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=False)
        formatos = info.get('formats', [])

        print(f"{'ID':<10} | {'EXT':<5} | {'RESOLUCIÓN':<15} | {'TAMAÑO (MB)':<15} | {'NOTA'}")
        print("-" * 70)

        for f in formatos:
            # Calculamos tamaño en MB si existe, sino mostramos 'N/A'
            size = f.get('filesize')
            size_str = f"{size / (1024*1024):.2f} MB" if size else "N/A"
            
            # Nota sobre si es video+audio o solo video
            nota = "Video+Audio" if f.get('acodec') != 'none' and f.get('vcodec') != 'none' else "Solo Video/Audio"

            print(f"{f['format_id']:<10} | {f['ext']:<5} | {f.get('resolution', 'N/A'):<15} | {size_str:<15} | {nota}")



async def descargar_segmento(session, url, headers, start, end, filename):
    # AQUÍ irá la lógica del acelerador (Range Headers)
    pass

async def gestor_descargas(url_publica):
    data = obtener_info_video(url_publica)
    nombre_archivo = f"{CARPETA_SALIDA}/{data['title']}.{data['ext']}"
    
    print(f"Video detectado: {data['title']} ({data['filesize']} bytes)")
    
    # Aquí iniciaremos la sesión aiohttp más adelante
    print("Preparando descarga asíncrona...")

if __name__ == "__main__":
    url = input("Introduce la URL del video: ")
    listar_formatos(url)
    #asyncio.run(gestor_descargas(url))

    """


import asyncio
import yt_dlp
import aiohttp
import aiofiles
import os

# Configuración
CARPETA_SALIDA = "descargas"
if not os.path.exists(CARPETA_SALIDA):
    os.makedirs(CARPETA_SALIDA)

def obtener_info_video(url):
    print(f"Extrayendo info de: {url}...")
    ydl_opts = {
        'quiet': True,
        'config_location': 'yt-dlp.conf',
        # CRÍTICO: Forzar MP4 con video+audio unidos
        'format': 'best[ext=mp4]',
        'merge_output_format': 'mp4',
        'default_search': 'auto',
        # FIX: Formato correcto para js_runtimes
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        # Validación: Asegurar que el formato final sea MP4
        if info.get('ext') != 'mp4':
            raise ValueError(f"No se encontró formato MP4 disponible. Formato detectado: {info.get('ext')}")
        
        return {
            'url': info['url'],
            'headers': info.get('http_headers', {}),
            'title': info['title'],
            'ext': info['ext'],
            'filesize': info.get('filesize')
        }

def listar_formatos(url):
    """Lista SOLO formatos MP4 disponibles"""
    opciones = {
        'quiet': True,
        # FIX: Configuración correcta para YouTube
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=False)
        formatos = info.get('formats', [])
        
        # Filtrar solo MP4
        formatos_mp4 = [f for f in formatos if f.get('ext') == 'mp4']
        
        if not formatos_mp4:
            print("⚠️  No se encontraron formatos MP4 disponibles para este video")
            return
        
        print(f"\n{'ID':<10} | {'RESOLUCIÓN':<15} | {'TAMAÑO (MB)':<15} | {'CODEC':<20} | {'TIPO'}")
        print("-" * 80)
        
        for f in formatos_mp4:
            size = f.get('filesize')
            size_str = f"{size / (1024*1024):.2f} MB" if size else "N/A"
            
            # Determinar tipo
            tiene_video = f.get('vcodec') != 'none'
            tiene_audio = f.get('acodec') != 'none'
            
            if tiene_video and tiene_audio:
                tipo = "✅ Video+Audio"
            elif tiene_video:
                tipo = "🎥 Solo Video"
            elif tiene_audio:
                tipo = "🔊 Solo Audio"
            else:
                tipo = "❓ Desconocido"
            
            codec = f"{f.get('vcodec', 'none')}/{f.get('acodec', 'none')}"
            
            print(f"{f['format_id']:<10} | {f.get('resolution', 'N/A'):<15} | {size_str:<15} | {codec:<20} | {tipo}")
        
        print(f"\n📊 Total formatos MP4: {len(formatos_mp4)}")

async def descargar_segmento(session, url, headers, start, end, filename):
    # AQUÍ irá la lógica del acelerador (Range Headers)
    pass

async def gestor_descargas(url_publica):
    try:
        data = obtener_info_video(url_publica)
        nombre_archivo = f"{CARPETA_SALIDA}/{data['title']}.{data['ext']}"
        
        print(f"\n✅ Video detectado: {data['title']}")
        print(f"📦 Tamaño: {data['filesize'] / (1024*1024):.2f} MB")
        print(f"🎬 Formato: MP4")
        print("Preparando descarga asíncrona...")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    url = input("Introduce la URL del video: ")
    
    print("\n🔍 Analizando formatos MP4 disponibles...")
    listar_formatos(url)
    
    confirmacion = input("\n¿Descargar el mejor formato MP4? (s/n): ").lower()
    if confirmacion == 's':
        asyncio.run(gestor_descargas(url))