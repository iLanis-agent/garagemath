// Garage math - pure arithmetic engine, runs in browser and node.
(function(root){
"use strict";
function r0(x){ return Math.round(x); }
function r1(x){ return Math.round(x*10)/10; }
function r2(x){ return Math.round(x*100)/100; }
var MIRROR_CM = 25; // labeled: extra width for open door mirrors
function pos(nums, msg){
  for (var i=0;i<nums.length;i++){ if (!isFinite(nums[i]) || nums[i] <= 0) return { error: msg }; }
  return null;
}
function fitPlan(garageL, garageW, carL, carW){
  var bad = pos([garageL, garageW, carL, carW], "garage and car dimensions must be positive");
  if (bad) return bad;
  var side = r0((garageW - carW) / 2);
  var end = r0((garageL - carL) / 2);
  return { sideCm: side, endCm: end, fits: side >= 0 && end >= 0 };
}
function doorPlan(doorW, doorH, carW, carH){
  var bad = pos([doorW, doorH, carW, carH], "door and car dimensions must be positive");
  if (bad) return bad;
  var wClear = r0(doorW - (carW + MIRROR_CM));
  var hClear = r0(doorH - carH);
  return { wClear: wClear, hClear: hClear, clears: wClear >= 0 && hClear >= 0 };
}
function shelfPlan(wallM, depthM, spacingM, heightM){
  var bad = pos([wallM, depthM, spacingM, heightM], "wall, depth, spacing and height must be positive");
  if (bad) return bad;
  if (spacingM > heightM) return { error: "the shelf spacing must not exceed the wall height" };
  var levels = Math.floor(heightM / spacingM);
  var area = r2(levels * wallM * depthM);
  var board = r1(levels * wallM);
  var volume = r2(levels * wallM * depthM * spacingM);
  return { levels: levels, areaM2: area, boardM: board, volumeM3: volume };
}
function cmWord(n){ return n + " cm"; }
function plural(n, w){ return n + " " + w + (n === 1 ? "" : "s"); }
function renderFit(r){
  if (r.fits){
    return "Centered in the garage, the car gets " + cmWord(r.sideCm) + " on each side and " + cmWord(r.endCm) + " at each end.";
  }
  var parts = [];
  if (r.sideCm < 0) parts.push(cmWord(-r.sideCm * 2) + " too wide");
  if (r.endCm < 0) parts.push(cmWord(-r.endCm * 2) + " too long");
  return "The car does not fit: " + parts.join(" and ") + " for that garage.";
}
function renderDoor(r){
  if (r.clears){
    return "Through the door: " + cmWord(r.wClear) + " of width to spare counting a labeled " + MIRROR_CM + " cm for open mirrors, and " + cmWord(r.hClear) + " of height.";
  }
  var parts = [];
  if (r.wClear < 0) parts.push(cmWord(-r.wClear) + " of width");
  if (r.hClear < 0) parts.push(cmWord(-r.hClear) + " of height");
  return "The car will not clear the door: short " + parts.join(" and ") + ", counting a labeled " + MIRROR_CM + " cm for open mirrors.";
}
function renderShelf(r){
  return plural(r.levels, "level") + " on that wall: " + r.areaM2 + " m² of shelf, " + r.boardM + " m of board, and about " + r.volumeM3 + " m³ of storage.";
}
var api = { MIRROR_CM: MIRROR_CM, fitPlan: fitPlan, doorPlan: doorPlan, shelfPlan: shelfPlan,
  renderFit: renderFit, renderDoor: renderDoor, renderShelf: renderShelf };
if (typeof module !== "undefined" && module.exports) module.exports = api;
root.GarageMath = api;
})(typeof window !== "undefined" ? window : globalThis);
