from __future__ import annotations

import argparse

from src.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate vibration analysis report from raw Excel parser input or JSON parser output."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path ke file input. Bisa .xlsx, .xlsm, atau .json",
    )
    parser.add_argument(
        "--output-docx",
        required=True,
        help="Path file DOCX output.",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Path file JSON final report.",
    )
    parser.add_argument(
        "--mode",
        choices=["agent", "fallback"],
        default="agent",
        help="Mode agent memakai LangChain OpenRouter atau fallback deterministic.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_pipeline(
        input_path=args.input,
        output_docx=args.output_docx,
        output_json=args.output_json,
        mode=args.mode,
    )
    print(f"Report generated: {args.output_docx}")
    print(f"Rows analyzed: {len(report.rows)}")


if __name__ == "__main__":
    main()