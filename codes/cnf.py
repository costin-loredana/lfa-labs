
class CNFConverter:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.new_rules = {}
        self.counter = 1
        self.terminal_map = {}
        self.production_cache = {}

    def convert(self):
        if [] in self.grammar.get(self.start_symbol, []):
            new_start = f"{self.start_symbol}'"
            self.grammar[new_start] = [[self.start_symbol]]
            self.start_symbol = new_start

        self.remove_null_productions()
        self.deduplicate_rules()

        self.remove_unit_productions()
        self.deduplicate_rules()

        self.remove_useless_symbols()
        self.deduplicate_rules()

        self.convert_to_cnf()
        self.deduplicate_rules()

        self.optimize_grammar()
        self.deduplicate_rules()  

        return self.grammar

    def deduplicate_rules(self):
        for k in self.grammar:
            unique_rules = set(tuple(rule) for rule in self.grammar[k])
            self.grammar[k] = [list(rule) for rule in unique_rules]

    def optimize_grammar(self):
        self._merge_identical_productions()
        self._merge_equivalent_structures()
        self.deduplicate_rules()

    def _merge_identical_productions(self):
        production_map = {}
        for nt, productions in self.grammar.items():
            prod_key = frozenset(tuple(tuple(prod) for prod in productions))
            production_map.setdefault(prod_key, []).append(nt)

        substitutions = {}
        for nts in production_map.values():
            if len(nts) > 1:
                keep = nts[0]
                for replace in nts[1:]:
                    if replace != self.start_symbol:
                        substitutions[replace] = keep

        if substitutions:
            self._apply_substitutions(substitutions)

    def _merge_equivalent_structures(self):
        while True:
            signatures = {}
            for nt, productions in self.grammar.items():
                sig_parts = []
                for prod in productions:
                    if len(prod) == 2:
                        pattern = ("BIN", prod[0] in self.grammar, prod[1] in self.grammar, prod[0] == prod[1])
                    elif len(prod) == 1:
                        pattern = ("UNARY", prod[0] not in self.grammar)
                    else:
                        continue
                    sig_parts.append(pattern)

                signature = frozenset(sig_parts)
                signatures.setdefault(signature, []).append(nt)

            substitutions = {}
            for sig, nts in signatures.items():
                if len(nts) > 1 and sig:
                    pattern_groups = {}
                    for nt in nts:
                        patterns = [tuple(prod) for prod in self.grammar[nt]]
                        pattern_key = frozenset(patterns)
                        pattern_groups.setdefault(pattern_key, []).append(nt)

                    for group in pattern_groups.values():
                        if len(group) > 1:
                            keep = group[0]
                            for replace in group[1:]:
                                if replace != self.start_symbol:
                                    substitutions[replace] = keep

            if not substitutions:
                break

            self._apply_substitutions(substitutions)

    def _apply_substitutions(self, substitutions):
        new_grammar = {}
        for nt, prods in self.grammar.items():
            if nt in substitutions:
                continue
            new_grammar[nt] = []

        for nt, prods in self.grammar.items():
            if nt not in substitutions:
                for prod in prods:
                    new_prod = [substitutions.get(symbol, symbol) for symbol in prod]
                    if new_prod not in new_grammar[nt]:
                        new_grammar[nt].append(new_prod)

        self.grammar = new_grammar
        self.deduplicate_rules()

    def remove_null_productions(self):
        nullable = set(k for k, productions in self.grammar.items() if [] in productions)

        changed = True
        while changed:
            changed = False
            for k, productions in self.grammar.items():
                if k not in nullable:
                    for prod in productions:
                        if all(symbol in nullable for symbol in prod):
                            nullable.add(k)
                            changed = True
                            break

        new_grammar = {k: [] for k in self.grammar}
        for k, productions in self.grammar.items():
            for prod in productions:
                if prod:
                    self._add_combinations(k, prod, 0, [], nullable, new_grammar)
            if k == self.start_symbol and [] in self.grammar[k]:
                new_grammar[k].append([])

        self.grammar = new_grammar

    def _add_combinations(self, nt, prod, index, current, nullable, new_grammar):
        if index == len(prod):
            if current:
                if current not in new_grammar[nt]:
                    new_grammar[nt].append(current[:])
            return

        symbol = prod[index]
        current.append(symbol)
        self._add_combinations(nt, prod, index + 1, current, nullable, new_grammar)
        current.pop()

        if symbol in nullable:
            self._add_combinations(nt, prod, index + 1, current, nullable, new_grammar)

    def remove_unit_productions(self):
        unit_pairs = {(k, k) for k in self.grammar}

        for k, productions in self.grammar.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] in self.grammar:
                    unit_pairs.add((k, prod[0]))

        changed = True
        while changed:
            changed = False
            new_pairs = set()
            for a, b in unit_pairs:
                for c in self.grammar:
                    if (b, c) in unit_pairs and (a, c) not in unit_pairs:
                        new_pairs.add((a, c))
                        changed = True
            unit_pairs.update(new_pairs)

        new_grammar = {k: [] for k in self.grammar}
        for a, b in unit_pairs:
            if a != b:
                for prod in self.grammar[b]:
                    if len(prod) != 1 or prod[0] not in self.grammar:
                        if prod not in new_grammar[a]:
                            new_grammar[a].append(prod)

        for k, productions in self.grammar.items():
            for prod in productions:
                if len(prod) != 1 or prod[0] not in self.grammar:
                    if prod not in new_grammar[k]:
                        new_grammar[k].append(prod)

        self.grammar = new_grammar

    def remove_useless_symbols(self):
        generating = set()
        for k, productions in self.grammar.items():
            for prod in productions:
                if all(symbol not in self.grammar for symbol in prod):
                    generating.add(k)
                    break

        changed = True
        while changed:
            changed = False
            for k, productions in self.grammar.items():
                if k not in generating:
                    for prod in productions:
                        if all(symbol in generating or symbol not in self.grammar for symbol in prod):
                            generating.add(k)
                            changed = True
                            break

        reachable = {self.start_symbol}
        changed = True
        while changed:
            changed = False
            new_reachable = set(reachable)
            for k in reachable:
                if k in self.grammar:
                    for prod in self.grammar[k]:
                        for symbol in prod:
                            if symbol in self.grammar and symbol not in new_reachable:
                                new_reachable.add(symbol)
                                changed = True
            reachable = new_reachable

        useful = generating.intersection(reachable)

        new_grammar = {}
        for k in useful:
            new_grammar[k] = []
            for prod in self.grammar[k]:
                if all(symbol in useful or symbol not in self.grammar for symbol in prod):
                    new_grammar[k].append(prod)

        self.grammar = new_grammar

    def convert_to_cnf(self):
        self._replace_terminals_in_long_rules()
        self._break_long_productions()

    def _replace_terminals_in_long_rules(self):
        for k in list(self.grammar):
            new_productions = []
            for prod in self.grammar[k]:
                if len(prod) > 1:
                    new_prod = []
                    for symbol in prod:
                        if symbol not in self.grammar:
                            if symbol not in self.terminal_map:
                                t_name = f"T_{symbol}"
                                self.terminal_map[symbol] = t_name
                                self.new_rules.setdefault(t_name, [])
                                if [symbol] not in self.new_rules[t_name]:
                                    self.new_rules[t_name].append([symbol])
                            new_prod.append(self.terminal_map[symbol])
                        else:
                            new_prod.append(symbol)
                    if new_prod not in new_productions:
                        new_productions.append(new_prod)
                else:
                    if prod not in new_productions:
                        new_productions.append(prod)
            self.grammar[k] = new_productions

        for k, v in self.new_rules.items():
            self.grammar.setdefault(k, [])
            for rule in v:
                if rule not in self.grammar[k]:
                    self.grammar[k].append(rule)
        self.new_rules = {}

    def _break_long_productions(self):
        for k in list(self.grammar):
            new_prods = []
            for prod in self.grammar[k]:
                if len(prod) <= 2:
                    if prod not in new_prods:
                        new_prods.append(prod)
                else:
                    current_prod = prod
                    while len(current_prod) > 2:
                        sub_pattern = tuple(current_prod[:2])
                        if sub_pattern in self.production_cache:
                            new_sym = self.production_cache[sub_pattern]
                        else:
                            new_sym = f"N{self.counter}"
                            self.counter += 1
                            self.new_rules.setdefault(new_sym, [])
                            if list(sub_pattern) not in self.new_rules[new_sym]:
                                self.new_rules[new_sym].append(list(sub_pattern))
                            self.production_cache[sub_pattern] = new_sym
                        current_prod = [new_sym] + current_prod[2:]
                    if current_prod not in new_prods:
                        new_prods.append(current_prod)
            self.grammar[k] = new_prods

        for k, v in self.new_rules.items():
            self.grammar.setdefault(k, [])
            for rule in v:
                if rule not in self.grammar[k]:
                    self.grammar[k].append(rule)
        self.new_rules = {}

def print_cnf(grammar):
    print("=== CNF Grammar Productions ===")
    for head, rules in sorted(grammar.items()):
        for rule in sorted([' '.join(r) for r in rules]):
            print(f"{head} -> {rule}")

if __name__ == "__main__":
    # Example grammar (not in CNF)
    example_grammar = {
        'S': [['d', 'B'], ['A', 'B']],
        'A': [['d'], ['d', 'S'], ['a', 'A', 'a', 'A', 'b'], []],  # [] represents epsilon
        'B': [['a'], ['a', 'S'], ['A']],
        'D': [['A', 'b', 'a']]
    }

    start_symbol = "S"

    converter = CNFConverter(example_grammar, start_symbol)
    cnf_grammar = converter.convert()
    print_cnf(cnf_grammar)

