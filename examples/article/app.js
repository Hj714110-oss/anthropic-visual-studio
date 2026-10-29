
const settings=savedRead('ft-article-v2',{});let size=Number.isFinite(settings.size)?Math.min(22,Math.max(14,settings.size)):17,bookmarked=settings.bookmarked===true;
function apply(){document.querySelector('.essay').style.setProperty('--reading-size',size+'px');document.querySelector('#bookmark').setAttribute('aria-pressed',bookmarked);document.querySelector('#bookmark').textContent=bookmarked?'已收藏 ✓':'收藏这篇文章';document.querySelector('#font-up').disabled=size>=22;document.querySelector('#font-down').disabled=size<=14;}
function save(){savedWrite('ft-article-v2',{size,bookmarked});apply();}
document.querySelector('#font-up').onclick=()=>{size=Math.min(22,size+1);save();};document.querySelector('#font-down').onclick=()=>{size=Math.max(14,size-1);save();};document.querySelector('#bookmark').onclick=()=>{bookmarked=!bookmarked;save();notify(bookmarked?'已保存在当前浏览器。':'已取消收藏。');};apply();
