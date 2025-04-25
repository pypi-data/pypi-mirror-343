#!/usr/bin/env python
"""
CubicPy コマンドラインインターフェース
キューブを積み上げて物理シミュレーションを行う子供向けPython学習ツール
"""
import argparse
import os
import sys
import locale
import random
import asyncio
import threading
from cubicpy import CubicPyApp, list_samples, get_sample_path, DEFAULT_GRAVITY_FACTOR, DEFAULT_WINDOW_SIZE_X, DEFAULT_WINDOW_SIZE_Y, RESTITUTION, FRICTION, WebSocketServer

# 言語に応じたメッセージ
MESSAGES = {
    'ja': {
        'description': 'CubicPy - コードで物理オブジェクトを配置・構築する3Dプログラミング学習アプリ',
        'epilog': '例: cubicpy -e cube_tower_sample または cubicpy my_script.py',
        'example_help': '実行するサンプル名（例: cube_tower_sample）',
        'list_help': '利用可能なサンプル一覧を表示',
        'gravity_help': '重力係数（デフォルト: 0）',
        'window_size_help': 'ウィンドウサイズをカンマ区切りで指定（例: 1280,720）デフォルト: 900,600',
        'file_help': '実行するPythonファイル（オプション）',
        'camera_lens_help': 'カメラレンズのタイプ（perspective または orthographic）デフォルト: perspective',
        'restitution_help': '反発係数（0.0から1.0の範囲）デフォルト: 0.5',
        'friction_help': '摩擦係数（0.0から1.0の範囲）デフォルト: 0.5',
        'external_help': 'WebSocket通信モードで起動',
        'room_help': 'WebSocket通信のルーム名を指定（デフォルト: ランダムな4桁の数字）',
        'version_help': 'バージョン情報を表示',
        'version_info': 'CubicPy バージョン {0}',
        'available_samples': '利用可能なサンプル:',
        'running_sample': "サンプル '{0}' を実行します",
        'error_sample_not_found': "エラー: {0}",
        'error_file_not_found': "エラー: ファイル '{0}' が見つかりません",
        'running_file': "ファイル '{0}' を実行します",
        'running_default_sample': "デフォルトサンプル '{0}' を実行します",
        'error_default_sample': "エラー: デフォルトサンプルが見つかりません: {0}",
        'error_application': "エラー: アプリケーションの実行中にエラーが発生しました: {0}",
        'error_window_size': "エラー: ウィンドウサイズの形式が無効です。例: 1280,720",
        'code_preview': "--- サンプルコード ---",
        'code_preview_end': "--- コード終了 ---"
    },
    'en': {
        'description': 'CubicPy - 3D programming learning app: place physics objects with code and build',
        'epilog': 'Example: cubicpy -e cube_tower_sample or cubicpy my_script.py',
        'example_help': 'Sample name to run (e.g. cube_tower_sample)',
        'list_help': 'Display list of available samples',
        'gravity_help': 'Gravity factor (default: 0)',
        'window_size_help': 'Window size as comma-separated values (e.g. 1280,720) default: 900,600',
        'file_help': 'Python file to run (optional)',
        'camera_lens_help': 'Camera lens type (perspective or orthographic) default: perspective',
        'restitution_help': 'Restitution coefficient (0.0 to 1.0) default: 0.5',
        'friction_help': 'Friction coefficient (0.0 to 1.0) default: 0.5',
        'external_help': 'Start in WebSocket communication mode',
        'room_help': 'Specify WebSocket communication room name (default: random 4-digit number)',
        'version_help': 'Display version information',
        'version_info': 'CubicPy version {0}',
        'available_samples': 'Available samples:',
        'running_sample': "Running sample '{0}'",
        'error_sample_not_found': "Error: {0}",
        'error_file_not_found': "Error: File '{0}' not found",
        'running_file': "Running file '{0}'",
        'running_default_sample': "Running default sample '{0}'",
        'error_default_sample': "Error: Default sample not found: {0}",
        'error_application': "Error: An error occurred while running the application: {0}",
        'error_window_size': "Error: Invalid window size format. Example: 1280,720",
        'code_preview': "--- Sample Code ---",
        'code_preview_end': "--- End of Code ---"
    }
}


def get_system_language():
    """システムの言語を取得する"""
    try:
        language, _ = locale.getdefaultlocale()
        if language and language.startswith('ja'):
            return 'ja'
    except:
        pass
    return 'en'


def display_code(code_file, lang):
    """コードファイルの内容をコンソールに表示する"""
    try:
        with open(code_file, 'r', encoding='utf-8') as file:
            code_content = file.read()

        print(f"\n{MESSAGES[lang]['code_preview']}")
        print(code_content)
        print(f"{MESSAGES[lang]['code_preview_end']}\n")
    except Exception as e:
        print(f"Error reading code file: {e}")


def parse_window_size(size_str, lang):
    """ウィンドウサイズの文字列をタプルに変換する"""
    try:
        width, height = map(int, size_str.split(','))
        return (width, height)
    except ValueError:
        print(MESSAGES[lang]['error_window_size'])
        return None


def run_websocket_server(api, room=None):
    """WebSocketサーバーを実行する関数"""
    server = WebSocketServer(api, room=room)
    server.start()


def main():
    """コマンドラインエントリーポイント"""
    # システムの言語を取得
    lang = get_system_language()
    msgs = MESSAGES[lang]

    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(
        description=msgs['description'],
        epilog=msgs['epilog']
    )
    parser.add_argument('--example', '-e',
                        help=msgs['example_help'])
    parser.add_argument('--list', '-l', action='store_true',
                        help=msgs['list_help'])
    parser.add_argument('--gravity', '-g', type=float, default=DEFAULT_GRAVITY_FACTOR,
                        help=msgs['gravity_help'])
    parser.add_argument('--external', '-x', action='store_true',
                        help=msgs['external_help'])
    parser.add_argument('--room', '-m', type=str, default=None,
                        help=msgs['room_help'])
    parser.add_argument('--window-size', '-w', default="900,600",
                        help=msgs['window_size_help'])
    parser.add_argument('--version', '-v', action='store_true',
                        help=msgs['version_help'])
    parser.add_argument('file', nargs='?',
                        help=msgs['file_help'])
    parser.add_argument('--camera-lens', '-c', choices=['perspective', 'orthographic'],
                        default='perspective',
                        help=msgs['camera_lens_help'])
    parser.add_argument('--restitution', '-r', type=float, default=0.5,
                        help=msgs['restitution_help'])
    parser.add_argument('--friction', '-f', type=float, default=0.5,
                        help=msgs['friction_help'])

    args = parser.parse_args()

    # バージョン情報の表示
    if args.version:
        print(msgs['version_info'].format(__version__))
        return 0

    # ウィンドウサイズのパース
    window_size = parse_window_size(args.window_size, lang)
    if window_size is None:
        return 1

    # サンプル一覧の表示
    if args.list:
        print(msgs['available_samples'])
        for sample in list_samples():
            print(f"  {sample}")
        return 0

    # ファイルパスの決定
    if args.example:
        try:
            code_file = get_sample_path(args.example)
            print(msgs['running_sample'].format(args.example))
            # サンプルコードを表示
            display_code(code_file, lang)
        except ValueError as e:
            print(msgs['error_sample_not_found'].format(e))
            return 1
    elif args.file:
        # ユーザー指定のファイル
        code_file = args.file

        # ファイルの存在確認
        if not os.path.exists(code_file):
            print(msgs['error_file_not_found'].format(code_file))
            return 1

        # 安全なパスに変換
        code_file = os.path.abspath(code_file)
        print(msgs['running_file'].format(code_file))
    elif args.external:
        code_file = None
    else:
        # デフォルトサンプル - 最初のサンプルを使用
        default_sample = random.choice(list_samples()) if list_samples() else 'cube_tower_sample'
        try:
            code_file = get_sample_path(default_sample)
            print(msgs['running_default_sample'].format(default_sample))
            # サンプルコードを表示
            display_code(code_file, lang)
        except ValueError as e:
            print(msgs['error_default_sample'].format(e))
            return 1

    try:
        # アプリを起動
        app = CubicPyApp(
            code_file, 
            gravity_factor=args.gravity, 
            window_size=window_size, 
            camera_lens=args.camera_lens,
            restitution=args.restitution,
            friction=args.friction)

        # 外部通信モードの場合
        if args.external:
            print(f"WebSocketクライアントを開始します")
            # WebSocketサーバーを別スレッドで実行
            websocket_thread = threading.Thread(target=run_websocket_server, args=(app, args.room))
            websocket_thread.daemon = True  # メインスレッドが終了したら自動的に終了
            websocket_thread.start()

        # アプリケーションを実行
        print(f"アプリケーションを実行します")
        app.run()
    except Exception as e:
        print(msgs['error_application'].format(e))
        return 1

    return 0


# モジュールとして直接実行された場合のエントリーポイント
if __name__ == '__main__':
    sys.exit(main())