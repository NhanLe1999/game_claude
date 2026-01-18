// lib_stub.js - minimal Astrocade host stub for local running

// asset_map.js defines: const assets = {...}
const assetsSource = (typeof assets !== "undefined") ? assets : {};

window.mode = window.mode || "play";
window.gameConfig = window.gameConfig || {};

window.lib = window.lib || {};
window.lib.getAsset = (id) => assetsSource[id];
window.lib.log = (...args) => console.log("[lib.log]", ...args);

// Optional stubs (so code won't crash if it calls them)
window.lib.addPlayerScoreToLeaderboard = async () => ({ success: false, entries: [], userRank: null });
window.lib.getTopNEntriesFromLeaderboard = async () => ({ success: false, entries: [], userRank: null });
window.lib.saveUserGameState = async (state) => ({ success: false, state });
window.lib.getUserGameState = async () => ({ success: false, state: null });
window.lib.deleteUserGameState = async () => ({ success: true });
