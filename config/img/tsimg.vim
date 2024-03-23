syntax match tsimg /^.*$/ contains=tsimgKeyword, tsimgNumber nextgroup=tsingInstruction

syntax keyword tsimgKeyword contained img rect

syntax match tsimgNumber contained /0[xX]\x\+/
syntax match tsimgNumber contained /\d\+/

syntax match tsimgInstruction contained /^img\s\+\d\+\s\+\d\+$/
syntax match tsimgInstruction contained /^rect\s\+[0-9A-F]\{6}\s\+\d\+\s\+\d\+\s\+\d\+\s\+\d\+$/

highlight default link tsimgNumber Number
highlight default link tsimgKeyword Keyword