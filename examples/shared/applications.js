
'use strict';
let toastTimer;
function notify(message){const box=document.querySelector('#toast');box.textContent=message;box.classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>box.classList.remove('visible'),2200);}
function downloadText(name,text,type='text/plain'){const url=URL.createObjectURL(new Blob([text],{type:type+';charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
function savedRead(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback;}catch{return fallback;}}
function savedWrite(key,data){try{localStorage.setItem(key,JSON.stringify(data));return true;}catch{notify('浏览器未允许存储，本次更改仅保留在当前页面。');return false;}}
function progress(){const max=document.documentElement.scrollHeight-innerHeight;document.querySelector('#reading-progress').style.width=(max>0?Math.min(100,scrollY/max*100):0)+'%';}
addEventListener('scroll',progress,{passive:true});addEventListener('resize',progress);progress();
