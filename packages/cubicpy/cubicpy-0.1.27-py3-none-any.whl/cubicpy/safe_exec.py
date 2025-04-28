import math
import random
import numpy as np

class SafeExec:
    def __init__(self, user_code_file):
        self.file_path = user_code_file
        self.safe_globals = {
            "__builtins__": {
                "range": range,
                "len": len,
                "abs": abs,
                "min": min,
                "max": max,
                "sum": sum,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "tuple": tuple,
                "dict": dict,
                "set": set,
                "bool": bool,
                "complex": complex,
                "callable": callable,
                "isinstance": isinstance,
                "issubclass": issubclass,
                "type": type,
                "all": all,
                "any": any,
                "zip": zip,
                "enumerate": enumerate,
                "reversed": reversed,
                "sorted": sorted,
                "filter": filter,
                "map": map,
                "round": round,
                "next": next,
                "iter": iter,
                "slice": slice,
                "pow": pow,
                "divmod": divmod,
                "format": format,
                "hash": hash,
                "id": id,
                "print": print,
                "input": input,
                "open": open,
                "exec": exec,
                "eval": eval,
                "compile": compile,
                "globals": globals,
                "locals": locals,
                "dir": dir,
                "vars": vars,
                "hasattr": hasattr,
                "getattr": getattr,
                "setattr": setattr,
                "delattr": delattr,
                "chr": chr,
                "ord": ord,
                "bin": bin,
                "oct": oct,
                "hex": hex,
                "ascii": ascii,
                "repr": repr,

            },
            "sin": math.sin, "cos": math.cos, "tan": math.tan, "degrees": math.degrees,
            "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
            "sqrt": math.sqrt, "pi": math.pi, "exp": math.exp,
            "log": math.log, "pow": math.pow, "fabs": math.fabs,
            "ceil": math.ceil, "floor": math.floor,
            "math": math,
            'random': random,
            'randint': random.randint, 'choice': random.choice, 'uniform': random.uniform,
            'seed': random.seed, 'shuffle': random.shuffle,
            "np": np,
        }

    def run(self):
        safe_locals = {}

        # ファイルからユーザーコードを読み込む
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                user_code_lines = f.readlines()  # すべての行をリストとして読み込む

            # "import" または "from" で始まる行を削除
            filtered_code_lines = [line for line in user_code_lines if not line.strip().startswith(("import", "from"))]

            # 改行を含めて結合
            user_code = "".join(filtered_code_lines)

        except FileNotFoundError:
            print(f"Error: ファイル '{self.file_path}' が見つかりません")
            user_code = ""
        except Exception as e:
            print(f"Error: ファイルを読み込めません ({e})")
            user_code = ""

        # exec() の実行
        try:
            exec(user_code, self.safe_globals, safe_locals)
            body_data = safe_locals.get("body_data", [])
            return body_data
        except Exception as e:
            print(f"Execution error: {e}")
            return []
