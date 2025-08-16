#!/usr/bin/env python3
"""
Travel Itinerary Maker (offline)
Usage:
  python main.py --input "City: Paris; Days: 3"
"""
import argparse, requests, os, sys, re

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "llama3.2:4b"
TIMEOUT = 300

def run_llama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def build_prompt(spec):
    # Expect spec like "City: Paris; Days: 3" or similar
    return (
        "Plan a multi-day itinerary. For each day provide Morning / Afternoon / Evening, "
        "food suggestions, a hidden gem, and transit tips. Keep each day under 180 words.\n\n"
        f"{spec}"
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="City and days e.g. 'City: Paris; Days: 3'")
    args = p.parse_args()
    print(run_llama(build_prompt(args.input)))

if __name__ == "__main__":
    main()
