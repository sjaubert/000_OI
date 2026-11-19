const { chromium } = require('playwright'); const fs=require('fs');
const J=JSON.parse(fs.readFileSync('/tmp/claude-0/w/out_g/donnees_G.json')).J;
(async()=>{ const b=await chromium.launch(); const p=await b.newPage();
 await p.goto('file:///tmp/claude-0/op/new.html'); await p.waitForTimeout(300);
 for (const [cle,T,res] of [['rrarbres4','0.4','0.01'],['rrbutees4','0.15','0.001']]) {
  await p.selectOption('#inK','4');
  const L=J[cle].lignes;
  for(let i=0;i<10;i++) for(let c=0;c<8;c++){ const j=Math.floor(c/2), m=c%2;
    await p.fill(`input[data-i="${i}"][data-j="${j}"][data-m="${m}"]`, L[i][c+1]); }
  await p.fill('#inT',T); await p.fill('#inRes',res);
  await p.click('#btnCalc'); await p.waitForTimeout(300);
  console.log(cle, (await p.textContent('#verdict')).replace(/\s+/g,' ').slice(0,200));
  console.log((await p.textContent('#chiffres')).replace(/\s+/g,' ').slice(0,500));
 }
 await b.close(); })();
