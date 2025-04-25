from pise.config.environment import Environment

def init_env():
    print("\n🔧 PISE 環境設定を開始します\n")

    cluster = input("使用クラスタ名を入力してください（genkai/laurel）: ").strip()
    submit_command = input("ジョブ投入コマンドを入力してください（pjsub/sbatch）: ").strip()
    vasp_path = input("VASP実行ファイルのパスを入力してください: ").strip()

    print("\n✅ 以下の設定で保存します：")
    print(f"  クラスタ名        : {cluster}")
    print(f"  ジョブ投入コマンド: {submit_command}")
    print(f"  VASPの実行パス    : {vasp_path}")

    confirm = input("保存してよろしいですか？ (y/n): ").strip().lower()
    if confirm == "y":
        env = Environment(cluster, submit_command, vasp_path)
        env.save()
        print("\n✅ 環境設定が ~/.pise_env.json に保存されました！")
    else:
        print("\n❌ 保存をキャンセルしました。")
