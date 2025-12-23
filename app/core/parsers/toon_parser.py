import re
from typing import Dict, Any, Optional

class ToonParser:
    """
    Parses TOON (Token-Oriented Object Notation) strings into Python dictionaries.
    Manual implementation since the library seems to lack a public decode API yet.
    """
    
    @staticmethod
    def parse(toon_string: str) -> Dict[str, Any]:
        """
        Parses a TOON formatted string.
        Supports:
        - key: value
        - key[n]: val1, val2
        """
        try:
            # Clean up
            cleaned = toon_string.strip()
            if cleaned.startswith("```toon"): cleaned = cleaned[7:]
            if cleaned.startswith("```"): cleaned = cleaned[3:]
            if cleaned.endswith("```"): cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            data = {}
            
            # Simple line-based parser
            lines = cleaned.split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # Match "key[n]: val1, val2" (Array)
                array_match = re.match(r"^(\w+)\[(\d+)\]:\s*(.*)$", line)
                if array_match:
                    key, count, values_str = array_match.groups()
                    # Split by comma, respecting quotes could be added but keeping simple for now
                    # TOON uses CSV style
                    values = [v.strip() for v in values_str.split(',')]
                    data[key] = values
                    continue
                
                # Match "key: value" (Scalar)
                # Handle potential quoting
                scalar_match = re.match(r"^(\w+):\s*(.*)$", line)
                if scalar_match:
                    key, val = scalar_match.groups()
                    # Remove surrounding quotes if present
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    data[key] = val
                    continue
            
            return data
            
        except Exception as e:
            print(f"Error parsing TOON: {e}")
            return {"error": str(e), "raw": toon_string}

    @staticmethod
    def dump(data: Dict[str, Any]) -> str:
        # Simple dumper
        lines = []
        for k, v in data.items():
            if isinstance(v, list):
                lines.append(f"{k}[{len(v)}]: {','.join(map(str, v))}")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)
