import os
import uuid
import pillow_heif
from PIL import Image, ImageOps


pillow_heif.register_heif_opener()


def change_filename_generate(filename: str):
    """
    画像のファイル名をuuidを使って変換する関数
    Args:
        filename: 画像のファイル名
    Returns:
        変換後のファイル名
    """
    if not filename:
        raise ValueError('filename is empty: ファイルを指定してください')
    
    if not '.' in filename:
        raise ValueError('invalid filename:拡張子がありません')
    
    ext = filename.rsplit('.')[-1].lower()
    return f"{uuid.uuid4().hex}.{ext}"
    
def save_image_as_jpg(file, save_dir_path: str, max_width: int=1080):
    """
    Uploadされた画像ファイルを検証し、JPEG形式に変換して保存する。

    - Pillow を使用して画像の実体検証（verify）を行う
    - EXIF Orientation を考慮して画像の向きを補正する
    - JPEG 保存のために RGB カラーへ変換する
    - 指定された最大幅を超える場合は、アスペクト比を維持したままリサイズする
    - 変換後の画像は UUID ベースのファイル名で保存される

    Parameters
    ----------
    file : FileStorage or file-like object
        Flask の request.files から取得したアップロード画像、
        または Pillow で読み込み可能なファイルライクオブジェクト。

    save_dir_path : str
        変換後の JPEG 画像を保存するディレクトリパス。

    max_width : int, optional
        画像の最大幅（px）。デフォルトは 1080。
        画像の幅がこの値を超える場合のみリサイズされる。

    Returns
    -------
    str or None
        正常に保存された場合は生成された JPEG ファイル名を返す。
        画像として不正なファイルが渡された場合は None を返す。

    Notes
    -----
    - 本関数はファイルを保存する副作用を持つ。
    - img.verify() 実行後に file.seek(0) を行い、再度読み込み可能な状態にしている。
    - 保存されるファイル形式は常に JPEG であり、元の拡張子は保持されない。
    """
    filename = f'{uuid.uuid4().hex}.jpg'
    file_path = os.path.join(save_dir_path, filename)

    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        return None
    
    file.seek(0)

    img = Image.open(file)
    img = ImageOps.exif_transpose(img)

    img = img.convert('RGB')

    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

    img.save(file_path,'JPEG', quality=85, optimize=True)
    return filename
