# Garage math

Will the car actually fit, how much door does it clear counting the mirrors, and how many shelves can the back wall hold. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/garagemath/

## The three tools

- **Fit plan** - `fitPlan(garageL, garageW, carL, carW)`: clearances on each side and each end, or how much too big the car is.
- **Door plan** - `doorPlan(doorW, doorH, carW, carH)`: the squeeze through the opening, with a labeled 25 cm mirror allowance.
- **Shelf plan** - `shelfPlan(wallM, depthM, spacingM, heightM)`: levels, shelf area, board length and storage volume.

## Labeled norms (illustrative references, not rules)

- Mirror allowance: 25 cm of extra width for open door mirrors.
- Single garage: about 500 x 300 cm inside, 240 x 210 cm door. Measure your own space and your own car, mirrors out.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (40 cases, 164 checks)

Regenerate the oracle expectations: `python3 oracle.py`
