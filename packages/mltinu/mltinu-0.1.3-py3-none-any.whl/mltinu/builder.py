import os
import pandas as pd
import logging
from typing import Dict, Optional, Tuple
from langchain_openai import ChatOpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CodeBuilder:
    def __init__(
        self,
        csv_path: str,
        target: str,
        model_name: str,
        api_key: Optional[str] = None
    ):
        self.csv_path = csv_path
        self.target = target
        self.model_name = model_name
        self.api_key = "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"

        if not self.api_key:
            raise ValueError("Please set MLTINU_API_KEY env var or provide api_key.")
        if not os.path.isfile(self.csv_path):
            raise FileNotFoundError(f"CSV not found: {self.csv_path}")

        self.llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
            model="llama-3.3-70b-versatile",
        )

    def _get_csv_info(self) -> Tuple[str, Dict[str, str]]:
        df = pd.read_csv(self.csv_path)
        head = df.head().to_string(index=False)
        dtypes = df.dtypes.apply(lambda dt: dt.name).to_dict()
        return head, dtypes

    def _build_prompt(self, head: str, dtypes: Dict[str, str]) -> str:
        return f"""You are a helpful Python + Scikit-learn expert.

Based on the following dataset preview and column data types, generate a SINGLE Jupyter Notebook code cell that:

- Loads the CSV file
- Preprocesses numeric and categorical features appropriately
- Trains a Scikit-learn `{self.model_name}` model on target column `{self.target}`
- Splits the data
- Evaluates using appropriate metrics
- Plots relevant graphs (e.g. confusion matrix, residual plot, cluster plot)

### Dataset Preview
{head}

### Data Types
{dtypes}

Please output only valid Python code — no explanation. Code must work in one notebook cell.
"""

    def generate_code(self) -> str:
        head, dtypes = self._get_csv_info()
        prompt = self._build_prompt(head, dtypes)
        logger.debug("Prompt sent to LLM:\n%s", prompt)

        response = self.llm.invoke([
            {"role": "system", "content": "You are a professional data science code generator."},
            {"role": "user", "content": prompt}
        ])
        return getattr(response, "content", str(response)).strip()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a ML pipeline notebook cell using LLM.")
    parser.add_argument("csv_path", help="Path to CSV file")
    parser.add_argument("--target", required=True, help="Target column name")
    parser.add_argument("model_name", help="Scikit-learn model class name")

    args = parser.parse_args()
    builder = CodeBuilder(args.csv_path, args.target, args.model_name)
    print(builder.generate_code())
