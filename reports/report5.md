# Chomsky Normal Form
**Course**: Formal Languages & Finite Automata  
**Author**: Loredana Costin

---

## Theory

Chomsky Normal Form (CNF) is a restricted form of context-free grammars (CFGs) where every production rule adheres to a specific structure. CNF is important because it simplifies parsing algorithms (like the CYK algorithm) and theoretical proofs in automata theory.

A CFG is in Chomsky Normal Form if all its production rules are of one of the following forms:

1. non-terminal -> terminal (A->a);
2. non-terminal -> 2 non-terminals (A->BC);
3. special case for the start symbol: S->`&epsilon`;

Key restrictions in CNF:
1. no unit productions (like A-> B);
2. No mixed productions (like A->aB);
3. No productions with more than two non-terminals on the right-hand side (RHS).

Steps to convert a CFG into CNF:
1. Eliminate `&epsilon`-Productions (Nullable Non-terminals). Identify all non-terminals that can derive `&epsilon`. For each production A -> `&alpha`, add new productions where nullable non-terminals are removed in all possible combinations.
2. Eliminate Unit Productions (A → B). If A→B and B→`&alpha`, replace A→B with A→`&alpha`. Repeat until no unit productions remain.
3. Eliminate Non-Terminals Mixed with Terminals. Replace terminals in productions with more than one symbol using new non-terminals. For every terminal a, introduce a new rule T→a.
4. Break Long Productions into Pairs of Non-Terminals. Break Long Productions into Pairs of Non-Terminals. A->BCD. Then A-> BE, where E-> CD.

The reason to use CNF:
1. Simplifies Parsing: The CYK algorithm (used for membership testing) requires CNF.
2. Easier Proofs: Many theoretical results (e.g., pumping lemma for CFLs) assume CNF.
3. Removes Ambiguity: Helps in reducing structural ambiguity in grammars.
---

## Objectives:

- Learn about Chomsky Normal Form (CNF).
- Get familiar with the approaches of normalizing a grammar.
- Implement a method for normalizing an input grammar by the rules of CNF.
    a. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    b. The implemented functionality needs executed and tested.
    c. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.
---

## Implementation Description

1. **Removing null productions**  

The code identifies all non-terminals that can derive ε either directly or indirectly, using a fixed-point loop. It then recursively generates all combinations of each production with nullable symbols optionally removed. This ensures that the grammar no longer relies on ε-productions while preserving language equivalence. The method _add_combinations is used to generate these variations systematically.

```python
nullable = set(k for k, productions in self.grammar.items() if [] in productions) 
```
Then, it extends the nullable set to include non-terminals that indirectly lead to ε. It checks whether all symbols in a production are already nullable, in which case the head non-terminal becomes nullable too. The loop repeats until no new nullable symbols are found. This ensures the grammar accounts for all ε derivations.

```python
while changed:
            changed = False
            for k, productions in self.grammar.items():
                if k not in nullable:
                    for prod in productions:
                        if all(symbol in nullable for symbol in prod):
                            nullable.add(k)
                            changed = True
                            break
```

This small part recursively creates all valid versions of a production with nullable symbols removed. It uses backtracking to try all inclusion/exclusion paths for nullable symbols. These variants are stored in the updated grammar. It prevents loss of derivations when removing ε-productions.


```python
    self._add_combinations(k, prod, 0, [], nullable, new_grammar)         
```

2. **Removing the unit productions**

We also need to have a function which detects direct unit productions, i.e., rules where one non-terminal leads directly to another (e.g., A → B). It starts by including reflexive pairs (like A → A) to aid in closure computation. Then it adds real unit relationships found in the grammar. These pairs are stored for further processing in the next step.

```python
        unit_pairs = {(k, k) for k in self.grammar}

        for k, productions in self.grammar.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] in self.grammar:
                    unit_pairs.add((k, prod[0]))
```

Then, it computes all indirect unit derivations using transitive closure logic. If A → B and B → C, then it adds A → C. The loop continues until all such indirect connections are found. It ensures that unit rules are fully resolved across the grammar.

```python
        while changed:
            changed = False
            new_pairs = set()
            for a, b in unit_pairs:
                for c in self.grammar:
                    if (b, c) in unit_pairs and (a, c) not in unit_pairs:
                        new_pairs.add((a, c))
                        changed = True
            unit_pairs.update(new_pairs)
```

Finally, it takes each unit pair and copies all non-unit productions from the second non-terminal to the first. It skips over rules that would recreate unit productions. Duplicates are avoided to keep the grammar minimal. The result is a grammar with all unit rules fully replaced.


```python
        new_grammar = {k: [] for k in self.grammar}
        for a, b in unit_pairs:
            if a != b:
                for prod in self.grammar[b]:
                    if len(prod) != 1 or prod[0] not in self.grammar:
                        if prod not in new_grammar[a]:
                            new_grammar[a].append(prod)
```

3. **Replace terminals in long rules**

CNF requires that productions with more than one symbol on the RHS must consist solely of non-terminals. This step ensures terminals in long productions are replaced with new non-terminals. For each terminal in a long production, a new non-terminal is introduced: A mapping (terminal_map) stores the association between terminals and their corresponding new non-terminals (e.g., a → T_a). The new rule T_a → a is added to new_rules.

```python
 if symbol not in self.grammar:
    if symbol not in self.terminal_map:
        t_name = f"T_{symbol}"
        self.terminal_map[symbol] = t_name
        self.new_rules.setdefault(t_name, [])
        if [symbol] not in self.new_rules[t_name]:
            self.new_rules[t_name].append([symbol])
    new_prod.append(self.terminal_map[symbol])
```
This step incorporates the temporary T_a → a rules into the main grammar structure. It ensures each new non-terminal for terminals has a defined rule. The check prevents duplicate rules from being added. After merging, it resets the temporary rule store.

```python
 for k, v in self.new_rules.items():
            self.grammar.setdefault(k, [])
            for rule in v:
                if rule not in self.grammar[k]:
                    self.grammar[k].append(rule)
        self.new_rules = {}
```
                        
    
4. **The process of having unique procution rules**

In order to have unique production rules, it is needed to be created a signature for each non-terminal based on the structure of its productions. It records whether the production is binary or unary, whether symbols are terminals/non-terminals, and whether both symbols are the same. These patterns are used to detect structurally equivalent non-terminals. This lays the groundwork for grammar simplification.

```python
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
```

This final part clusters non-terminals with the same production patterns and replaces all but one with a shared representative. It avoids collapsing the start symbol to maintain grammar integrity. This reduces redundancy and simplifies the grammar without changing the language. It’s a form of structural optimization to make the CNF cleaner.

```python

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
```




---
## Results and Conclusion
![The CNF convertion](outputs/output-lab5.png)
![The CNF conversion on paper](outputs/cnf-varianta10.png)

In conclusion, the implementation successfully converts an input CFG into CNF by systematically applying each of the four steps stated above. The final grammar adheres strictly to CNF rules, making it suitable for use with algorithms that rely on CNF grammars. The most complicated part was to make the production rules unique. The variant solved on paper matches the output of the code.



---
## References  

1. **Online Resources:**  
   - [Wikipedia - Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)  
   - [CSE 322 - Introduction to Formal Methods in Computer Science](https://courses.cs.washington.edu/courses/cse322/08au/lec14.pdf)  
   -  [Medium- Converting Context-free Grammar to Chomsky Normal Form](https://developers.google.com/edu/python/regular-expressions)

2. **Books and Slides:**  
   - [Automata Theory, Languages, & Computation - 3rd Edition (PDF)](https://mrce.in/ebooks/Automata%20Theory,%20Languages,%20&%20Computation%20Introduction%203rd%20Ed.pdf)  
   - [Course Slides (Google Drive)](https://drive.google.com/file/d/19muyiabGeGaoNDK-7PeuzYYDe6_c0e-t/view)  
