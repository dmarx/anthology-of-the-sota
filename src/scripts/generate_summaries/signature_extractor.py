# signature_extractor.py
"""Extracts and formats Python code signatures with proper nesting."""
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict
from loguru import logger

@dataclass
class Signature:
    """Represents a Python function or class signature with documentation."""
    name: str
    kind: str  # 'function', 'method', or 'class'
    args: list[str]
    returns: str | None
    docstring: str | None
    decorators: list[str]
    methods: list['Signature']  # For storing class methods

class ParentNodeTransformer(ast.NodeTransformer):
    """Add parent references to all nodes in the AST."""
    
    def visit(self, node: ast.AST) -> ast.AST:
        """Visit a node and add parent references to all its children."""
        for child in ast.iter_child_nodes(node):
            child.parent = node
        return super().visit(node)

class SignatureExtractor:
    """Extracts detailed signatures from Python files."""
    
    def get_type_annotation(self, node: ast.AST) -> str:
        """Convert AST annotation node to string representation."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Subscript):
            container = self.get_type_annotation(node.value)
            params = self.get_type_annotation(node.slice)
            return f"{container}[{params}]"
        elif isinstance(node, ast.BinOp):
            left = self.get_type_annotation(node.left)
            right = self.get_type_annotation(node.right)
            return f"{left} | {right}"
        elif isinstance(node, ast.Tuple):
            elts = [self.get_type_annotation(e) for e in node.elts]
            return f"[{', '.join(elts)}]"
        return "Any"
    
    def get_arg_string(self, arg: ast.arg) -> str:
        """Convert function argument to string with type annotation."""
        arg_str = arg.arg
        if arg.annotation:
            type_str = self.get_type_annotation(arg.annotation)
            arg_str += f": {type_str}"
        return arg_str

    def extract_signatures(self, source: str) -> List[Signature]:
        """Extract all function and class signatures from source code."""
        try:
            # Parse and add parent references
            tree = ast.parse(source)
            transformer = ParentNodeTransformer()
            transformer.visit(tree)
            
            signatures: List[Signature] = []
            classes: Dict[ast.ClassDef, Signature] = {}
            
            for node in ast.walk(tree):
                # Handle functions
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = []
                    for arg in node.args.args:
                        args.append(self.get_arg_string(arg))
                    
                    returns = None
                    if node.returns:
                        returns = self.get_type_annotation(node.returns)
                    
                    decorators = []
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            decorators.append(f"@{decorator.id}")
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name):
                                decorators.append(f"@{decorator.func.id}(...)")
                    
                    sig = Signature(
                        name=node.name,
                        kind='method' if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef) else 'function',
                        args=args,
                        returns=returns,
                        docstring=ast.get_docstring(node),
                        decorators=decorators,
                        methods=[]
                    )
                    
                    # Add to appropriate parent
                    if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef) and node.parent in classes:
                        classes[node.parent].methods.append(sig)
                    else:
                        signatures.append(sig)
                
                # Handle classes
                elif isinstance(node, ast.ClassDef):
                    bases = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            bases.append(base.id)
                    
                    decorators = []
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            decorators.append(f"@{decorator.id}")
                    
                    class_sig = Signature(
                        name=node.name,
                        kind='class',
                        args=bases,
                        returns=None,
                        docstring=ast.get_docstring(node),
                        decorators=decorators,
                        methods=[]
                    )
                    
                    classes[node] = class_sig
                    signatures.append(class_sig)
                    
            return signatures
        except Exception as e:
            logger.error(f"Error parsing source: {e}")
            return []

    def format_signature(self, sig: Signature, indent: int = 0) -> List[str]:
        """Format a signature for display with proper indentation."""
        lines = []
        indent_str = "    " * indent
        
        # Add decorators
        for decorator in sig.decorators:
            lines.append(f"{indent_str}{decorator}")
        
        # Format the signature line
        if sig.kind == 'class':
            base_str = f"({', '.join(sig.args)})" if sig.args else ""
            lines.append(f"{indent_str}class {sig.name}{base_str}")
        else:
            async_prefix = "async " if "async" in sig.decorators else ""
            args_str = ", ".join(sig.args)
            return_str = f" -> {sig.returns}" if sig.returns else ""
            lines.append(f"{indent_str}{async_prefix}def {sig.name}({args_str}){return_str}")
        
        # Add docstring if present
        if sig.docstring:
            doc_lines = sig.docstring.split('\n')
            if len(doc_lines) == 1:
                lines.append(f'{indent_str}    """{sig.docstring}"""')
            else:
                lines.append(f'{indent_str}    """')
                for doc_line in doc_lines:
                    if doc_line.strip():
                        lines.append(f"{indent_str}    {doc_line}")
                lines.append(f'{indent_str}    """')
        
        # Add methods for classes
        if sig.methods:
            lines.append("")  # Add spacing
            for method in sig.methods:
                lines.extend(self.format_signature(method, indent + 1))
                lines.append("")  # Add spacing between methods
        
        return lines

def generate_python_summary(root_dir: str | Path) -> str:
    """Generate enhanced Python project structure summary.
    
    Args:
        root_dir: Root directory of the project
        
    Returns:
        Formatted markdown string of Python signatures
    """
    root_dir = Path(root_dir)
    extractor = SignatureExtractor()
    content = ["# Python Project Structure\n"]
    
    for file in sorted(root_dir.rglob("*.py")):
        if any(part.startswith('.') for part in file.parts):
            continue
        if '__pycache__' in file.parts:
            continue
            
        try:
            # Get relative path
            rel_path = file.relative_to(root_dir)
            
            # Read and extract signatures
            source = file.read_text()
            signatures = extractor.extract_signatures(source)
            
            # Only include files that have actual content
            if signatures:
                content.append(f"## {rel_path}")
                content.append("```python")
                
                # Format each signature
                for sig in signatures:
                    content.extend(extractor.format_signature(sig))
                    content.append("")  # Add spacing between top-level items
                
                content.append("```\n")
            
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")
    
    return "\n".join(content)
