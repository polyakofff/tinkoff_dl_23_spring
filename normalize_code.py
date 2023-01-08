import ast


class StringConstantRemover(ast.NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            return ast.Constant('')
        return node


class PrintRemover(ast.NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Call(self, node: ast.Call):
        super().generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            return ast.Tuple([])
        return node


class ExpressionFlattener(ast.NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Expr(self, node: ast.Expr):
        super().generic_visit(node)
        if isinstance(node.value, ast.Tuple):
            exprs = []
            for expr in node.value.elts:
                exprs.append(ast.Expr(expr))
            return exprs
        return node


class CompareNormalizer(ast.NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Compare(self, node: ast.Compare):
        super().generic_visit(node)
        if len(node.ops) == 1:
            op = type(node.ops[0])
            left = node.left
            right = node.comparators[0]
            if op in {ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot}:
                if type(left).__name__ > type(right).__name__:
                    node.left = right
                    node.comparators = [left]
                    if op in {ast.Lt, ast.LtE, ast.Gt, ast.GtE}:
                        node.ops = [{ast.Lt: ast.Gt, ast.Gt: ast.Lt, ast.LtE: ast.GtE, ast.GtE: ast.LtE}[op]()]
        return node

        
class NameTransformer(ast.NodeTransformer):

    def __init__(self):
        super().__init__()
        self.class_names = set()
        self.function_names = set()
        self.variable_names = set()
        self.second_pass = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        super().generic_visit(node)
        if not self.second_pass:
            self.function_names.add(node.name)
        else:
            node.name = 'f'
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        super().generic_visit(node)
        if not self.second_pass:
            self.function_names.add(node.name)
        else:
            node.name = 'f'
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        super().generic_visit(node)
        if not self.second_pass:
            self.class_names.add(node.name)
        else:
            node.name = 'c'
        return node

    def visit_arg(self, node: ast.arg):
        if not self.second_pass:
            self.variable_names.add(node.arg)
        else:
            node.arg = 'v'
            node.annotation = None
        return node

    def visit_Name(self, node: ast.Name):
        if not self.second_pass:
            if isinstance(node.ctx, ast.Store):
                self.variable_names.add(node.id)
        else:
            if node.id in self.class_names:
                node.id = 'c'
            elif node.id in self.function_names:
                node.id = 'f'
            elif node.id in self.variable_names:
                node.id = 'v'
        return node

    def visit_twice(self, node: ast.Name):
        super().generic_visit(node)
        self.second_pass = True
        super().generic_visit(node)
        return node
        

def normalize_code(code):
    tree = ast.parse(code)
    tree = ast.fix_missing_locations(StringConstantRemover().visit(tree))
    tree = ast.fix_missing_locations(PrintRemover().visit(tree))
    tree = ast.fix_missing_locations(ExpressionFlattener().visit(tree))
    tree = ast.fix_missing_locations(CompareNormalizer().visit(tree))
    tree = ast.fix_missing_locations(NameTransformer().visit_twice(tree))
    return ast.unparse(tree)
