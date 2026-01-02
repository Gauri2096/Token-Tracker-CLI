import argparse
import csv
from datetime import datetime
import tiktoken

input_price=0.0005
output_price=0.0015

def count_tokens(text:str,model:str="gpt-3.5-turbo")->int:
    try:
        encoding=tiktoken.encoding_for_model(model)
    except Exception:
        encoding=tiktoken.encoding_for_model("cl100k_base")
    return len(encoding.encode(text))

def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    
    cost_input = (input_tokens / 1000) * input_price
    cost_output = (output_tokens / 1000) * output_price
    return cost_input + cost_output

def append_csv(path:str,date_str:str,model:str,input_tokens:int,output_tokens:int,cost:float)->None:
    file_exists=False
    try:
        with open(path,"r",newline="",encoding="utf-8"):
            file_exists=True
    except FileNotFoundError:
        file_exists=False
    with open(path,"a",newline="",encoding="utf-8") as f:
        writer=csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Model", "Input Tokens", "Output Tokens", "Cost"])
        writer.writerow([date_str, model, input_tokens, output_tokens, f"{cost:.6f}"])

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Token & cost tracker CLI")
    parser.add_argument("--model", required=True, help="Model name, e.g. gpt-3.5-turbo")
    parser.add_argument("--prompt", required=True, help="Prompt text sent to model")
    parser.add_argument("--response", required=True, help="Model response text")
    parser.add_argument("--csv_path", default="usage_log.csv", help="CSV file path")
    parser.add_argument("--verbose",action="store_true",help="Print detailed token & cost info to stdout")
    return parser.parse_args()

def main()->None:
    args=parse_args()
    input_tokens=count_tokens(args.prompt,args.model)
    output_tokens=count_tokens(args.response,args.model)
    total_cost=estimate_cost(input_tokens,output_tokens)
    date_str=datetime.now().isoformat(timespec="seconds")
    append_csv(args.csv_path,date_str,args.model,input_tokens,output_tokens,total_cost)
    if args.verbose:
        print(f"Date: {date_str}")
        print(f"Model: {args.model}")
        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Total cost (USD): {total_cost:.6f}")
        print(f"Logged to: {args.csv_path}")
if __name__=="__main__":
    main()