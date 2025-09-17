from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
import unicodedata
import re


# Create your models here.


class SupabaseStorage(Storage):
    """
    Implementación mínima para usar Supabase Storage como DEFAULT_FILE_STORAGE.
    Soporta: save (upload), url (get_public_url), delete (remove).
    No implementa open() (no necesario para solo servir).
    """

    def __init__(self, bucket=None):
        self.client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY,
        )
        self.bucket = bucket or settings.SUPABASE_BUCKET_NAME

    def _save(self, name, content):
        # Normalizar nombre: quitar tildes y caracteres no ASCII
        normalized = unicodedata.normalize("NFKD", name)
        safe_name = normalized.encode("ascii", "ignore").decode("ascii")
        safe_name = re.sub(
            r"[^A-Za-z0-9._/-]", "_", safe_name
        )  # reemplazar lo que quede raro

        file_bytes = content.read()
        self.client.storage.from_(self.bucket).upload(
            path=safe_name,
            file=file_bytes,
        )
        return safe_name

    def exists(self, name):
        # Forzar False para que Django intente guardar (o podrías verificar con list())
        return False

    def url(self, name):
        # Si el bucket es público, get_public_url te da la url. Si no, tendrás que firmarla.
        public = self.client.storage.from_(self.bucket).get_public_url(name)
        # la respuesta puede venir en diferentes formas según versión; intenta varias claves:
        if isinstance(public, dict):
            # algunos clients devuelven {'data': {'publicUrl': '...'}}
            data = public.get("data") or public.get("publicUrl") or public
            if isinstance(data, dict) and data.get("publicUrl"):
                return data.get("publicUrl")
            elif isinstance(data, str):
                return data
        # fallback manual (formato estándar):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket}/{name}"

    def delete(self, name):
        # remove recibe lista de paths
        self.client.storage.from_(self.bucket).remove([name])
        return
