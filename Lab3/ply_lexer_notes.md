# PLY Lexer — Concept Notes (Compiler Construction, Lab 3)

## 1. Lexer kya hota hai?

Lexer (lexical analyzer) ek "scanner" hota hai jo raw text (characters ka sequence) ko chhote **meaningful chunks (tokens)** mein todta hai — jaise insaan ek sentence ko words mein tod ke samajhta hai.

Bina lexer ke, computer ke liye `"123 + 456"` sirf random characters ka dher hai. Lexer isay `Number(123)`, `PLUS(+)`, `Number(456)` jaise labeled pieces mein badal deta hai, taake aage ka program (parser) inhe samajh sake.

---

## 2. `lex.lex()` — Machine banane wala function

```python
lexer = lex.lex()
```

- Ye tumhari file scan karta hai
- `tokens` list dhoondta hai (token naamon ki list)
- Har `t_<name>` rule (string ya function) dhoondta hai
- In sab se ek **internal lexer machine** assemble karta hai
- Ye machine `lexer` variable mein return hoti hai

**Yaad rakho:** `lex.lex()` khud text ko tokenize nahi karta — sirf machine **banata** hai. Tokenizing baad mein hoti hai.

---

## 3. `.input(data)` aur `.token()`

| Function | Kaam |
|---|---|
| `lexer.input(data)` | Machine ko batata hai ke kis string par kaam karna hai (raw material dena) |
| `lexer.token()` | Har call par **agla ek token** return karta hai. Jab tokens khatam ho jayen → `None` return karta hai |

```python
lexer.input("123 456")
lexer.token()   # → LexToken(Number,'123',...)
lexer.token()   # → LexToken(Number,'456',...)
lexer.token()   # → None (khatam)
```

Isi liye loop mein `if not tok: break` likha jata hai.

---

## 4. String rules vs Function rules

### String rule (simple, fixed regex):
```python
t_PLUS = r'\+'
```
Sirf ek regex batata hai — koi extra logic nahi.

### Function rule (jab extra logic chahiye ho):
```python
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'   # <-- regex docstring, PEHLI line hona ZAROORI hai
    t.type = reserved.get(t.value, 'ID')
    return t
```
- Function ke andar **pehli line regex docstring** honi chahiye — PLY isay wahan se uthata hai
- **PLY function rules ko string rules se PEHLE check karta hai** — is liye reserved keywords (`if`, `while`) pehle function-based `t_ID` se guzarte hain, tab jaake decide hota hai ke `IF` banana hai ya `ID`

⚠️ **Common mistake:** Ek hi token naam (jaise `Number`) ko **do dafa** define karna (ek dafa string se, ek dafa function se) — PLY error dega: `"previously defined"` aur `"Can't build lexer"`. Ek naam = sirf ek definition.

---

## 5. `t.value` aur `t.type` ka matlab

Jab lexer koi word match karta hai, wo usay `t` object mein store karta hai:

- `t.value` = jo **actual text** match hua (jaise `"if"` ya `"fatima"`)
- `t.type` = us token ki **category/naam** (jaise `"ID"` ya `"IF"`)

---

## 6. Reserved keywords kaise pakde jaate hain

```python
reserved = {
    'if': 'IF',
    'while': 'WHILE',
    ...
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t
```

**Flow (dono cases ek hi function se guzarte hain):**

```
Word match hua (regex se) — chahe "if" ho ya "fatima"
        ↓
Hamesha t_ID function mein jata hai
        ↓
Andar check: reserved dictionary mein hai kya?
        ↓                              ↓
     Haan ("if")                   Nahi ("fatima")
        ↓                              ↓
   t.type = "IF"                  t.type = "ID"
        ↓                              ↓
        └──────── return t ────────────┘
```

`reserved.get(t.value, 'ID')` ka matlab: *"dictionary mein `t.value` ki key dhoondo; mil jaye to uski value do, warna default `'ID'` do."*

**Reserved word alag "class/raasta" mein NAHI jata** — sirf ek dictionary lookup hai, same function ke andar.

---

## 7. `return t` ke baad value kahan jaati hai?

Tum `t_ID` ya `t_Number` ko khud kabhi call nahi karte. Lexer **internally** call karta hai jab scanning ke dauran pattern match ho:

```
tok = lexer.token()
        │
        ▼
lexer word dhoondta hai, matching function ko internally call karta hai
        │
        ▼
function ke andar t.type set hota hai
        │
        ▼
return t   →  ye value lexer.token() ko wapas milti hai
        │
        ▼
lexer.token() wahi t tumhare 'tok' variable ko de deta hai
        │
        ▼
print(tok)
```

---

## 8. `t_ignore` aur `t_error`

```python
t_ignore = ' \t'
```
Space aur tab ko **skip** karta hai — koi token nahi banta, bas gap consider hota hai.

```python
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)
```
Agar koi character kisi bhi rule se match na ho (jaise `@`), to ye function chalta hai. **Agar ye define na karo to PLY warning deta hai:** `"No t_error rule is defined"`.

---

## 9. Regex mein `\` (backslash escape) kab lagana hai

Kuch characters regex mein **special command** ka kaam karte hain — agar unhe **literal** (plain symbol) match karna ho to `\` laga ke unka special matlab cancel karna padta hai.

**Escape zaroori (special meaning cancel karne ke liye):**

| Character | Regex mein iska special matlab |
|---|---|
| `+` → `\+` | "1 ya zyada baar" |
| `*` → `\*` | "0 ya zyada baar" |
| `(` `)` → `\(` `\)` | Grouping |
| `[` `]` → `\[` `\]` | Character set |
| `{` `}` → `\{` `\}` | Repetition count |
| `.` `^` `$` `?` `\|` | Bhi special hain |

**Escape ZAROORI NAHI (already plain/normal characters):**

| Character | Wajah |
|---|---|
| `/` | Koi special meaning nahi |
| `-` (akele) | Sirf `[]` ke andar special hota hai (jaise `[a-z]`), akela normal hai |
| `=` `;` `,` `<` `>` `_` | Sab plain characters hain regex ke liye |

**Test:** Agar special character escape na karo (jaise `t_PLUS = r'+'` bina `\`), to error aayega: `re.error: nothing to repeat`.

---

## 10. Quick Summary Table

| Concept | Ek line mein yaad |
|---|---|
| `lex.lex()` | Rules se lexer machine banata hai (sirf ek dafa) |
| `.input(data)` | Machine ko string deta hai |
| `.token()` | Har call par agla token deta hai, khatam hone par `None` |
| String rule | Simple, fixed regex — extra logic nahi |
| Function rule | Extra logic ke liye — regex docstring pehli line mein zaroori |
| Function vs string order | Function rules pehle check hoti hain |
| `t.value` | Match hua actual text |
| `t.type` | Token ki category |
| `reserved.get(t.value,'ID')` | Dictionary lookup — keyword hai to uska type, warna default `ID` |
| `return t` | Token wapas `lexer.token()` ko, phir tumhare code ko jata hai |
| `t_ignore` | Characters jo skip ho jaate hain (koi token nahi banta) |
| `t_error` | Undefined/illegal character ka handler — na ho to warning aati hai |
| `\` escape | Sirf un characters par jo regex mein special command hain |
