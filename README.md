# The AI & Cloud Era series

The landing page for five free online books on building modern software systems, published at
<https://oleksiyp.github.io/softwarebook-series/>.

| # | Book | Site |
|---|---|---|
| 1 | Software Architecture in the AI & Cloud Era | <https://oleksiyp.github.io/arch-book/> |
| 2 | Building Products in the AI & Cloud Era | <https://oleksiyp.github.io/buildproducts-book/> |
| 3 | Building Software at Scale in the AI & Cloud Era | <https://oleksiyp.github.io/buildsoftware-book/> |
| 4 | Building Resilient Systems in the AI & Cloud Era | <https://oleksiyp.github.io/resilienteng-book/> |
| 5 | Operating Production Systems in the AI & Cloud Era | <https://oleksiyp.github.io/prodsys-book/> |

The page is one static `index.html`. The covers in `assets/books/` are rendered from each book's
`assets/cover/wrap.svg` by `node tools/covers.mjs` (run beside the book repositories), then converted
with `cwebp -q 84`.
