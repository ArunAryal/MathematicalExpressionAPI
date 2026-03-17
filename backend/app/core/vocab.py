import re

VOCAB = [
    "<pad>", "<sos>", "<eos>", "<unk>",
    "_", "^", "{", "}", "&", "\\\\", " ",
    "a","b","c","d","e","f","g","h","i","j","k","l","m",
    "n","o","p","q","r","s","t","u","v","w","x","y","z",
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
    "0","1","2","3","4","5","6","7","8","9",
    "\\mathbb{A}","\\mathbb{B}","\\mathbb{C}","\\mathbb{D}","\\mathbb{E}",
    "\\mathbb{F}","\\mathbb{G}","\\mathbb{H}","\\mathbb{I}","\\mathbb{J}",
    "\\mathbb{K}","\\mathbb{L}","\\mathbb{M}","\\mathbb{N}","\\mathbb{O}",
    "\\mathbb{P}","\\mathbb{Q}","\\mathbb{R}","\\mathbb{S}","\\mathbb{T}",
    "\\mathbb{U}","\\mathbb{V}","\\mathbb{W}","\\mathbb{X}","\\mathbb{Y}",
    "\\mathbb{Z}","\\mathbb",
    ",",";",":","!","?",".","(",")","]","[","\\{","\\}",
    "*","/","+","-","\\_","\\&","\\#","\\%","|","\\backslash",
    "\\alpha","\\beta","\\delta","\\Delta","\\epsilon","\\eta","\\chi",
    "\\gamma","\\Gamma","\\iota","\\kappa","\\lambda","\\Lambda","\\nu",
    "\\mu","\\omega","\\Omega","\\phi","\\Phi","\\pi","\\Pi","\\psi",
    "\\Psi","\\rho","\\sigma","\\Sigma","\\tau","\\theta","\\Theta",
    "\\upsilon","\\Upsilon","\\varphi","\\varpi","\\varsigma","\\vartheta",
    "\\xi","\\Xi","\\zeta",
    "\\frac","\\sqrt","\\prod","\\sum","\\iint","\\int","\\oint",
    "\\hat","\\tilde","\\vec","\\overline","\\underline","\\prime",
    "\\dot","\\not",
    "\\begin{matrix}","\\end{matrix}",
    "\\langle","\\rangle","\\lceil","\\rceil","\\lfloor","\\rfloor","\\|",
    "\\ge","\\gg","\\le","\\ll","<",">",
    "=","\\approx","\\cong","\\equiv","\\ne","\\propto","\\sim","\\simeq",
    "\\in","\\ni","\\notin","\\sqsubseteq","\\subset","\\subseteq",
    "\\subsetneq","\\supset","\\supseteq","\\emptyset",
    "\\times","\\bigcap","\\bigcirc","\\bigcup","\\bigoplus","\\bigvee",
    "\\bigwedge","\\cap","\\cup","\\div","\\mp","\\odot","\\ominus",
    "\\oplus","\\otimes","\\pm","\\vee","\\wedge",
    "\\hookrightarrow","\\leftarrow","\\leftrightarrow","\\Leftrightarrow",
    "\\longrightarrow","\\mapsto","\\rightarrow","\\Rightarrow",
    "\\rightleftharpoons","\\iff",
    "\\bullet","\\cdot","\\circ",
    "\\aleph","\\angle","\\dagger","\\exists","\\forall","\\hbar",
    "\\infty","\\models","\\nabla","\\neg","\\partial","\\perp","\\top",
    "\\triangle","\\triangleleft","\\triangleq","\\vdash","\\Vdash","\\vdots",
]

VOCAB_SIZE = len(VOCAB)
char_to_index = {c: i for i, c in enumerate(VOCAB)}
index_to_char = {i: c for c, i in char_to_index.items()}

PAD_ID = char_to_index["<pad>"]
SOS_ID = char_to_index["<sos>"]
EOS_ID = char_to_index["<eos>"]
UNK_ID = char_to_index["<unk>"]

_CMD = re.compile(
    r"\\(mathbb{[a-zA-Z]}|begin{[a-z]+}|end{[a-z]+}|operatorname\*|[a-zA-Z]+|.)"
)

def tokenize(s: str) -> list:
    tokens = []
    while s:
        if s[0] == "\\":
            tokens.append(_CMD.match(s).group(0))
        else:
            tokens.append(s[0])
        s = s[len(tokens[-1]):]
    return tokens