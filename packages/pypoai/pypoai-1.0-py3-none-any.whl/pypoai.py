import json
import re
from typing import Dict, Any, List, Optional

# AI desteği için google.genai kitaplığı opsiyonel
try:
    from google import genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

class Poai:
    """
    .po <-> JSON çift yönlü dönüşüm sınıfı.
    - read_po/read_json ile yükler ve Python veri yapısını döndürür.
    - save_json/save_po ile dosyaya kaydeder.
    - translate_with_ai ile AI çevirisi yapabilir (opsiyonel).
    - replace_from_json ile harici JSON’dan güncelleyebilir.

    Args:
        encoding: Dosya kodlaması (varsayılan 'utf-8').
        show_empty: False ise, çevirisi boş mesajları filtreler; True ise tüm mesajlar dahil.
        api_key: Gemini API anahtarı (AI özellikleri için opsiyonel).
    """

    def __init__(
        self,
        encoding: str = 'utf-8',
        show_empty: bool = False,
        api_key: Optional[str] = None
    ):
        self.encoding = encoding
        self.show_empty = show_empty
        self.api_key = api_key
        self.data: Optional[Dict[str, Any]] = None

    def read_po(self, po_path: str) -> Dict[str, Any]:
        """PO dosyasını oku, ayrıştır, filtrele ve Python veri yapısını döndür."""
        with open(po_path, 'r', encoding=self.encoding) as f:
            content = f.read()
        parsed = self._parse_po(content)
        if not self.show_empty:
            parsed['messages'] = [m for m in parsed['messages']
                                  if m.get('msgstr') or any(m.get('msgstr_plural', {}).values())]
        self.data = parsed
        return self.data

    def save_json(self, json_path: str) -> None:
        """İçsel self.data’yı JSON dosyasına kaydet."""
        if not self.data:
            raise ValueError("Önce read_po veya read_json çağırın.")
        with open(json_path, 'w', encoding=self.encoding) as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def read_json(self, json_path: str) -> Dict[str, Any]:
        """JSON dosyasını oku ve Python veri yapısını döndür."""
        with open(json_path, 'r', encoding=self.encoding) as f:
            self.data = json.load(f)
        return self.data

    def save_po(self, po_path: str) -> None:
        """İçsel self.data’yı PO formatına dönüştürüp dosyaya yaz."""
        if not self.data:
            raise ValueError("Önce read_po veya read_json çağırın.")
        content = self._dict_to_po(self.data)
        with open(po_path, 'w', encoding=self.encoding) as f:
            f.write(content)

    def get_messages(self) -> List[Dict[str, Any]]:
        """self.data içindeki mesaj listesini döndürür."""
        return (self.data or {}).get('messages', [])

    def set_messages(self, messages: List[Dict[str, Any]]) -> None:
        """self.data içindeki mesaj listesini günceller."""
        if self.data is None:
            self.data = {'header': {}, 'messages': []}
        self.data['messages'] = messages

    def translate_with_ai(
        self,
        translate_all: bool = False,
        only_empty: bool = True,
        fallback_to_source: bool = True,
        target_lang: str = 'Turkish',
        model: str = 'gemini-1.5-flash-latest',
        batch_size: int = 50
    ) -> None:
        """
        AI ile çeviri yapar: msgstr ve msgstr_plural alanlarını doldurur.
        - translate_all=True ise tüm mesajları çevirir.
        - only_empty=True ise sadece çevirisi boş olanları işler.
        - fallback_to_source=True ise çeviri gelmeyen boş alanlara msgid/msgid_plural değerini atar.
        """
        if not AI_AVAILABLE:
            raise RuntimeError("AI modu yüklenemedi: google.genai mevcut değil.")
        if not self.api_key:
            raise RuntimeError("AI çeviri için api_key gereklidir.")
        msgs = self.get_messages()
        to_translate = []
        for m in msgs:
            single_empty = not m.get('msgstr')
            plural_empty = not any(m.get('msgstr_plural', {}).values())
            if not translate_all and only_empty and not (single_empty or plural_empty):
                continue
            entry: Dict[str, Any] = {'msgid': m['msgid'], 'msgctxt': m.get('msgctxt')}
            if 'msgid_plural' in m:
                entry['msgid_plural'] = m['msgid_plural']
            to_translate.append(entry)
        client = genai.Client(api_key=self.api_key)
        for i in range(0, len(to_translate), batch_size):
            batch = to_translate[i:i+batch_size]
            prompt = {'messages': batch, 'target_language': target_lang}
            resp = client.models.generate_content(
                model=model,
                contents=json.dumps(prompt, ensure_ascii=False),
                config={'response_mime_type': 'application/json'}
            )
            try:
                result = json.loads(resp.text)
            except Exception as e:
                raise RuntimeError(f"AI dönüşü JSON değil: {e} {resp.text}")
            for out in result.get('messages', []):
                for m in msgs:
                    if m['msgid'] == out.get('msgid') and m.get('msgctxt') == out.get('msgctxt'):
                        if 'msgstr' in out:
                            m['msgstr'] = out['msgstr']
                        if 'msgstr_plural' in out:
                            m['msgstr_plural'] = out['msgstr_plural']
        # Fallback: çeviri gelmeyenleri kaynak metne eşitle
        if fallback_to_source:
            for m in msgs:
                if not m.get('msgstr'):
                    m['msgstr'] = m['msgid']
                if 'msgstr_plural' in m:
                    for idx, val in m['msgstr_plural'].items():
                        if not val:
                            m['msgstr_plural'][idx] = m.get('msgid_plural', m['msgid'])

    def replace_from_json(
        self,
        json_path: str,
        only_empty: bool = True
    ) -> None:
        """
        Harici JSON’dan msgstr ve msgstr_plural alanlarını günceller.
        Eşleştirme msgid+msgctxt bazlı yapılır.
        """
        if not self.data:
            raise ValueError("Önce read_po veya read_json çağırın.")
        with open(json_path, 'r', encoding=self.encoding) as f:
            new = json.load(f)
        for nm in new.get('messages', []):
            for m in self.get_messages():
                if m['msgid'] == nm.get('msgid') and m.get('msgctxt') == nm.get('msgctxt'):
                    if 'msgstr' in nm and (not only_empty or not m.get('msgstr')):
                        m['msgstr'] = nm['msgstr']
                    if 'msgstr_plural' in nm and (not only_empty or not any(m.get('msgstr_plural', {}).values())):
                        m['msgstr_plural'] = nm['msgstr_plural']

    """
    .po <-> JSON çift yönlü dönüşüm sınıfı.
    - read_po/read_json ile yükler ve Python veri yapısını döndürür.
    - save_json/save_po ile dosyaya kaydeder.
    - translate_with_ai ile AI çevirisi yapabilir (opsiyonel).
    - replace_from_json ile harici JSON’dan güncelleyebilir.

    Args:
        encoding: Dosya kodlaması (varsayılan 'utf-8').
        show_empty: False ise, çevirisi boş mesajları filtreler; True ise tüm mesajlar dahil.
        api_key: Gemini API anahtarı (AI özellikleri için opsiyonel).
    """

    def __init__(
        self,
        encoding: str = 'utf-8',
        show_empty: bool = False,
        api_key: Optional[str] = None
    ):
        self.encoding = encoding
        self.show_empty = show_empty
        self.api_key = api_key
        self.data: Optional[Dict[str, Any]] = None

    def read_po(self, po_path: str) -> Dict[str, Any]:
        """
        PO dosyasını oku, ayrıştır, filtrele ve Python veri yapısını döndür.
        """
        with open(po_path, 'r', encoding=self.encoding) as f:
            content = f.read()
        parsed = self._parse_po(content)
        if not self.show_empty:
            parsed['messages'] = [m for m in parsed['messages']
                                  if m.get('msgstr') or any(m.get('msgstr_plural', {}).values())]
        self.data = parsed
        return self.data

    def save_json(self, json_path: str) -> None:
        """İçsel self.data’yı JSON dosyasına kaydet."""
        if not self.data:
            raise ValueError("Önce read_po veya read_json çağırın.")
        with open(json_path, 'w', encoding=self.encoding) as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def read_json(self, json_path: str) -> Dict[str, Any]:
        """JSON dosyasını oku ve Python veri yapısını döndür."""
        with open(json_path, 'r', encoding=self.encoding) as f:
            self.data = json.load(f)
        return self.data

    def save_po(self, po_path: str) -> None:
        """İçsel self.data’yı PO formatına dönüştürüp dosyaya yaz."""
        if not self.data:
            raise ValueError("Önce read_po veya read_json çağırın.")
        content = self._dict_to_po(self.data)
        with open(po_path, 'w', encoding=self.encoding) as f:
            f.write(content)

    def get_messages(self) -> List[Dict[str, Any]]:
        """self.data içindeki mesaj listesini döndürür."""
        return (self.data or {}).get('messages', [])

    def set_messages(self, messages: List[Dict[str, Any]]) -> None:
        """self.data içindeki mesaj listesini günceller."""
        if self.data is None:
            self.data = {'header': {}, 'messages': []}
        self.data['messages'] = messages

    def translate_with_ai(
        self,
        only_empty: bool = True,
        target_lang: str = 'Turkish',
        model: str = 'gemini-1.5-flash-latest',
        batch_size: int = 50
    ) -> None:
        """
        AI ile çeviri yapar: msgstr ve msgstr_plural alanlarını doldurur.
        only_empty=True ise yalnızca boş çevirileri işler.
        """
        if not AI_AVAILABLE:
            raise RuntimeError("AI modu yüklenemedi: google.genai mevcut değil.")
        if not self.api_key:
            raise RuntimeError("AI çeviri için api_key gereklidir.")
        msgs = self.get_messages()
        to_translate = []
        for m in msgs:
            empty_single = not m.get('msgstr')
            empty_plural = not any(m.get('msgstr_plural', {}).values())
            if only_empty and not (empty_single or empty_plural):
                continue
            entry = {'msgid': m['msgid'], 'msgctxt': m.get('msgctxt')}
            if 'msgid_plural' in m:
                entry['msgid_plural'] = m['msgid_plural']
            to_translate.append(entry)
        client = genai.Client(api_key=self.api_key)
        # Batch API çağrısı
        for i in range(0, len(to_translate), batch_size):
            batch = to_translate[i:i+batch_size]
            prompt = {'messages': batch, 'target_language': target_lang}
            resp = client.models.generate_content(
                model=model,
                contents=json.dumps(prompt, ensure_ascii=False),
                config={'response_mime_type': 'application/json'}
            )
            try:
                result = json.loads(resp.text)
            except Exception as e:
                raise RuntimeError(f"AI dönüşü JSON değil: {e}\n{resp.text}")
            for out in result.get('messages', []):
                for m in msgs:
                    if (m['msgid'] == out.get('msgid') and
                        m.get('msgctxt') == out.get('msgctxt')):
                        if 'msgstr' in out:
                            m['msgstr'] = out['msgstr']
                        if 'msgstr_plural' in out:
                            m['msgstr_plural'] = out['msgstr_plural']

    def replace_from_json(
        self,
        json_path: str,
        only_empty: bool = True
    ) -> None:
        """
        Harici JSON’dan msgstr ve msgstr_plural alanlarını günceller.
        Eşleştirme msgid+msgctxt bazlı yapılır.
        """
        if not self.data:
            raise ValueError("Önce read_po veya read_json çağırın.")
        with open(json_path, 'r', encoding=self.encoding) as f:
            new = json.load(f)
        for nm in new.get('messages', []):
            for m in self.get_messages():
                if (m['msgid'] == nm.get('msgid') and
                    m.get('msgctxt') == nm.get('msgctxt')):
                    if 'msgstr' in nm and (not only_empty or not m.get('msgstr')):
                        m['msgstr'] = nm['msgstr']
                    if 'msgstr_plural' in nm and (not only_empty or not any(m.get('msgstr_plural', {}).values())):
                        m['msgstr_plural'] = nm['msgstr_plural']

    # --- Dahili yardımcılar ---
    def _parse_po(self, text: str) -> Dict[str, Any]:
        header: Dict[str, str] = {}
        messages: List[Dict[str, Any]] = []
        lines = text.splitlines()
        entry: Dict[str, Any] = {}
        buf_key: Optional[str] = None
        buf: List[str] = []

        def flush():
            nonlocal buf_key, buf, entry
            if not buf_key or not buf:
                return
            val = ''.join(buf).strip('"')
            val = val.replace('\\n', '\n').replace('\\"', '"')
            if buf_key == 'msgctxt':
                entry['msgctxt'] = val
            elif buf_key == 'msgid':
                entry['msgid'] = val
            elif buf_key == 'msgid_plural':
                entry['msgid_plural'] = val
            elif buf_key == 'msgstr':
                entry['msgstr'] = val
            elif buf_key.startswith('msgstr['):
                idx = buf_key[len('msgstr['):-1]
                entry.setdefault('msgstr_plural', {})[idx] = val
            buf_key = None
            buf = []

        for line in lines + ['']:
            if not line.strip():
                flush()
                if 'msgid' in entry:
                    if entry.get('msgid') == '':
                        for h in entry.get('msgstr', '').split('\n'):
                            if ':' in h:
                                k, v = h.split(':', 1)
                                header[k.strip()] = v.strip()
                    else:
                        messages.append(entry.copy())
                entry.clear()
                buf_key = None
                buf = []
                continue

            if line.startswith('#'):
                entry.setdefault('translator_comments', []).append(line)
                continue

            m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+(.*)', line)
            if m:
                flush()
                buf_key, rest = m.groups()
                buf = [rest.strip()]
            elif buf_key:
                buf.append(line.strip())

        return {'header': header, 'messages': messages}

    def _dict_to_po(self, data: Dict[str, Any]) -> str:
        parts: List[str] = []
        # Header
        parts.append('msgid ""')
        parts.append('msgstr ""')
        for k, v in data.get('header', {}).items():
            parts.append(f'"{k}: {v}\n"')
        parts.append('')
        # Mesajlar
        for m in data.get('messages', []):
            for c in m.get('translator_comments', []):
                parts.append(c)
            for c in m.get('extracted_comments', []):
                parts.append(f'#. {c}')
            for r in m.get('references', []):
                parts.append(f'#: {r}')
            if m.get('flags'):
                parts.append(f"#, {', '.join(m['flags'])}")
            if 'msgctxt' in m:
                parts.append(f'msgctxt "{m["msgctxt"]}"')
            parts.append(f'msgid "{m["msgid"]}"')
            if 'msgid_plural' in m:
                parts.append(f'msgid_plural "{m["msgid_plural"]}"')
                for i, strp in sorted(m.get('msgstr_plural', {}).items(), key=lambda x: int(x[0])):
                    parts.append(f'msgstr[{i}] "{strp}"')
            else:
                parts.append(f'msgstr "{m.get("msgstr", "")}"')
            parts.append('')
        return '/n'.join(parts)



    