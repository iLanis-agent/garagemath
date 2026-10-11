const E = require('./engine.js');
const cases = require('./expected.json');
const fns = { fitPlan: E.fitPlan, doorPlan: E.doorPlan, shelfPlan: E.shelfPlan };
const renders = { fitPlan: E.renderFit, doorPlan: E.renderDoor, shelfPlan: E.renderShelf };
let checks = 0, failed = 0;
for (const c of cases) {
  const got = fns[c.fn](...c.args);
  const keys = Object.keys(c.result);
  for (const k of keys) {
    checks++;
    if (got[k] !== c.result[k]) { failed++; console.log('FAIL', c.fn, c.args, k, 'expected', c.result[k], 'got', got[k]); }
  }
  if (c.render !== undefined) {
    checks++;
    const g = renders[c.fn](got);
    if (g !== c.render) { failed++; console.log('FAIL render', c.fn, c.args, '\n exp:', c.render, '\n got:', g); }
  }
}
console.log(cases.length + ' cases, ' + checks + ' checks ' + (failed ? failed + ' FAILED' : 'green'));
process.exit(failed ? 1 : 0);
