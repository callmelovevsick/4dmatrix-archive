import os
import sys
import time
import random
import string
import marshal
import zlib
import bz2
import base64
from typing import Optional

TOOL_NAME = "4dmatrix"
TOOL_VERSION = "69-data"
DEFAULT_CONTACT = "giaithuatholic@proton.me"

# ---------------------- ANSI colors & banner ----------------------
RESET = "\033[0m"
BOLD = "\033[1m"
FG = {
    "green": "\033[92m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "white": "\033[97m",
    "grey": "\033[90m",
}

ASCII_ART = r"""
⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣟⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⠟⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣇⡀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣿⣿⣟⣃⡤⠤⠿⠿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣴⡶⠦⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⠟⠁⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⡆⠀⢿⣿⠁⠀⠀⠈⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⠯⠀⢠⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣧⠀⣿⡏⠀⠀⠀⢠⡀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣿⠀⠀⠘⡆⠀⣰⣿⣿⣿⣿⣿⣿⣿⣜⣷⣿⠁⠀⠀⠀⢸⡇⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢻⠀⠀⠘⣿⢠⣿⣿⣿⣿⣿⣿⣟⠿⢿⠛⠁⠓⠆⠀⠀⣼⠁⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⡄⠀⠀⣾⣾⣷⣿⣿⣿⠿⢿⣿⣶⣾⣶⣶⣷⣶⣶⣶⣿⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⢹⣇⣾⣿⢿⡟⠀⠸⣿⡄⢹⡁⠀⠀⠀⠀⠈⢹⢰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⣿⡟⠉⠘⣇⠀⠀⠉⠙⠺⡇⠀⠀⠀⠀⡓⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣷⠀⠀⣼⡿⠧⠒⠒⠛⠛⠒⣶⢤⣄⣳⡀⣀⣀⡤⠥⠤⠬⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⡤⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠁⢹⣿⣿⡿⠑⠀⠀⠀⠀⠀⠈⠙⠓⠢⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢰⢋⣷⠊⠀⠀⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣌⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣯⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⡤⢄⡀⠀⠀⠀⠀⠀⠀⠀
⢠⡴⢻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣗⡇⠀⠀⠀⠀⠀⠀⠀
⠈⣷⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀
⠈⢿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀
⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀
⠀⢹⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣷⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀
⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡾⣿⣿⣿⡟⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡷⠖⠒⠲⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢁⣢⣿⡿⡿⣇⠈⠙⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢞⡞⠀⠀⠀⣀⣀⡀⠀⠀
⢠⠞⠀⠀⠀⠀⠀⠹⣶⢤⡀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠈⡇⢀⠔⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⢀⡴⠊⠁⠀⠈⢦⡀
⡞⠀⠀⠀⠀⠀⠀⠀⠙⠳⣽⣷⡀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⡇⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢷⣶⡿⠀⠀⠀⠀⠀⠀⢧
⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⢦⡀⠀⢠⢿⠀⠀⠀⠀⠀⢧⠈⠀⠀⠀⠀⣀⡤⠤⠤⠤⣴⣻⣳⠋⠀⠀⠀⠀⠀⠀⠀⠀⣾
⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣧⣏⡇⢹⡀⣸⡏⠀⠀⠀⠀⠀⠘⡆⠀⠀⣰⠋⠁⠀⠀⠀⢰⣳⣧⡇⠀⡆⠀⠀⠀⠀⠀⠀⢀⡟
⠘⣆⠀⠀⠀⠀⠀⠀⣄⢧⣾⣿⣿⠁⠀⢷⡿⠀⠀⠀⠀⠀⠀⠀⢱⠀⡴⠃⠀⠀⠀⠀⠀⣾⣿⢧⣧⠀⡇⢰⠀⠀⠀⠀⠀⣼⠃
⠀⠸⡄⠀⠀⠀⠀⠀⠈⣿⣿⡽⠃⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⢸⢸⠁⠀⠀⠀⠀⠀⠀⣿⣮⣿⣷⡇⠀⡄⠀⠀⠀⣔⡏⠀
⠀⢰⠻⡄⠀⠀⠀⠀⠀⢹⣏⡄⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠸⡌⠒⠀⠀⠀⠀⠀⠀⠀⢘⣻⣿⡟
"""

def color_gradient(text: str, c1: str = "green", c2: str = "cyan") -> str:
    out = []
    colors = [FG.get(c1, ""), FG.get(c2, "")]
    L = max(1, len(text))
    for i, ch in enumerate(text):
        col = colors[0] if i < L//2 else colors[1]
        out.append(col + ch)
    out.append(RESET)
    return "".join(out)

def print_banner():
    banner = ASCII_ART
    for ln in banner.splitlines():
        if ln.strip() == "":
            print()
        else:
            print(color_gradient(ln))
    print(FG["cyan"] + f"[{TOOL_NAME}] {TOOL_NAME} packer — v{TOOL_VERSION}" + RESET)
    print()

# ---------------------- Safe Noise Utilities ----------------------

SAFE_NOISE_CHARSET = string.ascii_letters + string.digits + "địtconmẹlũchúngmàycrackhộthằngbốmàycáifuckuallcrackitforurdadДаладновамвсем, треснитерадисвоегоотцаΓαμώτοόλοισας,σπάστετογιατονμπαμπάσαςみんな父親のためにそれをやれよНиггер, тупой ниггер, заткнись нахуй, если не можешь взломать/расшифровать это дерьмо, лузер ниггерđịtconmẹlũchúngmàycrackhộthằngbốmàycái"

def random_junk(n=6) -> str:
    first = "_" + random.choice(string.ascii_letters)
    rest = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n-1))
    return first + rest

def make_long_noise_string(length=100) -> str:
    return ''.join(random.choice(SAFE_NOISE_CHARSET) for _ in range(length))

def random_comment_line() -> str:
    phrases = ["SYSTEM_HALT", "0xDEADBEEF", "KERNEL_PANIC", "MEMORY_DUMP", "STACK_OVERFLOW", "NULL_POINTER", "SEGMENTATION_FAULT", "BYPASS_DETECTED", "NIGGA_DUMP", "SYBAU_AND_STFU", "JUST_SUCK_MY_DICK"]
    return "# " + random.choice(phrases) + "_" + random_junk(8)

def obfuscate_b64_simple(data: str, block=4, junk="xyZZ") -> str:
    out = []
    L = len(data)
    for i in range(0, L, block):
        chunk = data[i:i+block]
        out.append(chunk + junk)
    return "".join(out)

# ---------------------- Advanced Noise Generators ----------------------

def make_long_comment_noise():
    noise_content = make_long_noise_string(random.randint(50, 150))
    return f"# {noise_content}"

def make_fake_var_noise():
    var_name = random_junk(80)
    noise_str = make_long_noise_string(random.randint(60, 200))
    s = []
    s.append(f"{var_name} = {repr(noise_str)}")
    s.append(f"if len({var_name}) > 10000: pass")
    s.append(f"del {var_name}")
    return "\n".join(s)

def make_try_except_noise():
    v_exc = random_junk(60)
    n = random.randint(0, 0xFFFF)
    noise_str = make_long_noise_string(20)
    s = []
    s.append("try:")
    s.append(f"    # {noise_str}")
    s.append(f"    if {random.randint(1,100)} > {random.randint(200,300)}: raise Exception({hex(n)})")
    s.append(f"except Exception as {v_exc}:")
    s.append(f"    if getattr({v_exc}, 'args', [None])[0] == {hex(n)}: pass")
    return "\n".join(s)

def make_complex_calc_noise():
    v1 = random_junk(50)
    v2 = random_junk(50)
    val = random.randint(1000, 99999)
    s = []
    s.append(f"{v1} = {val}")
    s.append(f"{v2} = ({v1} * 2) + {random.randint(1,99)}")
    s.append(f"if {v2} == 0: {v2} = 1")
    return "\n".join(s)

NOISE_GENERATORS = [
    make_long_comment_noise,
    make_fake_var_noise,
    make_try_except_noise,
    make_complex_calc_noise
]

def gen_noise_blocks(nblocks=10):
    blocks = []
    for _ in range(nblocks):
        blocks.append(random.choice(NOISE_GENERATORS)())
    return blocks

# ---------------------- CHEMICAL IMPORT GENERATOR (UPDATED) ----------------------
 
def generate_scattered_components(stub_func_name, decoder_body_str):
    """
    Hàm này không trả về 1 chuỗi lớn, mà trả về:
    1. setup_block: Phần khởi tạo ma trận (bắt buộc chạy trước).
    2. scattered_blocks: Danh sách các dòng lệnh "chức năng" đã bị xé nhỏ để trộn với rác.
    """
     
    # --- Phần 1: Tạo ma trận và import (Giữ nguyên logic cũ) ---
    target_words = ["marshal", "zlib", "base64", "bz2", "loads", "decompress", "b64decode", "exec", "compile", "globals", "bytes", "utf-8"]
    needed_chars = set("".join(target_words))
    pool = list(string.ascii_letters + string.digits)
    for char in needed_chars:
        if char not in pool: pool.append(char)
     
    rows, cols = 123, 123
    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    random.shuffle(all_positions)
    needed_list = list(needed_chars)
     
    for i, char in enumerate(needed_list):
        r, c = all_positions[i]
        matrix[r][c] = char
    for r in range(rows):
        for c in range(cols):
            if not matrix[r][c]: matrix[r][c] = random.choice(pool)
             
    char_locations = {}
    for r in range(rows):
        for c in range(cols):
            char = matrix[r][c]
            if char not in char_locations: char_locations[char] = []
            char_locations[char].append((r, c))
 
    def find_char(c):
        return random.choice(char_locations.get(c, [(0,0)]))
 
    matrix_var_name = "LOVEVSICKONTOP_" + random_junk(5).upper()
     
    def build_str_code(word):
        parts = [f"{matrix_var_name}[{r}][{c}]" for r, c in [find_char(ch) for ch in word]]
        return "+".join(parts)
 
    # Setup block (phải nằm ở đầu code sau này)
    setup_lines = []
    setup_lines.append(f"{matrix_var_name} = {repr(matrix)}")
    setup_lines.append(f"globals()['ch2oh4p2so4'] = (__import__) if bool(1) else __import__")
    setup_lines.append(f"globals()['agno3'] = (vars) if bool(1) else vars")
    setup_lines.append(f"_0x0 = ch2oh4p2so4({build_str_code('marshal')})")
    setup_lines.append(f"_0x1 = ch2oh4p2so4({build_str_code('zlib')})")
    setup_lines.append(f"_0x2 = ch2oh4p2so4({build_str_code('base64')})")
    setup_lines.append(f"_0x3 = ch2oh4p2so4({build_str_code('bz2')})")
     
    # Logic lấy hàm giải nén (Extractor)
    setup_lines.append("_0x4 = agno3().copy()")
    setup_lines.append(f"for _k, _v in agno3(_0x1).items():\n    if _k == {build_str_code('decompress')}: _0x4['_chem_zdec'] = _v")
    setup_lines.append(f"for _k, _v in agno3(_0x3).items():\n    if _k == {build_str_code('decompress')}: _0x4['_chem_bdec'] = _v")
    setup_lines.append(f"for _k, _v in agno3(_0x2).items():\n    if _k == {build_str_code('b64decode')}: _0x4['_chem_b64'] = _v")
    setup_lines.append("globals().update(_0x4)")
     
    setup_block = "\n".join(setup_lines)
 
    # --- Phần 2: Phân mảnh Logic (Scattered Blocks) ---
    scattered_blocks = []
 
    # 2.1: Phân tán việc tạo Mock Modules (zlib, bz2, base64 giả)
    # Thay vì viết 1 cụm, ta tạo biến tạm rồi gán dần dần
     
    # ZLIB
    v_z = random_junk(6)
    scattered_blocks.append(f"{v_z} = type('module', (), {{}})()")
    scattered_blocks.append(f"{v_z}.decompress = _chem_zdec")
    scattered_blocks.append(f"zlib = {v_z}")
 
    # BZ2
    v_b = random_junk(6)
    scattered_blocks.append(f"{v_b} = type('module', (), {{}})()")
    scattered_blocks.append(f"{v_b}.decompress = _chem_bdec")
    scattered_blocks.append(f"bz2 = {v_b}")
 
    # BASE64
    v_64 = random_junk(6)
    scattered_blocks.append(f"{v_64} = type('module', (), {{}})()")
    scattered_blocks.append(f"{v_64}.b64decode = _chem_b64")
    scattered_blocks.append(f"base64 = {v_64}")
 
    # 2.2: Phân tán Body của hàm giải mã (Decoder)
    # Ta sẽ cắt chuỗi code giải mã thành nhiều mảnh nhỏ, nhét vào 1 list toàn cục
    code_storage_var = "SECRET_" + random_junk(6).upper()
    scattered_blocks.append(f"{code_storage_var} = []") # Khởi tạo list
     
    # Cắt chuỗi thành các chunk nhỏ (độ dài ngẫu nhiên từ 10-30 ký tự)
    chunks = []
    i = 0
    while i < len(decoder_body_str):
        sz = random.randint(15, 40)
        chunks.append(decoder_body_str[i:i+sz])
        i += sz
     
    # Tạo các dòng lệnh append rải rác
    for chunk in chunks:
        # Đảo ngược chunk để khó đọc bằng mắt thường, lúc chạy sẽ đảo lại
        # Hoặc giữ nguyên cho đơn giản, ở đây ta giữ nguyên để đảm bảo độ ổn định
        scattered_blocks.append(f"{code_storage_var}.append({repr(chunk)})")
 
    # 2.3: Hàm Runner cuối cùng (Trigger)
    # Hàm này chỉ việc join cái list lại và exec
    final_func = f"""
def {stub_func_name}(d):
    _full_code = "".join({code_storage_var})
    exec(compile(_full_code, '<chemical_reaction>', 'exec'), globals(), {{'d': d}})
"""
    scattered_blocks.append(final_func)
 
    return setup_block, scattered_blocks
 
# ---------------------- Packer Core (UPDATED) ----------------------
 
def pack_code_with_noise(
    source: str,
    user: str,
    author: str = "lovevsick",
    version: str = "1.0",
    contact: str = DEFAULT_CONTACT,
    layers: int = 2,
    use_xor: bool = True,
    xor_key_len: int = 8,
    chunks: int = 16,
    comment_lines: int = 12,
    b64_block_junk: str = "xyZZ",
    b64_block_size: int = 4,
    noise_blocks: int = 40 
) -> str:
     
    # 1. Prepare Payload
    data = source.encode('utf-8')
    for i in range(layers):
        data = zlib.compress(data) if i % 2 == 0 else bz2.compress(data)
 
    xor_key = None
    if use_xor:
        xor_key = bytes(random.choice(range(1, 256)) for _ in range(xor_key_len))
        data = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(data))
 
    b64 = base64.b64encode(data).decode("ascii")
    b64_junked = obfuscate_b64_simple(b64, block=b64_block_size, junk=b64_block_junk)
 
    if chunks < 1: chunks = 1
    part_len = max(1, len(b64_junked) // chunks)
    parts = [b64_junked[i:i+part_len] for i in range(0, len(b64_junked), part_len)]
    literal_parts = [repr(p) for p in parts]
 
    payload_var = random_junk(8)
    run_func = random_junk(8)
     
    # 2. Construct Runner Body Code (String)
    runner_lines = []
    runner_lines.append(f"__s = d.replace({repr(b64_block_junk)}, '')")
    runner_lines.append("if len(__s) % 4 != 0: __s += '=' * ((4 - (len(__s) % 4)) % 4)")
    runner_lines.append("raw = base64.b64decode(__s)")
    if xor_key:
        hex_k = xor_key.hex()
        runner_lines.append(f"_kx = bytes.fromhex({repr(hex_k)})")
        runner_lines.append("new_raw = bytearray()")
        runner_lines.append("for i, b in enumerate(raw):")
        runner_lines.append("    new_raw.append(b ^ _kx[i % len(_kx)])")
        runner_lines.append("raw = bytes(new_raw)")
    for i in reversed(range(layers)):
        runner_lines.append("raw = zlib.decompress(raw)" if i % 2 == 0 else "raw = bz2.decompress(raw)")
     
    runner_lines.append("import sys")
    runner_lines.append("if sys.version_info < (3, 10): sys.exit(1)")
    runner_lines.append("exec(raw.decode('utf-8'), globals())")
     
    runner_body = "\n".join(runner_lines)
 
    # 3. Generate Scattered Logic
    # Thay vì gọi generate_chemical_import_stub cũ, ta gọi hàm mới
    setup_block, functional_shards = generate_scattered_components(run_func, runner_body)
     
    payload_block = f"{payload_var} = " + " + ".join(literal_parts)
    trigger_block = f"{run_func}({payload_var})"
 
    top_meta = f"__author__={repr(author)}\n__version__={repr(version)}\n__contact__={repr(contact)}\n__user__={repr(user)}"
 
    # 4. Shuffle & Inject (QUAN TRỌNG: Trộn lẫn functional_shards vào noise)
     
    # Tạo danh sách noise ban đầu
    all_blocks_to_shuffle = gen_noise_blocks(noise_blocks)
     
    # Thêm các mảnh chức năng (mock modules, decoder parts) vào danh sách noise để trộn
    all_blocks_to_shuffle.extend(functional_shards)
     
    # Xáo trộn thật kỹ
    random.shuffle(all_blocks_to_shuffle)
     
    # Sắp xếp bố cục file:
    # Header -> Setup Block (Bắt buộc đầu) -> [Hỗn hợp Noise + Chức năng rải rác] -> Payload -> Trigger
     
    final_blocks = []
     
    for _ in range(comment_lines):
        final_blocks.append(random_comment_line())
    final_blocks.append(top_meta)
    final_blocks.append(f"# {make_long_noise_string(50)}") 
     
    # SETUP BLOCK phải nằm trên cùng để khởi tạo ma trận và import
    final_blocks.append(setup_block)
     
    # Chèn hỗn hợp đã xáo trộn
    # Lưu ý: Payload và Trigger nên nằm gần cuối hoặc xen kẽ, nhưng để đơn giản ta chèn hỗn hợp vào giữa
    # Ta có thể chèn Payload vào giữa hỗn hợp này luôn cũng được, nhưng để an toàn payload nên nằm sau setup
     
    mid_point = len(all_blocks_to_shuffle) // 2
     
    final_blocks.extend(all_blocks_to_shuffle[:mid_point])
    final_blocks.append(payload_block) # Chèn payload vào giữa đống rác
    final_blocks.extend(all_blocks_to_shuffle[mid_point:])
     
    final_blocks.append(trigger_block) # Kích hoạt ở cuối
 
    final_text = "\n\n".join(block for block in final_blocks if block) + "\n"
    return final_text

# ---------------------- Interactive UI ----------------------

def prompt_yesno(question: str, default: bool = False) -> bool:
    yes = ("y","yes")
    no = ("n","no")
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        ans = input(question + suffix + ": ").strip().lower()
        if ans == "": return default
        if ans in yes: return True
        if ans in no: return False
        print("Answer y or n")

def run_interactive():
    print_banner()
    src = input(FG["yellow"] + "File -> " + RESET).strip()
    if not src:
        print(FG["red"] + "No file given." + RESET)
        sys.exit(1)
    if not os.path.isfile(src):
        print(FG["red"] + "File not found." + RESET)
        sys.exit(1)

    user = input(FG["cyan"] + "Username -> " + RESET).strip() or "anonymous"
    
    try: layers_in = int(input(FG["yellow"] + "Layers (default 3) -> " + RESET) or "3")
    except: layers_in = 3
    
    xor = prompt_yesno(FG["yellow"] + "XOR Obfuscation?" + RESET, default=True)
    
    try: chunks = int(input(FG["yellow"] + "Chunks (default 25) -> " + RESET) or "25")
    except: chunks = 25

    try: noise = int(input(FG["yellow"] + "Noise Blocks (default 50) -> " + RESET) or "50")
    except: noise = 50

    base, _ = os.path.splitext(os.path.basename(src))
    default_out = f"{base}_obf.py"
    out = input(FG["cyan"] + f"Output (default {default_out}) -> " + RESET) or default_out

    print(FG["magenta"] + "\nPacking ..." + RESET)
    start = time.time()

    with open(src, "r", encoding="utf-8") as f:
        src_text = f.read()

    loader = pack_code_with_noise(
        source=src_text,
        user=user,
        layers=layers_in,
        use_xor=xor,
        chunks=chunks,
        noise_blocks=noise,
        version=TOOL_VERSION
    )

    with open(out, "w", encoding="utf-8") as fo:
        fo.write(loader)

    print(FG["green"] + f"Done in {time.time()-start:.2f}s. Saved to {out}" + RESET)
    print()

def main():
    import argparse
    p = argparse.ArgumentParser(prog=TOOL_NAME)
    p.add_argument("src", nargs="?")
    p.add_argument("-o", "--out")
    p.add_argument("--no-interactive", action="store_true")
    p.add_argument("--user", default="anonymous")
    p.add_argument("--noise", type=int, default=50)
    args = p.parse_args()

    if args.src and args.no_interactive:
        if not os.path.isfile(args.src): return
        with open(args.src, "r", encoding="utf-8") as f: txt = f.read()
        out = args.out or f"{os.path.splitext(os.path.basename(args.src))[0]}_chem.py"
        code = pack_code_with_noise(txt, args.user, noise_blocks=args.noise, chunks=30)
        with open(out, "w", encoding="utf-8") as f: f.write(code)
        print(f"Saved {out}")
        return

    run_interactive()

if __name__ == "__main__":
    main()