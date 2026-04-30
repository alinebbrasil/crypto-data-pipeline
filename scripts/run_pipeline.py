"""
run_pipeline.py

Objetivo:
Executar o pipeline completo de criptomoedas em sequência.

Etapas:
1. Coleta dados da API e salva JSON na camada RAW
2. Transforma arquivos RAW em camada PROCESSED
3. Cria camada ANALYTICS para consumo no dashboard

Uso:
python scripts/run_pipeline.py
"""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


PIPELINE_STEPS = [
    {
        "name": "Ingestão RAW",
        "script": PROJECT_ROOT / "scripts" / "02_save_raw_json.py",
    },
    {
        "name": "Transformação PROCESSED",
        "script": PROJECT_ROOT / "scripts" / "03_transform_raw.py",
    },
    {
        "name": "Criação da camada ANALYTICS",
        "script": PROJECT_ROOT / "scripts" / "04_create_analytics.py",
    },
]


def run_step(step_name: str, script_path: Path) -> None:
    """
    Executa uma etapa do pipeline.

    Args:
        step_name: nome amigável da etapa.
        script_path: caminho do script Python que será executado.
    """
    print(f"\nIniciando etapa: {step_name}")

    if not script_path.exists():
        raise FileNotFoundError(f"Script não encontrado: {script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Erro na etapa: {step_name}")

    print(f"Etapa concluída: {step_name}")


def main() -> None:
    """
    Executa todas as etapas do pipeline.
    """
    print("Executando pipeline completo de criptomoedas...")

    for step in PIPELINE_STEPS:
        run_step(step["name"], step["script"])

    print("\nPipeline completo executado com sucesso.")


if __name__ == "__main__":
    main()